import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
from database import create_database

DB_FILE = "students.db"
current_user = None


def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        if 'root' in globals():
            messagebox.showerror("Database Error", str(e), parent=root)
        else:
            print("Database Error:", e)
        return False


def fetch_all(query, params=()):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        if 'root' in globals():
            messagebox.showerror("Database Error", str(e), parent=root)
        else:
            print("Database Error:", e)
        return []


def fetch_one(query, params=()):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return row
    except sqlite3.Error as e:
        if 'root' in globals():
            messagebox.showerror("Database Error", str(e), parent=root)
        else:
            print("Database Error:", e)
        return None


def show_text_window(title, text_content):
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry("700x500")
    window.transient(root)
    window.lift()
    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))

    text_area = scrolledtext.ScrolledText(window, width=90, height=30)
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    text_area.insert(tk.END, text_content)
    text_area.configure(state="disabled")


def safe_call(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}", parent=root)
    return wrapper


def verify_login(username, password):
    """Verify user credentials against the database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(f"Login error: {e}")
        return None


def show_login_window():
    """Display login dialog and return True if login successful"""
    global current_user, root
    
    login_window = tk.Tk()
    login_window.title("Login - Student Management System")
    login_window.geometry("400x200")
    login_window.resizable(False, False)
    login_window.attributes("-topmost", True)
    
    # Center on screen
    login_window.update_idletasks()
    width = login_window.winfo_width()
    height = login_window.winfo_height()
    x = (login_window.winfo_screenwidth() // 2) - (width // 2)
    y = (login_window.winfo_screenheight() // 2) - (height // 2)
    login_window.geometry(f"+{x}+{y}")
    
    tk.Label(login_window, text="Student Management System", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(login_window, text="Login Required", font=("Arial", 12)).pack()
    
    tk.Label(login_window, text="Username:").pack(anchor="w", padx=20, pady=(10, 0))
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(padx=20, pady=5)
    username_entry.focus()
    
    tk.Label(login_window, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(padx=20, pady=5)
    
    def login_attempt():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.", parent=login_window)
            return
        
        user = verify_login(username, password)
        if user:
            current_user = user
            login_window.destroy()
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=login_window)
    
    def on_closing():
        login_window.destroy()
        import sys
        sys.exit()
    
    button_frame = tk.Frame(login_window)
    button_frame.pack(pady=15)
    
    tk.Button(button_frame, text="Login", width=10, command=login_attempt).pack(side="left", padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=on_closing).pack(side="left", padx=5)
    
    tk.Label(login_window, text="Demo: admin/admin123 or user/user123", font=("Arial", 8, "italic"), fg="gray").pack(side="bottom", pady=5)
    
    login_window.protocol("WM_DELETE_WINDOW", on_closing)
    login_window.mainloop()


def add_student():
    student_id = simpledialog.askstring("Add Student", "Student ID:", parent=root)
    if not student_id:
        return

    name = simpledialog.askstring("Add Student", "Student Name:", parent=root)
    if not name:
        return

    age = simpledialog.askinteger("Add Student", "Student Age:", parent=root)
    if age is None:
        return

    email = simpledialog.askstring("Add Student", "Student Email:", parent=root)
    if email is None:
        return

    phone = simpledialog.askstring("Add Student", "Student Phone:", parent=root)
    if phone is None:
        phone = ""

    try:
        execute_query(
            "INSERT INTO students(student_id, name, age, email, phone) VALUES (?, ?, ?, ?, ?)",
            (student_id, name, age, email, phone)
        )
        messagebox.showinfo("Success", "Student added successfully.", parent=root)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Student ID already exists or email is already used.", parent=root)


def view_students():
    rows = fetch_all("SELECT student_id, name, age, email, phone FROM students")
    if not rows:
        show_text_window("View Students", "No students found.")
        return

    text = "ID\tName\tAge\tEmail\tPhone\n"
    text += "-" * 80 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"

    show_text_window("View Students", text)


def search_student():
    student_id = simpledialog.askstring("Search Student", "Student ID:", parent=root)
    if not student_id:
        return

    row = fetch_one("SELECT student_id, name, age, email, phone FROM students WHERE student_id = ?", (student_id,))
    if row:
        messagebox.showinfo("Student Found", f"ID: {row[0]}\nName: {row[1]}\nAge: {row[2]}\nEmail: {row[3]}\nPhone: {row[4]}", parent=root)
    else:
        messagebox.showinfo("Not Found", "No student found with that ID.", parent=root)


def update_student():
    student_id = simpledialog.askstring("Update Student", "Student ID:", parent=root)
    if not student_id:
        return

    row = fetch_one("SELECT student_id, name, age, email, phone FROM students WHERE student_id = ?", (student_id,))
    if not row:
        messagebox.showerror("Error", "Student not found.", parent=root)
        return

    name = simpledialog.askstring("Update Student", "Student Name:", initialvalue=row[1], parent=root)
    if not name:
        return

    age = simpledialog.askinteger("Update Student", "Student Age:", initialvalue=row[2], parent=root)
    if age is None:
        return

    email = simpledialog.askstring("Update Student", "Student Email:", initialvalue=row[3], parent=root)
    if email is None:
        return

    phone = simpledialog.askstring("Update Student", "Student Phone:", initialvalue=row[4], parent=root)
    if phone is None:
        phone = ""

    execute_query(
        "UPDATE students SET name = ?, age = ?, email = ?, phone = ? WHERE student_id = ?",
        (name, age, email, phone, student_id)
    )
    messagebox.showinfo("Success", "Student updated successfully.", parent=root)


def delete_student():
    student_id = simpledialog.askstring("Delete Student", "Student ID:", parent=root)
    if not student_id:
        return

    execute_query("DELETE FROM students WHERE student_id = ?", (student_id,))
    messagebox.showinfo("Success", "Student deleted if it existed.", parent=root)


def add_course():
    course_name = simpledialog.askstring("Add Course", "Course Name:", parent=root)
    if not course_name:
        return

    description = simpledialog.askstring("Add Course", "Description:", parent=root)
    if description is None:
        description = ""

    duration = simpledialog.askstring("Add Course", "Duration:", parent=root)
    if duration is None:
        duration = ""

    execute_query(
        "INSERT INTO courses (course_name, description, duration) VALUES (?, ?, ?)",
        (course_name, description, duration)
    )
    messagebox.showinfo("Success", "Course added successfully.", parent=root)


def view_courses():
    rows = fetch_all("SELECT course_id, course_name, description, duration FROM courses")
    if not rows:
        show_text_window("View Courses", "No courses found.")
        return

    text = "ID\tCourse Name\tDescription\tDuration\n"
    text += "-" * 80 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\n"

    show_text_window("View Courses", text)


def search_course():
    course_id = simpledialog.askinteger("Search Course", "Course ID:", parent=root)
    if course_id is None:
        return

    row = fetch_one("SELECT course_id, course_name, description, duration FROM courses WHERE course_id = ?", (course_id,))
    if row:
        messagebox.showinfo("Course Found", f"ID: {row[0]}\nName: {row[1]}\nDescription: {row[2]}\nDuration: {row[3]}", parent=root)
    else:
        messagebox.showinfo("Not Found", "No course found with that ID.", parent=root)


def update_course():
    course_id = simpledialog.askinteger("Update Course", "Course ID:", parent=root)
    if course_id is None:
        return

    row = fetch_one("SELECT course_name, description, duration FROM courses WHERE course_id = ?", (course_id,))
    if not row:
        messagebox.showerror("Error", "Course not found.", parent=root)
        return

    course_name = simpledialog.askstring("Update Course", "Course Name:", initialvalue=row[0], parent=root)
    if not course_name:
        return

    description = simpledialog.askstring("Update Course", "Description:", initialvalue=row[1], parent=root)
    if description is None:
        description = ""

    duration = simpledialog.askstring("Update Course", "Duration:", initialvalue=row[2], parent=root)
    if duration is None:
        duration = ""

    execute_query(
        "UPDATE courses SET course_name = ?, description = ?, duration = ? WHERE course_id = ?",
        (course_name, description, duration, course_id)
    )
    messagebox.showinfo("Success", "Course updated successfully.", parent=root)


def delete_course():
    course_id = simpledialog.askinteger("Delete Course", "Course ID:", parent=root)
    if course_id is None:
        return

    execute_query("DELETE FROM courses WHERE course_id = ?", (course_id,))
    messagebox.showinfo("Success", "Course deleted if it existed.", parent=root)


def assign_student_to_course():
    student_id = simpledialog.askstring("Assign Enrollment", "Student ID:", parent=root)
    if not student_id:
        return

    course_id = simpledialog.askinteger("Assign Enrollment", "Course ID:", parent=root)
    if course_id is None:
        return

    enrollment_date = simpledialog.askstring("Assign Enrollment", "Enrollment Date (YYYY-MM-DD):", parent=root)
    if enrollment_date is None:
        return

    execute_query(
        "INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES (?, ?, ?)",
        (student_id, course_id, enrollment_date)
    )
    messagebox.showinfo("Success", "Enrollment added successfully.", parent=root)


def view_enrollments():
    rows = fetch_all(
        "SELECT enrollments.enrollment_id, students.student_id, students.name, courses.course_name, enrollments.enrollment_date "
        "FROM enrollments "
        "JOIN students ON enrollments.student_id = students.student_id "
        "JOIN courses ON enrollments.course_id = courses.course_id"
    )
    if not rows:
        show_text_window("View Enrollments", "No enrollments found.")
        return

    text = "Enroll ID\tStudent ID\tName\tCourse\tDate\n"
    text += "-" * 100 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"

    show_text_window("View Enrollments", text)


def view_students_by_course():
    course_id = simpledialog.askinteger("Students by Course", "Course ID:", parent=root)
    if course_id is None:
        return

    rows = fetch_all(
        "SELECT students.student_id, students.name, courses.course_name "
        "FROM enrollments "
        "JOIN students ON enrollments.student_id = students.student_id "
        "JOIN courses ON enrollments.course_id = courses.course_id "
        "WHERE courses.course_id = ?",
        (course_id,)
    )
    if not rows:
        show_text_window("Students by Course", "No students found for that course.")
        return

    text = "Student ID\tName\tCourse\n"
    text += "-" * 80 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\n"

    show_text_window("Students by Course", text)


def view_courses_by_student():
    student_id = simpledialog.askstring("Courses by Student", "Student ID:", parent=root)
    if not student_id:
        return

    rows = fetch_all(
        "SELECT students.name, courses.course_name "
        "FROM enrollments "
        "JOIN students ON enrollments.student_id = students.student_id "
        "JOIN courses ON enrollments.course_id = courses.course_id "
        "WHERE students.student_id = ?",
        (student_id,)
    )
    if not rows:
        show_text_window("Courses by Student", "No courses found for that student.")
        return

    text = "Student Name\tCourse\n"
    text += "-" * 80 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\n"

    show_text_window("Courses by Student", text)


def remove_enrollment():
    enrollment_id = simpledialog.askinteger("Remove Enrollment", "Enrollment ID:", parent=root)
    if enrollment_id is None:
        return

    execute_query("DELETE FROM enrollments WHERE enrollment_id = ?", (enrollment_id,))
    messagebox.showinfo("Success", "Enrollment removed if it existed.", parent=root)


def record_attendance():
    student_id = simpledialog.askstring("Record Attendance", "Student ID:", parent=root)
    if not student_id:
        return

    course_id = simpledialog.askinteger("Record Attendance", "Course ID:", parent=root)
    if course_id is None:
        return

    attendance_date = simpledialog.askstring("Record Attendance", "Attendance Date (YYYY-MM-DD):", parent=root)
    if attendance_date is None:
        return

    status = simpledialog.askstring("Record Attendance", "Status (Present/Absent):", parent=root)
    if status is None:
        return
    status = status.title()
    if status not in ("Present", "Absent"):
        messagebox.showerror("Error", "Status must be Present or Absent.", parent=root)
        return

    execute_query(
        "INSERT INTO attendance (student_id, course_id, attendance_date, status) VALUES (?, ?, ?, ?)",
        (student_id, course_id, attendance_date, status)
    )
    messagebox.showinfo("Success", "Attendance recorded successfully.", parent=root)


def view_attendance():
    rows = fetch_all(
        "SELECT attendance.attendance_id, students.student_id, students.name, courses.course_name, attendance.attendance_date, attendance.status "
        "FROM attendance "
        "JOIN students ON attendance.student_id = students.student_id "
        "JOIN courses ON attendance.course_id = courses.course_id"
    )
    if not rows:
        show_text_window("View Attendance", "No attendance records found.")
        return

    text = "Attend ID\tStudent ID\tName\tCourse\tDate\tStatus\n"
    text += "-" * 120 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\n"

    show_text_window("View Attendance", text)


def search_attendance():
    student_id = simpledialog.askstring("Search Attendance", "Student ID:", parent=root)
    if not student_id:
        return

    rows = fetch_all(
        "SELECT attendance.attendance_id, students.name, courses.course_name, attendance.attendance_date, attendance.status "
        "FROM attendance "
        "JOIN students ON attendance.student_id = students.student_id "
        "JOIN courses ON attendance.course_id = courses.course_id "
        "WHERE attendance.student_id = ?",
        (student_id,)
    )
    if not rows:
        show_text_window("Search Attendance", "No attendance records found for that student.")
        return

    text = "Attend ID\tName\tCourse\tDate\tStatus\n"
    text += "-" * 120 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"

    show_text_window("Search Attendance", text)


def update_attendance():
    attendance_id = simpledialog.askinteger("Update Attendance", "Attendance ID:", parent=root)
    if attendance_id is None:
        return

    status = simpledialog.askstring("Update Attendance", "New Status (Present/Absent):", parent=root)
    if status is None:
        return
    status = status.title()
    if status not in ("Present", "Absent"):
        messagebox.showerror("Error", "Status must be Present or Absent.", parent=root)
        return

    execute_query("UPDATE attendance SET status = ? WHERE attendance_id = ?", (status, attendance_id))
    messagebox.showinfo("Success", "Attendance updated successfully.", parent=root)


def delete_attendance():
    attendance_id = simpledialog.askinteger("Delete Attendance", "Attendance ID:", parent=root)
    if attendance_id is None:
        return

    execute_query("DELETE FROM attendance WHERE attendance_id = ?", (attendance_id,))
    messagebox.showinfo("Success", "Attendance deleted if it existed.", parent=root)


def generate_reports():
    total_students = fetch_one("SELECT COUNT(*) FROM students")[0]
    total_courses = fetch_one("SELECT COUNT(*) FROM courses")[0]
    total_enrollments = fetch_one("SELECT COUNT(*) FROM enrollments")[0]

    students_per_course = fetch_all(
        "SELECT courses.course_name, COUNT(enrollments.student_id) "
        "FROM courses "
        "LEFT JOIN enrollments ON courses.course_id = enrollments.course_id "
        "GROUP BY courses.course_name"
    )

    attendance_records = fetch_all(
        "SELECT students.name, courses.course_name, attendance.attendance_date, attendance.status "
        "FROM attendance "
        "JOIN students ON attendance.student_id = students.student_id "
        "JOIN courses ON attendance.course_id = courses.course_id"
    )

    text = f"Total Students: {total_students}\n"
    text += f"Total Courses: {total_courses}\n"
    text += f"Total Enrollments: {total_enrollments}\n\n"
    text += "Students per Course:\n"
    for row in students_per_course:
        text += f"{row[0]}: {row[1]}\n"
    text += "\nAttendance Records:\n"
    if attendance_records:
        for row in attendance_records:
            text += f"{row[0]} - {row[1]} - {row[2]} - {row[3]}\n"
    else:
        text += "No attendance records found.\n"

    show_text_window("Reports", text)


create_database()

# Show login window first
show_login_window()

root = tk.Tk()
root.title("Student Management System")
root.geometry("700x650")
root.resizable(False, False)

# Add logged-in user info at the top
info_frame = tk.Frame(root)
info_frame.pack(fill="x", padx=10, pady=5)
tk.Label(info_frame, text=f"Logged in as: {current_user[1]} ({current_user[2]})", font=("Arial", 10, "italic")).pack(anchor="e")

title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)


# ---------------- Student ----------------

tk.Label(root, text="Student Management", font=("Arial", 14, "bold")).pack()

# student buttons
tk.Button(root, text="Add Student", width=30, command=safe_call(add_student)).pack(pady=2)
tk.Button(root, text="View Students", width=30, command=safe_call(view_students)).pack(pady=2)
tk.Button(root, text="Search Student", width=30, command=safe_call(search_student)).pack(pady=2)
tk.Button(root, text="Update Student", width=30, command=safe_call(update_student)).pack(pady=2)
tk.Button(root, text="Delete Student", width=30, command=safe_call(delete_student)).pack(pady=2)
# wrap callbacks with safe_call to show errors
# temporary duplicate removed


# ---------------- Courses ----------------

tk.Label(root, text="Course Management", font=("Arial", 14, "bold")).pack(pady=10)

# course buttons
tk.Button(root, text="Add Course", width=30, command=safe_call(add_course)).pack(pady=2)
tk.Button(root, text="View Courses", width=30, command=safe_call(view_courses)).pack(pady=2)
tk.Button(root, text="Search Course", width=30, command=safe_call(search_course)).pack(pady=2)
tk.Button(root, text="Update Course", width=30, command=safe_call(update_course)).pack(pady=2)
tk.Button(root, text="Delete Course", width=30, command=safe_call(delete_course)).pack(pady=2)


# ---------------- Enrollment ----------------

tk.Label(root, text="Enrollment", font=("Arial", 14, "bold")).pack(pady=10)

# enrollment buttons
tk.Button(root, text="Assign Student to Course", width=30, command=safe_call(assign_student_to_course)).pack(pady=2)
tk.Button(root, text="View Enrollments", width=30, command=safe_call(view_enrollments)).pack(pady=2)
tk.Button(root, text="View Students by Course", width=30, command=safe_call(view_students_by_course)).pack(pady=2)
tk.Button(root, text="View Courses by Student", width=30, command=safe_call(view_courses_by_student)).pack(pady=2)
tk.Button(root, text="Remove Enrollment", width=30, command=safe_call(remove_enrollment)).pack(pady=2)


# ---------------- Attendance ----------------

tk.Label(root, text="Attendance", font=("Arial", 14, "bold")).pack(pady=10)

# attendance buttons
tk.Button(root, text="Record Attendance", width=30, command=safe_call(record_attendance)).pack(pady=2)
tk.Button(root, text="View Attendance", width=30, command=safe_call(view_attendance)).pack(pady=2)
tk.Button(root, text="Search Attendance", width=30, command=safe_call(search_attendance)).pack(pady=2)
tk.Button(root, text="Update Attendance", width=30, command=safe_call(update_attendance)).pack(pady=2)
tk.Button(root, text="Delete Attendance", width=30, command=safe_call(delete_attendance)).pack(pady=2)


# ---------------- Reports ----------------

tk.Label(root, text="Reports", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Generate Reports", width=30, command=safe_call(generate_reports)).pack(pady=2)


tk.Button(
    root,
    text="Exit",
    width=30,
    bg="red",
    fg="white",
    command=root.destroy
).pack(pady=20)

root.mainloop()