"""Reusable Helper Functions"""

TITLE_PATTERN = ["Mr.", "Mrs.", "Ms.", "Dr.", "Miss", "Ms."]


# helper function to remove titles
def remove_titles(name):
    """Remove common titles from a name (TITLE_PATTERN) and then returns as is for sorting"""
    for title in TITLE_PATTERN:
        if name.startswith(title):
            return name[len(title) :].strip()
    return name


# Format and print user records, reducing copy/ paste in print statements
def print_user_record(record, record_type="Fetched"):
    """Prints a formatted user record."""
    print(
        f"{record_type} Record -> ID: {record[0]}, Name: {record[1]}, Email: {record[3]}, "
        f"Address: {record[6]}, {record[7]}, {record[8]}, {record[9]}"
    )
