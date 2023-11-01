#!/usr/bin/python3
""" Create a secret key printed to stdout. """
import secrets

if __name__ == '__main__':
    secret_key = secrets.token_hex(24)
    print(secret_key)
