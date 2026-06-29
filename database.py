import sqlite3


def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        description TEXT,
        duration TEXT,
        adoration TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        course_id INTEGER NOT NULL,
        enrollment_date TEXT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        course_id INTEGER NOT NULL,
        attendance_date TEXT,
        status TEXT CHECK(status IN ('Present', 'Absent')),
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)

    # Create default users if they don't exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("admin", "admin123", "admin"))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ("user", "user123", "user"))

    conn.commit()
    conn.close()

    print("Database and tables created successfully!")


def ensure_column(table, column, col_def):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cur.fetchall()]
    if column not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_def}")
        print(f"Added column {column} to {table}")
    conn.commit()
    conn.close()


def migrate_add_columns():
    ensure_column("students", "phone", "TEXT")
    ensure_column("courses", "adoration", "TEXT")
    ensure_column("courses", "duration", "TEXT")


if __name__ == "__main__":
    create_database()
    migrate_add_columns()