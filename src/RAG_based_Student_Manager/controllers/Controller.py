from fastapi import FastAPI, HTTPException

from src.RAG_based_Student_Manager.utils.file_handler import load_students, save_students
from src.RAG_based_Student_Manager.services.langchain_service import chain, chat_history, load_into_chroma

from pydantic import BaseModel

import requests
import logging
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
log_file_path = os.path.join(project_root, 'logs', 'app.log')

os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI()
GITHUB_URL = "https://api.github.com/users/"
logger = logging.getLogger(__name__)


class Student(BaseModel):
    name: str
    age: int
    github_username: str | None = None


class ChatRequest(BaseModel):
    message: str


@app.on_event("startup")
def startup_event():
    students = load_students()
    load_into_chroma(students)


@app.post("/chat")
def chat(req: ChatRequest):
    response = chain.invoke(req.message)

    chat_history.append(f"User: {req.message}")
    chat_history.append(f"AI: {response}")

    return {
        "response": response
    }


@app.post("/students")
def add_student(student: Student):
    students = load_students()

    if any(s["name"].casefold() == student.name.casefold() for s in students):
        raise HTTPException(status_code=400, detail="Student already exists")

    github_data = None
    if student.github_username:
        github_data = fetch_github_profile(student.github_username)

    new_student = {
        "name": student.name,
        "age": student.age,
        "github": github_data
    }

    students.append(new_student)
    save_students(students)

    load_into_chroma([new_student])

    return {
        "message": "Student added successfully",
        "student": new_student
    }


def fetch_github_profile(username: str):
    try:
        res = requests.get(GITHUB_URL + username, timeout=5)
        res.raise_for_status()
        github_data = res.json()

        return {
            "repos": github_data.get('public_repos') if github_data else None,
            "followers": github_data.get('followers') if github_data else None
        }

    except requests.exceptions.RequestException as e:
        logger.error("GitHub API error", e)
        return None


@app.get("/students")
def get_all_students():
    return load_students()


@app.get("/student/{name}")
def get_student(name: str):
    students = load_students()

    for student in students:
        if student["name"].casefold() == name.casefold():
            return student

    raise HTTPException(status_code=404, detail="Student not found")


@app.delete("/student/{name}")
def delete_student(name: str):
    students = load_students()

    new_students = [student for student in students if student["name"].casefold() != name.casefold()]

    if len(new_students) == len(students):
        raise HTTPException(status_code=404, detail="Student not found")

    save_students(new_students)

    load_into_chroma(new_students)

    return {
        "message": "Deleted successfully"
    }
