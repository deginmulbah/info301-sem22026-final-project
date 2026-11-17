"""checks.py - check if a typed answer is OK.

Each function returns True if the text is OK, otherwise False.
They never ask questions and never print anything.
"""

from datetime import datetime


def is_valid_date(text):
    """Date must look like YYYY-MM-DD and be a real date (2026-02-30 is not)."""
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return False
    return len(text) == 10  # rejects short forms such as 2026-1-5


def is_valid_time(text):
    """Time must look like HH:MM on a 24-hour clock (09:30 is fine, 25:00 is not)."""
    try:
        datetime.strptime(text, "%H:%M")
    except ValueError:
        return False
    return len(text) == 5


def is_valid_phone(text):
    """7 to 15 digits. Spaces, '-' and '+' are allowed."""
    digits = text.replace("-", "").replace(" ", "").replace("+", "")
    return digits.isdigit() and 7 <= len(digits) <= 15


def is_valid_email(text):
    """A very simple check: it needs an @ and a dot, and no spaces."""
    return "@" in text and "." in text and " " not in text


def is_positive_number(text):
    """A number greater than 0 (used for distance)."""
    try:
        number = float(text)
    except ValueError:
        return False
    return 0 < number <= 100000


def is_zero_or_more(text):
    """A number that is 0 or more (used for fares). Negative numbers are not allowed."""
    try:
        number = float(text)
    except ValueError:
        return False
    return 0 <= number <= 100000
