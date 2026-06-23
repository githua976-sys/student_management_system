import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")