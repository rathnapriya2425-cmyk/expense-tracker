"""Personal Expense Tracker with CSV
Record daily expenses by category and save them to a CSV file.
Features: add, view, filter expenses, and category summary statistics.
"""

import csv
import os
from datetime import datetime

FILENAME = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Health", "Entertainment", "Other"]


# ---------------- CSV read / write ----------------
def load_expenses():
    """Read all expenses from the CSV file (empty list if the file doesn't exist yet)."""
    if not os.path.exists(FILENAME):
        return []
    expenses = []
    with open(FILENAME, "r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


def save_expense(expense):
    """Append one expense to the CSV file, writing the header if the file is new."""
    is_new = not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0
    with open(FILENAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()
        writer.writerow(expense)


# ---------------- Input helpers ----------------
def get_date(prompt):
    """Ask for a date in YYYY-MM-DD format. Press Enter for today."""
    while True:
        text = input(prompt).strip()
        if text == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("  Invalid date. Use YYYY-MM-DD, e.g. 2026-10-05.")


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount > 0:
                return round(amount, 2)
            print("  Amount must be greater than 0.")
        except ValueError:
            print("  Invalid amount. Enter a number, e.g. 250 or 99.50.")


def get_category():
    print("Categories:")
    for i, name in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {name}")
    while True:
        text = input("Choose category number: ").strip()
        if text.isdigit() and 1 <= int(text) <= len(CATEGORIES):
            return CATEGORIES[int(text) - 1]
        print(f"  Enter a number from 1 to {len(CATEGORIES)}.")


# ---------------- Features ----------------
def add_expense():
    print("\n--- Add Expense ---")
    date = get_date("Date (YYYY-MM-DD, Enter for today): ")
    category = get_category()
    description = input("Description: ").strip() or "-"
    amount = get_amount("Amount (Rs): ")
    save_expense({"date": date, "category": category, "description": description, "amount": amount})
    print(f"Saved: {date} | {category} | {description} | Rs {amount:.2f}")


def print_table(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print(f"\n{'No.':<4}{'Date':<12}{'Category':<15}{'Description':<22}{'Amount':>10}")
    print("-" * 63)
    for i, e in enumerate(expenses, start=1):
        print(f"{i:<4}{e['date']:<12}{e['category']:<15}{e['description'][:20]:<22}{e['amount']:>10.2f}")
    print("-" * 63)
    print(f"{'Total':<53}{sum(e['amount'] for e in expenses):>10.2f}")


def view_expenses():
    print("\n--- All Expenses ---")
    print_table(sorted(load_expenses(), key=lambda e: e["date"]))


def filter_expenses():
    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By month (YYYY-MM)")
    print("3. By date range")
    choice = ""
    while choice not in ("1", "2", "3"):
        choice = input("Choose 1-3: ").strip()
    expenses = load_expenses()

    if choice == "1":
        category = get_category()
        result = [e for e in expenses if e["category"] == category]
    elif choice == "2":
        while True:
            month = input("Month (YYYY-MM): ").strip()
            try:
                datetime.strptime(month, "%Y-%m")
                break
            except ValueError:
                print("  Invalid month. Use YYYY-MM, e.g. 2026-10.")
        result = [e for e in expenses if e["date"].startswith(month)]
    else:
        start = get_date("Start date (YYYY-MM-DD): ")
        end = get_date("End date (YYYY-MM-DD): ")
        while end < start:
            print("  End date must be on or after the start date.")
            end = get_date("End date (YYYY-MM-DD): ")
        result = [e for e in expenses if start <= e["date"] <= end]

    print_table(sorted(result, key=lambda e: e["date"]))


def category_summary():
    print("\n--- Category Summary ---")
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    totals, counts = {}, {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    grand_total = sum(totals.values())

    print(f"\n{'Category':<15}{'Count':>6}{'Total':>12}{'Average':>10}{'Share':>8}")
    print("-" * 51)
    for cat, total in sorted(totals.items(), key=lambda item: -item[1]):
        print(f"{cat:<15}{counts[cat]:>6}{total:>12.2f}{total / counts[cat]:>10.2f}{total / grand_total * 100:>7.1f}%")
    print("-" * 51)
    biggest = max(expenses, key=lambda e: e["amount"])
    top_cat = max(totals, key=totals.get)
    print(f"Total spent     : Rs {grand_total:.2f} across {len(expenses)} expenses")
    print(f"Top category    : {top_cat} (Rs {totals[top_cat]:.2f})")
    print(f"Largest expense : Rs {biggest['amount']:.2f} - {biggest['description']} on {biggest['date']}")


# ---------------- Main menu ----------------
def main():
    print("=== Personal Expense Tracker ===")
    while True:
        print("\nMain Menu")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Category summary")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("Goodbye! Your expenses are saved in", FILENAME)
            break
        else:
            print("  Invalid option. Please enter 1 to 5.")


if __name__ == "__main__":
    main()
