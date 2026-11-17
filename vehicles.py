"""vehicles.py - vehicles (taxis).

Actions: register, list, search, update, delete.
Each action is split in two functions: one ASKS the user (add_vehicle),
one SAVES to the file with no questions (save_new_vehicle).
"""

import csv_files
import display
import inputs

# A vehicle is either "Available" or "Unavailable".
STATUSES = ["Available", "Unavailable"]


VEHICLE_TABLE = "vehicles"
VEHICLE_COLUMNS = ["vehicle_id", "registration", "model", "status"]


# --- Functions that work with the file (no questions asked) -----------------

def registration_exists(registration):
    """True if a vehicle already has this registration (number plate)."""
    for vehicle in csv_files.load_rows(VEHICLE_TABLE):
        if vehicle["registration"].upper() == registration.strip().upper():
            return True
    return False


def save_new_vehicle(registration, model, status="Available"):
    """Add a vehicle to the file and return it. Returns None if it could not be saved."""
    registration = registration.strip().upper()
    if registration_exists(registration):
        return None
    rows = csv_files.load_rows(VEHICLE_TABLE)
    vehicle = {
        "vehicle_id": csv_files.make_new_id("V", rows, "vehicle_id"),
        "registration": registration,
        "model": model,
        "status": status,
    }
    rows.append(vehicle)
    if csv_files.save_rows(VEHICLE_TABLE, rows):
        return vehicle
    return None


# --- Functions that talk to the user ----------------------------------------

def add_vehicle():
    print("\n--- Register vehicle ---")
    registration = inputs.ask_text("Registration (number plate)")
    if registration_exists(registration):
        print("  A vehicle with this registration already exists.")
        return
    model = inputs.ask_text("Make and model")
    status = inputs.ask_choice("Status", STATUSES)
    vehicle = save_new_vehicle(registration, model, status)
    if vehicle is not None:
        print(f"Saved. The new vehicle ID is {vehicle['vehicle_id']}.")


def show_vehicles():
    display.show_table(csv_files.load_rows(VEHICLE_TABLE), VEHICLE_COLUMNS)


def search_vehicles():
    print("\n--- Search vehicles ---")
    text = inputs.ask_text("Type an ID, registration, model or status to search for")
    found = csv_files.search_rows(csv_files.load_rows(VEHICLE_TABLE), text)
    if len(found) == 0:
        print(f"  No vehicle found for '{text}'.")
    else:
        display.show_table(found, VEHICLE_COLUMNS)


def update_vehicle():
    print("\n--- Update vehicle ---")
    vehicle_id = inputs.ask_text("Vehicle ID")
    rows = csv_files.load_rows(VEHICLE_TABLE)
    vehicle = csv_files.find_row(rows, "vehicle_id", vehicle_id)
    if vehicle is None:
        print(f"  Vehicle {vehicle_id} was not found.")
        return

    display.show_record(vehicle)
    choice = display.show_menu("What do you want to change?", [
        "1. Registration", "2. Model", "3. Status (availability)", "0. Cancel",
    ])
    if choice == "1":
        new_registration = inputs.ask_text("New registration").upper()
        if registration_exists(new_registration):
            print("  A vehicle with this registration already exists.")
            return
        vehicle["registration"] = new_registration
    elif choice == "2":
        vehicle["model"] = inputs.ask_text("New make and model")
    elif choice == "3":
        vehicle["status"] = inputs.ask_choice("New status", STATUSES)
    else:
        print("Nothing was changed.")
        return

    if csv_files.save_rows(VEHICLE_TABLE, rows):
        print("Vehicle updated.")


def delete_vehicle():
    print("\n--- Delete vehicle ---")
    vehicle_id = inputs.ask_text("Vehicle ID")
    rows = csv_files.load_rows(VEHICLE_TABLE)
    vehicle = csv_files.find_row(rows, "vehicle_id", vehicle_id)
    if vehicle is None:
        print(f"  Vehicle {vehicle_id} was not found.")
        return
    if csv_files.is_used_in_rides("vehicle_id", vehicle["vehicle_id"]):
        print("  This vehicle is on a ride, so the record cannot be deleted.")
        return

    display.show_record(vehicle)
    if inputs.ask_yes_no("Delete this vehicle?"):
        rows.remove(vehicle)
        if csv_files.save_rows(VEHICLE_TABLE, rows):
            print("Vehicle deleted.")
    else:
        print("Nothing was deleted.")


def vehicle_menu():
    while True:
        choice = display.show_menu("Vehicle Management", [
            "1. Register vehicle",
            "2. List vehicles",
            "3. Search vehicles",
            "4. Update vehicle (including availability)",
            "5. Delete vehicle",
            "0. Back",
        ])
        if choice == "1":
            add_vehicle()
        elif choice == "2":
            show_vehicles()
        elif choice == "3":
            search_vehicles()
        elif choice == "4":
            update_vehicle()
        elif choice == "5":
            delete_vehicle()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")
