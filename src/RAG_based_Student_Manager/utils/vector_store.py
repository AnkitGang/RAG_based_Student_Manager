import chromadb
from src.RAG_based_Student_Manager.utils.file_handler import load_students
from src.RAG_based_Student_Manager.services.rag_service import student_to_text
from src.RAG_based_Student_Manager.services.embedding_service import get_embeddings

client = chromadb.Client()
collection = client.get_or_create_collection(name="students")


def build_vector_store():
    students = load_students()

    if not students:
        return None

    client.delete_collection("students")
    global collection
    collection = client.get_or_create_collection("students")

    for i, student in enumerate(students):
        text = student_to_text(student)

        embedding = get_embeddings(text)

        if embedding:
            collection.add(
                ids=[str(i)],
                embeddings=[embedding],
                documents=[text]
            )


def query_vector_store(query, top_k=2):
    query_embedding = get_embeddings(query)

    if not query_embedding:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results.get("documents", [[]])[0]
