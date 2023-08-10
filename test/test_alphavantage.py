import os
import unittest
import dipzy as dz


class TestGetDaily(unittest.TestCase):
    def setUp(self):
        # API is restricted to 5 calls per minute
        api_key = os.environ.get("ALPHAVANTAGE_KEY")
        self.av = dz.AlphaVantage(api_key)
    
    def test_get_market_status(self):
        r = self.av.get_market_status()
        self.assertNotIn("Error Message", r.json()) 

    def test_get_daily_ohlcv(self):
        ohlcv = self.av.get_daily_ohlcv("AAPL", outputsize="full")

    def test_price_commodities(self):
        data = self.av.price_commodities("WTI")

    def test_FFR(self):
        data = self.av.FFR()
    
    def test_CPI(self):
        data = self.av.CPI()
