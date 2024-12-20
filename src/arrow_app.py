"""Brianne Wilhelmi Arrowhead CU Coding Challenge December 2024"""

import os
import sys

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from db import user_database


USERS_URL = "https://jsonplaceholder.typicode.com/users"


# 1. FETCH USER DATA
def fetch_users(url):
    """Fetching all user records from json url"""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    users = fetch_users(USERS_URL)
    print("#2. Display Records")
    for user in users:
        print(
            f"ID: {user['id']}, Name: {user['name']}, Username: {user['username']}, Email: {user['email']}, Address: {user['address']['street']} {user['address']['suite']}, {user['address']['city']}, {user['address']['zipcode']}, Phone: {user['phone']}, Website: {user['website']}, Company: {user['company']['name']}, {user['company']['catchPhrase']} "
        )

    # connecting to db
    connection = user_database.create_connection()

    # add table to db
    user_database.create_table(connection)
    return connection


if __name__ == "__main__":
    main()
