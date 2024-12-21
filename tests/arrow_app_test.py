import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch, MagicMock
import sqlite3
from arrow_app import fetch_users, sort_records, update_email, filter_by_longitude
from src.db import user_database


class TestArrowApp(unittest.TestCase):

    def setUp(self):
        """Setup a fresh database for each test"""
        self.connection = sqlite3.connect(":memory:")
        user_database.create_table(self.connection)

    def tearDown(self):
        """Close the connection after each test"""
        self.connection.close()

    @patch("arrow_app.requests.get")
    def test_fetch_users(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"id": 1, "name": "Test User"}]
        users = fetch_users("https://example.com/users")
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "Test User")

    def test_sort_records(self):
        user_database.insert_user(
            self.connection,
            {
                "id": 1,
                "name": "Mr. John Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "phone": "123-456-7890",
                "website": "johndoe.com",
                "address": {
                    "street": "Main St",
                    "suite": "Apt 1",
                    "city": "Springfield",
                    "zipcode": "12345",
                    "geo": {"lat": "0.0", "lng": "-110.0"},
                },
                "company": {
                    "name": "Doe Inc",
                    "catchPhrase": "We do it!",
                    "bs": "business stuff",
                },
            },
        )
        sorted_records = sort_records(self.connection)
        self.assertEqual(len(sorted_records), 1)
        self.assertEqual(sorted_records[0][1], "Mr. John Doe")

    def test_update_email(self):
        user_database.insert_user(
            self.connection,
            {
                "id": 1,
                "name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "phone": "123-456-7890",
                "website": "johndoe.com",
                "address": {
                    "street": "Main St",
                    "suite": "Apt 1",
                    "city": "Springfield",
                    "zipcode": "12345",
                    "geo": {"lat": "0.0", "lng": "-110.0"},
                },
                "company": {
                    "name": "Doe Inc",
                    "catchPhrase": "We do it!",
                    "bs": "business stuff",
                },
            },
        )
        updated_user = update_email(self.connection, "new_email@example.com", 1)
        self.assertEqual(updated_user[3], "new_email@example.com")

    def test_filter_by_longitude(self):
        user_database.insert_user(
            self.connection,
            {
                "id": 1,
                "name": "John Doe",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "phone": "123-456-7890",
                "website": "johndoe.com",
                "address": {
                    "street": "Main St",
                    "suite": "Apt 1",
                    "city": "Springfield",
                    "zipcode": "12345",
                    "geo": {"lat": "0.0", "lng": "-109.0"},
                },
                "company": {
                    "name": "Doe Inc",
                    "catchPhrase": "We do it!",
                    "bs": "business stuff",
                },
            },
        )
        filtered_records = filter_by_longitude(self.connection, -110.0)
        self.assertEqual(len(filtered_records), 1)
        self.assertEqual(filtered_records[0][1], "John Doe")

    # Error handling tests

    @patch("src.db.user_database.sqlite3.connect")
    def test_create_connection_error(self, mock_connect):
        # Simulating a connection error
        mock_connect.side_effect = sqlite3.Error("Connection failed")
        with self.assertRaises(Exception) as context:
            user_database.create_connection("invalid_db.db")
        self.assertEqual(
            str(context.exception),
            "Error connecting to database invalid_db.db: Connection failed",
        )

    @patch("src.db.user_database.sqlite3.connect")
    def test_create_table_error(self, mock_connect):
        # Simulating a table creation error
        connection = MagicMock()
        connection.execute.side_effect = sqlite3.Error("Table creation failed")
        with self.assertRaises(Exception) as context:
            user_database.create_table(connection)
        self.assertEqual(
            str(context.exception), "Error creating table: Table creation failed"
        )

    def test_insert_user_with_duplicate_id(self):
        """Test inserting user with duplicate id"""
        first_user = {
            "id": 11,
            "name": "John Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone": "123-456-7890",
            "website": "johndoe.com",
            "address": {
                "street": "Main St",
                "suite": "Apt 1",
                "city": "Springfield",
                "zipcode": "12345",
                "geo": {"lat": "0.0", "lng": "-110.0"},
            },
            "company": {
                "name": "Doe Inc",
                "catchPhrase": "We do it!",
                "bs": "business stuff",
            },
        }
        user_database.insert_user(self.connection, first_user)

        second_user = {
            "id": 11,  # Same ID as the first user
            "name": "Jane Doe",
            "username": "janedoe",
            "email": "janedoe@example.com",
            "phone": "987-654-3210",
            "website": "janedoe.com",
            "address": {
                "street": "Second St",
                "suite": "Apt 2",
                "city": "Shelbyville",
                "zipcode": "67890",
                "geo": {"lat": "1.0", "lng": "-120.0"},
            },
            "company": {
                "name": "Doe Inc",
                "catchPhrase": "We do it better!",
                "bs": "business stuff",
            },
        }

        with self.assertRaises(sqlite3.IntegrityError) as context:
            user_database.insert_user(self.connection, second_user)

        self.assertTrue("UNIQUE constraint failed" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
