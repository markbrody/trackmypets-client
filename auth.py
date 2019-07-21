#!/usr/bin/env python3

import json
import sqlite3
import time
import requests
import os
import sys
from dotenv import load_dotenv
from alert import *

class Auth():

    DATABASE = ".trackmypets.db"
    API_ENDPOINT = "oauth/token"

    def __init__(self):
        sys.path.append(os.getcwd())
        load_dotenv(".env")
        self.api_host = os.environ.get("API_HOST") or "http://localhost/"
        self.__connect()
        self.api_url = self.api_host + self.API_ENDPOINT
        self.client_id = os.environ.get("CLIENT_ID")
        self.client_secret = os.environ.get("CLIENT_SECRET")
        self.now = int(time.time())
        self.conn = sqlite3.connect(
            "/".join([os.environ.get("HOME"), self.DATABASE])
        )
        if self.conn is not None:
            self.cursor = self.conn.cursor()
            self.__create_auth_db()
            self.__set_token(self.__local_token())
        else:
            print("No database connection")

    def request_new_token(self, **credentials):
        username = credentials.pop("username", None)
        password = credentials.pop("password", None)
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": username,
            "password": password,
            "scope": "*"
        }
        response = requests.request("POST", self.api_url, data=data)
        auth = json.loads(response.text)
        return self.__save_auth_db(auth) if "token_type" in auth else False
        
    def __connect(self):
        try:
            _ = requests.get(self.api_host, timeout=(5, 10))
        except requests.ConnectionError:
            alert = Alert("No internet connection")
            sys.exit(1)
        except requests.exceptions.RequestException:
            alert = Alert("Request timed out")
            sys.exit(1)
        except:
            alert = Alert("Cannot connect to api host")
            sys.exit(1)

    def __create_auth_db(self):
        sql = """
            CREATE TABLE IF NOT EXISTS auth (
                token text NOT NULL,
                expiration integer
            )
        """
        try:
            self.cursor.execute(sql)
        except Error as error:
            print(error)
    
    def __save_auth_db(self, auth):
        sql = "INSERT INTO auth (expiration, token) VALUES (?, ?)"
        expiration = self.now + auth['expires_in']
        token = auth['access_token']
        with self.conn:
            self.cursor.execute("DELETE FROM auth")
            self.cursor.execute(sql, (expiration, token, ))
        self.__set_token(auth['access_token'])
        return auth['access_token']

    def __local_token(self):
        sql = "SELECT token FROM auth WHERE expiration > ? LIMIT 1"
        self.cursor.execute(sql, (self.now, ))
        result = self.cursor.fetchone()
        return result if result is None else result[0]

    def __get_token(self):
        return self.__token

    def __set_token(self, token):
        self.__token = token

    token = property(__get_token, __set_token)

if __name__ == "__main__":
    auth = Auth()
    while auth.token is None:
        username = input("Username: ")
        password = input("Password: ")
        auth.request_new_token(username=username, password=password)
    print(auth.token)

