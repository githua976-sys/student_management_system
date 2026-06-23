import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
    """)

    # Courses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()