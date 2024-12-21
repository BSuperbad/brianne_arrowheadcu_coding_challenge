"""SQL database for arrowhead user information"""

import os
import sqlite3


def create_connection(db_name="arrow_users.db"):
    """Creating connection to the SQLite database"""
    try:
        # Delete old db (if exists) and create new one
        if os.path.exists(db_name):
            os.remove(db_name)
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        raise Exception(f"Error connecting to database {db_name}: {e}")


def create_table(connection):
    """Creating users table if it doesn't already exist"""
    try:
        with connection:
            connection.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                username TEXT,
                email TEXT,
                phone TEXT,
                website TEXT,
                address_street TEXT,
                address_suite TEXT,
                address_city TEXT,
                address_zipcode TEXT,
                geo_lat TEXT,
                geo_lng TEXT,
                company_name TEXT,
                company_catch_phrase TEXT,
                company_bs TEXT
            );
            """
            )
            connection.commit()
    except sqlite3.Error as e:
        raise Exception(f"Error creating table: {e}")


def insert_user(connection, user):
    """Insert user data into users table"""
    try:
        connection.execute(
            """
            INSERT INTO users (id, name, username, email, phone, website, address_street, address_suite, address_city, address_zipcode, geo_lat, geo_lng, company_name, company_catch_phrase, company_bs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                user["id"],
                user["name"],
                user["username"],
                user["email"],
                user["phone"],
                user["website"],
                user["address"]["street"],
                user["address"]["suite"],
                user["address"]["city"],
                user["address"]["zipcode"],
                user["address"]["geo"]["lat"],
                user["address"]["geo"]["lng"],
                user["company"]["name"],
                user["company"]["catchPhrase"],
                user["company"]["bs"],
            ),
        )
        connection.commit()
    except sqlite3.IntegrityError as e:
        raise e
    except sqlite3.Error as e:
        raise Exception(f"Error inserting data into table: {e}")
