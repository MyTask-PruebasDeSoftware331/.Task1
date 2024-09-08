import os
import sqlite3
from config import DATABASE_NAME

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_migrations_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Migrations table initialized.")

def get_applied_migrations():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name FROM migrations')
    applied = [row['name'] for row in cur.fetchall()]
    conn.close()
    return applied

def apply_migration(migration_file):
    conn = get_db_connection()
    cur = conn.cursor()
    
    with open(os.path.join('migrations', migration_file), 'r') as f:
        sql = f.read()
    
    print(f"Executing SQL:\n{sql}")
    cur.executescript(sql)
    cur.execute('INSERT INTO migrations (name) VALUES (?)', (migration_file,))
    
    conn.commit()
    conn.close()

def ensure_migrations_directory():
    if not os.path.exists('migrations'):
        os.makedirs('migrations')
        print("Migrations directory created.")
    else:
        print("Migrations directory already exists.")

def run_migrations():
    ensure_migrations_directory()
    init_migrations_table()
    applied_migrations = get_applied_migrations()
    
    migration_files = sorted([f for f in os.listdir('migrations') if f.endswith('.sql')])
    
    for migration_file in migration_files:
        if migration_file not in applied_migrations:
            print(f"Applying migration: {migration_file}")
            apply_migration(migration_file)
            print(f"Migration applied: {migration_file}")
        else:
            print(f"Skipping already applied migration: {migration_file}")

    print("All migrations completed.")

if __name__ == "__main__":
    run_migrations()