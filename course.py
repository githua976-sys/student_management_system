import sqlite3


# Add Course
def add_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    course_name = input("Enter Course Name: ")
    description = input("Enter Course Description: ")

    cursor.execute("""
    INSERT INTO courses (course_name, description)
    VALUES (?, ?)
    """, (course_name, description))

    conn.commit()
    conn.close()

    print("Course added successfully!")


# View Courses
def view_courses():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    print("\n===== COURSES =====")

    for course in courses:
        print(course)

    conn.close()


# Search Course
def search_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    course_id = input("Enter Course ID: ")

    cursor.execute(
        "SELECT * FROM courses WHERE course_id = ?",
        (course_id,)
    )

    course = cursor.fetchone()

    if course:
        print("\nCourse Found:")
        print(course)
    else:
        print("Course not found!")

    conn.close()


# Update Course
def update_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    course_id = input("Enter Course ID: ")

    course_name = input("Enter New Course Name: ")
    description = input("Enter New Description: ")

    cursor.execute("""
    UPDATE courses
    SET course_name=?, description=?
    WHERE course_id=?
    """, (course_name, description, course_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("Course updated successfully!")
    else:
        print("Course not found!")

    conn.close()


# Delete Course
def delete_course():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    course_id = input("Enter Course ID: ")

    cursor.execute(
        "DELETE FROM courses WHERE course_id=?",
        (course_id,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Course deleted successfully!")
    else:
        print("Course not found!")

    conn.close()