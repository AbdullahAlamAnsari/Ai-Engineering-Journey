"""
#LIBRARIAN_CREDENTIALS = {"admin": "giki2025"}
Console-Based Library Management System
Atomcamp AI18 Python Project
Abdullah Alam Ansari
"""

import csv
import os
from datetime import datetime


books = []          # List of book dicts
issued_books = []   # List of issued record dicts
DATA_FILE = "library_data.csv"
ISSUED_FILE = "issued_data.csv"

def separator(char="─", width=55):
    print(char * width)

def header(title):
    separator()
    print(f"  {title}")
    separator()

def find_book_by_id(book_id):
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None

def find_book_by_title(title):
    results = []
    for book in books:
        if title.lower() in book["title"].lower():
            results.append(book)
    return results

def display_book(book):
    print(f"  ID       : {book['book_id']}")
    print(f"  Title    : {book['title']}")
    print(f"  Author   : {book['author']}")
    print(f"  Category : {book['category']}")
    print(f"  Quantity : {book['quantity']}")
    print(f"  Issued   : {book['issued']}")
    separator("-", 40)

# ─── FEATURE 1: ADD BOOK ──────────────────────────────────────────────────────
def add_book():
    header("ADD BOOK")
    try:
        book_id = input("  Enter Book ID    : ").strip()
        if not book_id:
            raise ValueError("Book ID cannot be empty.")
        if find_book_by_id(book_id):
            print("  [!] Book ID already exists.")
            return

        title    = input("  Enter Title      : ").strip()
        author   = input("  Enter Author     : ").strip()
        category = input("  Enter Category   : ").strip()
        quantity = int(input("  Enter Quantity   : ").strip())

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        book = {
            "book_id"  : book_id,
            "title"    : title,
            "author"   : author,
            "category" : category,
            "quantity" : quantity,
            "issued"   : 0
        }
        books.append(book)
        print(f"\n  [✓] Book '{title}' added successfully!")

    except ValueError as e:
        print(f"  [!] Invalid input: {e}")

# ─── FEATURE 2: VIEW ALL BOOKS ────────────────────────────────────────────────
def view_all_books():
    header("ALL BOOKS")
    if not books:
        print("  No books in the library.")
        return
    for book in books:
        display_book(book)

# ─── FEATURE 3: SEARCH BOOK ───────────────────────────────────────────────────
def search_book():
    header("SEARCH BOOK")
    print("  1. Search by Book ID")
    print("  2. Search by Title")
    choice = input("  Choose: ").strip()

    if choice == "1":
        book_id = input("  Enter Book ID: ").strip()
        book = find_book_by_id(book_id)
        if book:
            display_book(book)
        else:
            print("  [!] Book not found.")

    elif choice == "2":
        title = input("  Enter Title (partial ok): ").strip()
        results = find_book_by_title(title)
        if results:
            print(f"\n  Found {len(results)} result(s):\n")
            for book in results:
                display_book(book)
        else:
            print("  [!] No matching books found.")
    else:
        print("  [!] Invalid choice.")

# ─── FEATURE 4: UPDATE BOOK ───────────────────────────────────────────────────
def update_book():
    header("UPDATE BOOK")
    book_id = input("  Enter Book ID to update: ").strip()
    book = find_book_by_id(book_id)

    if not book:
        print("  [!] Book not found.")
        return

    print("\n  What to update?")
    print("  1. Title")
    print("  2. Author")
    print("  3. Category")
    print("  4. Quantity")
    choice = input("  Choose: ").strip()

    try:
        if choice == "1":
            book["title"] = input("  New Title: ").strip()
        elif choice == "2":
            book["author"] = input("  New Author: ").strip()
        elif choice == "3":
            book["category"] = input("  New Category: ").strip()
        elif choice == "4":
            book["quantity"] = int(input("  New Quantity: ").strip())
        else:
            print("  [!] Invalid choice.")
            return
        print("  [✓] Book updated successfully!")
    except ValueError:
        print("  [!] Invalid input.")

# ─── FEATURE 5: DELETE BOOK ───────────────────────────────────────────────────
def delete_book():
    header("DELETE BOOK")
    book_id = input("  Enter Book ID to delete: ").strip()
    book = find_book_by_id(book_id)

    if not book:
        print("  [!] Book not found.")
        return

    confirm = input(f"  Delete '{book['title']}'? (yes/no): ").strip().lower()
    if confirm == "yes":
        books.remove(book)
        print("  [✓] Book deleted successfully!")
    else:
        print("  [x] Deletion cancelled.")

# ─── FEATURE 6: ISSUE BOOK ────────────────────────────────────────────────────
def issue_book():
    header("ISSUE BOOK")
    try:
        student_name = input("  Student Name : ").strip()
        book_id      = input("  Book ID      : ").strip()
        book = find_book_by_id(book_id)

        if not book:
            print("  [!] Book not found.")
            return
        if book["quantity"] <= 0:
            print("  [!] No copies available.")
            return

        book["quantity"] -= 1
        book["issued"]   += 1

        record = {
            "student"    : student_name,
            "book_id"    : book_id,
            "title"      : book["title"],
            "issue_date" : datetime.now().strftime("%Y-%m-%d")
        }
        issued_books.append(record)
        print(f"\n  [✓] '{book['title']}' issued to {student_name}.")

    except Exception as e:
        print(f"  [!] Error: {e}")

# ─── FEATURE 7: RETURN BOOK ───────────────────────────────────────────────────
def return_book():
    header("RETURN BOOK")
    try:
        student_name = input("  Student Name : ").strip()
        book_id      = input("  Book ID      : ").strip()
        book = find_book_by_id(book_id)

        if not book:
            print("  [!] Book not found.")
            return

        # Find matching issued record
        record = None
        for r in issued_books:
            if r["book_id"] == book_id and r["student"].lower() == student_name.lower():
                record = r
                break

        if not record:
            print("  [!] No issued record found for this student and book.")
            return

        book["quantity"] += 1
        issued_books.remove(record)
        print(f"\n  [✓] '{book['title']}' returned by {student_name}.")

    except Exception as e:
        print(f"  [!] Error: {e}")

# ─── FEATURE 8: LIBRARY STATISTICS ───────────────────────────────────────────
def library_statistics():
    header("LIBRARY STATISTICS")

    if not books:
        print("  No books in the library.")
        return

    total_books      = sum(b["quantity"] + b["issued"] for b in books)
    total_available  = sum(b["quantity"] for b in books)    
    total_issued     = sum(b["issued"] for b in books)
    categories       = set(b["category"] for b in books)
    most_issued      = max(books, key=lambda b: b["issued"])

    print(f"  Total Book Titles   : {len(books)}")
    print(f"  Total Copies        : {total_books}")
    print(f"  Available Copies    : {total_available}")
    print(f"  Currently Issued    : {total_issued}")
    print(f"  Total Categories    : {len(categories)}")
    print(f"  Categories          : {', '.join(categories)}")
    print(f"  Most Issued Book    : {most_issued['title']} ({most_issued['issued']} times)")

    # BONUS: Top 5 most borrowed
    top5 = sorted(books, key=lambda b: b["issued"], reverse=True)[:5]
    print("\n  Top 5 Most Borrowed:")
    for i, b in enumerate(top5, 1):
        print(f"    {i}. {b['title']} — {b['issued']} issued")

# ─── FEATURE 9: SAVE DATA ─────────────────────────────────────────────────────
def save_data():
    try:
        with open(DATA_FILE, "w", newline="") as f:
            fieldnames = ["book_id", "title", "author", "category", "quantity", "issued"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)

        with open(ISSUED_FILE, "w", newline="") as f:
            fieldnames = ["student", "book_id", "title", "issue_date"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(issued_books)

        print("  [✓] Data saved successfully!")
    except Exception as e:
        print(f"  [!] Save error: {e}")

# ─── FEATURE 10: LOAD DATA ────────────────────────────────────────────────────
def load_data():
    global books, issued_books
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                reader = csv.DictReader(f)
                books = []
                for row in reader:
                    row["quantity"] = int(row["quantity"])
                    row["issued"]   = int(row["issued"])
                    books.append(row)
            print(f"  [✓] Loaded {len(books)} books from file.")
        else:
            print("  [i] No saved data found. Starting fresh.")

        if os.path.exists(ISSUED_FILE):
            with open(ISSUED_FILE, "r") as f:
                reader = csv.DictReader(f)
                issued_books = list(reader)

    except FileNotFoundError:
        print("  [!] Data file missing.")
    except Exception as e:
        print(f"  [!] Load error: {e}")

# ─── BONUS: SEARCH BY CATEGORY ────────────────────────────────────────────────
def search_by_category():
    header("SEARCH BY CATEGORY")
    category = input("  Enter Category: ").strip().lower()
    results = [b for b in books if b["category"].lower() == category]
    if results:
        print(f"\n  Found {len(results)} book(s) in '{category}':\n")
        for book in results:
            display_book(book)
    else:
        print("  [!] No books found in this category.")

# ─── BONUS: SORT BY QUANTITY ──────────────────────────────────────────────────
def sort_by_quantity():
    header("BOOKS SORTED BY QUANTITY")
    if not books:
        print("  No books available.")
        return
    sorted_books = sorted(books, key=lambda x: x["quantity"], reverse=True)
    for book in sorted_books:
        display_book(book)

# ─── BONUS: LIBRARIAN LOGIN ───────────────────────────────────────────────────
LIBRARIAN_CREDENTIALS = {"admin": "giki2025"}

def librarian_login():
    header("LIBRARIAN LOGIN")
    username = input("  Username: ").strip()
    password = input("  Password: ").strip()
    if LIBRARIAN_CREDENTIALS.get(username) == password:
        print("  [✓] Login successful!\n")
        return True
    else:
        print("  [!] Invalid credentials.")
        return False

# ─── LEETCODE PROBLEMS ────────────────────────────────────────────────────────
def reverse_titles(book_titles):
    """Problem 1: Reverse a list of book titles."""
    return book_titles[::-1]

def highest_quantity(book_list):
    """Problem 2: Find book with highest quantity."""
    return max(book_list, key=lambda x: x["quantity"])

def merge_catalogs(cat1, cat2):
    """Problem 3: Merge two library catalogs."""
    cat1.update(cat2)
    return cat1

def count_category(categories, category):
    """Problem 4: Count books in a category."""
    return categories.count(category)

def find_book(book_id):
    """Problem 5: Find book by ID."""
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None

# ─── MAIN MENU ────────────────────────────────────────────────────────────────
def main():
    print("\n" + "═" * 55)
    print("      LIBRARY MANAGEMENT SYSTEM")
    print("      Atomcamp AI18 | Abdullah Alam Ansari")
    print("═" * 55)

    # Login gate
    if not librarian_login():
        return

    load_data()

    while True:
        print("\n" + "─" * 55)
        print("  MAIN MENU")
        print("─" * 55)
        print("  1.  Add Book")
        print("  2.  View All Books")
        print("  3.  Search Book (ID / Title)")
        print("  4.  Update Book")
        print("  5.  Delete Book")
        print("  6.  Issue Book")
        print("  7.  Return Book")
        print("  8.  Library Statistics")
        print("  9.  Save Data")
        print("  10. Search by Category  [BONUS]")
        print("  11. Sort Books by Quantity [BONUS]")
        print("  0.  Exit")
        print("─" * 55)

        choice = input("  Enter choice: ").strip()

        menu = {
            "1" : add_book,
            "2" : view_all_books,
            "3" : search_book,
            "4" : update_book,
            "5" : delete_book,
            "6" : issue_book,
            "7" : return_book,
            "8" : library_statistics,
            "9" : save_data,
            "10": search_by_category,
            "11": sort_by_quantity,
        }

        if choice == "0":
            save_data()
            print("\n  Goodbye! Data saved.\n")
            break
        elif choice in menu:
            menu[choice]()
        else:
            print("  [!] Invalid choice. Try again.")


if __name__ == "__main__":
    main()
