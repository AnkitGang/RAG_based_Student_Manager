from fastapi import FastAPI, HTTPException
from file_handler import load_students, save_students
from llm_service import ask_llm
from rag_service import build_index, retrieve_relevant_info
from pydantic import BaseModel
import requests
import logging


logging.basicConfig(
    filename="app.log",
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


@app.post("/chat")
def chat(req: ChatRequest):
    index = build_index()

    if not index:
        return {
            "response": "No Student data available"
        }

    relevant = retrieve_relevant_info(req.message, index)

    context = ""

    for item in relevant:
        context += "\n- " + item["text"]

    prompt = f"""
        You are an assistant that answers ONLY using the provided student data.
        
        Rules:
        - Do NOT make up information
        - If answer is not in data, say "I don't know"
        
        Data:
        {context}
        
        Question:
        {req.message}
    """

    logger.info(f"--------Context---- {context}")
    logger.info(f"-------Prompt------ {prompt}")

    response = ask_llm(prompt)
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
    return {
        "message": "Student added successfully",
        "student": new_student
    }


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

    return {
        "message": "Deleted successfully"
    }
