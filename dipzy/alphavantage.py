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
    
    def _request(self, func, symbol, method="GET", **kwargs):
        params = {
            "function": func,
            "symbol": symbol,
            "apikey": self.api_key
        }
        # fixed API endpoint (i.e. URL)
        response = requests.request(
            method, self.base_url, params=params, **kwargs
        )
        if response.status_code != 200 and response.status_code != 201:
            raise Exception(
                f"Request returned an error: {response.status_code} {response.text}"
            )
        return response
    
    def _batch_request(self, func, symbols: Iterable[str], method="GET") -> Iterable:
        # Group API calls into batches of 5 to overcome rate limit
        if isinstance(symbols, str):
            symbols = [symbols]
            
        jsons = []
        start, stop = 0, 5
        n = math.ceil(len(symbols) / 5)
        print(f"Bundling API calls into {n} batches.")
        while stop < len(symbols):
            for symbol in symbols[start:stop]:
                jsons.append(self._request(func, symbol, method).json())
            print("Sleeping for 1 minute before next batch.")
            time.sleep(60)
            start += 5
            stop += 5    
        # Last batch
        for symbol in symbols[start:len(symbols)]:
            jsons.append(self._request(func, symbol, method).json())
            
        return jsons
    
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
