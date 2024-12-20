"""Brianne Wilhelmi Arrowhead CU Coding Challenge December 2024"""

import os
import sys

import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from db import user_database


USERS_URL = "https://jsonplaceholder.typicode.com/users"
TITLE_PATTERN = ["Mr.", "Mrs.", "Ms.", "Dr.", "Miss", "Ms."]


# 1. FETCH USER DATA
def fetch_users(url):
    """Fetching all user records from json url"""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


# helper function to remove titles
def remove_titles(name):
    """Remove common titles from a name (TITLE_PATTERN) and then returns as is for sorting"""
    for title in TITLE_PATTERN:
        if name.startswith(title):
            return name[len(title) :].strip()
    return name


# 5. SORT RECORDS BY NAME
def sort_records(connection):
    """Sort records by name, ignoring any title like 'Mr.' or 'Mrs.'"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY name ASC;")
    records = cursor.fetchall()
    sorted_records = sorted(records, key=lambda r: remove_titles(r[1]))
    return sorted_records


# 6. UPDATE EMAIL WITH USER ID OF 9
def update_email(connection, email, user_id):
    """Dynamically update email address for user by passing in user id variable and email variable."""
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
    connection.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    updated_user = cursor.fetchone()
    return updated_user


# 7. FILTER BY LONGITUDE
def filter_by_longitude(connection, geo_lng):
    """Filter users by longitude greater than specified value & sorts by name ascending"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE CAST(geo_lng AS FLOAT) > ? ORDER BY name ASC ;",
        (geo_lng,),
    )
    return cursor.fetchall()


def main():
    users = fetch_users(USERS_URL)
    print("#2. Display Records")
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
        print(
            f"ID: {r[0]}, Name: {r[1]}, Email: {r[3]}, Address: {r[6]}, {r[7]}, {r[8]}, {r[9]}"
        )

    # 6. UPDATE EMAIL OF ADDRESS WITH ID OF 9 TO `coding@arrowheadcu.org`
    updated_record = update_email(connection, "coding@arrowheadcu.org", 9)
    print(
        f"#6. Update Email:"
        f" ID: {updated_record[0]}, Name: {updated_record[1]}, Email: {updated_record[3]}, Address: {updated_record[6]}, {updated_record[7]}, {updated_record[8]}, {updated_record[9]}"
    )

    # 7. FILTER USERS TO ONLY RETRIEVE ALL USERS WITH LONGITUDE GREATER THAN -110.445
    lng_filtered_records = filter_by_longitude(connection, "-110.445")
    print(f"#7. Filtered by Longitude Greater than -110.445:")
    for r in lng_filtered_records:
        print(
            f"ID: {r[0]}, Name: {r[1]}, Address: {r[6]}, {r[7]}, {r[8]}, {r[9]}, Longitude: {r[11]}"
        )


if __name__ == "__main__":
    main()
