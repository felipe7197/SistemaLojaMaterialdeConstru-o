import sqlite3
import os
import sys


def get_base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "tbs.db")
BILL_PATH = os.path.join(BASE_DIR, "bill")

os.makedirs(BILL_PATH, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS supplier(
            invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            supdate TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Supplier TEXT,
            itemname TEXT,
            hsncode TEXT,
            price TEXT,
            qty TEXT,
            discount TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_no TEXT,
            pid INTEGER,
            itemname TEXT,
            hsncode TEXT,
            qty INTEGER,
            unit_price REAL,
            discount REAL,
            total REAL,
            customer_name TEXT,
            customer_contact TEXT,
            sale_date TEXT
        )
    """)

    con.commit()
    con.close()