import pandas as pd
import numpy as np

class StockData:
    '''
        This class holds the data for the static stock dividend data frame
        and the stock transactions data frame
    '''
    stock_dividend_data = pd.DataFrame({
        'stock': ['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
        'type': ['Common', 'Common', 'Common', 'Preferred', 'Common'],
        'last_dividend': [0, 8, 23, 8, 12],
        'fixed_dividend': [np.nan, np.nan, np.nan, .02, np.nan],
        'par_value': [100, 100, 60, 100, 250]
    })
    stock_transactions = pd.DataFrame({
        'timestamp': [],
        'stock': [],
        'quantity': [],
        'indicator': [],
        'price': []
    })

class SuperSimpleStockMarket:
    '''
        This class has the 5 functions for the simple stock market
    '''
    def calculate_dividend_yield(self, stock, price):
        '''
            This method calculates the dividend yield given a stock and price
        :param stock:
        :param price:
        :return:
        '''
        stocks = StockData.stock_dividend_data['stock']
        if stocks.isin([f'{stock}']).any():
            stock_info = StockData.stock_dividend_data[stocks == f'{stock}']
        else:
            return f'The stock={stock} is not currently in the stock dividend dataset.'

        last_dividend = stock_info['last_dividend']
        fixed_dividend = stock_info['fixed_dividend']
        par_value = stock_info['par_value']
        if (stock_info['type'].astype('string') == 'Common').bool():
            dividend_yield = last_dividend / price
        else:
            dividend_yield = None if np.isnan(fixed_dividend).bool() else (fixed_dividend * par_value) / price

        return dividend_yield.iloc[0]



if __name__ == '__main__':
    sm = SuperSimpleStockMarket()
    # print(sm.calculate_dividend_yield('AAPL', 200))
    print(sm.calculate_dividend_yield('GIN', 100))