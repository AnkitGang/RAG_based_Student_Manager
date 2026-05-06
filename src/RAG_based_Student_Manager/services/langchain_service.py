from langchain_ollama.llms import OllamaLLM
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_chroma.vectorstores import Chroma

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

from src.RAG_based_Student_Manager.services.rag_service import student_to_text

import os

# ---------- PATH SETUP ----------
project_root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )
)

chroma_db_path = os.path.join(project_root, 'data', 'chroma_db')


# ---------- LLM ----------
llm = OllamaLLM(model="llama3")


# ---------- EMBEDDINGS ----------
embeddings = OllamaEmbeddings(model="nomic-embed-text")


# ---------- VECTOR STORE ----------
vector_store = Chroma(
    collection_name="students",
    embedding_function=embeddings,
    persist_directory=chroma_db_path
)


# ---------- RETRIEVER ----------
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2}
)


# ---------- IN-MEMORY CHAT HISTORY ----------
chat_history = []


# ---------- PROMPT ----------
prompt = PromptTemplate.from_template(
"""
You are an assistant that answers ONLY using the provided student data.

Rules:
- Do NOT make up information
- If answer is not in data, say "I don't know"

Chat History:
{history}

Data:
{context}

Question:
{question}
"""
)


# ---------- FORMAT DOCS ----------
def format_docs(docs):
    if not docs:
        return "No relevant student data found."

    return "\n".join([
        doc.page_content for doc in docs
    ])


# ---------- CHAIN ----------
def build_chain():
    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
            "history": lambda _: "\n".join(chat_history)
        }
        | prompt
        | llm
        | StrOutputParser()
    )


chain = build_chain()


# ---------- LOAD DATA INTO CHROMA ----------
def load_into_chroma(students):
    docs = []
    ids = []

    for s in students:
        text = student_to_text(s)

        if not text:
            continue

        docs.append(Document(
            page_content=text,
            metadata={"name": s.get("name")}
        ))

        # IMPORTANT: use unique id (name lower)
        ids.append(s.get("name").lower())

    if docs:
        vector_store.add_documents(docs, ids=ids)
