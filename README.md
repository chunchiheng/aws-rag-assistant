# AWS Documentation RAG Assistant

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions about AWS documentation. The system retrieves relevant information from AWS documentation, reranks the retrieved results using a Cross-Encoder, and uses OpenAI GPT-4.1-mini to generate grounded answers with source references.

The application uses **React (JavaScript)** as the frontend and **FastAPI (Python)** as the backend.

---

## Features

* Ask questions about AWS services and documentation
* Retrieval-Augmented Generation (RAG) pipeline
* Semantic document retrieval using vector embeddings
* ChromaDB vector database
* Cross-Encoder reranking for improved retrieval relevance
* OpenAI GPT-4.1-mini for answer generation
* Source references showing the AWS documentation and page number
* React-based frontend
* FastAPI REST API backend
* CORS support for frontend-backend communication

---

## Architecture

```text
                         User
                           │
                           ▼
                 ┌───────────────────┐
                 │   React Frontend  │
                 │   JavaScript      │
                 │   localhost:3000  │
                 └─────────┬─────────┘
                           │
                     HTTP POST
                           │
                           ▼
                 ┌───────────────────┐
                 │  FastAPI Backend  │
                 │   localhost:8000  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │      RAG.py       │
                 └─────────┬─────────┘
                           │
                    Similarity Search
                           │
                           ▼
                 ┌───────────────────┐
                 │     ChromaDB      │
                 │  Vector Database  │
                 └─────────┬─────────┘
                           │
                      Top 10 Results
                           │
                           ▼
                 ┌───────────────────┐
                 │  Cross-Encoder    │
                 │     Reranker      │
                 └─────────┬─────────┘
                           │
                        Top 3
                           │
                           ▼
                 ┌───────────────────┐
                 │   OpenAI GPT      │
                 │    GPT-4.1-mini   │
                 └─────────┬─────────┘
                           │
                     Answer + Sources
                           │
                           ▼
                 ┌───────────────────┐
                 │   React Frontend  │
                 └───────────────────┘
```

---

## RAG Pipeline

The application follows a multi-stage RAG pipeline.

### 1. Document Ingestion

AWS documentation PDFs are loaded using `PyPDFLoader`.

```text
AWS Documentation PDFs
        ↓
PyPDFLoader
        ↓
Document Pages
```

The current documents cover:

* Amazon EC2
* Amazon S3
* Amazon VPC

The system can be extended to support additional AWS services by obtaining their official documentation from the AWS Documentation website and adding the documents to the data/documents/ directory.

---

### 2. Text Chunking

The extracted documents are divided into smaller chunks using `RecursiveCharacterTextSplitter`.

```text
Chunk Size: 1000 characters
Chunk Overlap: 200 characters
```

The overlap helps preserve contextual information between adjacent chunks.

---

### 3. Embeddings

Each chunk is converted into a vector representation using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

These embeddings are stored in ChromaDB for semantic similarity search.

---

### 4. Vector Retrieval

When a user submits a question, the system performs semantic similarity search against ChromaDB.

```text
User Question
      ↓
Embedding
      ↓
ChromaDB
      ↓
Top 10 Relevant Documents
```

---

### 5. Document Reranking

The retrieved Top 10 documents are reranked using:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

The Cross-Encoder evaluates the relevance between the user's question and each retrieved document.

```text
Top 10 Retrieved Documents
          ↓
     Cross-Encoder
          ↓
Top 3 Relevant Documents
```

---

### 6. Answer Generation

The Top 3 documents are combined into a context and provided to OpenAI GPT-4.1-mini.

The model is instructed to answer the question using only the retrieved documentation context.

```text
Top 3 Documents
       ↓
   Context
       ↓
GPT-4.1-mini
       ↓
Generated Answer
```

If the answer cannot be found in the provided context, the system is instructed to indicate that there is not enough information.

---

## Project Structure

```text
aws-rag-assistant/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── rag.py
│   ├── reranker.py
│   └── ingest.py
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── App.css
│       └── ...
│
├── data/
│   └── documents/
│       ├── ec2_user_guide.pdf
│       ├── s3_user_guide.pdf
│       └── vpc_user_guide.pdf
│
├── chroma_db/
├── .env
├── requirements.txt
└── README.md
```

### Backend

| File          | Description                                                                     |
| ------------- | ------------------------------------------------------------------------------- |
| `main.py`     | FastAPI application and REST API endpoints                                      |
| `rag.py`      | RAG pipeline, retrieval, context construction, and OpenAI generation            |
| `reranker.py` | Cross-Encoder document reranking                                                |
| `ingest.py`   | Loads PDFs, chunks documents, generates embeddings, and stores them in ChromaDB |

### Frontend

| File           | Description                                                             |
| -------------- | ----------------------------------------------------------------------- |
| `App.js`       | React application logic, user input, API requests, and result rendering |
| `App.css`      | Frontend styling                                                        |
| `package.json` | React project dependencies and scripts                                  |

### Data

The `data/documents/` directory contains the AWS documentation PDFs used by the RAG system.

### ChromaDB

The `chroma_db/` directory stores the generated vector embeddings and document metadata.

---

## Technologies Used

### Frontend

* React
* JavaScript
* HTML / JSX
* CSS
* Fetch API

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### RAG / AI

* LangChain
* ChromaDB
* Hugging Face Embeddings
* Sentence Transformers
* Cross-Encoder
* OpenAI API
* GPT-4.1-mini

### Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd aws-rag-assistant
```

---

### 2. Create and activate a Python virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure the OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

Do not commit the `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
node_modules/
```

---

## Document Ingestion

If the ChromaDB database has not been created yet, run the ingestion script from the project root:

```bash
python -m backend.ingest
```

The ingestion process will:

1. Find all AWS PDF documents
2. Load the PDF pages
3. Add AWS service metadata
4. Split documents into chunks
5. Generate embeddings
6. Generate deterministic chunk IDs
7. Store the chunks and embeddings in ChromaDB

After ingestion, the generated database will be stored in:

```text
chroma_db/
```

---

## Running the Backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

The FastAPI backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The main API endpoint is:

```text
POST /api/ask
```

Example request:

```json
{
  "query": "What is Amazon EC2?"
}
```

Example response:

```json
{
  "answer": "Amazon EC2 provides on-demand, scalable computing capacity...",
  "sources": [
    "ec2_user_guide.pdf — Page 23",
    "ec2_user_guide.pdf — Page 23",
    "ec2_user_guide.pdf — Page 3650"
  ]
}
```

---

## Running the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the JavaScript dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm start
```

The frontend will run at:

```text
http://localhost:3000
```

The React frontend communicates with the FastAPI backend through:

```text
POST http://127.0.0.1:8000/api/ask
```

---

## Application Workflow

When a user asks a question:

```text
1. User enters a question in React
             ↓
2. React sends POST request to FastAPI
             ↓
3. FastAPI receives the question
             ↓
4. RAG performs semantic similarity search
             ↓
5. ChromaDB returns Top 10 documents
             ↓
6. Cross-Encoder reranks the documents
             ↓
7. Top 3 documents are selected
             ↓
8. Retrieved context is sent to GPT-4.1-mini
             ↓
9. GPT generates an answer
             ↓
10. FastAPI returns answer + sources
             ↓
11. React displays the result
```

---

## API Endpoint

### `POST /api/ask`

Submit a question to the AWS documentation assistant.

#### Request

```json
{
  "query": "What is Amazon EC2?"
}
```

#### Response

```json
{
  "answer": "Amazon EC2 provides on-demand, scalable computing capacity...",
  "sources": [
    "ec2_user_guide.pdf — Page 23",
    "ec2_user_guide.pdf — Page 23",
    "ec2_user_guide.pdf — Page 3650"
  ]
}
```

---

## Development

Run the backend:

```bash
uvicorn backend.main:app --reload
```

Run the frontend in a separate terminal:

```bash
cd frontend
npm start
```

The two development servers communicate through HTTP requests.

```text
React
localhost:3000
      │
      │ POST /api/ask
      ↓
FastAPI
127.0.0.1:8000
```

---

## Future Improvements

Potential improvements include:

* Conversational chat history
* Streaming LLM responses
* AWS service filtering
* Better retrieval evaluation
* Authentication and user management
* Deployment using AWS services

---

## License

This project was developed as a personal academic/project application for demonstrating RAG, full-stack development, and AI application development.
