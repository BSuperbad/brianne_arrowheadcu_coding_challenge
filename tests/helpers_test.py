import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from src.utilities.helpers import (
    remove_titles,
    print_user_record,
)  # Assuming the helper functions are in 'helpers.py'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


class TestHelpers(unittest.TestCase):

    def test_remove_titles(self):
        """Test the remove_titles function."""
        # Test with various names with titles
        self.assertEqual(remove_titles("Mr. John Doe"), "John Doe")
        self.assertEqual(remove_titles("Dr. Jane Smith"), "Jane Smith")
        self.assertEqual(remove_titles("Ms. Emily Davis"), "Emily Davis")
        self.assertEqual(remove_titles("Miss Sarah Lee"), "Sarah Lee")
        self.assertEqual(remove_titles("Mr. John Doe Jr."), "John Doe Jr.")
        self.assertEqual(remove_titles("John Doe"), "John Doe")
        with self.assertRaises(ValueError):
            remove_titles(12345)

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_user_record(self, mock_stdout):
        """Test the print_user_record function."""
        # Prepare a sample record to pass to the function
        record = [
            1,
            "John Doe",
            "johndoe",
            "johndoe@example.com",
            "123-456-7890",
            "www.johndoe.com",
            "123 Main St",
            "Springfield",
            "IL",
            "12345",
        ]

        print_user_record(record, "Fetched")

        expected_output = (
            "Fetched Record -> ID: 1, Name: John Doe, Email: johndoe@example.com, "
            "Address: 123 Main St, Springfield, IL, 12345\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
