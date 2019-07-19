#!/usr/bin/env python3

from rest_client import RestClient

class Order(RestClient):
    API_ENDPOINT = "api/admin/orders/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)

if __name__ == "__main__":
    order = Order()
    print(order.get())

