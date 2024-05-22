'''
This module has the class StocksData which creates a singleton to access
stock dividend data and stock transactions data.
'''
from pandas import Timestamp
from src.utils.logger import error_logger

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
                     indicator: str, price: float) -> None:
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
            error_logger.log(level=4, msg=f'Invalid input data types ' \
                   f'timestamp type: {type(timestamp)} expected: {Timestamp}' \
                   f'stock type: {type(stock)} expected: {str}' \
                   f'price type: {type(price)} expected: {float}' \
                   f'quantity type: {type(quantity)} expected {int}' \
                   f'indicator type: {type(indicator)} expected {str}')
            raise TypeError(f'Invalid input data types ' \
                   f'timestamp type: {type(timestamp)} expected: {Timestamp}' \
                   f'stock type: {type(stock)} expected: {str}' \
                   f'price type: {type(price)} expected: {float}' \
                   f'quantity type: {type(quantity)} expected {int}' \
                   f'indicator type: {type(indicator)} expected {str}')
        except Exception as e:
            error_logger.log(level=4, msg=f'An error occured while '
                                          f'processing stock: {stock}: {str(e)}')
            raise Exception(f'An error occured while processing stock: {stock}: {str(e)}')