#!/usr/bin/env python3

from auth import Auth
from rest_client import RestClient

class Order(RestClient):
    API_ENDPOINT = "api/admin/orders/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)


class OrderStatus(RestClient):
    API_ENDPOINT = "api/order_statuses/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)


class User(RestClient):
    API_ENDPOINT = "api/admin/users/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)


if __name__ == "__main__":
    auth = Auth()
    order_status = OrderStatus(auth.token)
    print(order_status.get())

