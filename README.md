# Taxi Booking Application

INFO 301 Final Project - **Project 6**.
A simple Python console program to register customers, drivers and vehicles, book simulated rides and calculate a fare.

> Learning prototype. All data is **fictional**. No GPS, no maps, no real payments.

**Group:** _(group name)_

| Student ID | Name |
|---|---|
| 10273 | Herbert M. Taylor |
| 10288 | Prince S.K Marbiah |
| 10278 | Frank T. Morgan |
| 9118 | Mohammed A. Sheriff |
| 10367 | H. Nicika Darblo |
| 8822 | Julius G. Doe |
| 10900 | Jenkins D. Mulbah |
| 10757 | Aloysius B. Chappy |
| 9730 | Musu S. Josiah |
| 10504 | Josie J. Bealdeh |

## Features

- **Customers** - register, list, search, update, delete
- **Drivers** - register, list, search, update (including availability), delete
- **Vehicles** - register with registration (number plate), list, search, update (including availability), delete
- **Book a ride** - customer, pickup, destination, date, time
- **Fare** - base fare + rate per km x distance (you type the numbers)
- **Ride status** - Requested, Accepted, Completed or Cancelled
- **Reports** - rides by date, by customer or by driver
- **CSV files** - everything is saved and is still there after you restart

## Requirements

Python 3 (no extra libraries to install).

## How to run

Open a terminal in this folder and type:

```bash
python main.py
```

(On some computers: `python3 main.py`.) Type the number of a menu option and press Enter.

To run the automatic tests:

```bash
python test_app.py
```

## The menu

```
1. Customer Management
2. Driver Management
3. Vehicle Management
4. Book Ride
5. Update/View Ride
6. Calculate Fare
7. Basic Reports
8. Exit
```

## The fare formula

```
fare = base fare + (rate per km x distance)
```

Example: base fare 5, rate 2.5 per km, 12 km -> 5 + (2.5 x 12) = **35.00**

The distance must be greater than 0. The base fare and rate cannot be negative. The formula is written in one place only: `calculate_fare()` in `rides.py`.

## Ride status rules

```
Requested --> Accepted --> Completed
    |             |
    +--> Cancelled <--+
```

- A ride must be for a customer who exists.
- To **accept** a ride you give a driver ID and a vehicle ID. Both must exist and be "Available". They become "Unavailable" until the ride is completed or cancelled.
- "Completed" and "Cancelled" rides cannot be changed again.
- A customer, driver or vehicle that is used by a ride cannot be deleted.

## Files in this project

| File | What it does |
|---|---|
| `main.py` | Starts the program and shows the main menu |
| `people.py` | Customers and drivers (two sections, same actions in each) |
| `vehicles.py` | Vehicles: register, list, search, update, delete |
| `rides.py` | The fare formula, booking rides, ride status, reports |
| `csv_files.py` | Reading and saving the CSV files, making new IDs, finding and searching rows |
| `checks.py` | Checks if a typed answer is OK (date, time, phone, email, numbers): True or False |
| `inputs.py` | Asks the user questions and repeats them until the answer is good |
| `display.py` | Prints menus, tables and single records |
| `test_app.py` | 29 automatic tests |
| `data/` | The 4 CSV files |
| `docs/Code_Guide.pdf` | A beginner's guide that explains every file and function |

### How the data is stored

Each CSV file is one table. In the program a table is a **list**, and each row is a **dictionary**:

```python
customers = [
    {"customer_id": "C001", "name": "Amara Johnson", "phone": "555-0101", "email": "..."},
    {"customer_id": "C002", "name": "Benjamin Cole", "phone": "555-0102", "email": "..."},
]
```

To change data the program does the same three steps every time: **load** the CSV into a list, **change** the list, **save** the list back to the CSV.

### A pattern you will see in every file

Each action is split into two functions:

- one that **asks the user** questions (for example `add_customer()`)
- one that **saves to the file** with no questions (for example `save_new_customer()`)

This makes the code easy to read and lets `test_app.py` test the saving part without typing anything.

## The CSV files (`data/`)

| File | Columns | Records |
|---|---|---|
| `customers.csv` | customer_id, name, phone, email | 30 |
| `drivers.csv` | driver_id, name, phone, license_number, status | 30 |
| `vehicles.csv` | vehicle_id, registration, model, status | 30 |
| `rides.csv` | ride_id, customer_id, pickup, destination, date, time, distance_km, base_fare, rate_per_km, fare, driver_id, vehicle_id, status | 36 |

If a CSV file is missing or empty, the program creates it with its header row.

## Input checks and errors

- Names, places and IDs cannot be empty.
- Dates must be `YYYY-MM-DD` and real (2026-02-30 is refused). Times must be `HH:MM`.
- Phone: 7 to 15 digits. Email: needs `@` and a dot.
- Distance must be more than 0. Fare amounts cannot be negative. Letters are refused.
- Wrong input never crashes the program: it prints a message and asks again.
- `try/except` is used when reading and saving files (for example when a file is open in Excel) and when turning text into numbers.

## Limitations

- No login, no real payments, no maps: you type the distance yourself.
- Driver clashes at the same time are not checked: a driver is only "Available" or "Unavailable".
- One person at a time should use the program.
- The whole CSV file is read and saved each time (fine for a small project).

---

## Test checklist (do by hand during the demonstration)

Start the program with `python main.py`. Tick the box when the test gives the expected result.
(`python test_app.py` runs the automatic tests that cover the same ideas.)

### Normal cases

| # | Test | What to do | Expected result | Done |
|---|---|---|---|---|
| 1 | Add a valid customer | Menu 1 > 1: name `Test Person`, phone `555-0199`, email `test@example.com` | "Saved. The new customer ID is C031." | [ ] |
| 2 | See it in the list | Menu 1 > 2 | C031 is at the bottom of the list | [ ] |
| 3 | Search an existing record | Menu 1 > 3: type `Test Person` | The row for C031 is shown | [ ] |
| 4 | Update a record | Menu 1 > 4: `C031`, choose 1, new name `Test Person Two` | "Customer updated." and the list shows the new name | [ ] |
| 5 | Add a driver and a vehicle | Menu 2 > 1 and Menu 3 > 1 | New IDs D031 and V031, status Available | [ ] |
| 6 | Book a ride | Menu 4: `C031`, `Central Market`, `Airport Terminal`, `2026-11-21`, `08:30`, `12`, `5`, `2.5` | Ride R037 Requested. Fare 5.00 + (2.50 x 12.00) = 35.00 | [ ] |
| 7 | Sample fare | Menu 6 > 1: `10`, `5`, `2.5` | 5.00 + (2.50 x 10.00) = 30.00 | [ ] |
| 8 | Accept a ride | Menu 5 > 3: `R037`, `Accepted`, driver `D031`, vehicle `V031` | "Ride R037 is now Accepted." D031 and V031 become Unavailable | [ ] |
| 9 | Complete a ride | Menu 5 > 3: `R037`, `Completed` | "Ride R037 is now Completed." D031 and V031 are Available again | [ ] |
| 10 | Reports | Menu 7 > 1: `2026-10-26` (6 rides). Menu 7 > 2: `C001` (4 rides). Menu 7 > 3: `D018` (3 rides) | Tables with those rides | [ ] |
| 11 | **Restart keeps the data** | Choose 8 to exit. Run `python main.py` again. Menu 5 > 1 | Ride R037 is still in the list | [ ] |

### Invalid input (the program must not crash)

| # | Test | What to do | Expected result | Done |
|---|---|---|---|---|
| 12 | Search a **missing ID** | Menu 1 > 3: `C999` | "No customer found for 'C999'." | [ ] |
| 13 | View a missing ride | Menu 5 > 2: `R999` | "Ride R999 was not found." | [ ] |
| 14 | Empty name | Menu 1 > 1: just press Enter | "This cannot be empty." and it asks again | [ ] |
| 15 | Bad phone and bad email | Phone `abc`, email `hello` | Messages explaining the format, asks again | [ ] |
| 16 | Wrong menu choice | At any menu type `abc`, `99` or press Enter | "Invalid choice..." and the menu is shown again | [ ] |
| 17 | Ride for a customer that does not exist | Menu 4: `C999` | "Customer C999 was not found. Register the customer first." | [ ] |
| 18 | Same pickup and destination | Menu 4: both `Airport Terminal` | "Pickup and destination must be different places." | [ ] |
| 19 | Invalid date | `21-11-2026`, `2026-02-30`, `tomorrow` | "Use the format YYYY-MM-DD..." | [ ] |
| 20 | Invalid time | `9:30`, `25:00` | "Use the format HH:MM..." | [ ] |
| 21 | **Zero distance** | Menu 6 > 1: `0` | "Please enter a number greater than 0." | [ ] |
| 22 | **Negative distance** | Menu 6 > 1: `-5` | Same message | [ ] |
| 23 | Negative fare amount or letters | Base fare `-1`, rate `abc` | "Please enter a number that is 0 or more." | [ ] |
| 24 | Accept with a driver that does not exist | Menu 5 > 3 on a Requested ride: `Accepted`, driver `D999` | "Not changed: Driver D999 was not found." | [ ] |
| 25 | Accept with an unavailable driver | Same, driver `D005` (busy on another ride) | "Not changed: Driver D005 is not available." | [ ] |
| 26 | Wrong status change | Try to change a Completed ride | "This ride is finished and its status cannot be changed." | [ ] |
| 27 | Delete a record that is in use | Menu 1 > 5: `C001` (has rides) | "This customer has rides, so the record cannot be deleted." | [ ] |
| 28 | Duplicate vehicle registration | Menu 3 > 1: `TX-1001` | "A vehicle with this registration already exists." | [ ] |
| 29 | Missing CSV file | Close the program, delete `data/customers.csv`, run it, list customers | The file is created again (empty list), no crash | [ ] |

**Before the demonstration:** testing adds records. Restore the original `data/` folder (30+ records each) so the IDs above match.
