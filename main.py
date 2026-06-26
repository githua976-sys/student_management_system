from database import create_database

from students import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
)

from course import (
    add_course,
    view_courses,
    search_course,
    update_course,
    delete_course
)

from enrollment import (
    assign_student_to_course,
    view_enrollments,
    view_students_by_course,
    view_courses_by_student,
    remove_enrollment
)


def menu():
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Add Course")
        print("7. View Courses")
        print("8. Search Course")
        print("9. Update Course")
        print("10. Delete Course")
        print("11. Assign Student to Course")
        print("12. View Students by Course")
        print("13. Record Attendance")
        print("14. Generate Reports")
        print("15. Exit")

        choice = input("\nEnter your choice: ")

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

        elif choice == "11":
            print("Assign Student to Course - Coming Soon")

        elif choice == "12":
            print("View Students by Course - Coming Soon")

        elif choice == "13":
            print("Record Attendance - Coming Soon")

        elif choice == "14":
            print("Generate Reports - Coming Soon")

        elif choice == "15":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_database()
    menu()