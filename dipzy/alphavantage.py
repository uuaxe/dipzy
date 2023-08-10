from typing import Iterable

import math
import requests
import time

import numpy as np
import pandas as pd


class AlphaVantage:
    base_url = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def _request(self, func, symbol=None, method="GET", params=None, **kwargs):
        parameters = {
            "function": func,
            "symbol": symbol,
            "apikey": self.api_key
        }
        if params is not None:
            parameters.update(params)
            
        # fixed API endpoint (i.e. URL)
        r = requests.request(
            method, self.base_url, params=parameters, **kwargs
        )
        # Alphavantage API does not reflect error in status code 
        if "Error Message" in r.json(): 
            raise Exception(f"Request error: {r.json()['Error Message']}")
        
        return r
    
    def _batch_request(
        self, func, symbols: Iterable[str], method="GET", **kwargs
    ) -> Iterable:
        # Group API calls into batches of 5 to overcome rate limit
        if isinstance(symbols, str):
            symbols = [symbols]
        
        jsons = []
        start, stop = 0, 5
        n = math.ceil(len(symbols) / 5)
        print(f"Bundling API calls into {n} batches.")
        while stop < len(symbols):
            for symbol in symbols[start:stop]:
                jsons.append(
                    self._request(func, symbol, method, **kwargs).json()
                )
            print("Sleeping for 1 minute before next batch.")
            time.sleep(60)
            start += 5
            stop += 5    
        # Last batch
        for symbol in symbols[start:len(symbols)]:
            jsons.append(self._request(func, symbol, method, **kwargs).json())
            
        return jsons
    
    def get_market_status(self):
        r = self._request("MARKET_STATUS")
        return r

    def FFR(self, interval="monthly"):
        '''Federal funds rate
        '''
        r = self._request("FEDERAL_FUNDS_RATE", params={"interval": interval})
        data = pd.DataFrame(r.json()["data"])
        data.set_index("date", inplace=True)
        data.index = pd.to_datetime(data.index)
        data = data.apply(pd.to_numeric)
        return data
    
    def CPI(self, interval="monthly"):
        '''CPI
        '''
        r = self._request("CPI", params={"interval": interval})
        data = pd.DataFrame(r.json()["data"])
        data.set_index("date", inplace=True)
        data.index = pd.to_datetime(data.index)
        data = data.apply(pd.to_numeric)
        return data

    def price_commodities(self, commodities, interval="monthly"):
        '''
        Args:
            commodities (str): [WTI, BRENT, NATURAL_GAS, COPPER, ALUMINUM,
                WHEAT, CORN, COTTON, SUGAR, COFFEE, ALL_COMMODITIES]
        '''
        r = self._request(commodities, params={"interval": interval})
        data = pd.DataFrame(r.json()["data"])
        data.set_index("date", inplace=True)
        data.index = pd.to_datetime(data.index)
        data.replace({".": np.nan}, inplace=True)
        data = data.apply(pd.to_numeric)
        return data
    
    def get_fundamentals(self, symbols: Iterable[str]):
        jsons = self._batch_request("OVERVIEW", symbols)
        data = pd.DataFrame(jsons)
        data.set_index("Symbol", inplace=True)
        data.replace("-", np.nan, inplace=True)
        
        return data.apply(pd.to_numeric, errors="ignore")
    
    def get_income_statement(self, symbols: str):
        # TODO: Complete
        jsons = self._batch_request("INCOME_STATEMENT", symbols)
        return jsons
#         data = pd.DataFrame(jsons)
#         data.replace("-", np.nan, inplace=True)
#         return data.apply(pd.to_numeric, errors="ignore")

    def get_price(self, symbols: str):
        jsons = self._batch_request("GLOBAL_QUOTE", symbols)
        prices = [
            [d["Global Quote"]["01. symbol"], d["Global Quote"]["05. price"]]
            for d in jsons
        ]
        data = pd.DataFrame(prices, columns=["Symbol", "Price"]).set_index("Symbol")
        return data

    def get_daily_ohlcv(
        self, symbols: Iterable[str], outputsize="compact"
    ) -> list | pd.DataFrame:
        # outputsize: ["compact", "full"]
        jsons = self._batch_request(
            "TIME_SERIES_DAILY_ADJUSTED", symbols,
            params={"outputsize": outputsize}
        )
        list_ohlcv = [
            pd.DataFrame.from_dict(
                json['Time Series (Daily)'], orient="index", dtype='float'
            ).sort_index() for json in jsons
        ]
        colnames = {colname: colname[3:] for colname in list(list_ohlcv[0])}
        for data in list_ohlcv:
            data.rename(columns=colnames, inplace=True)
            data.index = pd.to_datetime(data.index)

        if len(list_ohlcv) == 1:
            return list_ohlcv[0]

        return list_ohlcv
