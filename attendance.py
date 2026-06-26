import sqlite3


# Record Attendance
def record_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")
    course_id = input("Enter Course ID: ")
    attendance_date = input("Enter Attendance Date (YYYY-MM-DD): ")
    status = input("Enter Status (Present/Absent): ")

    try:
        cursor.execute("""
        INSERT INTO attendance (student_id, course_id, attendance_date, status)
        VALUES (?, ?, ?, ?)
        """, (student_id, course_id, attendance_date, status))

        conn.commit()
        print("Attendance recorded successfully!")

    except sqlite3.Error as e:
        print("Error:", e)

    conn.close()


# View Attendance Records
def view_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT attendance.attendance_id,
           students.student_id,
           students.name,
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

    print("\n===== ATTENDANCE RECORDS =====")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found.")

    conn.close()


# Search Attendance by Student
def search_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    student_id = input("Enter Student ID: ")

    cursor.execute("""
    SELECT attendance.attendance_id,
           students.name,
           courses.course_name,
           attendance.attendance_date,
           attendance.status
    FROM attendance
    JOIN students
        ON attendance.student_id = students.student_id
    JOIN courses
        ON attendance.course_id = courses.course_id
    WHERE attendance.student_id = ?
    """, (student_id,))

    records = cursor.fetchall()

    print("\n===== ATTENDANCE DETAILS =====")

    if records:
        for record in records:
            print(record)
    else:
        print("No attendance records found.")

    conn.close()


# Update Attendance
def update_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    attendance_id = input("Enter Attendance ID: ")
    status = input("Enter New Status (Present/Absent): ")

    cursor.execute("""
    UPDATE attendance
    SET status = ?
    WHERE attendance_id = ?
    """, (status, attendance_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Attendance updated successfully!")
    else:
        print("Attendance record not found.")

    conn.close()


# Delete Attendance
def delete_attendance():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    attendance_id = input("Enter Attendance ID: ")

    cursor.execute("""
    DELETE FROM attendance
    WHERE attendance_id = ?
    """, (attendance_id,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Attendance deleted successfully!")
    else:
        print("Attendance record not found.")

    conn.close()