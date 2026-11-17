"""main.py - start here.  Run the program with:   python main.py

Taxi Booking Application - INFO 301 final project (Project 6).
A learning prototype: fictional data only, simulated rides, no GPS or maps.
"""

import csv_files
import display
import people
import rides
import vehicles



def main():
    # Make sure the CSV files exist (they are created with headers if missing).
    try:
        csv_files.create_missing_files()
    except OSError as error:
        print(f"Cannot create the data files: {error}")
        return

    print("=" * 40)
    print("   TAXI BOOKING APPLICATION")
    print("=" * 40)

    try:
        while True:
            choice = display.show_menu("Main Menu", [
                "1. Customer Management",
                "2. Driver Management",
                "3. Vehicle Management",
                "4. Book Ride",
                "5. Update/View Ride",
                "6. Calculate Fare",
                "7. Basic Reports",
                "8. Exit",
            ])
            if choice == "1":
                people.customer_menu()
            elif choice == "2":
                people.driver_menu()
            elif choice == "3":
                vehicles.vehicle_menu()
            elif choice == "4":
                rides.book_ride()
            elif choice == "5":
                rides.ride_menu()
            elif choice == "6":
                rides.fare_menu()
            elif choice == "7":
                rides.report_menu()
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please type a number from 1 to 8.")
    except (EOFError, KeyboardInterrupt):
        # The user pressed Ctrl+C / Ctrl+D. Saved records are already in the CSV files.
        print("\nProgram stopped.")

    print("Goodbye!")


# This line runs main() only when you start this file (python main.py).
if __name__ == "__main__":
    main()
