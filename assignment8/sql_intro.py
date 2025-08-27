import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/magazines.db")

def create_tables(cursor):
    """
    Create the necessary tables in the database.
    """
    # Create the publishers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publishers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    # Create the magazines table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS magazines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name  TEXT UNIQUE NOT NULL,
        publisher_id INTEGER NOT NULL,
        FOREIGN KEY (publisher_id) REFERENCES publishers (id)
    );
    """)

    # Create the subscribers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL
    );
    """)

    # Create the subscriptions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        subscriber_id INTEGER NOT NULL,
        magazine_id INTEGER NOT NULL,
        expiration_date TEXT NOT NULL,
        PRIMARY KEY (subscriber_id, magazine_id),
        FOREIGN KEY (subscriber_id) REFERENCES subscribers(id),
        FOREIGN KEY (magazine_id) REFERENCES magazines(id)
    );
    """)

def add_publishers(cursor, name):
    """
    Add a new publisher to the database.
    """
    if not name.strip(): 
        print("Error: publisher name cannot be empty.")
        return
    
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"Publisher {name} is already in the database.")

def add_magazine(cursor, name, publisher_id):
    """
    Add a new magazine to the database.
    """
    if not name.strip():
        print("Error: magazine name cannot be empty.")
        return

    if not publisher_id:
        print("Error: publisher_id cannot be empty.")
        return

    try:
        cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?, ?)", (name, publisher_id))
    except sqlite3.IntegrityError:
        print(f"Magazine {name} is already in the database.")

def add_subscriber(cursor, name, address):
    """
    Add a new subscriber to the database.
    """
    if not name.strip() or not address.strip():
        print("Error: name and address cannot be empty.")
        return
    
    cursor.execute(
        "SELECT * FROM subscribers WHERE name = ? AND address = ?",
        (name, address)
    )
    if cursor.fetchone():
        print(f"Subscriber '{name}' at '{address}' already exists.")
        return
    
    try:
        cursor.execute("INSERT INTO subscribers (name, address) VALUES (?, ?)", (name, address))
    except sqlite3.Error as e:
        print(f"Error inserting subscriber: {e}")

def add_subscription(cursor, subscriber_id, magazine_id, expiration_date):
    """
    Add a new subscription to the database.
    """
    if not subscriber_id:
        print("Error: subscriber_id cannot be empty or 0.")
        return
    if not magazine_id:
        print("Error: magazine_id cannot be empty or 0.")
        return
    if not expiration_date.strip():
        print("Error: expiration_date cannot be empty.")
        return
    
    try:
        cursor.execute("INSERT INTO subscriptions (subscriber_id, magazine_id, expiration_date) VALUES (?, ?, ?)",
                       (subscriber_id, magazine_id, expiration_date))
    except sqlite3.IntegrityError:
        print(f"Subscription for subscriber {subscriber_id} and magazine {magazine_id} is already in the database.")

def populate_tables(cursor):
    """
    Populate the database tables with initial data.
    """

    # Add initial publishers
    add_publishers(cursor, "Shueisha")
    add_publishers(cursor, "Triumph Books")
    add_publishers(cursor, "MDPI")

    # Add initial magazines
    add_magazine(cursor, "Weekly Shonen Jump", 1)
    add_magazine(cursor, "Baseball Preview Guides", 2)
    add_magazine(cursor, "Cryptography", 3)

    # Add initial subscribers
    add_subscriber(cursor, "Joey Tribbiani", "425 Grove Street apt 19")
    add_subscriber(cursor, "Hercule Poirot", "Apt 56B Whitehaven Mansions")
    add_subscriber(cursor, "Rocky Balboa", "1818 Tusculum Street")

    # Add initial subscriptions
    add_subscription(cursor, 1, 1, "2026-04-16")
    add_subscription(cursor, 2, 3, "2025-12-31")
    add_subscription(cursor, 3, 2, "2026-06-18")

def print_query_results(cursor, query, params=(), title="Results"):
    """
    Print the results of a database query.
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()
    print(title + ":")
    for row in rows:
        print(row)
    print("-" * 40)

# Main execution
try:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        conn.execute("PRAGMA foreign_keys = 1");

        create_tables(cursor)
        populate_tables(cursor)

        print_query_results(cursor, "SELECT * FROM subscribers")
        print_query_results(cursor, "SELECT * FROM magazines ORDER BY name")
        print_query_results(cursor, "SELECT m.name FROM magazines m JOIN publishers p ON m.publisher_id = p.id WHERE p.name = ?", ("Shueisha",))

        conn.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}")

