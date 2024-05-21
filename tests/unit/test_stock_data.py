from src.stocks_data import StocksData
import pandas as pd

def test_singleton():
    instance1 = StocksData()
    instance2 = StocksData()

    assert instance1 is instance2

def test_record_trade():
    time_now = pd.Timestamp.now()
    stocks_data = StocksData()

    stocks_data.record_trade(time_now, 'TSLA', 20000, 'BUY', 175.00)
    assert stocks_data.stock_transactions['stock'].isin(['TSLA']).any() == True

    stocks_data.record_trade(time_now, 'GOOG', 20000, 'BUY', 177.00)
    assert stocks_data.stock_transactions['stock'].isin(['GOOG']).any() == True

    assert stocks_data.stock_transactions.shape[0] == 2