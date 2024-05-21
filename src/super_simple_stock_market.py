from datetime import timedelta

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

    def record_trade(self, timestamp, stock, quantity, indicator, price):
        '''
            This function records stock transactions.
        :param timestamp:
        :param stock:
        :param quantity:
        :param indicator:
        :param price:
        :return:
        '''
        new_record = pd.DataFrame({
            'timestamp': [timestamp],
            'stock': [stock],
            'quantity': [quantity],
            'indicator': [indicator],
            'price': [price]
        })
        StocksData.stock_transactions = pd.concat([StocksData.stock_transactions, new_record], ignore_index=True)


class SuperSimpleStockMarket:
    '''
        This class the simple methods for the super simple stock market
    '''

    def _check_stock(self, stock, dataset='stock_dividend_data'):
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

    def get_stocks(self, dataset='stock_dividend_data'):
        '''
            Helper method to return stocks in a given dataset
        :param dataset:
        :return:
        '''
        return StocksData().stock_dividend_data['stock'] if dataset == 'stock_dividend_data' \
            else StocksData().stock_transactions['stock']

    def calculate_dividend_yield(self, stock, price):
        '''
            This method calculates the dividend yield given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        stocks_data = StocksData()
        stocks = self.get_stocks()
        if self._check_stock(stock):
            stock_info = stocks_data.stock_dividend_data[stocks == f'{stock}']
        else:
            return f'The stock={stock} is not currently in the stock dividend dataset.'

        last_dividend = stock_info['last_dividend']
        fixed_dividend = stock_info['fixed_dividend']
        par_value = stock_info['par_value']
        if (stock_info['type'].astype('string') == 'Common').bool():
            dividend_yield = np.round((last_dividend / price).iloc[0], decimals=2)
        else:
            dividend_yield = np.nan if np.isnan(fixed_dividend).bool() else np.round(((fixed_dividend * par_value) / price).iloc[0], decimals=2)

        return dividend_yield

    def calculate_pe_ratio(self, stock, price):
        '''
            This function calculates the pe ratio given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        stocks_data = StocksData()
        stocks = self.get_stocks()
        if self._check_stock(stock):
            stock_info = stocks_data.stock_dividend_data[stocks == f'{stock}']
        else:
            return f'The stock={stock} is not currently in the stock dividend dataset.'

        dividend = stock_info['last_dividend']
        pe = np.nan if np.isnan(dividend).bool() else np.round((price / dividend).iloc[0], decimals=2)
        return pe

    def calculate_volume_weighted_stock_price(self, stock, minutes=15):
        stocks_data = StocksData()
        if not self._check_stock(stock, 'transactions'):
            return f'The stock={stock} is not currently in the stock transactions dataset.'
        now = pd.Timestamp.now().tz_localize('UTC')
        time_range = now - timedelta(minutes=minutes)

        current_stock_data = stocks_data.stock_transactions[
            (stocks_data.stock_transactions['stock'] == stock) &
            (stocks_data.stock_transactions['timestamp'] >= time_range)
        ]

        current_stock_data['price_volume'] = current_stock_data['price'] * current_stock_data['quantity']
        total_price_volume = current_stock_data['price_volume'].sum()
        total_quantity = current_stock_data['quantity'].sum()

        return np.round(total_price_volume / total_quantity, decimals=2) if total_quantity > 0 else np.nan






if __name__ == '__main__':
    sm = SuperSimpleStockMarket()
    print(sm.calculate_pe_ratio('GIN', 100))
