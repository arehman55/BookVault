# BookVault CLI

A simple command-line library catalog I built using Python and SQLite. This project helps me understand relational databases, Foreign Keys, and writing safe parameterized SQL queries.

## Database Schema
This project uses a local SQLite database file (`bookvault.db`). It contains two related tables:

**1. authors**
* `id`: INTEGER (Primary Key, Auto-increment)
* `name`: TEXT (Unique, Not Null)

**2. books**
* `id`: INTEGER (Primary Key, Auto-increment)
* `title`: TEXT (Not Null)
* `author_id`: INTEGER (Foreign Key linking to `authors.id`)

## Setup Instructions
You do not need to install any external packages for this project. It uses Python's built-in `sqlite3` and `sys` modules.

1. Open your terminal.
2. Navigate to the project folder.
3. Run any command below. The script will automatically create the `bookvault.db` file and insert some default testing data (Pakistani authors and common books) if the database is empty.

## Available Commands

**Add a new author:**
`python bookvault.py add-author "Tariq Mahmood"`

**Add a new book (The author must be added first):**
`python bookvault.py add-book "Web Development" "Tariq Mahmood"`

**List all books with their author names:**
`python bookvault.py list-books`

**Search for a book by its title:**
`python bookvault.py search "Python"`

**Show how many books each author has written:**
`python bookvault.py stats`