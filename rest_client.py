#!/usr/bin/env python3

import json
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

class RestClient:

    def __init__(self, token=None):
        load_dotenv(join(dirname(__file__), '.env'))
        self.api_host = os.environ.get("API_HOST") or "http://localhost/"
        self.token = token
        try:
            self.api_url = self.api_host + self.API_ENDPOINT
        except:
            self.api_url = None

    def get(self, **options):
        options.update({"method": "GET"})
        response = self.__request(**options)
        return json.loads(response)

    def put(self, **options):
        options.update({"method": "PUT"})
        response = self.__request(**options)
        return json.loads(response)

    def post(self):
        pass

    def delete(self):
        pass

    def __request(self, **options):
        if self.api_url is not None:
            method = options.pop("method", "GET")
            id = options.pop("id", None)
            data = options.pop("data", {})
            params = options.pop("params", {})
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            }
            api_url = self.api_url if id is None else self.api_url + id
            response = requests.request(method, api_url, headers=headers,
                                        params=params, data=data)
            return response.text

if __name__ == "__main__":
    rest_client = RestClient("foo")
    print(rest_client.api_host)
    print(rest_client.token)

