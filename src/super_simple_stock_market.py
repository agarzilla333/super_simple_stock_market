'''
This module handles all 5 of the basic stock calculations
'''

from datetime import timedelta
from typing import Union
from scipy.stats import gmean
from pandas import Timestamp
from numpy.typing import NDArray
import pandas as pd
import numpy as np


class StocksData:
    '''
        This class holds the data for the static stock dividend data frame
        and the stock transactions data frame
    '''
    _instance = None
    def __new__(cls):
        '''
            This method on the python data model ensures we initialize the dataframes only once,
            effectively creating a singleton.
        '''
        if cls._instance is None:
            cls._instance = super(StocksData, cls).__new__(cls)
            cls._initialize_data()
        return cls._instance

    @staticmethod
    def _initialize_data():
        '''
            This private function initializes stock dividend and stock transactions data.
        :return:
        '''
        StocksData.stock_dividend_data = pd.DataFrame({
            'stock': ['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
            'type': ['Common', 'Common', 'Common', 'Preferred', 'Common'],
            'last_dividend': [0, 8, 23, 8, 12],
            'fixed_dividend': [np.nan, np.nan, np.nan, .02, np.nan],
            'par_value': [100, 100, 60, 100, 250]
        })
        StocksData.stock_transactions = pd.DataFrame({
            'timestamp': [],
            'stock': [],
            'quantity': [],
            'indicator': [],
            'price': []
        })

    def record_trade(self, timestamp: Timestamp, stock: str, quantity: int,
                     indicator: str, price: float) -> Union[None, str]:
        '''
            This function records stock transactions.
        :param timestamp:
        :param stock:
        :param quantity:
        :param indicator:
        :param price:
        :return:
        '''
        try:
            new_record = pd.DataFrame({
                'timestamp': [timestamp],
                'stock': [stock],
                'quantity': [quantity],
                'indicator': [indicator],
                'price': [price]
            })
            cleaned_transactions = StocksData.stock_transactions.dropna(axis=1, how='all')
            StocksData.stock_transactions = pd.concat([cleaned_transactions, new_record],
                                                      ignore_index=True)
        except TypeError:
            return f'Invalid input data types ' \
                   f'timestamp type: {type(timestamp)} expected: {Timestamp}' \
                   f'stock type: {type(stock)} expected: {str}' \
                   f'price type: {type(price)} expected: {float}' \
                   f'quantity type: {type(quantity)} expected {int}' \
                   f'indicator type: {type(indicator)} expected {str}'
        except Exception as e:
            return f'An error occured while processing stock: {stock}: {str(e)}'



class SuperSimpleStockMarket:
    '''
        This class the simple methods for the super simple stock market
    '''

    def _check_stock(self, stock: str, dataset: str='stock_dividend_data') -> bool:
        '''
            Helper method to determine if stock is in dataset
        :param stock:
        :param dataset:
        :return:
        '''
        if dataset == 'stock_dividend_data':
            stocks = StocksData().stock_dividend_data['stock']
        else:
            stocks = StocksData().stock_transactions['stock']
        return True if stocks.isin([f'{stock}']).any() else False

    def get_stocks(self, dataset: str='stock_dividend_data') -> NDArray[str]:
        '''
            Helper method to return stocks in a given dataset
        :param dataset:
        :return:
        '''
        return StocksData().stock_dividend_data['stock'] if dataset == 'stock_dividend_data' \
            else StocksData().stock_transactions['stock']

    def calculate_dividend_yield(self, stock: str, price: float) -> Union[float, str]:
        '''
            This method calculates the dividend yield given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        try:
            stocks_data = StocksData()
            stocks = self.get_stocks()
            if not self._check_stock(stock):
                return f'The stock={stock} is not currently in the stock dividend dataset.'

            stock_info = stocks_data.stock_dividend_data[stocks == f'{stock}']
            last_dividend = stock_info['last_dividend']
            fixed_dividend = stock_info['fixed_dividend']
            par_value = stock_info['par_value']
            if (stock_info['type'].astype('string') == 'Common').any():
                dividend_yield = np.round((last_dividend / price).iloc[0], decimals=2)
            else:
                dividend_yield = np.nan if np.isnan(fixed_dividend).any() else \
                    np.round(((fixed_dividend * par_value) / price).iloc[0], decimals=2)

            return dividend_yield
        except TypeError:
            return f'Invalid input data types stock type {type(stock)} expected {str}, ' \
                   f'price type {type(price)} expected {float}'
        except Exception as e:
            return f'An error occured while processing stock: {stock}: {str(e)}'

    def calculate_pe_ratio(self, stock: str, price: float) -> Union[float, str]:
        '''
            This function calculates the pe ratio given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        try:
            stocks_data = StocksData()
            stocks = self.get_stocks()
            if not self._check_stock(stock):
                return f'The stock={stock} is not currently in the stock dividend dataset.'
            stock_info = stocks_data.stock_dividend_data[stocks == f'{stock}']
            dividend = stock_info['last_dividend']
            pe = np.nan if np.isnan(dividend).any() else \
                np.round((price / dividend).iloc[0], decimals=2)
            return pe
        except TypeError:
            return f'Invalid input data types stock type {type(stock)} expected {str}, ' \
                   f'price type {type(price)} expected {float}'
        except Exception as e:
            return f'An error occured while processing stock: {stock}: {str(e)}'


    def calculate_volume_weighted_stock_price(self, stock: str,
                                              minutes: int=15) -> Union[float, str]:
        '''
            This method calculates the vwap for a stock at some specified time interval
        :param stock:
        :param minutes:
        :return:
        '''
        try:
            stocks_data = StocksData()
            if not self._check_stock(stock, 'transactions'):
                return f'The stock={stock} is not currently in the stock transactions dataset.'
            now = pd.Timestamp.now()
            time_range = now - timedelta(minutes=minutes)

            current_stock_data = stocks_data.stock_transactions[
                (stocks_data.stock_transactions['stock'] == stock) &
                (stocks_data.stock_transactions['timestamp'] >= time_range)].copy()

            current_stock_data['price_volume'] = \
                current_stock_data['price'] * current_stock_data['quantity']
            total_price_volume = current_stock_data['price_volume'].sum()
            total_quantity = current_stock_data['quantity'].sum()

            return np.round(total_price_volume / total_quantity, decimals=2) \
                if total_quantity > 0 else np.nan
        except TypeError:
            return f'Invalid input data types stock type {type(stock)} expected {str}, ' \
                   f'minutes type {type(minutes)} expected {int}'
        except Exception as e:
            return f'An error occured while processing stock: {stock}: {str(e)}'

    def calculate_geometric_mean(self) -> Union[float, str]:
        '''
            This method calculates the geometric mean for all
            stocks based off of last transaction price
        :return:
        '''
        try:
            stocks_data = StocksData()
            last_transactions = stocks_data.stock_transactions.\
                groupby('stock').last().reset_index()
            last_prices = last_transactions['price']
            return np.round(gmean(last_prices), decimals=2) \
                if len(last_prices) > 0 else np.nan
        except Exception as e:
            return f'The following error occured while calculating the geometric mean: {str(e)}.'

if __name__ == '__main__':
    sm = SuperSimpleStockMarket()
    print(sm.calculate_pe_ratio('GIN', 100))
