from database import create_database
from students import (
    add_student,
    view_students,
    search_student,
    update_student,
    delete_student
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
        print("8. Update Course")
        print("9. Delete Course")
        print("10. Assign Student to Course")
        print("11. View Students by Course")
        print("12. Record Attendance")
        print("13. View Attendance")
        print("14. Generate Reports")
        print("15. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            print("Add Student Selected")

        elif choice == "2":
            print("View Students Selected")

        elif choice == "3":
            print("Search Student Selected")

        elif choice == "4":
            print("Update Student Selected")

        elif choice == "5":
            print("Delete Student Selected")

        elif choice == "6":
            print("Add Course Selected")

        elif choice == "7":
            print("View Courses Selected")

        elif choice == "8":
            print("Update Course Selected")

        elif choice == "9":
            print("Delete Course Selected")

        elif choice == "10":
            print("Assign Student To Course Selected")

        elif choice == "11":
            print("View Students By Course Selected")

        elif choice == "12":
            print("Record Attendance Selected")

        elif choice == "13":
            print("View Attendance Selected")

        elif choice == "14":
            print("Generate Reports Selected")

        elif choice == "15":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice. Please try again.")

            # Create database and tables
create_database()

# Run menu
menu()