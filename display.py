"""display.py - print menus, tables and single records on the screen."""


def show_menu(title, options):
    """Print a menu and return what the user typed."""
    print(f"\n=== {title} ===")
    for option in options:
        print(option)
    return input("Choose an option: ").strip()


def show_table(rows, columns):
    """Print rows as a table. 'columns' lists which columns to show."""
    if len(rows) == 0:
        print("  No records found.")
        return

    # Each column is as wide as its longest value.
    # widths is a dictionary, for example {"name": 14, "phone": 8}
    widths = {}
    for column in columns:
        width = len(column)
        for row in rows:
            if len(row[column]) > width:
                width = len(row[column])
        widths[column] = width

    # ljust(n) adds spaces to the right of a text until it is n characters long.
    heading = ""
    for column in columns:
        heading += column.ljust(widths[column] + 2)
    print(heading)
    print("-" * len(heading))

    for row in rows:
        line = ""
        for column in columns:
            line += row[column].ljust(widths[column] + 2)
        print(line)
    if len(rows) == 1:
        print("(1 record)")
    else:
        print(f"({len(rows)} records)")


def show_record(row):
    """Print one row, one detail per line."""
    for name, value in row.items():
        print(f"  {name}: {value}")
