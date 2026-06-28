import tkinter as tk
from tkinter import messagebox

# Student Functions
from students import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
)

# Course Functions
from course import (
    add_course,
    view_courses,
    search_course,
    update_course,
    delete_course
)

# Enrollment Functions
from enrollment import (
    assign_student_to_course,
    view_enrollments,
    view_students_by_course,
    view_courses_by_student,
    remove_enrollment
)

# Attendance Functions
from attendance import (
    record_attendance,
    view_attendance,
    search_attendance,
    update_attendance,
    delete_attendance
)

# Report Function
from report import generate_reports


root = tk.Tk()
root.title("Student Management System")
root.geometry("700x650")
root.resizable(False, False)


title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)


# ---------------- Student ----------------

tk.Label(root, text="Student Management", font=("Arial", 14, "bold")).pack()

tk.Button(root, text="Add Student", width=30, command=add_student).pack(pady=2)
tk.Button(root, text="View Students", width=30, command=view_students).pack(pady=2)
tk.Button(root, text="Search Student", width=30, command=search_student).pack(pady=2)
tk.Button(root, text="Update Student", width=30, command=update_student).pack(pady=2)
tk.Button(root, text="Delete Student", width=30, command=delete_student).pack(pady=2)


# ---------------- Courses ----------------

tk.Label(root, text="Course Management", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Add Course", width=30, command=add_course).pack(pady=2)
tk.Button(root, text="View Courses", width=30, command=view_courses).pack(pady=2)
tk.Button(root, text="Search Course", width=30, command=search_course).pack(pady=2)
tk.Button(root, text="Update Course", width=30, command=update_course).pack(pady=2)
tk.Button(root, text="Delete Course", width=30, command=delete_course).pack(pady=2)


# ---------------- Enrollment ----------------

tk.Label(root, text="Enrollment", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Assign Student to Course", width=30, command=assign_student_to_course).pack(pady=2)
tk.Button(root, text="View Enrollments", width=30, command=view_enrollments).pack(pady=2)
tk.Button(root, text="View Students by Course", width=30, command=view_students_by_course).pack(pady=2)
tk.Button(root, text="View Courses by Student", width=30, command=view_courses_by_student).pack(pady=2)
tk.Button(root, text="Remove Enrollment", width=30, command=remove_enrollment).pack(pady=2)


# ---------------- Attendance ----------------

tk.Label(root, text="Attendance", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Record Attendance", width=30, command=record_attendance).pack(pady=2)
tk.Button(root, text="View Attendance", width=30, command=view_attendance).pack(pady=2)
tk.Button(root, text="Search Attendance", width=30, command=search_attendance).pack(pady=2)
tk.Button(root, text="Update Attendance", width=30, command=update_attendance).pack(pady=2)
tk.Button(root, text="Delete Attendance", width=30, command=delete_attendance).pack(pady=2)


# ---------------- Reports ----------------

tk.Label(root, text="Reports", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Generate Reports", width=30, command=generate_reports).pack(pady=2)


tk.Button(
    root,
    text="Exit",
    width=30,
    bg="red",
    fg="white",
    command=root.destroy
).pack(pady=20)

root.mainloop()