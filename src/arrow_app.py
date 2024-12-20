"""Brianne Wilhelmi Arrowhead CU Coding Challenge December 2024"""

import requests

USERS_URL = "https://jsonplaceholder.typicode.com/users"

# 1. FETCH USER DATA
def fetch_users(url):
    """Fetching all user records from json url"""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    users = fetch_users(USERS_URL)
    print(users)

if __name__ == "__main__":
    main()