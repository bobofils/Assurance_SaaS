import sqlite3
from datetime import datetime
from security import hash_password

DB_NAME = "users.db"

# =========================
# INIT DATABASE
# =========================
def init_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

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
# CREATE USER (SAFE)
# =========================
def create_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        hashed = hash_password(password)

        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# =========================
# GET USER
# =========================
def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    conn.close()
    return user


# =========================
# SAVE CLIENT
# =========================
def save_client(age, revenu, couverture, risque, prime):
    conn = sqlite3.connect(DB_NAME)
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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM clients ORDER BY id DESC")
    data = c.fetchall()

    conn.close()
    return data