import sys
from student_service import add_student, view_student, delete_student, search_student, fetch_github_profile
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    while True:
        print("\n1. Add Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. Fetch GitHub Profile")
        print("6. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError as e:
            logging.error("Invalid input!!!!!!")
            # print("Invalid input!!!!!!")
            continue

        if choice == 1:
            add_student()
        elif choice == 2:
            view_student()
        elif choice == 3:
            delete_student()
        elif choice == 4:
            search_student()
        elif choice == 5:
            fetch_github_profile()
        else:
            logging.info("Exiting !!!!!!!!!!!")
            # print("Exiting !!!!!!!!!!!")
            sys.exit()


if __name__ == "__main__":
    main()
