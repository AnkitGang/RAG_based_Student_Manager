import json
import logging

# FILE_NAME = "CLI_Student_Manager.txt"
FILE_NAME = "../../../data/students.json"
logger = logging.getLogger(__name__)


def load_students():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("File not found, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error loading students: {e}")
        return []


def save_students(students):
    with open(FILE_NAME, "w") as f:
        json.dump(students, f, indent=4)


# def load_students():
#     students = []
#     try:
#         with open(FILE_NAME, "r") as f:
#             for line in f:
#                 name, age = line.strip().split(",")
#                 students.append({
#                     "Name": name,
#                     "Age": int(age)
#                 })
#     except FileNotFoundError:
#         pass
#
#     return students


# def save_students(students):
#     with open(FILE_NAME, "w") as f:
#         for student in students:
#             f.write(f"{student['Name']},{student['Age']}\n")
