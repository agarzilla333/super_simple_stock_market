from src import super_simple_stock_market

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