# database.py

import sqlite3
import os
from config import DATABASE_NAME

def get_db_connection():
    db_path = os.path.abspath(DATABASE_NAME)
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    print("Database initialized.")
    conn.close()