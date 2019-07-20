#!/usr/bin/env python3

from rest_client import RestClient

class Version(RestClient):
    API_ENDPOINT = "api/version/"

    def __init__(self, *args, **kwargs):
        RestClient.__init__(self, *args, **kwargs)

if __name__ == "__main__":
    version = Version()
    print(version.get())

