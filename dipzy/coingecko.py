import logging
import requests
import pandas as pd


logger = logging.getLogger(__name__) # module-level logger

class CoinGecko:
    base_url = 'https://api.coingecko.com/api/v3'

    def __init__(self):
        self.base_url = base_url

    def _request(self, endpoint, method="GET", params=None, **kwargs):
        url = self.base_url + endpoint 
        r = requests.request(method, url, params=params, **kwargs)
        if r.status_code != 200 and r.status_code != 201:
            raise Exception(f"Request error: {r.status_code} {r.text}")
        
        return r

    def convert_symbols(self, symbols=None):
        '''
        Convert token symbols to CoinGecko IDs. Does not return symbols not
        found in CoinGecko.
        
        Args:
            symbols (List): List of symbols. Symbols have to be lowercase.
        
        Returns:
            pandas.Series: Coingecko IDs
        ''' 
        endpoint =  "/coins/list"
        r = self._request(endpoint)
        coingecko_tokens = pd.read_json(r.json())
        coingecko_tokens.set_index('symbol', inplace=True)
        
        if symbols is None:
            return coingecko_tokens
        
        missing_symbols = [s for s in symbols if s not in coingecko_tokens.index]
        if len(missing_symbols) > 0:
            logger.info(
                f'Symbols missing from CoinGecko: {missing_symbols}'
            )
        
        present_symbols = set(coingecko_tokens.index.tolist()) & set(symbols)
        ids = coingecko_tokens.id.loc[present_symbols]
        
        ambiguous_symbols = ids.index[ids.index.duplicated(keep=False)].unique()
        if len(ambiguous_symbols) > 0:
            logger.info(f'Following symbols are ambiguous: {ambiguous_symbols}')
        
        ids.index = ids.index.str.upper()
        return ids

    def get_coins_markets(
        self,
        ids=None,
        select=['symbol', 'name', 'current_price', 'total_volume'],
        order='market_cap',
        timepoints='24h'
    ):
        '''
        Get prices market data of tokens from CoinGecko API: coins/markets.
        If ids is not provided, returns top tokens ranked by total volume.
        
        Args:
            ids (List): List of coingecko IDs.
            select (List): List of column names of coingecko response data.
            timepoints (str): Time points of percentage change. E.g. '24h,7d,1y'
        
        Return:
            pandas.DataFrame: Prices and percentage change of tokens.
        '''
        endpoint = "/coins/markets"
        
        if ids is not None:
            ids_str = ','.join(ids)
            params = {
                'vs_currency': 'usd',
                'ids': ids_str,
                'order': order,
                'price_change_percentage': timepoints
            }
        else:
            params = {
                'vs_currency': 'usd',
                'order': 'volume_desc',
                'price_change_percentage': timepoints
            }
        
        r = self._request(endpoint, params=params)
        data = pd.DataFrame(response.json())
        
        # Filter out unnecessary info from data
        list_timepoints = timepoints.split(',')
        keys_timepoints = [
            f'price_change_percentage_{x}_in_currency'
            for x in list_timepoints
        ]

        features = select + keys_timepoints
        data_selected = data[features]
        data_selected.columns = select + list_timepoints
        # data_selected.sort_values('symbol', inplace=True)
        
        return data_selected
