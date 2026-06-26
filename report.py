import sqlite3


# Total Students
def total_students():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    print("\n===== TOTAL STUDENTS =====")
    print(f"Total Students: {total}")

    conn.close()


# Total Courses
def total_courses():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM courses")
    total = cursor.fetchone()[0]

    print("\n===== TOTAL COURSES =====")
    print(f"Total Courses: {total}")

    conn.close()


# Total Enrollments
def total_enrollments():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM enrollments")
    total = cursor.fetchone()[0]

    print("\n===== TOTAL ENROLLMENTS =====")
    print(f"Total Enrollments: {total}")

    conn.close()


# Students Per Course
def students_per_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT courses.course_name,
           COUNT(enrollments.student_id)
    FROM courses
    LEFT JOIN enrollments
        ON courses.course_id = enrollments.course_id
    GROUP BY courses.course_name
    """)

    results = cursor.fetchall()

    print("\n===== STUDENTS PER COURSE =====")

    if results:
        for course in results:
            print(f"{course[0]} : {course[1]} Student(s)")
    else:
        print("No data available.")

    conn.close()


# Attendance Report
def attendance_report():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.name,
           courses.course_name,
           attendance.attendance_date,
           attendance.status
    FROM attendance
    JOIN students
        ON attendance.student_id = students.student_id
    JOIN courses
        ON attendance.course_id = courses.course_id
    """)

    records = cursor.fetchall()

    print("\n===== ATTENDANCE REPORT =====")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found.")

    conn.close()


# Complete Report
def generate_reports():
    print("\n===================================")
    print("      STUDENT MANAGEMENT REPORT")
    print("===================================")

    total_students()
    total_courses()
    total_enrollments()
    students_per_course()
    attendance_report()