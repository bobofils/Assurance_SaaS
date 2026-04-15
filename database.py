import sqlite3
from datetime import datetime

# =========================
# INIT DB USERS + CLIENTS
# =========================
def init_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # CLIENTS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        revenu REAL,
        couverture REAL,
        risque REAL,
        prime REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# SAVE CLIENT
# =========================
def save_client(age, revenu, couverture, risque, prime):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO clients (age, revenu, couverture, risque, prime, date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (age, revenu, couverture, risque, prime, datetime.now()))

    conn.commit()
    conn.close()


# =========================
# GET CLIENTS
# =========================
def get_clients():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM clients")
    data = c.fetchall()

    conn.close()
    return data