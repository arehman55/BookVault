import sqlite3
import sys

# DATABASE SETUP


def setup_database():
    # Database Connection
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()

    # Create authors table
    # id is unique for author and name cannot be empty (unique)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM authors")
    if cursor.fetchone()[0] == 0:
        # Insert local authors
        default_authors = ["Ahmad Ali", "Usman Shahid", "Asif"]
        for author in default_authors:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (author,))

        # Insert books
        default_books = [("Python", 1), ("Database", 2), ("Pak Studies", 3)]
        for title, author_id in default_books:
            cursor.execute(
                "INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id)
            )

        print("Database is ready! Added default authors and books for testing.")
    else:
        print("Database is ready and tables are connected.")

    # Save changes and close connection
    conn.commit()
    conn.close()


# COMMAND FUNCTIONS


def add_author(author_name):
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (author_name,))
        conn.commit()
        print(f"Success: Added author '{author_name}' to the database.")
    except sqlite3.IntegrityError:
        print(f"Error: The author '{author_name}' already exists.")

    conn.close()


def add_book(book_title, author_name):
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()

    # find the author
    cursor.execute("SELECT id FROM authors WHERE name = ?", (author_name,))
    author_result = cursor.fetchone()

    # If author not found, book cannot be added
    if author_result is None:
        print(f"Error: Author '{author_name}' not found. Please add the author first.")
    else:
        author_id = author_result[0]

        cursor.execute(
            "INSERT INTO books (title, author_id) VALUES (?, ?)",
            (book_title, author_id),
        )
        conn.commit()
        print(f"Success: Added book '{book_title}' by {author_name}.")

    conn.close()


def list_books():
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT books.title, authors.name 
        FROM books
        JOIN authors ON books.author_id = authors.id
    """)

    all_books = cursor.fetchall()

    if len(all_books) == 0:
        print("No books found in the database.")
    else:
        print("\n--- List of All Books ---")
        for book in all_books:
            print(f"Book: {book[0]} | Author: {book[1]}")
        print("-------------------------\n")

    conn.close()


def search_books(search_term):
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()
    safe_search_term = f"%{search_term}%"

    cursor.execute(
        """
        SELECT books.title, authors.name 
        FROM books
        JOIN authors ON books.author_id = authors.id
        WHERE books.title LIKE ?
    """,
        (safe_search_term,),
    )

    results = cursor.fetchall()

    if len(results) == 0:
        print(f"No books found containing '{search_term}'.")
    else:
        print(f"\n--- Search Results for '{search_term}' ---")
        for book in results:
            print(f"Found: {book[0]} by {book[1]}")
        print("-----------------------------------\n")

    conn.close()


def show_stats():
    conn = sqlite3.connect("bookvault.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT authors.name, COUNT(books.id) 
        FROM authors
        LEFT JOIN books ON authors.id = books.author_id
        GROUP BY authors.id
    """)

    stats = cursor.fetchall()

    print("\n--- Author Statistics ---")
    for stat in stats:
        print(f"Author: {stat[0]} | Total Books: {stat[1]}")
    print("-------------------------\n")

    conn.close()


if __name__ == "__main__":
    setup_database()

    if len(sys.argv) < 2:
        print("\nError: Please provide a command.")
        print("Commands: add-author, add-book, list-books, search, stats")
    else:
        command = sys.argv[1]

        if command == "add-author" and len(sys.argv) == 3:
            author_name = sys.argv[2]
            add_author(author_name)

        elif command == "add-book" and len(sys.argv) == 4:
            book_title = sys.argv[2]
            author_name = sys.argv[3]
            add_book(book_title, author_name)

        elif command == "list-books":
            list_books()

        elif command == "search" and len(sys.argv) == 3:
            search_term = sys.argv[2]
            search_books(search_term)

        elif command == "stats":
            show_stats()

        else:
            print("\nError: Invalid command or missing arguments.")
            print("Examples:")
            print('  python bookvault.py add-author "Usman Shahid"')
            print('  python bookvault.py add-book "Database" "Usman Shahid"')
            print('  python bookvault.py search "Pak"')
