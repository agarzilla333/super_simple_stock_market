from src import super_simple_stock_market
import pandas as pd
import numpy as np

def test_calculate_dividend_yield():
    sm = super_simple_stock_market.SuperSimpleStockMarket()
    dividend_yield = sm.calculate_dividend_yield('POP', 200)
    assert dividend_yield == 0.04

    dividend_yield = sm.calculate_dividend_yield('GIN', 100)
    assert dividend_yield == 0.02

    dividend_yield = sm.calculate_dividend_yield('AAPL', 200)
    assert dividend_yield == 'The stock=AAPL is not currently in the stock dividend dataset.'


def test_calculate_pe_ratio():
    sm = super_simple_stock_market.SuperSimpleStockMarket()
    pe = sm.calculate_pe_ratio('POP', 200)
    assert pe == 25.00

    pe = sm.calculate_pe_ratio('GIN', 100)
    assert pe == 12.50

    pe = sm.calculate_pe_ratio('AAPL', 500)
    assert pe == 'The stock=AAPL is not currently in the stock dividend dataset.'


def test_record_trade():
    time_now = pd.Timestamp.now().tz_localize('UTC')
    stocks_data = super_simple_stock_market.StocksData()

    stocks_data.record_trade(time_now, 'TSLA', 20000, 'BUY', 175.00)
    assert stocks_data.stock_transactions['stock'].isin(['TSLA']).any() == True

    stocks_data.record_trade(time_now, 'GOOG', 20000, 'BUY', 177.00)
    assert stocks_data.stock_transactions['stock'].isin(['GOOG']).any() == True

    assert stocks_data.stock_transactions.shape[0] == 2


def test_calculate_volume_weighted_stock_price():
    time_now = pd.Timestamp.now().tz_localize('UTC')
    stocks_data = super_simple_stock_market.StocksData()
    simple_market = super_simple_stock_market.SuperSimpleStockMarket()
    for i in range(0, 1000, 100):
        price = 170 + (i%3)
        shares = i
        stocks_data.record_trade(time_now, 'GE', shares, 'BUY', price)

    stocks_data.record_trade(time_now, 'MSFT', 0, 'BUY', 177.50)

    assert simple_market.calculate_volume_weighted_stock_price('GE') == 170.93
    assert simple_market.calculate_volume_weighted_stock_price('AAPL') == \
           'The stock=AAPL is not currently in the stock transactions dataset.'
    assert np.isnan(simple_market.calculate_volume_weighted_stock_price('MSFT'))

def test_calculate_geometric_mean():
    time_now = pd.Timestamp.now().tz_localize('UTC')
    stocks_data = super_simple_stock_market.StocksData()
    simple_market = super_simple_stock_market.SuperSimpleStockMarket()
    stocks = ['AMZN', 'NVDA','BRK.B','META','UNH','XOM','LLY','JPM','JNJ','V']
    prices = [182.69, 948.33, 414.47, 464.82, 522.28, 118.40, 804.01, 198.05, 151.11, 275.16]
    side = ['BUY', 'BUY', 'SELL', 'BUY', 'SELL', 'BUY', 'SELL', 'BUY', 'BUY', 'BUY']
    for i in range(10):
        stocks_data.record_trade(time_now, stocks[i], 100, side[i], prices[i])
    assert simple_market.calculate_geometric_mean() == 326.26




