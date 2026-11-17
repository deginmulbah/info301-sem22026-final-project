"""test_app.py - automatic tests. Run with:   python test_app.py

Each test is a small function whose name starts with test_.
'assert' means: "this must be True, otherwise the test FAILS".

The tests that use files work in a TEMPORARY folder, so your real data/ folder
is never changed. (Only the last tests read the real data folder, and only read.)
"""

import os
import tempfile

import checks
import csv_files
import people
import rides
import vehicles

REAL_DATA_FOLDER = csv_files.DATA_FOLDER


def use_empty_temporary_folder():
    """Point the program at a brand new empty folder (with empty CSV files)."""
    csv_files.DATA_FOLDER = tempfile.mkdtemp()
    csv_files.create_missing_files()


def use_real_data_folder():
    csv_files.DATA_FOLDER = REAL_DATA_FOLDER


# ---------------------------------------------------------------- fare tests

def test_fare_normal():
    assert rides.calculate_fare(12, 5, 2.5) == 35.0          # 5 + 2.5 x 12
    assert rides.calculate_fare(10, 5, 2.5) == 30.0


def test_fare_with_zero_base_fare():
    assert rides.calculate_fare(4, 0, 2) == 8.0


def test_fare_is_rounded_to_2_decimals():
    assert rides.calculate_fare(3, 1.10, 0.33) == 2.09        # 1.10 + 0.99


def test_zero_or_negative_distance_is_not_accepted():
    assert checks.is_positive_number("0") is False
    assert checks.is_positive_number("-5") is False
    assert checks.is_positive_number("abc") is False
    assert checks.is_positive_number("") is False
    assert checks.is_positive_number("12.5") is True


def test_negative_fare_values_are_not_accepted():
    assert checks.is_zero_or_more("-1") is False
    assert checks.is_zero_or_more("abc") is False
    assert checks.is_zero_or_more("0") is True
    assert checks.is_zero_or_more("2.5") is True


# ---------------------------------------------------------- validation tests

def test_valid_and_invalid_dates():
    assert checks.is_valid_date("2026-11-21") is True
    assert checks.is_valid_date("21-11-2026") is False
    assert checks.is_valid_date("2026-13-01") is False         # no month 13
    assert checks.is_valid_date("2026-02-30") is False         # no 30 February
    assert checks.is_valid_date("2026-1-5") is False           # must be YYYY-MM-DD
    assert checks.is_valid_date("tomorrow") is False
    assert checks.is_valid_date("") is False


def test_valid_and_invalid_times():
    assert checks.is_valid_time("08:30") is True
    assert checks.is_valid_time("23:59") is True
    assert checks.is_valid_time("25:00") is False
    assert checks.is_valid_time("09:60") is False
    assert checks.is_valid_time("9:30") is False
    assert checks.is_valid_time("noon") is False


def test_valid_and_invalid_phones_and_emails():
    assert checks.is_valid_phone("555-0123") is True
    assert checks.is_valid_phone("abc") is False
    assert checks.is_valid_phone("123") is False
    assert checks.is_valid_email("ann@example.com") is True
    assert checks.is_valid_email("not-an-email") is False


# ----------------------------------------------------------- CSV file tests

def test_missing_files_are_created_with_headers():
    use_empty_temporary_folder()
    for table in csv_files.COLUMNS:
        with open(csv_files.file_path(table)) as file:
            first_line = file.readline().strip()
        assert first_line == ",".join(csv_files.COLUMNS[table])
        assert csv_files.load_rows(table) == []


def test_saved_rows_can_be_read_back():
    use_empty_temporary_folder()
    people.save_new_customer("Ann Test", "555-0100", "ann@example.com")
    rows = csv_files.load_rows("customers")        # reads the file again
    assert len(rows) == 1
    assert rows[0]["name"] == "Ann Test"


def test_commas_in_names_are_kept():
    use_empty_temporary_folder()
    people.save_new_customer("Smith, Ann", "555-0100", "ann@example.com")
    assert csv_files.load_rows("customers")[0]["name"] == "Smith, Ann"


# ------------------------------------------------------------ customer tests

def test_add_valid_customer_appears_in_list():
    use_empty_temporary_folder()
    customer = people.save_new_customer("Ann Test", "555-0100", "ann@example.com")
    assert customer["customer_id"] == "C001"
    names = [row["name"] for row in csv_files.load_rows("customers")]
    assert "Ann Test" in names


def test_customer_ids_are_unique():
    use_empty_temporary_folder()
    first = people.save_new_customer("Ann", "555-0100", "a@example.com")
    second = people.save_new_customer("Ben", "555-0101", "b@example.com")
    assert first["customer_id"] == "C001"
    assert second["customer_id"] == "C002"


def test_search_existing_and_missing_customer():
    use_empty_temporary_folder()
    people.save_new_customer("Findable Person", "555-0100", "f@example.com")
    rows = csv_files.load_rows("customers")
    assert csv_files.find_row(rows, "customer_id", "C001") is not None
    assert csv_files.find_row(rows, "customer_id", "c001") is not None   # capitals do not matter
    assert csv_files.find_row(rows, "customer_id", "C999") is None       # missing ID
    assert len(csv_files.search_rows(rows, "findable")) == 1
    assert csv_files.search_rows(rows, "nobody") == []


# ------------------------------------------------- drivers and vehicle tests

def test_add_driver_and_vehicle():
    use_empty_temporary_folder()
    driver = people.save_new_driver("Dan Driver", "555-0200", "dl-1001")
    vehicle = vehicles.save_new_vehicle("tx-1001", "Toyota Corolla")
    assert driver["driver_id"] == "D001"
    assert driver["license_number"] == "DL-1001"          # saved in capitals
    assert vehicle["vehicle_id"] == "V001"
    assert vehicle["status"] == "Available"


def test_duplicate_vehicle_registration_is_refused():
    use_empty_temporary_folder()
    vehicles.save_new_vehicle("TX-1001", "Toyota Corolla")
    assert vehicles.registration_exists("tx-1001") is True
    assert vehicles.save_new_vehicle("TX-1001", "Honda Civic") is None
    assert len(csv_files.load_rows("vehicles")) == 1


# --------------------------------------------------------------- ride tests

def make_test_data():
    """One customer, one driver, one vehicle and one ride, in a fresh temporary folder."""
    use_empty_temporary_folder()
    people.save_new_customer("Ann Test", "555-0100", "ann@example.com")
    people.save_new_driver("Dan Driver", "555-0200", "DL-1001")
    vehicles.save_new_vehicle("TX-1001", "Toyota Corolla")
    rides.save_new_ride("C001", "Central Market", "Airport", "2026-11-21", "08:30", 12, 5, 2.5)


def test_book_ride_saves_fare_and_status_requested():
    make_test_data()
    ride = csv_files.load_rows("rides")[0]
    assert ride["ride_id"] == "R001"
    assert ride["fare"] == "35.00"
    assert ride["status"] == "Requested"
    assert ride["driver_id"] == ""


def test_ride_needs_an_existing_customer():
    make_test_data()
    assert people.customer_exists("C001") is True
    assert people.customer_exists("C999") is False      # book_ride() stops here


def test_accept_ride_marks_driver_and_vehicle_unavailable():
    make_test_data()
    worked, message = rides.change_ride_status("R001", "Accepted", "D001", "V001")
    assert worked is True
    assert csv_files.load_rows("rides")[0]["status"] == "Accepted"
    assert csv_files.load_rows("drivers")[0]["status"] == "Unavailable"
    assert csv_files.load_rows("vehicles")[0]["status"] == "Unavailable"


def test_completing_a_ride_frees_driver_and_vehicle():
    make_test_data()
    rides.change_ride_status("R001", "Accepted", "D001", "V001")
    worked, message = rides.change_ride_status("R001", "Completed")
    assert worked is True
    assert csv_files.load_rows("drivers")[0]["status"] == "Available"
    assert csv_files.load_rows("vehicles")[0]["status"] == "Available"


def test_cancelling_a_requested_ride():
    make_test_data()
    worked, message = rides.change_ride_status("R001", "Cancelled")
    assert worked is True
    assert csv_files.load_rows("rides")[0]["status"] == "Cancelled"


def test_wrong_status_changes_are_refused():
    make_test_data()
    worked, message = rides.change_ride_status("R001", "Completed")   # Requested -> Completed
    assert worked is False
    rides.change_ride_status("R001", "Cancelled")
    worked, message = rides.change_ride_status("R001", "Accepted", "D001", "V001")
    assert worked is False                                             # Cancelled is final
    assert csv_files.load_rows("rides")[0]["status"] == "Cancelled"


def test_status_change_for_missing_ride():
    make_test_data()
    worked, message = rides.change_ride_status("R999", "Cancelled")
    assert worked is False
    assert "not found" in message


def test_accept_needs_existing_driver_and_vehicle():
    make_test_data()
    worked, message = rides.change_ride_status("R001", "Accepted", "D999", "V001")
    assert worked is False and "Driver" in message
    worked, message = rides.change_ride_status("R001", "Accepted", "D001", "V999")
    assert worked is False and "Vehicle" in message
    assert csv_files.load_rows("rides")[0]["status"] == "Requested"


def test_accept_needs_available_driver():
    make_test_data()
    rides.set_status("drivers", "driver_id", "D001", "Unavailable")
    worked, message = rides.change_ride_status("R001", "Accepted", "D001", "V001")
    assert worked is False
    assert "not available" in message


def test_reports_by_date_customer_and_driver():
    make_test_data()
    people.save_new_customer("Ben Test", "555-0101", "ben@example.com")
    rides.save_new_ride("C002", "A", "B", "2026-11-22", "10:00", 5, 5, 2.5)
    rides.change_ride_status("R001", "Accepted", "D001", "V001")
    assert len(rides.rides_on_date("2026-11-21")) == 1
    assert rides.rides_on_date("2030-01-01") == []
    assert len(rides.rides_for("customer_id", "C001")) == 1
    assert len(rides.rides_for("driver_id", "D001")) == 1
    assert rides.rides_for("driver_id", "D999") == []


def test_cannot_delete_customer_who_has_rides():
    make_test_data()
    assert csv_files.is_used_in_rides("customer_id", "C001") is True
    assert csv_files.is_used_in_rides("customer_id", "C002") is False


# ------------------------------------------------ the real data/ folder files

def test_real_data_has_at_least_30_records_in_every_file():
    use_real_data_folder()
    for table in csv_files.COLUMNS:
        assert len(csv_files.load_rows(table)) >= 30, table


def test_every_real_ride_points_to_real_records_and_has_the_right_fare():
    use_real_data_folder()
    customer_ids = [row["customer_id"] for row in csv_files.load_rows("customers")]
    driver_ids = [row["driver_id"] for row in csv_files.load_rows("drivers")]
    vehicle_ids = [row["vehicle_id"] for row in csv_files.load_rows("vehicles")]
    for ride in csv_files.load_rows("rides"):
        assert ride["customer_id"] in customer_ids, ride["ride_id"]
        if ride["driver_id"] != "":
            assert ride["driver_id"] in driver_ids, ride["ride_id"]
        if ride["vehicle_id"] != "":
            assert ride["vehicle_id"] in vehicle_ids, ride["ride_id"]
        expected = rides.calculate_fare(float(ride["distance_km"]), float(ride["base_fare"]),
                                        float(ride["rate_per_km"]))
        assert float(ride["fare"]) == expected, ride["ride_id"]


# -------------------------------------------------------------- run the tests

def run_all_tests():
    passed = 0
    failed = 0
    # globals() holds everything defined in this file. We run each function named test_...
    for name, function in list(globals().items()):
        if name.startswith("test_"):
            try:
                function()
                print(f"PASS  {name}")
                passed += 1
            except Exception as error:
                print(f"FAIL  {name}  ->  {type(error).__name__}: {error}")
                failed += 1
    use_real_data_folder()
    print(f"\n{passed} passed, {failed} failed")
    return failed


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
