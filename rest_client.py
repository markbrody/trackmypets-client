#!/usr/bin/env python3

import json
import requests
import os
import sys
from dotenv import load_dotenv
from alert import *

class RestClient:

    def __init__(self, token=None):
        sys.path.append(os.getcwd())
        load_dotenv(".env")
        self.api_host = os.environ.get("API_HOST") or "http://localhost/"
        self.token = token
        try:
            self.api_url = self.api_host + self.API_ENDPOINT
        except:
            self.api_url = None

    def get(self, **options):
        options.update({"method": "GET"})
        return self.request(**options)

    def put(self, **options):
        options.update({"method": "PUT"})
        return self.request(**options)

    def post(self):
        pass

    def delete(self):
        pass

    def request(self, **options):
        method = options.pop("method", "GET")
        url = options.pop("url", None)
        id = options.pop("id", None)
        data = options.pop("data", {})
        params = options.pop("params", {})
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        if url is not None:
            api_url = url
        elif self.api_url is not None:
            api_url = self.api_url if id is None else self.api_url + str(id)
        else:
            api_url = "http://localhost/"
        try:
            response = requests.request(
                method, api_url, headers=headers, params=params, data=data,
                timeout=(5, 30)
            )
        except:
            alert = Alert("Request failed.")
        else:
            return json.loads(response.text)

if __name__ == "__main__":
    rest_client = RestClient("foo")
    print(rest_client.api_host)
    print(rest_client.token)

