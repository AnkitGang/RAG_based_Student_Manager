from src.RAG_based_Student_Manager.utils.file_handler import load_students
from src.RAG_based_Student_Manager.services.embedding_service import get_embeddings
import numpy as np


def build_index():
    students = load_students()

    if not students:
        return None

    index = []

    for student in students:
        text = student_to_text(student)

        if not text:
            continue

        embedding = get_embeddings(text)

        if embedding:
            index.append({
                "student": student,
                "text": text,
                "embedding": embedding
            })

    return index


def retrieve_relevant_info(query, index, top_k=2):
    query_embedding = get_embeddings(query)

    if not query_embedding:
        return []

    scores = []

    for item in index:
        similarity = cosine_similarity(query_embedding, item["embedding"])
        scores.append((similarity, item))

    print([(similarity, item["text"]) for similarity, item in scores])

    scores.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in scores[:top_k]]


def cosine_similarity(a, b):
    if a is None or b is None:
        return 0

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0

    return np.dot(a, b) / (norm_a * norm_b)


def student_to_text(student):
    if not student["name"]:
        return None

    if not student["age"]:
        return None

    github = student.get("github")

    text = f"{student['name']} is {student['age']} years old. "

    if github and isinstance(github, dict):
        repos = github.get("repos", "")
        followers = github.get("followers", "")
        if repos is not None and repos != "" and followers is not None and followers != "":
            text += f"They has {repos} repos and {followers} followers on GitHub."
        else:
            text += "They does not have Github profile"
    else:
        text += "They does not have Github profile"

    return text

