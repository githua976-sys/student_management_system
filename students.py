import sqlite3


# Add Student
def add_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    email = input("Enter Email: ")

    try:
        cursor.execute("""
        INSERT INTO students (student_id, name, age, email)
        VALUES (?, ?, ?, ?)
        """, (student_id, name, age, email))

        conn.commit()
        print("Student added successfully!")

    except sqlite3.IntegrityError:
        print("Student ID already exists!")

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
def search_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found:")
        print(student)
    else:
        print("Student not found!")

    conn.close()


# Update Student
def update_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    name = input("Enter New Name: ")
    age = int(input("Enter New Age: "))
    email = input("Enter New Email: ")

    cursor.execute("""
    UPDATE students
    SET name=?, age=?, email=?
    WHERE student_id=?
    """, (name, age, email, student_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully!")
    else:
        print("Student not found!")

    conn.close()


# Delete Student
def delete_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")
    else:
        print("Student not found!")

    conn.close()