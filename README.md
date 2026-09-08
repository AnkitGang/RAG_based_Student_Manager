# RAG-Based Student Manager

An AI-powered Student Management application built with **Python, FastAPI, LangChain, ChromaDB, and Ollama**.

The project combines traditional REST APIs for student management with a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to ask natural-language questions about student data and receive context-aware responses.

## Features

* Create, retrieve, and delete student records
* Query student information through REST APIs
* AI-powered chat using Retrieval-Augmented Generation (RAG)
* Semantic search over student data using vector embeddings
* Persistent vector storage using ChromaDB
* Local LLM inference using Ollama and Llama 3
* Embeddings generated using `nomic-embed-text`
* MMR-based document retrieval
* GitHub API integration to retrieve public repository and follower information
* Input validation using Pydantic
* Logging and exception handling for external API requests
* Modular project structure separating controllers, services, and utilities

## Architecture

```text
                    ┌─────────────────────┐
                    │      Client         │
                    │  Postman / Browser  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │     REST APIs       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌──────────────────┐             ┌──────────────────┐
     │ Student Manager  │             │    RAG Pipeline  │
     │ CRUD Operations  │             │                  │
     └────────┬─────────┘             └────────┬─────────┘
              │                                │
              ▼                                ▼
     ┌──────────────────┐             ┌──────────────────┐
     │ Student Data     │             │    ChromaDB      │
     │ File Storage     │             │  Vector Store    │
     └────────┬─────────┘             └────────┬─────────┘
              │                                │
              │                                ▼
              │                       ┌──────────────────┐
              │                       │ MMR Retriever    │
              │                       │      k = 2       │
              │                       └────────┬─────────┘
              │                                │
              │                                ▼
              │                       ┌──────────────────┐
              │                       │  PromptTemplate  │
              │                       └────────┬─────────┘
              │                                │
              │                                ▼
              │                       ┌──────────────────┐
              │                       │ Ollama / Llama 3 │
              │                       └────────┬─────────┘
              │                                │
              └────────────────────────────────┘
                                               │
                                               ▼
                                      ┌──────────────────┐
                                      │ AI Response      │
                                      └──────────────────┘
```

## RAG Pipeline

The `/chat` endpoint uses the following workflow:

```text
User Question
      │
      ▼
FastAPI /chat endpoint
      │
      ▼
ChromaDB Retriever
      │
      ▼
MMR Similarity Retrieval
      │
      ▼
Relevant Student Data
      │
      ▼
PromptTemplate
      │
      ▼
Ollama - Llama 3
      │
      ▼
Generated Response
```

The prompt instructs the model to use only the supplied student data and respond with `"I don't know"` when the requested information is not available. This helps keep responses grounded in the retrieved context.

## Technology Stack

### Programming Language

* Python

### Frameworks & Libraries

* FastAPI
* Pydantic
* LangChain
* LangChain Ollama
* LangChain Chroma

### AI / RAG

* Retrieval-Augmented Generation (RAG)
* Llama 3
* Ollama
* `nomic-embed-text`
* Vector Search
* MMR Retrieval
* Prompt Engineering

### Storage

* ChromaDB
* File-based student data

### APIs & Tools

* GitHub REST API
* Uvicorn
* Requests
* Postman

## Project Structure

```text
RAG_based_Student_Manager/
│
├── src/
│   └── RAG_based_Student_Manager/
│       │
│       ├── controllers/
│       │   └── Controller.py
│       │
│       ├── services/
│       │   ├── langchain_service.py
│       │   ├── llm_service.py
│       │   └── rag_service.py
│       │
│       └── utils/
│           └── file_handler.py
│
├── data/
│   └── chroma_db/
│
├── logs/
│   └── app.log
│
├── requirements.txt
├── Steps_and_Commands to Run this project.txt
└── README.md
```

## API Endpoints

### Chat

```http
POST /chat
```

Ask questions about the available student data.

Example request:

```json
{
  "message": "Which student has the highest number of GitHub repositories?"
}
```

Example response:

```json
{
  "response": "..."
}
```

### Add Student

```http
POST /students
```

Example request:

```json
{
  "name": "John",
  "age": 21,
  "github_username": "john123"
}
```

If a GitHub username is provided, the application attempts to retrieve public GitHub information such as:

* Public repositories
* Followers

### Get All Students

```http
GET /students
```

### Get Student

```http
GET /student/{name}
```

### Delete Student

```http
DELETE /student/{name}
```

## How RAG Works in This Project

When the application starts, student data is loaded and converted into documents before being stored in ChromaDB.

For each student:

```text
Student Data
     │
     ▼
Text Representation
     │
     ▼
Embedding Generation
(nomic-embed-text)
     │
     ▼
ChromaDB
```

When a user sends a question:

```text
Question
   │
   ▼
Retriever
   │
   ▼
Relevant Documents
   │
   ▼
Prompt with Context
   │
   ▼
Llama 3
   │
   ▼
Final Answer
```

This allows the LLM to generate responses using the application's student data rather than relying only on its general knowledge.

## Prerequisites

Make sure you have the following installed:

* Python 3.10+
* Git
* Ollama

Download and install Ollama from:

https://ollama.com/

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/AnkitGang/RAG_based_Student_Manager.git
```

```bash
cd RAG_based_Student_Manager
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configure Ollama

Start the Llama 3 model:

```bash
ollama run llama3
```

Ollama should be available at:

```text
http://localhost:11434/
```

The project also uses the `nomic-embed-text` model for embeddings. Make sure it is available in your Ollama installation:

```bash
ollama pull nomic-embed-text
```

## Run the Application

From the project root directory:

```bash
uvicorn src.RAG_based_Student_Manager.controllers.Controller:app --reload
```

The FastAPI server will start locally.

Open:

```text
http://127.0.0.1:8000
```

## FastAPI Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI or Postman to test the APIs.

## Example RAG Interaction

Example question:

```text
Tell me about the student named Ankit.
```

The application:

1. Receives the question through the `/chat` endpoint.
2. Searches ChromaDB for relevant student information.
3. Retrieves the most relevant documents using MMR.
4. Inserts the retrieved information into the prompt.
5. Sends the prompt to Llama 3 through Ollama.
6. Returns the generated response through the API.

## GitHub API Integration

When a student is added with a GitHub username, the application calls the GitHub REST API to retrieve public profile information.

Currently, the application extracts:

```text
Public repositories
Followers
```

A timeout is also configured for the external request, and request failures are logged.

## Error Handling

The application includes handling for several common scenarios:

* Duplicate student records
* Student not found
* Invalid request data
* GitHub API failures
* LLM/API request failures
* Missing relevant RAG context

## Current Limitations

* Student data is stored using local file-based storage.
* Ollama must be running locally for the LLM functionality.
* Chat history is maintained in memory.
* GitHub integration currently retrieves limited public profile information.
* The application is intended primarily as a learning and demonstration project.

## Future Improvements

Potential improvements include:

* Replace file-based storage with PostgreSQL or MySQL
* Add authentication and authorization
* Add a frontend interface
* Improve chat history persistence
* Add automated tests
* Containerize the application using Docker
* Add CI/CD using GitHub Actions
* Add richer GitHub profile information
* Introduce more advanced RAG evaluation and retrieval strategies
* Deploy the application to a cloud environment

## Learning Outcomes

This project provided practical experience with:

* Building REST APIs using FastAPI
* Designing modular Python applications
* Retrieval-Augmented Generation
* Vector databases and semantic retrieval
* Embeddings
* Local LLM integration
* LangChain pipelines
* Prompt engineering
* External API integration
* Exception handling and logging
* API testing with Swagger and Postman

## Author

**Ankit Gangwar**

GitHub:
https://github.com/AnkitGang

Project Repository:
https://github.com/AnkitGang/RAG_based_Student_Manager

---

⭐ If you find this project useful, consider giving the repository a star.
