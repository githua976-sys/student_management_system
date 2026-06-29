import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, ttk
from database import create_database, migrate_add_columns

DB_FILE = "students.db"
root = None
current_role = None
pages = {}


def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        if root is not None:
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
        if root is not None:
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
        if root is not None:
            messagebox.showerror("Database Error", str(e), parent=root)
        else:
            print("Database Error:", e)
        return None


def show_text_window(title, text_content):
    window = tk.Toplevel(root)
    window.title(title)
    window.geometry("780x520")
    window.transient(root)
    window.lift()
    window.attributes("-topmost", True)
    window.after(100, lambda: window.attributes("-topmost", False))

    text_area = scrolledtext.ScrolledText(window, width=95, height=32, wrap=tk.NONE)
    text_area.pack(fill="both", expand=True, padx=12, pady=12)
    text_area.insert(tk.END, text_content)
    text_area.configure(state="disabled")


def safe_call(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if root is not None:
                messagebox.showerror("Error", f"An error occurred:\n{e}", parent=root)
            else:
                print("Error:", e)
    return wrapper


def require_permission(action):
    if current_role == "admin":
        return True

    allowed_for_user = {
        "view students",
        "view courses",
        "view enrollments",
        "record attendance",
        "view attendance",
        "search attendance",
        "generate reports",
        "search students",
        "search courses",
        "view students by course",
        "view courses by student",
    }

    if action in allowed_for_user:
        return True

    messagebox.showwarning("Access denied", f"Only the admin can {action}.", parent=root)
    return False


def add_student():
    if not require_permission("add students"):
        return

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

    execute_query(
        "INSERT INTO students(student_id, name, age, email, phone) VALUES (?, ?, ?, ?, ?)",
        (student_id, name, age, email, phone),
    )
    messagebox.showinfo("Success", "Student added successfully.", parent=root)


def view_students():
    if not require_permission("view students"):
        return

    rows = fetch_all("SELECT student_id, name, age, email, phone FROM students")
    if not rows:
        show_text_window("View Students", "No students found.")
        return

    text = "ID\tName\tAge\tEmail\tPhone\n"
    text += "-" * 100 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"

    show_text_window("View Students", text)


def search_student():
    if not require_permission("search students"):
        return

    student_id = simpledialog.askstring("Search Student", "Student ID:", parent=root)
    if not student_id:
        return

    row = fetch_one("SELECT student_id, name, age, email, phone FROM students WHERE student_id = ?", (student_id,))
    if row:
        messagebox.showinfo(
            "Student Found",
            f"ID: {row[0]}\nName: {row[1]}\nAge: {row[2]}\nEmail: {row[3]}\nPhone: {row[4]}",
            parent=root,
        )
    else:
        messagebox.showinfo("Not Found", "No student found with that ID.", parent=root)


def update_student():
    if not require_permission("update students"):
        return

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
        (name, age, email, phone, student_id),
    )
    messagebox.showinfo("Success", "Student updated successfully.", parent=root)


def delete_student():
    if not require_permission("delete students"):
        return

    student_id = simpledialog.askstring("Delete Student", "Student ID:", parent=root)
    if not student_id:
        return

    execute_query("DELETE FROM students WHERE student_id = ?", (student_id,))
    messagebox.showinfo("Success", "Student deleted if it existed.", parent=root)


def add_course():
    if not require_permission("manage courses"):
        return

    course_name = simpledialog.askstring("Add Course", "Course Name:", parent=root)
    if not course_name:
        return

    description = simpledialog.askstring("Add Course", "Description:", parent=root)
    if description is None:
        description = ""

    duration = simpledialog.askstring("Add Course", "Duration:", parent=root)
    if duration is None:
        duration = ""

    adoration = simpledialog.askstring("Add Course", "Adoration:", parent=root)
    if adoration is None:
        adoration = ""

    execute_query(
        "INSERT INTO courses (course_name, description, duration, adoration) VALUES (?, ?, ?, ?)",
        (course_name, description, duration, adoration),
    )
    messagebox.showinfo("Success", "Course added successfully.", parent=root)


def view_courses():
    if not require_permission("view courses"):
        return

    rows = fetch_all("SELECT course_id, course_name, description, duration, adoration FROM courses")
    if not rows:
        show_text_window("View Courses", "No courses found.")
        return

    text = "ID\tCourse Name\tDescription\tDuration\tAdoration\n"
    text += "-" * 120 + "\n"
    for row in rows:
        text += f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n"

    show_text_window("View Courses", text)


def search_course():
    if not require_permission("search courses"):
        return

    course_id = simpledialog.askinteger("Search Course", "Course ID:", parent=root)
    if course_id is None:
        return

    row = fetch_one("SELECT course_id, course_name, description, duration, adoration FROM courses WHERE course_id = ?", (course_id,))
    if row:
        messagebox.showinfo(
            "Course Found",
            f"ID: {row[0]}\nName: {row[1]}\nDescription: {row[2]}\nDuration: {row[3]}\nAdoration: {row[4]}",
            parent=root,
        )
    else:
        messagebox.showinfo("Not Found", "No course found with that ID.", parent=root)


def update_course():
    if not require_permission("manage courses"):
        return

    course_id = simpledialog.askinteger("Update Course", "Course ID:", parent=root)
    if course_id is None:
        return

    row = fetch_one("SELECT course_name, description, duration, adoration FROM courses WHERE course_id = ?", (course_id,))
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

    adoration = simpledialog.askstring("Update Course", "Adoration:", initialvalue=row[3], parent=root)
    if adoration is None:
        adoration = ""

    execute_query(
        "UPDATE courses SET course_name = ?, description = ?, duration = ?, adoration = ? WHERE course_id = ?",
        (course_name, description, duration, adoration, course_id),
    )
    messagebox.showinfo("Success", "Course updated successfully.", parent=root)


def delete_course():
    if not require_permission("manage courses"):
        return

    course_id = simpledialog.askinteger("Delete Course", "Course ID:", parent=root)
    if course_id is None:
        return

    execute_query("DELETE FROM courses WHERE course_id = ?", (course_id,))
    messagebox.showinfo("Success", "Course deleted if it existed.", parent=root)


def assign_student_to_course():
    if not require_permission("enroll students"):
        return

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
        (student_id, course_id, enrollment_date),
    )
    messagebox.showinfo("Success", "Enrollment added successfully.", parent=root)


def view_enrollments():
    if not require_permission("view enrollments"):
        return

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
    if not require_permission("view enrollments"):
        return

    course_id = simpledialog.askinteger("Students by Course", "Course ID:", parent=root)
    if course_id is None:
        return

    rows = fetch_all(
        "SELECT students.student_id, students.name, courses.course_name "
        "FROM enrollments "
        "JOIN students ON enrollments.student_id = students.student_id "
        "JOIN courses ON enrollments.course_id = courses.course_id "
        "WHERE courses.course_id = ?",
        (course_id,),
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
    if not require_permission("view enrollments"):
        return

    student_id = simpledialog.askstring("Courses by Student", "Student ID:", parent=root)
    if not student_id:
        return

    rows = fetch_all(
        "SELECT students.name, courses.course_name "
        "FROM enrollments "
        "JOIN students ON enrollments.student_id = students.student_id "
        "JOIN courses ON enrollments.course_id = courses.course_id "
        "WHERE students.student_id = ?",
        (student_id,),
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
    if not require_permission("delete enrollments"):
        return

    enrollment_id = simpledialog.askinteger("Remove Enrollment", "Enrollment ID:", parent=root)
    if enrollment_id is None:
        return

    execute_query("DELETE FROM enrollments WHERE enrollment_id = ?", (enrollment_id,))
    messagebox.showinfo("Success", "Enrollment removed if it existed.", parent=root)


def record_attendance():
    if not require_permission("record attendance"):
        return

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
        (student_id, course_id, attendance_date, status),
    )
    messagebox.showinfo("Success", "Attendance recorded successfully.", parent=root)


def view_attendance():
    if not require_permission("view attendance"):
        return

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
    if not require_permission("view attendance"):
        return

    student_id = simpledialog.askstring("Search Attendance", "Student ID:", parent=root)
    if not student_id:
        return

    rows = fetch_all(
        "SELECT attendance.attendance_id, students.name, courses.course_name, attendance.attendance_date, attendance.status "
        "FROM attendance "
        "JOIN students ON attendance.student_id = students.student_id "
        "JOIN courses ON attendance.course_id = courses.course_id "
        "WHERE attendance.student_id = ?",
        (student_id,),
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
    if not require_permission("manage attendance"):
        return

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
    if not require_permission("manage attendance"):
        return

    attendance_id = simpledialog.askinteger("Delete Attendance", "Attendance ID:", parent=root)
    if attendance_id is None:
        return

    execute_query("DELETE FROM attendance WHERE attendance_id = ?", (attendance_id,))
    messagebox.showinfo("Success", "Attendance deleted if it existed.", parent=root)


def generate_reports():
    if not require_permission("generate reports"):
        return

    total_students = fetch_one("SELECT COUNT(*) FROM students")
    total_students = total_students[0] if total_students else 0
    total_courses = fetch_one("SELECT COUNT(*) FROM courses")
    total_courses = total_courses[0] if total_courses else 0
    total_enrollments = fetch_one("SELECT COUNT(*) FROM enrollments")
    total_enrollments = total_enrollments[0] if total_enrollments else 0

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


def show_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("380x250")
    login_window.resizable(False, False)
    login_window.transient(root)
    login_window.grab_set()

    tk.Label(login_window, text="Student Management Login", font=("Segoe UI", 14, "bold")).pack(pady=(16, 6))
    tk.Label(login_window, text="Enter your credentials to continue.", font=("Segoe UI", 10)).pack()

    tk.Label(login_window, text="Username", anchor="w").pack(fill="x", padx=24, pady=(14, 2))
    username_entry = tk.Entry(login_window)
    username_entry.pack(fill="x", padx=24)

    tk.Label(login_window, text="Password", anchor="w").pack(fill="x", padx=24, pady=(10, 2))
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(fill="x", padx=24)

    def submit_login():
        global current_role
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == "admin" and password == "admin123":
            current_role = "admin"
        elif username == "user" and password == "user123":
            current_role = "user"
        else:
            messagebox.showerror("Login failed", "Invalid username or password.", parent=login_window)
            return

        login_window.destroy()
        build_main_window()

    button_frame = tk.Frame(login_window)
    button_frame.pack(fill="x", pady=16, padx=24)

    tk.Button(button_frame, text="Login", width=12, command=submit_login).pack(side="left")
    tk.Button(button_frame, text="Cancel", width=12, command=root.destroy).pack(side="right")

    tk.Label(login_window, text="Admin: admin/admin123 | User: user/user123", fg="#4b5563", font=("Segoe UI", 8)).pack(pady=(10, 0))
    username_entry.focus()
    login_window.bind("<Return>", lambda event: submit_login())
    root.wait_window(login_window)


def build_main_window():
    global pages
    root.deiconify()
    root.title("Student Management System")
    root.geometry("1160x760")
    root.minsize(1040, 680)
    root.configure(bg="#eff3f7")

    for widget in root.winfo_children():
        widget.destroy()

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Sidebar.TFrame", background="#1f2937")
    style.configure("Sidebar.TButton", background="#374151", foreground="white", padding=10, font=("Segoe UI", 10, "bold"))
    style.map("Sidebar.TButton", background=[("active", "#4b5563"), ("pressed", "#111827")])
    style.configure("Action.TButton", padding=10, font=("Segoe UI", 10, "bold"))

    container = tk.Frame(root, bg="#eff3f7")
    container.pack(fill="both", expand=True)

    sidebar = ttk.Frame(container, style="Sidebar.TFrame", width=260)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = tk.Frame(container, bg="#eff3f7")
    content.pack(side="left", fill="both", expand=True)

    header = tk.Frame(content, bg="#eff3f7", pady=22, padx=22)
    header.pack(fill="x")

    tk.Label(header, text="Student Management System", bg="#eff3f7", fg="#111827", font=("Segoe UI", 24, "bold")).pack(anchor="w")
    tk.Label(header, text="Use the menu to access students, courses, enrollments, attendance, and reports.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 11)).pack(anchor="w", pady=(6, 0))
    tk.Label(header, text=f"Signed in as: {current_role.title()}", bg="#eff3f7", fg="#2563eb", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(6, 0))

    nav_title = tk.Label(sidebar, text="Navigation", bg="#1f2937", fg="white", font=("Segoe UI", 14, "bold"))
    nav_title.pack(anchor="w", padx=18, pady=(18, 12))

    def nav_button(text, page_name):
        button = ttk.Button(sidebar, text=text, style="Sidebar.TButton", command=lambda: show_page(page_name))
        button.pack(fill="x", padx=16, pady=8)
        return button

    nav_button("Dashboard", "dashboard")
    nav_button("Students", "students")
    nav_button("Courses", "courses")
    nav_button("Enrollments", "enrollments")
    nav_button("Reports", "reports")

    tk.Button(sidebar, text="Logout", bg="#ef4444", fg="white", font=("Segoe UI", 10, "bold"), bd=0, command=lambda: logout()).pack(fill="x", padx=16, pady=20, side="bottom")

    page_frame = tk.Frame(content, bg="#eff3f7")
    page_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    pages = {}

    def create_page(name):
        page = tk.Frame(page_frame, bg="#eff3f7")
        page.place(relx=0, rely=0, relwidth=1, relheight=1)
        pages[name] = page
        return page

    def show_page(name):
        if name not in pages:
            return
        for page in pages.values():
            page.lower()
        pages[name].lift()
        if name == "dashboard":
            refresh_dashboard()
        elif name == "students":
            refresh_students_page()
        elif name == "courses":
            refresh_courses_page()
        elif name == "enrollments":
            refresh_enrollments_page()
        elif name == "reports":
            refresh_reports_page()

    def create_action_button(parent, text, command):
        return ttk.Button(parent, text=text, style="Action.TButton", command=safe_call(command))

    def create_info_card(parent, label_text, value_text, accent):
        card = tk.Frame(parent, bg="white", bd=1, relief="solid", padx=16, pady=16)
        tk.Label(card, text=label_text, bg="white", fg="#6b7280", font=("Segoe UI", 10)).pack(anchor="w")
        tk.Label(card, text=value_text, bg="white", fg=accent, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(8, 0))
        card.pack(side="left", expand=True, fill="x", padx=8)
        return card

    def refresh_dashboard():
        student_count = fetch_one("SELECT COUNT(*) FROM students")
        student_count = student_count[0] if student_count else 0
        course_count = fetch_one("SELECT COUNT(*) FROM courses")
        course_count = course_count[0] if course_count else 0
        enrollment_count = fetch_one("SELECT COUNT(*) FROM enrollments")
        enrollment_count = enrollment_count[0] if enrollment_count else 0
        attendance_count = fetch_one("SELECT COUNT(*) FROM attendance")
        attendance_count = attendance_count[0] if attendance_count else 0

        for widget in pages["dashboard"].winfo_children():
            widget.destroy()

        tk.Label(pages["dashboard"], text="Dashboard", bg="#eff3f7", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(14, 10))
        tk.Label(pages["dashboard"], text="Quick summary of the current system state.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w")

        cards = tk.Frame(pages["dashboard"], bg="#eff3f7")
        cards.pack(fill="x", pady=16)
        create_info_card(cards, "Students", str(student_count), "#2563eb")
        create_info_card(cards, "Courses", str(course_count), "#16a34a")
        create_info_card(cards, "Enrollments", str(enrollment_count), "#f59e0b")
        create_info_card(cards, "Attendance", str(attendance_count), "#dc2626")

        summary = tk.Frame(pages["dashboard"], bg="white", bd=1, relief="solid", padx=20, pady=20)
        summary.pack(fill="both", expand=True)
        tk.Label(summary, text="Access Overview", bg="white", fg="#111827", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(
            summary,
            text=(
                "Admin users can manage students, courses, enrollments, attendance, and reports.\n"
                "Standard users can view students, courses, enrollments, and attendance, plus record attendance and generate reports."
            ),
            bg="white",
            fg="#4b5563",
            justify="left",
            wraplength=760,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(10, 0))

    def refresh_students_page():
        for widget in pages["students"].winfo_children():
            widget.destroy()

        tk.Label(pages["students"], text="Students", bg="#eff3f7", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(14, 10))
        tk.Label(pages["students"], text="View and manage student records.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w")

        actions = tk.Frame(pages["students"], bg="#eff3f7")
        actions.pack(fill="x", pady=14)
        create_action_button(actions, "View Students", view_students).grid(row=0, column=0, padx=6, pady=6)
        create_action_button(actions, "Search Student", search_student).grid(row=0, column=1, padx=6, pady=6)
        if current_role == "admin":
            create_action_button(actions, "Add Student", add_student).grid(row=1, column=0, padx=6, pady=6)
            create_action_button(actions, "Update Student", update_student).grid(row=1, column=1, padx=6, pady=6)
            create_action_button(actions, "Delete Student", delete_student).grid(row=1, column=2, padx=6, pady=6)

        summary = tk.Frame(pages["students"], bg="white", bd=1, relief="solid", padx=20, pady=18)
        summary.pack(fill="both", expand=True)
        student_count = fetch_one("SELECT COUNT(*) FROM students")
        student_count = student_count[0] if student_count else 0
        tk.Label(summary, text=f"Total students: {student_count}", bg="white", fg="#111827", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(
            summary,
            text="Only admins can add, edit, or delete student information." if current_role != "admin" else "You have full student management rights.",
            bg="white",
            fg="#4b5563",
            wraplength=760,
            justify="left",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(10, 0))

    def refresh_courses_page():
        for widget in pages["courses"].winfo_children():
            widget.destroy()

        tk.Label(pages["courses"], text="Courses", bg="#eff3f7", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(14, 10))
        tk.Label(pages["courses"], text="View and manage course offerings.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w")

        actions = tk.Frame(pages["courses"], bg="#eff3f7")
        actions.pack(fill="x", pady=14)
        create_action_button(actions, "View Courses", view_courses).grid(row=0, column=0, padx=6, pady=6)
        create_action_button(actions, "Search Course", search_course).grid(row=0, column=1, padx=6, pady=6)
        if current_role == "admin":
            create_action_button(actions, "Add Course", add_course).grid(row=1, column=0, padx=6, pady=6)
            create_action_button(actions, "Update Course", update_course).grid(row=1, column=1, padx=6, pady=6)
            create_action_button(actions, "Delete Course", delete_course).grid(row=1, column=2, padx=6, pady=6)

        summary = tk.Frame(pages["courses"], bg="white", bd=1, relief="solid", padx=20, pady=18)
        summary.pack(fill="both", expand=True)
        course_count = fetch_one("SELECT COUNT(*) FROM courses")
        course_count = course_count[0] if course_count else 0
        tk.Label(summary, text=f"Total courses: {course_count}", bg="white", fg="#111827", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(
            summary,
            text="Only admins can manage courses." if current_role != "admin" else "You have full course management rights.",
            bg="white",
            fg="#4b5563",
            wraplength=760,
            justify="left",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(10, 0))

    def refresh_enrollments_page():
        for widget in pages["enrollments"].winfo_children():
            widget.destroy()

        tk.Label(pages["enrollments"], text="Enrollments", bg="#eff3f7", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(14, 10))
        tk.Label(pages["enrollments"], text="View and manage student enrollments.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w")

        actions = tk.Frame(pages["enrollments"], bg="#eff3f7")
        actions.pack(fill="x", pady=14)
        create_action_button(actions, "View Enrollments", view_enrollments).grid(row=0, column=0, padx=6, pady=6)
        create_action_button(actions, "Students by Course", view_students_by_course).grid(row=0, column=1, padx=6, pady=6)
        create_action_button(actions, "Courses by Student", view_courses_by_student).grid(row=0, column=2, padx=6, pady=6)
        if current_role == "admin":
            create_action_button(actions, "Assign Enrollment", assign_student_to_course).grid(row=1, column=0, padx=6, pady=6)
            create_action_button(actions, "Remove Enrollment", remove_enrollment).grid(row=1, column=1, padx=6, pady=6)

        summary = tk.Frame(pages["enrollments"], bg="white", bd=1, relief="solid", padx=20, pady=18)
        summary.pack(fill="both", expand=True)
        enroll_count = fetch_one("SELECT COUNT(*) FROM enrollments")
        enroll_count = enroll_count[0] if enroll_count else 0
        tk.Label(summary, text=f"Total enrollments: {enroll_count}", bg="white", fg="#111827", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(
            summary,
            text="Admins can create and remove enrollments." if current_role == "admin" else "You can view enrollment records and student/course relationships.",
            bg="white",
            fg="#4b5563",
            wraplength=760,
            justify="left",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(10, 0))

    def refresh_reports_page():
        for widget in pages["reports"].winfo_children():
            widget.destroy()

        tk.Label(pages["reports"], text="Reports", bg="#eff3f7", fg="#111827", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=(14, 10))
        tk.Label(pages["reports"], text="Generate summaries and manage attendance.", bg="#eff3f7", fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w")

        actions = tk.Frame(pages["reports"], bg="#eff3f7")
        actions.pack(fill="x", pady=14)
        create_action_button(actions, "Generate Reports", generate_reports).grid(row=0, column=0, padx=6, pady=6)
        create_action_button(actions, "Record Attendance", record_attendance).grid(row=0, column=1, padx=6, pady=6)
        create_action_button(actions, "View Attendance", view_attendance).grid(row=0, column=2, padx=6, pady=6)
        create_action_button(actions, "Search Attendance", search_attendance).grid(row=1, column=0, padx=6, pady=6)
        if current_role == "admin":
            create_action_button(actions, "Update Attendance", update_attendance).grid(row=1, column=1, padx=6, pady=6)
            create_action_button(actions, "Delete Attendance", delete_attendance).grid(row=1, column=2, padx=6, pady=6)

        summary = tk.Frame(pages["reports"], bg="white", bd=1, relief="solid", padx=20, pady=18)
        summary.pack(fill="both", expand=True)
        tk.Label(summary, text="Attendance and reporting", bg="white", fg="#111827", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(
            summary,
            text="You may record, view, and search attendance records, and generate reports.",
            bg="white",
            fg="#4b5563",
            wraplength=760,
            justify="left",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(10, 0))

    create_page("dashboard")
    create_page("students")
    create_page("courses")
    create_page("enrollments")
    create_page("reports")

    show_page("dashboard")
    root.protocol("WM_DELETE_WINDOW", root.destroy)


def logout():
    global current_role
    current_role = None
    root.destroy()
    launch_app()


def launch_app():
    global root
    create_database()
    migrate_add_columns()

    root = tk.Tk()
    root.withdraw()
    show_login_window()
    root.mainloop()


if __name__ == "__main__":
    launch_app()
