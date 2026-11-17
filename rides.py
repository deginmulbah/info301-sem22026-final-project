"""rides.py - fare, booking rides, ride status and ride reports.

Part 1: the fare formula and the sample fare calculator
Part 2: booking rides, changing ride status, and reports

THE FARE FORMULA (used everywhere in the program):

    fare = base fare + (rate per km x distance in km)

Example: base fare 5.00, rate 2.50 per km, distance 12 km
         fare = 5.00 + (2.50 x 12) = 35.00

Ride status life cycle:

    Requested --> Accepted --> Completed
        |             |
        +--> Cancelled <--+

* Requested : the customer booked the ride, no driver yet.
* Accepted  : a driver and a vehicle are assigned. Both must be "Available",
              and both become "Unavailable" while the ride is open.
* Completed or Cancelled : final. The driver and vehicle become "Available" again.
"""

import csv_files
import display
import inputs
import people


# ===========================================================================
# PART 1 - FARE
# ===========================================================================

def calculate_fare(distance, base_fare, rate_per_km):
    """Return the fare, rounded to 2 decimals. This is the ONLY place the formula is written."""
    return round(base_fare + rate_per_km * distance, 2)


def fare_menu():
    while True:
        choice = display.show_menu("Calculate Fare", [
            "1. Sample fare calculator (nothing is saved)",
            "0. Back",
        ])
        if choice == "1":
            print("\nFormula: fare = base fare + (rate per km x distance)")
            distance = inputs.ask_positive_number("Distance in km")
            base_fare = inputs.ask_zero_or_more("Base fare")
            rate_per_km = inputs.ask_zero_or_more("Rate per km")
            fare = calculate_fare(distance, base_fare, rate_per_km)
            print(f"  {base_fare:.2f} + ({rate_per_km:.2f} x {distance:.2f}) = {fare:.2f}")
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")


# ===========================================================================
# PART 2 - RIDES
# ===========================================================================
TABLE = "rides"

# For each status: which statuses it may change to.
ALLOWED_CHANGES = {
    "Requested": ["Accepted", "Cancelled"],
    "Accepted": ["Completed", "Cancelled"],
    "Completed": [],
    "Cancelled": [],
}

# The columns shown in lists of rides (view one ride shows everything).
LIST_COLUMNS = ["ride_id", "date", "time", "pickup", "destination", "fare", "status"]


# --- Functions that work with the file (no questions asked) -----------------

def save_new_ride(customer_id, pickup, destination, date, time, distance, base_fare, rate_per_km):
    """Calculate the fare, add the ride (status Requested) to the file, and return it."""
    rows = csv_files.load_rows(TABLE)
    fare = calculate_fare(distance, base_fare, rate_per_km)
    ride = {
        "ride_id": csv_files.make_new_id("R", rows, "ride_id"),
        "customer_id": customer_id.upper(),
        "pickup": pickup,
        "destination": destination,
        "date": date,
        "time": time,
        "distance_km": f"{distance:.2f}",
        "base_fare": f"{base_fare:.2f}",
        "rate_per_km": f"{rate_per_km:.2f}",
        "fare": f"{fare:.2f}",
        "driver_id": "",
        "vehicle_id": "",
        "status": "Requested",
    }
    rows.append(ride)
    if csv_files.save_rows(TABLE, rows):
        return ride
    return None


def set_status(table, id_column, the_id, new_status):
    """Change the status of one driver or vehicle (used to make them Available/Unavailable)."""
    rows = csv_files.load_rows(table)
    row = csv_files.find_row(rows, id_column, the_id)
    if row is not None:
        row["status"] = new_status
        csv_files.save_rows(table, rows)


def change_ride_status(ride_id, new_status, driver_id="", vehicle_id=""):
    """Change a ride's status if the rules allow it.

    Returns two things: True/False (did it work?) and a message to show the user.
    driver_id and vehicle_id are only needed when the new status is "Accepted".
    """
    all_rides = csv_files.load_rows(TABLE)
    ride = csv_files.find_row(all_rides, "ride_id", ride_id)
    if ride is None:
        return False, f"Ride {ride_id} was not found."

    old_status = ride["status"]
    if new_status not in ALLOWED_CHANGES[old_status]:
        return False, f"A {old_status} ride cannot change to {new_status}."

    if new_status == "Accepted":
        driver = csv_files.find_row(csv_files.load_rows("drivers"), "driver_id", driver_id)
        vehicle = csv_files.find_row(csv_files.load_rows("vehicles"), "vehicle_id", vehicle_id)
        if driver is None:
            return False, f"Driver {driver_id} was not found."
        if vehicle is None:
            return False, f"Vehicle {vehicle_id} was not found."
        if driver["status"] != "Available":
            return False, f"Driver {driver['driver_id']} is not available."
        if vehicle["status"] != "Available":
            return False, f"Vehicle {vehicle['vehicle_id']} is not available."
        ride["driver_id"] = driver["driver_id"]
        ride["vehicle_id"] = vehicle["vehicle_id"]
        set_status("drivers", "driver_id", driver["driver_id"], "Unavailable")
        set_status("vehicles", "vehicle_id", vehicle["vehicle_id"], "Unavailable")

    if old_status == "Accepted":
        # The ride is finished (Completed or Cancelled): free the driver and vehicle.
        set_status("drivers", "driver_id", ride["driver_id"], "Available")
        set_status("vehicles", "vehicle_id", ride["vehicle_id"], "Available")

    ride["status"] = new_status
    if csv_files.save_rows(TABLE, all_rides):
        return True, f"Ride {ride['ride_id']} is now {new_status}."
    return False, "The change could not be saved."


# --- Functions that talk to the user ----------------------------------------

def book_ride():
    print("\n--- Book ride ---")
    customer_id = inputs.ask_text("Customer ID")
    # Rule: the customer must already exist.
    if not people.customer_exists(customer_id):
        print(f"  Customer {customer_id} was not found. Register the customer first.")
        return

    pickup = inputs.ask_text("Pickup location")
    destination = inputs.ask_text("Destination")
    while destination.lower() == pickup.lower():
        print("  Pickup and destination must be different places.")
        destination = inputs.ask_text("Destination")
    date = inputs.ask_date()
    time = inputs.ask_time()
    distance = inputs.ask_positive_number("Distance in km")
    base_fare = inputs.ask_zero_or_more("Base fare (for example 5)")
    rate_per_km = inputs.ask_zero_or_more("Rate per km (for example 2.5)")

    ride = save_new_ride(customer_id, pickup, destination, date, time,
                         distance, base_fare, rate_per_km)
    if ride is not None:
        print(f"Ride booked. Ride ID: {ride['ride_id']}  Status: {ride['status']}")
        print(f"  Fare: {base_fare:.2f} + ({rate_per_km:.2f} x {distance:.2f}) = {ride['fare']}")


def show_rides():
    display.show_table(csv_files.load_rows(TABLE), LIST_COLUMNS)


def view_one_ride():
    print("\n--- View one ride ---")
    ride_id = inputs.ask_text("Ride ID")
    ride = csv_files.find_row(csv_files.load_rows(TABLE), "ride_id", ride_id)
    if ride is None:
        print(f"  Ride {ride_id} was not found.")
    else:
        display.show_record(ride)


def update_ride_status():
    print("\n--- Update ride status ---")
    ride_id = inputs.ask_text("Ride ID")
    ride = csv_files.find_row(csv_files.load_rows(TABLE), "ride_id", ride_id)
    if ride is None:
        print(f"  Ride {ride_id} was not found.")
        return

    print(f"Ride {ride['ride_id']} is {ride['status']}.")
    allowed = ALLOWED_CHANGES[ride["status"]]
    if len(allowed) == 0:
        print("  This ride is finished and its status cannot be changed.")
        return

    new_status = inputs.ask_choice("New status", allowed)
    driver_id = ""
    vehicle_id = ""
    if new_status == "Accepted":
        print("Assign a driver and a vehicle (both must be Available).")
        driver_id = inputs.ask_text("Driver ID")
        vehicle_id = inputs.ask_text("Vehicle ID")

    worked, message = change_ride_status(ride_id, new_status, driver_id, vehicle_id)
    if worked:
        print("  " + message)
    else:
        print("  Not changed: " + message)


def ride_menu():
    while True:
        choice = display.show_menu("Update / View Ride", [
            "1. List all rides",
            "2. View one ride",
            "3. Update ride status",
            "0. Back",
        ])
        if choice == "1":
            show_rides()
        elif choice == "2":
            view_one_ride()
        elif choice == "3":
            update_ride_status()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")


# --- Reports: view rides by date, customer or driver ------------------------

def rides_on_date(date):
    """Return the rides booked for this date."""
    found = []
    for ride in csv_files.load_rows(TABLE):
        if ride["date"] == date:
            found.append(ride)
    return found


def rides_for(id_column, the_id):
    """Return the rides of one customer (id_column="customer_id") or driver ("driver_id")."""
    found = []
    for ride in csv_files.load_rows(TABLE):
        if ride[id_column].upper() == the_id.strip().upper():
            found.append(ride)
    return found


def report_by_date():
    print("\n--- Rides by date ---")
    date = inputs.ask_date()
    print(f"Rides on {date}:")
    display.show_table(rides_on_date(date), LIST_COLUMNS)


def report_by_customer():
    print("\n--- Rides by customer ---")
    customer_id = inputs.ask_text("Customer ID")
    if not people.customer_exists(customer_id):
        print(f"  Customer {customer_id} was not found.")
        return
    print(f"Rides for customer {customer_id.upper()}:")
    display.show_table(rides_for("customer_id", customer_id), LIST_COLUMNS)


def report_by_driver():
    print("\n--- Rides by driver ---")
    driver_id = inputs.ask_text("Driver ID")
    if csv_files.find_row(csv_files.load_rows("drivers"), "driver_id", driver_id) is None:
        print(f"  Driver {driver_id} was not found.")
        return
    print(f"Rides for driver {driver_id.upper()}:")
    display.show_table(rides_for("driver_id", driver_id), LIST_COLUMNS)


def report_menu():
    while True:
        choice = display.show_menu("Basic Reports", [
            "1. Rides by date",
            "2. Rides by customer",
            "3. Rides by driver",
            "0. Back",
        ])
        if choice == "1":
            report_by_date()
        elif choice == "2":
            report_by_customer()
        elif choice == "3":
            report_by_driver()
        elif choice == "0":
            return
        else:
            print("Invalid choice. Please type one of the numbers shown.")
