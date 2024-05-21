import pandas as pd
import numpy as np

class StockData:
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
            cls._instance = super(StockData, cls).__new__(cls)
            cls._initialize_data()
        return cls._instance

    @staticmethod
    def _initialize_data():
        '''
            This private function initializes stock dividend and stock transactions data.
        :return:
        '''
        StockData.stock_dividend_data = pd.DataFrame({
            'stock': ['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
            'type': ['Common', 'Common', 'Common', 'Preferred', 'Common'],
            'last_dividend': [0, 8, 23, 8, 12],
            'fixed_dividend': [np.nan, np.nan, np.nan, .02, np.nan],
            'par_value': [100, 100, 60, 100, 250]
        })
        StockData.stock_transactions = pd.DataFrame({
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
        StockData.stock_transactions = pd.concat([StockData.stock_transactions, new_record], ignore_index=True)


class SuperSimpleStockMarket:
    '''
        This class has the 5 functions for the super simple stock market
    '''
    def _check_stock(self, stock):
        stocks = StockData().stock_dividend_data['stock']
        return True if stocks.isin([f'{stock}']).any() else False

    def calculate_dividend_yield(self, stock, price):
        '''
            This method calculates the dividend yield given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        stock_data = StockData()
        stocks = stock_data.stock_dividend_data['stock']
        if self._check_stock(stock):
            stock_info = stock_data.stock_dividend_data[stocks == f'{stock}']
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
        stock_data = StockData()
        stocks = stock_data.stock_dividend_data['stock']
        if self._check_stock(stock):
            stock_info = stock_data.stock_dividend_data[stocks == f'{stock}']
        else:
            return f'The stock={stock} is not currently in the stock dividend dataset.'

        dividend = stock_info['last_dividend']
        pe = np.nan if np.isnan(dividend).bool() else np.round((price / dividend).iloc[0], decimals=2)
        return pe







if __name__ == '__main__':
    sm = SuperSimpleStockMarket()
    print(sm.calculate_pe_ratio('GIN', 100))
