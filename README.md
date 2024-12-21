# Brianne Wilhelmi - Arrowhead Credit Union Coding Challenge

## December 2024

### Tasks Overview

1. **Fetch User Data:**  
   I retrieved user data from the following
   API: [https://jsonplaceholder.typicode.com/users](https://jsonplaceholder.typicode.com/users). Data includes user
   details like `name`, `email`, `address`, `phone`, and `company` information.

2. **Display Records:**  
   The user data gets printed to the terminal in a clean, readable format.

3. **Create SQL Table:**  
   Created SQL table to store user data with appropriate fields for all relevant attributes, such as `id`, `name`,
   `email`, `address_street`, `address_suite`, `address_city`, `address_zipcode`, `phone`, and `company`.

4. **Insert Records:**  
   Implemented a function to insert the fetched user data into the SQL table. This function pulls all records from the
   API call, including the nested records like the `lat` and `lng` values from within `address`.

5. **Sort Records**  
   Wrote a SQL query to sort the user records alphabetically by the name field. The query ignores any titles (like "Mr."
   or "Mrs.") when sorting to ensure a clean alphabetical order. After sorting, the titles are re-added to the names
   when displaying the results to the end user in the terminal, preserving the original format of the data.

6. **Update Email:**  
   Wrote a function to update the email of users based on their ID dynamically. In `main`, I updated the email address
   of the user with `id = 9` to `coding@arrowheadcu.org`.

7. **Filter by Longitude:**  
   A SQL query was written to filter users based on the `longitude` field, retrieving all users with a longitude greater
   than `-110.455`. Refactored to make it dynamic.

### Error Handling

#### Functions

1. **Fetch User Data:**  
   `fetch_users` handles potential errors during the API request, such as connection issues, timeouts, or invalid
   responses. It uses `try-except` blocks to catch `requests.exceptions.RequestException`, logs the error message, and
   returns an empty list in case of failure.

2. **Sort Records:**  
   Error handling in `sort_records` manages database query issues like connection problems or invalid SQL syntax. A
   `try-except` block catches `sqlite3.DatabaseError` exceptions, prints an error message, and returns an empty list.
    - The `remove_titles` function checks if the name is a string. If not, it raises a `ValueError` with the message "
      Input must be a string."
    - If the name is a string, it checks for common titles (defined in `TITLE_PATTERN`) and removes any matching titles.
    - If no title is found, the original name is returned.

3. **Update Email:**  
   `update_email` includes error handling for database-related issues, such as connection errors or failed update
   operations. A `try-except` block catches `sqlite3.DatabaseError` exceptions. If an error occurs, the error message is
   printed, and the function returns `None`, indicating failure.

4. **Filtering by Longitude:**  
   A try-except block catches sqlite3.DatabaseError exceptions. If an error is encountered, the error message is
   printed, and an empty list is returned to allow the program to continue.
    - Again, `remove_titles` function checks if the name is a string. If not, it raises a `ValueError` with the
      message "
      Input must be a string."

#### Database Side:

1. **Create Connection:**  
   A `try-except` block catches `sqlite3.Error` exceptions. If an error occurs, an `Exception` is raised with a message
   indicating the issue, including the database name and error details.

2. **Create Table:**  
   A `try-except` block ensures that if an error occurs, an `Exception` is raised with a message detailing the error
   that occurred while creating the table.

3. **Insert User:**  
   Specifically catches `sqlite3.IntegrityError` to handle cases like inserting duplicate data (e.g., primary key
   violation) and raises the exception if this occurs. For other `sqlite3.Error` exceptions, an `Exception` is raised
   with an error message detailing the insertion failure.

### Unit Testing

1. **Helper Functions**
    - Includes tests for utility functions like removing titles from names and formatting
      user records. The tests check for correct outputs and handle errors for invalid inputs.

2. **Database Operations**
    - Tests the creation of a new database and table, ensuring proper
      initialization. Error handling is checked for failed database connections or issues with creating tables.
    - Verifies that records can be inserted into the database correctly. Tests include inserting
      valid records and handling errors when attempting to insert records with duplicate keys (like primary key of id).

3. **Data Fetching and Updating**
    - Simulates fetching data from API and ensures the data is
      correctly parsed and returned.
    - Tests updating records in the database, such as modifying user information (e.g., email), and
      checks that the updates are correctly reflected.

4. **Filtering and Sorting Data**
    - Verifies that records can be sorted properly (e.g., by user names) and checks if the sorted
      data is returned as expected.
    - Tests filtering records based on specific criteria (e.g., longitude values), ensuring that the
      filter logic works as expected.
