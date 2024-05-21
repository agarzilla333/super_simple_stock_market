from src import super_simple_stock_market

def test_calculate_dividend_yield():
    sm = super_simple_stock_market.SuperSimpleStockMarket()
    dividend_yield = sm.calculate_dividend_yield('POP', 200)
    assert dividend_yield == 0.04

    dividend_yield = sm.calculate_dividend_yield('GIN', 100)
    assert dividend_yield == 0.02

    dividend_yield = sm.calculate_dividend_yield('AAPL', 200)
    assert dividend_yield == 'The stock=AAPL is not currently in the stock dividend dataset.'