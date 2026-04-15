import sqlite3
from security import hash_password, check_password

# INIT DB
def init_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


# ➕ CREATE USER
def create_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed = hash_password(password)

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# 🔍 GET USER
def get_user(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    conn.close()
    return user