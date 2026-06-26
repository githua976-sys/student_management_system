import sqlite3


# Assign Student to Course
def assign_student_to_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")
    course_id = input("Enter Course ID: ")
    enrollment_date = input("Enter Enrollment Date (YYYY-MM-DD): ")

    try:
        cursor.execute("""
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (?, ?, ?)
        """, (student_id, course_id, enrollment_date))

        conn.commit()
        print("Student assigned to course successfully!")

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()


# View All Enrollments
def view_enrollments():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT enrollments.enrollment_id,
           students.student_id,
           students.name,
           courses.course_name,
           enrollments.enrollment_date
    FROM enrollments
    JOIN students
        ON enrollments.student_id = students.student_id
    JOIN courses
        ON enrollments.course_id = courses.course_id
    """)

    records = cursor.fetchall()

    print("\n===== ENROLLMENTS =====")

    if records:
        for record in records:
            print(record)
    else:
        print("No enrollments found.")

    conn.close()


# View Students by Course
def view_students_by_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    course_id = input("Enter Course ID: ")

    cursor.execute("""
    SELECT students.student_id,
           students.name,
           courses.course_name
    FROM enrollments
    JOIN students
        ON enrollments.student_id = students.student_id
    JOIN courses
        ON enrollments.course_id = courses.course_id
    WHERE courses.course_id = ?
    """, (course_id,))

    students = cursor.fetchall()

    print("\n===== STUDENTS IN COURSE =====")

    if students:
        for student in students:
            print(student)
    else:
        print("No students enrolled in this course.")

    conn.close()


# View Courses by Student
def view_courses_by_student():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute("""
    SELECT students.name,
           courses.course_name
    FROM enrollments
    JOIN students
        ON enrollments.student_id = students.student_id
    JOIN courses
        ON enrollments.course_id = courses.course_id
    WHERE students.student_id = ?
    """, (student_id,))

    courses = cursor.fetchall()

    print("\n===== STUDENT COURSES =====")

    if courses:
        for course in courses:
            print(course)
    else:
        print("Student is not enrolled in any course.")

    conn.close()


# Remove Student from Course
def remove_enrollment():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    enrollment_id = input("Enter Enrollment ID: ")

    cursor.execute("""
    DELETE FROM enrollments
    WHERE enrollment_id = ?
    """, (enrollment_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Enrollment removed successfully!")
    else:
        print("Enrollment not found.")

    conn.close()