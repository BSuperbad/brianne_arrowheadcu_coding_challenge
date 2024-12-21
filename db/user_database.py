"""SQL database for arrowhead user information"""

import os
import sqlite3


def create_connection(db_name="arrow_users.db"):
    # Delete old db (if exists) and create new one
    if os.path.exists(db_name):
        os.remove(db_name)
    return sqlite3.connect(db_name)


def create_table(connection):
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


def insert_user(connection, user):
    """Insert user data into users, addresses, geo, and companies tables"""
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
