"""Reusable Helper Functions"""

TITLE_PATTERN = ["Mr.", "Mrs.", "Ms.", "Dr.", "Miss", "Ms."]


# helper function to remove titles
def remove_titles(name):
    """Remove common titles from a name (TITLE_PATTERN) and then returns as is for sorting"""
    if not isinstance(name, str):
        raise ValueError("Input must be a string")

    for title in TITLE_PATTERN:
        if name.startswith(title):
            return name[len(title) :].strip()
    return name


# Format and print user records, reducing copy/ paste in print statements
def print_user_record(record, record_type="Fetched"):
    """Prints a formatted user record."""
    if not isinstance(record, (dict, list, tuple)):
        raise ValueError("Input must be a dictionary, list, or tuple")
    if not isinstance(record_type, str):
        raise ValueError("Input must be a string")
    print(
        f"{record_type} Record -> ID: {record[0]}, Name: {record[1]}, Username: {record[2]}, Email: {record[3]}, Phone: {record[4]}, Website: {record[5]},"
        f"Address: {record[6]}, {record[7]}, {record[8]}, {record[9]}, Latitude: {record[10]}, Longitude: {record[11]}, Longitude: {record[12]}, Company: {record[13]}, {record[14]}"
    )
