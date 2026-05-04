import logging
import requests
from src.RAG_based_Student_Manager.utils.file_handler import load_students, save_students

logger = logging.getLogger(__name__)
GITHUB_URL = "https://api.github.com/users/"


def fetch_github_profile():
    username = input("Enter GitHub username: ")

    try:
        res = requests.get(GITHUB_URL + username, timeout=5)
        res.raise_for_status()
        data = res.json()

        print("Name:", data["name"])
        print("Public repos:", data["public_repos"])

        return data

    except requests.exceptions.HTTPError as e:
        print("Server Issue")
        return None
    except requests.exceptions.RequestException as e:
        print("Error fetching GitHub data")
        return None


def add_student():
    students = load_students()
    name = input("Enter Name: ")

    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Invalid age!")
        return

    data = fetch_github_profile()
    github_info = {
        "repos": data.get('public_repos') if data else None,
        "followers": data.get('followers') if data else None
    }

    students.append({
        "name": name,
        "age": age,
        "github": github_info
    })

    save_students(students)
    print("Student added successfully!")


def view_student():
    students = load_students()

    if not students:
        print("No students found.")
        return

    for student in students:
        print(f"Name: {student['name']}, Age: {student['age']}, GitHub Profile: {student['github']}")
    # try:
    #     with open(FILE_NAME, "r") as f:
    #         print("\n--- Student List ---")
    #         for line in f:
    #             name, age = line.strip().split(",")
    #             print(f"Name: {name}, Age: {age}")
    # except (FileNotFoundError, ValueError):
    #     print("No student records found.")


def delete_student():
    students = load_students()
    name = input("Enter name of Student to delete: ")

    new_students = [
        student for student in students if student['name'].casefold() != name.casefold()    # List Comprehension
    ]

    if len(new_students) == len(students):
        print(f"Student {name} not found")
    else:
        save_students(new_students)
        print(f"Deleted: {name} successfully")

    # try:
    #     with open(FILE_NAME, "r+") as f:
    #         name = input("Enter name of Student to delete: ")
    #         copy_content = []
    #         flag = False
    #
    #         for line in f:
    #             n = line.strip().split(",")[0]
    #             if n.casefold() == name.casefold():
    #                 flag = True
    #                 continue
    #             else:
    #                 copy_content.append(line)
    #
    #         if flag:
    #             f.seek(0)
    #             f.writelines(copy_content)
    #             f.truncate()
    #             print(f"Deleted: {name} successfully")
    #         else:
    #             print(f"Student {name} not found")
    #
    # except FileNotFoundError:
    #     print("Exception occurred!")
    #     return


def search_student():
    students = load_students()
    search = input("Enter Name to search: ")

    student = next(
        (s for s in students if s["name"].casefold() == search.casefold()),
        None
    )

    if student:
        github = student.get("github", {})

        if isinstance(github, dict):
            repos = github.get("repos", "N/A")
            followers = github.get("followers", "N/A")
        else:
            repos = followers = "N/A"

        print("Details found:")
        print(f'Name: {student["name"]}, Age: {student["age"]}, GitHub Profile: [Public Repos - {repos}, Followers - {followers}]')
    else:
        print(f"Student {search} not found")


    # student = next((s for s in students if s['name'].casefold() == search.casefold()), f"Student {search} not found")
    # # if type(student) == dict:
    # if isinstance(student, dict):
    #     print("Details found:")
    #     print(f"Name: {student['name']}, Age: {student['age']}")
    # else:
    #     print(student)


    # for student in students:
    #     if student['name'].casefold() == search.casefold():
    #         print("Details found:")
    #         print(f"Name: {student['name']}, Age: {student['age']}")
    #         return
    #
    # print("Student Details not found")


    # try:
    #     with open(FILE_NAME, "r") as f:
    #         search = input("Enter Name to search: ")
    #         for line in f:
    #             n, age = line.strip().split(",")
    #             if n.casefold() == search.casefold():
    #                 print("Details found:")
    #                 print(f"Name: {n}, Age: {age}")
    #                 return
    #
    #         print("Student Details not found")
    # except FileNotFoundError:
    #     print("Exception occurred")
    #     return



