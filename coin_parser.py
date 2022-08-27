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

    def __get_keys_values(self, options: str) -> dict[Any, Any]:
        response = self.__get_response(options)
        return dict.copy(response.json())

    def __get_response(self, option: str) -> json:
        url = f'{self.base_url}{option}'
        return requests.get(url)

    def get_live_data(self) -> dict:
        return self.__get_keys_values(f'live?access_key={self.api_access_key}')

    def get_historical_data(self, date: str) -> dict | str:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            date_str = date_obj.strftime('%Y-%m-%d')
            return self.__get_keys_values(f'{date_str}?access_key={self.api_access_key}')
        except Exception as ex:
            return f'{ex}\n enter a date in the correct format: YYYY-MM-DD'


