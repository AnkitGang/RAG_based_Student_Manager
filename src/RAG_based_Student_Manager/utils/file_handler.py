import json
import logging
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Build path to students.json relative to the project structure
FILE_NAME = os.path.join(script_dir, "..", "..", "..", "data", "students.json")
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
