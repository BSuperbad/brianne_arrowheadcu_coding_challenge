"""Brianne Wilhelmi Arrowhead CU Coding Challenge December 2024"""

import os
import sqlite3
import sys

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from src.db import user_database
from src.utilities import helpers

USERS_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_users(url):
    """Fetching all user records from json url"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f"Error fetching users: {err}")
        return []


def sort_records(connection):
    """Sort records by name, ignoring any title like 'Mr.' or 'Mrs.'"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users ORDER BY name ASC;")
        records = cursor.fetchall()
        sorted_records = sorted(records, key=lambda r: helpers.remove_titles(r[1]))
        return sorted_records
    except sqlite3.DatabaseError as err:
        print(f"Error querying db: {err}")
        return []


def update_email(connection, email, user_id):
    """Update a user's email address by their user ID."""
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
        connection.commit()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated_user = cursor.fetchone()
        return updated_user
    except sqlite3.DatabaseError as err:
        print(f"Error updating email: {err}")
        return None


def filter_by_longitude(connection, geo_lng):
    """Filter users by longitude greater than specified value & sorts by name ascending"""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE CAST(geo_lng AS FLOAT) > ? ORDER BY name ASC ;",
            (geo_lng,),
        )
        records = cursor.fetchall()
        sorted_records = sorted(records, key=lambda r: helpers.remove_titles(r[1]))
        return sorted_records
    except sqlite3.DatabaseError as err:
        print(f"Error filtering records by lng: {err}")
        return []


def main():
    # 1. FETCH USER DATA
    users = fetch_users(USERS_URL)
    print(f"#1. Fetch User Data: {users}")

    # 2. DISPLAY RECORDS
    print("#2. Display Records:")
    for user in users:
        print(
            f"ID: {user['id']}, Name: {user['name']}, Username: {user['username']}, Email: {user['email']}, Address: {user['address']['street']} {user['address']['suite']}, {user['address']['city']}, {user['address']['zipcode']}, Phone: {user['phone']}, Website: {user['website']}, Company: {user['company']['name']}, {user['company']['catchPhrase']}"
        )

    # connecting to db
    connection = user_database.create_connection()

    # 3. CREATE SQL TABLE
    user_database.create_table(connection)

    # 4. INSERT USER RECORDS INTO TABLE
    for user in users:
        user_database.insert_user(connection, user)
        print("inserting users into db")
    connection.commit()

    # 5. SORT RECORDS BY NAME ASCENDING
    sorted_records = sort_records(connection)
    print("#5. Sort Records:")
    for r in sorted_records:
        helpers.print_user_record(r, record_type="Sorted")

    # 6. UPDATE EMAIL OF ADDRESS WITH ID OF 9 TO `coding@arrowheadcu.org`
    updated_record = update_email(connection, "coding@arrowheadcu.org", 9)
    print("#6. Update Email:")
    helpers.print_user_record(updated_record, record_type="Updated Email")

    # 7. FILTER USERS TO ONLY RETRIEVE ALL USERS WITH LONGITUDE GREATER THAN -110.445
    lng_filtered_records = filter_by_longitude(connection, "-110.445")
    print(f"#7. Filtered by Longitude Greater than -110.445:")
    for r in lng_filtered_records:
        helpers.print_user_record(r, record_type="Filtered by Longitude")


if __name__ == "__main__":
    main()
