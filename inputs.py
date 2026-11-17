"""inputs.py - ask the user questions.

Each function repeats the question until the answer is good,
then returns the answer.
"""

import checks


def ask_text(prompt):
    """Ask for text that is not empty."""
    while True:
        answer = input(prompt + ": ").strip()
        if answer != "":
            return answer
        print("  This cannot be empty. Please try again.")


def ask_phone():
    while True:
        answer = input("Phone number: ").strip()
        if checks.is_valid_phone(answer):
            return answer
        print("  Phone must have 7 to 15 digits (for example 555-0123).")


def ask_email():
    while True:
        answer = input("Email: ").strip()
        if checks.is_valid_email(answer):
            return answer
        print("  Email must look like name@example.com.")


def ask_date():
    while True:
        answer = input("Date (YYYY-MM-DD): ").strip()
        if checks.is_valid_date(answer):
            return answer
        print("  Use the format YYYY-MM-DD and a real date, for example 2026-11-21.")


def ask_time():
    while True:
        answer = input("Time (HH:MM): ").strip()
        if checks.is_valid_time(answer):
            return answer
        print("  Use the format HH:MM, for example 08:30.")


def ask_positive_number(prompt):
    """Ask for a number greater than 0 and return it as a number."""
    while True:
        answer = input(prompt + ": ").strip()
        if checks.is_positive_number(answer):
            return float(answer)
        print("  Please enter a number greater than 0.")


def ask_zero_or_more(prompt):
    """Ask for a number that is 0 or more and return it as a number."""
    while True:
        answer = input(prompt + ": ").strip()
        if checks.is_zero_or_more(answer):
            return float(answer)
        print("  Please enter a number that is 0 or more.")


def ask_choice(prompt, choices):
    """Ask until the answer is one of the choices, for example Available / Unavailable."""
    while True:
        answer = input(f"{prompt} ({'/'.join(choices)}): ").strip().title()
        if answer in choices:
            return answer
        print("  Please type one of: " + ", ".join(choices))


def ask_yes_no(question):
    """Return True for yes, False for no."""
    while True:
        answer = input(question + " (yes/no): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("  Please type yes or no.")
