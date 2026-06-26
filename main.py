from database import create_database

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

# Report Functions
from report import generate_reports


def menu():
    while True:
        print("\n========================================")
        print("      STUDENT MANAGEMENT SYSTEM")
        print("========================================")

        print("\n--- STUDENT MANAGEMENT ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")

        print("\n--- COURSE MANAGEMENT ---")
        print("6. Add Course")
        print("7. View Courses")
        print("8. Search Course")
        print("9. Update Course")
        print("10. Delete Course")

        print("\n--- ENROLLMENT MANAGEMENT ---")
        print("11. Assign Student to Course")
        print("12. View All Enrollments")
        print("13. View Students by Course")
        print("14. View Courses by Student")
        print("15. Remove Enrollment")

        print("\n--- ATTENDANCE MANAGEMENT ---")
        print("16. Record Attendance")
        print("17. View Attendance")
        print("18. Search Attendance")
        print("19. Update Attendance")
        print("20. Delete Attendance")

        print("\n--- REPORTS ---")
        print("21. Generate Reports")

        print("\n22. Exit")

        choice = input("\nEnter your choice: ")

        # Student Management
        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        # Course Management
        elif choice == "6":
            add_course()

        elif choice == "7":
            view_courses()

        elif choice == "8":
            search_course()

        elif choice == "9":
            update_course()

        elif choice == "10":
            delete_course()

        # Enrollment Management
        elif choice == "11":
            assign_student_to_course()

        elif choice == "12":
            view_enrollments()

        elif choice == "13":
            view_students_by_course()

        elif choice == "14":
            view_courses_by_student()

        elif choice == "15":
            remove_enrollment()

        # Attendance Management
        elif choice == "16":
            record_attendance()

        elif choice == "17":
            view_attendance()

        elif choice == "18":
            search_attendance()

        elif choice == "19":
            update_attendance()

        elif choice == "20":
            delete_attendance()

        # Reports
        elif choice == "21":
            generate_reports()

        # Exit
        elif choice == "22":
            print("\nThank you for using Student Management System!")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    create_database()
    menu()