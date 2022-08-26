from __future__ import annotations
import json
from typing import Any
from datetime import datetime
import requests


class CoinlayerParser:
    """
    https://coinlayer.com/documentation
    Options:
        - live - get live json dict
        - date(YYYY-MM-DD) - get historical data
    """

    def __init__(self, api_access_key: str, base_url: str):
        self.api_access_key = api_access_key
        self.base_url = base_url

    def get_keys_values(self, options: str) -> dict[Any, Any]:
        response = self.get_response(options)
        return dict.copy(response.json())

    def get_response(self, option: str) -> json:
        url = f'{self.base_url}{option}'
        return requests.get(url)

    def get_live_data(self) -> dict:
        return self.get_keys_values(f'live?access_key={self.api_access_key}')

    def get_historical_data(self, date: str) -> dict | str:
        try:
            date = datetime.strftime(date, r'%y-%m-%d')
        except Exception as ex:
            return f'{ex}\n enter the date in the correct format: YYYY-MM-DD'
        finally:
            return self.get_keys_values(f'{date}?access_key={self.api_access_key}')
