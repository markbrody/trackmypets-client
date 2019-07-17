#!/usr/bin/env python3

from rest_client import RestClient

class OrderStatus(RestClient):
    API_ENDPOINT = "api/order_statuses/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)

if __name__ == "__main__":
    order_status = OrderStatus()
    print(order_status.get())

