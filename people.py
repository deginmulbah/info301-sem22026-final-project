"""people.py - customers and drivers.

Both have the same actions: register, list, search, update, delete.
Each action is split in two functions: one ASKS the user (add_customer),
one SAVES to the file with no questions (save_new_customer).
"""

import csv_files
import display
import inputs

# A driver is either "Available" or "Unavailable".
STATUSES = ["Available", "Unavailable"]


# ===========================================================================
# CUSTOMERS
# ===========================================================================

CUSTOMER_TABLE = "customers"
CUSTOMER_COLUMNS = ["customer_id", "name", "phone", "email"]


# --- Functions that work with the file (no questions asked) -----------------

def save_new_customer(name, phone, email):
    """Give the customer a new ID, add to the file, and return the new customer."""
    rows = csv_files.load_rows(CUSTOMER_TABLE)
    customer = {
        "customer_id": csv_files.make_new_id("C", rows, "customer_id"),
        "name": name,
        "phone": phone,
        "email": email,
    }
    rows.append(customer)
    if csv_files.save_rows(CUSTOMER_TABLE, rows):
        return customer
    return None


def customer_exists(customer_id):
    """True if a customer with this ID is in the file."""
    rows = csv_files.load_rows(CUSTOMER_TABLE)
    return csv_files.find_row(rows, "customer_id", customer_id) is not None


# --- Functions that talk to the user ----------------------------------------

def add_customer():
    print("\n--- Register customer ---")
    name = inputs.ask_text("Full name")
    phone = inputs.ask_phone()
    email = inputs.ask_email()
    customer = save_new_customer(name, phone, email)
    if customer is not None:
        print(f"Saved. The new customer ID is {customer['customer_id']}.")


def show_customers():
    display.show_table(csv_files.load_rows(CUSTOMER_TABLE), CUSTOMER_COLUMNS)


def search_customers():
    print("\n--- Search customers ---")
    text = inputs.ask_text("Type an ID, name, phone or email to search for")
    found = csv_files.search_rows(csv_files.load_rows(CUSTOMER_TABLE), text)
    if len(found) == 0:
        print(f"  No customer found for '{text}'.")
    else:
        display.show_table(found, CUSTOMER_COLUMNS)


def update_customer():
    print("\n--- Update customer ---")
    customer_id = inputs.ask_text("Customer ID")
    rows = csv_files.load_rows(CUSTOMER_TABLE)
    customer = csv_files.find_row(rows, "customer_id", customer_id)
    if customer is None:
        print(f"  Customer {customer_id} was not found.")
        return

    display.show_record(customer)
    choice = display.show_menu("What do you want to change?", [
        "1. Name", "2. Phone", "3. Email", "0. Cancel",
    ])
    if choice == "1":
        customer["name"] = inputs.ask_text("New name")
    elif choice == "2":
        customer["phone"] = inputs.ask_phone()
    elif choice == "3":
        customer["email"] = inputs.ask_email()
    else:
        print("Nothing was changed.")
        return

    if csv_files.save_rows(CUSTOMER_TABLE, rows):
        print("Customer updated.")


def delete_customer():
    print("\n--- Delete customer ---")
    customer_id = inputs.ask_text("Customer ID")
    rows = csv_files.load_rows(CUSTOMER_TABLE)
    customer = csv_files.find_row(rows, "customer_id", customer_id)
    if customer is None:
        print(f"  Customer {customer_id} was not found.")
        return
    # Safety rule: do not delete a customer who has rides.
    if csv_files.is_used_in_rides("customer_id", customer["customer_id"]):
        print("  This customer has rides, so the record cannot be deleted.")
        return

    display.show_record(customer)
    if inputs.ask_yes_no("Delete this customer?"):
        rows.remove(customer)
        if csv_files.save_rows(CUSTOMER_TABLE, rows):
            print("Customer deleted.")
    else:
        print("Nothing was deleted.")


def customer_menu():
    while True:
        choice = display.show_menu("Customer Management", [
            "1. Register customer",
            "2. List customers",
            "3. Search customers",
            "4. Update customer",
            "5. Delete customer",
            "0. Back",
        ])
        if choice == "1":
            add_customer()
        elif choice == "2":
            show_customers()
        elif choice == "3":
            search_customers()
        elif choice == "4":
            update_customer()
        elif choice == "5":
            delete_customer()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")


# ===========================================================================
# DRIVERS
# ===========================================================================

DRIVER_TABLE = "drivers"
DRIVER_COLUMNS = ["driver_id", "name", "phone", "license_number", "status"]


# --- Functions that work with the file (no questions asked) -----------------

def save_new_driver(name, phone, license_number, status="Available"):
    """Give the driver a new ID, add to the file, and return the new driver."""
    rows = csv_files.load_rows(DRIVER_TABLE)
    driver = {
        "driver_id": csv_files.make_new_id("D", rows, "driver_id"),
        "name": name,
        "phone": phone,
        "license_number": license_number.upper(),
        "status": status,
    }
    rows.append(driver)
    if csv_files.save_rows(DRIVER_TABLE, rows):
        return driver
    return None


# --- Functions that talk to the user ----------------------------------------

def add_driver():
    print("\n--- Register driver ---")
    name = inputs.ask_text("Full name")
    phone = inputs.ask_phone()
    license_number = inputs.ask_text("Licence number")
    status = inputs.ask_choice("Status", STATUSES)
    driver = save_new_driver(name, phone, license_number, status)
    if driver is not None:
        print(f"Saved. The new driver ID is {driver['driver_id']}.")


def show_drivers():
    display.show_table(csv_files.load_rows(DRIVER_TABLE), DRIVER_COLUMNS)


def search_drivers():
    print("\n--- Search drivers ---")
    text = inputs.ask_text("Type an ID, name, phone, licence or status to search for")
    found = csv_files.search_rows(csv_files.load_rows(DRIVER_TABLE), text)
    if len(found) == 0:
        print(f"  No driver found for '{text}'.")
    else:
        display.show_table(found, DRIVER_COLUMNS)


def update_driver():
    print("\n--- Update driver ---")
    driver_id = inputs.ask_text("Driver ID")
    rows = csv_files.load_rows(DRIVER_TABLE)
    driver = csv_files.find_row(rows, "driver_id", driver_id)
    if driver is None:
        print(f"  Driver {driver_id} was not found.")
        return

    display.show_record(driver)
    choice = display.show_menu("What do you want to change?", [
        "1. Name", "2. Phone", "3. Licence number", "4. Status (availability)", "0. Cancel",
    ])
    if choice == "1":
        driver["name"] = inputs.ask_text("New name")
    elif choice == "2":
        driver["phone"] = inputs.ask_phone()
    elif choice == "3":
        driver["license_number"] = inputs.ask_text("New licence number").upper()
    elif choice == "4":
        driver["status"] = inputs.ask_choice("New status", STATUSES)
    else:
        print("Nothing was changed.")
        return

    if csv_files.save_rows(DRIVER_TABLE, rows):
        print("Driver updated.")


def delete_driver():
    print("\n--- Delete driver ---")
    driver_id = inputs.ask_text("Driver ID")
    rows = csv_files.load_rows(DRIVER_TABLE)
    driver = csv_files.find_row(rows, "driver_id", driver_id)
    if driver is None:
        print(f"  Driver {driver_id} was not found.")
        return
    if csv_files.is_used_in_rides("driver_id", driver["driver_id"]):
        print("  This driver is on a ride, so the record cannot be deleted.")
        return

    display.show_record(driver)
    if inputs.ask_yes_no("Delete this driver?"):
        rows.remove(driver)
        if csv_files.save_rows(DRIVER_TABLE, rows):
            print("Driver deleted.")
    else:
        print("Nothing was deleted.")


def driver_menu():
    while True:
        choice = display.show_menu("Driver Management", [
            "1. Register driver",
            "2. List drivers",
            "3. Search drivers",
            "4. Update driver (including availability)",
            "5. Delete driver",
            "0. Back",
        ])
        if choice == "1":
            add_driver()
        elif choice == "2":
            show_drivers()
        elif choice == "3":
            search_drivers()
        elif choice == "4":
            update_driver()
        elif choice == "5":
            delete_driver()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")
