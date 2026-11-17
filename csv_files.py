"""csv_files.py - reading and saving the CSV files (the only code that opens them).

Every table (customers, drivers, vehicles, rides) is one CSV file.
In the program, a table is a LIST of rows, and each row is a DICTIONARY:

    {"customer_id": "C001", "name": "Amara Johnson", "phone": "555-0101", ...}
"""

import csv
import os
import sys


# The "data" folder sits next to this file.
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# The column names of each file (the header row).
COLUMNS = {
    "customers": ["customer_id", "name", "phone", "email"],
    "drivers": ["driver_id", "name", "phone", "license_number", "status"],
    "vehicles": ["vehicle_id", "registration", "model", "status"],
    "rides": [
        "ride_id", "customer_id", "pickup", "destination", "date", "time",
        "distance_km", "base_fare", "rate_per_km", "fare",
        "driver_id", "vehicle_id", "status",
    ],
}


def file_path(table):
    """Example: file_path("customers") -> .../data/customers.csv"""
    return os.path.join(DATA_FOLDER, table + ".csv")


def create_missing_files():
    """Create any CSV file that does not exist (or is empty), with its header row."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    for table in COLUMNS:
        path = file_path(table)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            with open(path, "w", newline="", encoding="utf-8") as file:
                csv.writer(file).writerow(COLUMNS[table])


def load_rows(table):
    """Read a CSV file and return its rows as a list of dictionaries."""
    create_missing_files()
    try:
        # "utf-8-sig" also reads files that were saved by Excel.
        with open(file_path(table), newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != COLUMNS[table]:
                print(f"Problem: {table}.csv must have these columns: {COLUMNS[table]}")
                sys.exit(1)
            rows = list(reader)
    except (OSError, csv.Error) as error:
        print(f"Problem reading {table}.csv: {error}")
        sys.exit(1)

    # A row with too few or too many values is a damaged row.
    # The csv module shows this with None: a missing value becomes None,
    # and extra values are stored under the column name None.
    for row in rows:
        damaged = False
        if None in row:
            damaged = True
        for value in row.values():
            if value is None:
                damaged = True
        if damaged:
            print(f"Problem: {table}.csv has a row with the wrong number of columns.")
            sys.exit(1)
    return rows


def save_rows(table, rows):
    """Write the whole list of rows back to the CSV file. Returns True if it worked."""
    try:
        with open(file_path(table), "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=COLUMNS[table])
            writer.writeheader()
            writer.writerows(rows)
        return True
    except OSError as error:
        print(f"Could not save {table}.csv: {error}")
        print("Is the file open in another program (for example Excel)? Close it and try again.")
        return False


def make_new_id(letter, rows, id_column):
    """Make the next ID, for example C031: the highest number in use plus 1."""
    highest = 0
    for row in rows:
        number = row[id_column][1:]  # "C012" -> "012"
        if number.isdigit() and int(number) > highest:
            highest = int(number)
    # ":03d" writes the number with 3 digits, adding zeros in front: 31 -> "031"
    return f"{letter}{highest + 1:03d}"


def find_row(rows, id_column, wanted_id):
    """Return the row with this ID (capitals do not matter), or None if there is none."""
    for row in rows:
        if row[id_column].upper() == wanted_id.strip().upper():
            return row
    return None


def search_rows(rows, search_text):
    """Return every row where ANY value contains the search text."""
    search_text = search_text.strip().lower()
    found = []
    for row in rows:
        for value in row.values():
            if search_text in value.lower():
                found.append(row)
                break  # stop looking at this row, we already have it
    return found


def is_used_in_rides(id_column, wanted_id):
    """True if any ride uses this customer / driver / vehicle ID."""
    for ride in load_rows("rides"):
        if ride[id_column].upper() == wanted_id.upper():
            return True
    return False
