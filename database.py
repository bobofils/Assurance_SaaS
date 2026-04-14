import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

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


def save_client(age, revenu, couverture, risque, prime):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO clients (age, revenu, couverture, risque, prime, date)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (age, revenu, couverture, risque, prime))

    conn.commit()
    conn.close()


def get_clients():
    conn = sqlite3.connect("users.db")
    data = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()
    return data