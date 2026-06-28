import sqlite3

def add_student(student_id, name, age, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO students(student_id, name, age, email)
        VALUES(?,?,?,?)
        """, (student_id, name, age, email))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# View Students
def view_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n===== STUDENTS =====")

    for student in students:
        print(student)

    conn.close()


# Search Student
def search_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    return student


# Update Student
def update_student(student_id, name, age, email):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET name=?, age=?, email=?
    WHERE student_id=?
    """, (name, age, email, student_id))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated > 0

# Delete Student
def delete_student(student_id):
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()

    deleted = cursor.rowcount

    conn.close()

    return deleted > 0