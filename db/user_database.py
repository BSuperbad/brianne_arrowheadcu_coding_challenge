"""SQL database for arrowhead user information"""

import os
import sqlite3


def create_connection(db_name="arrow_users.db"):
    # Delete old db (if exists) and create new one
    if os.path.exists(db_name):
        os.remove(db_name)
    return sqlite3.connect(db_name)


# 3. CREATE SQL TABLE TO STORE THE USER DATA
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
            geo_lng TEXT
        );
        """
        )
        print("Table 'users' created or already exists.")
        connection.commit()
