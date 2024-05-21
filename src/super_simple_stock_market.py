'''
This module has class SuperSimpleStockMarket which handles the basic stock calculations
'''

from datetime import timedelta
from typing import Union
from scipy.stats import gmean
from numpy.typing import NDArray
from .stocks_data import StocksData
import pandas as pd
import numpy as np


class SuperSimpleStockMarket:
    '''
    This class has simple methods for calculating metrics
    related to the super simple stock market
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
        This method calculates the geometric mean for all stocks
        based off of last transaction price
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
