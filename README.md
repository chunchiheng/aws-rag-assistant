# AWS Documentation RAG Assistant

An end-to-end Retrieval-Augmented Generation (RAG) application that answers questions using official AWS documentation for **Amazon EC2, Amazon S3, and Amazon VPC**.

The system combines **semantic retrieval, cross-encoder reranking, and an OpenAI LLM** to generate grounded answers with document and page-level source references.

---

## Demo

The application provides a simple Streamlit interface where users can ask natural-language questions about AWS services.

Example:

> **What is Amazon VPC and why is it used with EC2?**

The system retrieves relevant AWS documentation, reranks the retrieved chunks, and generates an answer based on the most relevant sources.

Each answer also includes the source document and page number.

---

## Project Architecture

```text
                    AWS Documentation
                  /        |        \
                 /         |         \
              EC2.pdf    S3.pdf     VPC.pdf
                 \         |         /
                  \        |        /
                   Document Loading
                          |
                          v
                   Text Chunking
                          |
                          v
              Sentence Transformer
                    Embeddings
                          |
                          v
                      ChromaDB
                          |
                          v
                 Semantic Retrieval
                       Top 10
                          |
                          v
                Cross-Encoder Reranker
                       Top 3
                          |
                          v
                    OpenAI LLM
                          |
                          v
                 Answer + Sources
                          |
                          v
                    Streamlit UI
```

---

## RAG Pipeline

### 1. Document Ingestion

The system loads AWS PDF documentation using LangChain's `PyPDFLoader`.

The current knowledge base contains:

| Document              |     Pages |
| --------------------- | --------: |
| Amazon EC2 User Guide |     3,942 |
| Amazon S3 User Guide  |     3,659 |
| Amazon VPC User Guide |       712 |
| **Total**             | **8,313** |

The documents are split into smaller chunks using `RecursiveCharacterTextSplitter`.

Current configuration:

```text
Chunk size:    1000 characters
Chunk overlap: 200 characters
```

The three documents currently produce approximately:

```text
18,341 document chunks
```

---

### 2. Text Embeddings

Each document chunk is converted into a numerical vector using:

**`sentence-transformers/all-MiniLM-L6-v2`**

The model produces a **384-dimensional embedding vector**.

For example:

```text
Document Chunk
      ↓
Sentence Transformer
      ↓
[0.0057, 0.0473, 0.00006, ..., 0.1067]
      ↓
384-dimensional vector
```

These embeddings allow the system to perform semantic similarity search.

---

### 3. Vector Database

The generated embeddings are stored in **ChromaDB**.

Each chunk is assigned a deterministic ID containing the AWS service, page number, and chunk index.

Example:

```text
ec2_page_22_chunk_42
```

This makes the stored documents easier to identify and helps avoid accidental duplicate insertion during ingestion.

---

### 4. Semantic Retrieval

When a user submits a question, the query is converted into an embedding and compared against the vectors stored in ChromaDB.

The system retrieves the **Top 10 candidate chunks**.

```text
User Query
    ↓
Query Embedding
    ↓
ChromaDB Similarity Search
    ↓
Top 10 Candidate Chunks
```

Retrieving more candidates at this stage increases the chance that the relevant information is included before reranking.

---

### 5. Cross-Encoder Reranking

The initial Top 10 results are passed through a cross-encoder reranker.

Instead of only comparing vector similarity, the reranker evaluates the relationship between the **user query and each retrieved document**.

```text
User Query + Retrieved Document
              ↓
       Cross-Encoder
          Reranker
              ↓
        Relevance Score
```

The system then selects the **Top 3** most relevant chunks.

```text
Top 10 Retrieved
       ↓
   Reranking
       ↓
Top 3 Relevant
```

This two-stage retrieval strategy improves retrieval quality while keeping the amount of context sent to the LLM small.

---

### 6. LLM Generation

The Top 3 reranked chunks are passed to an **OpenAI LLM** as context.

The LLM generates the final answer based on the retrieved AWS documentation.

The system also returns the source document and page number.

Example:

```text
Answer:

An EC2 instance is a virtual server in the AWS Cloud.
The instance type determines the hardware available
to the instance...

Sources:

- ec2_user_guide.pdf — Page 23
```

---

## Retrieval Quality Example

The system was tested with:

```text
Query:
What is Amazon VPC and why is it used with EC2?
```

The initial vector retrieval returned 10 documents.

After reranking, the Top 3 results were all relevant sections from the Amazon VPC User Guide.

### Top 3 Results

| Rank | Source                  | Content                         |
| ---- | ----------------------- | ------------------------------- |
| 1    | VPC User Guide, Page 12 | What is Amazon VPC?             |
| 2    | VPC User Guide, Page 18 | VPCs and subnets                |
| 3    | VPC User Guide, Page 14 | Getting started with Amazon VPC |

This demonstrates that the reranker can filter the initial retrieval results and prioritize documents that are more directly related to the user's question.

---

## Streamlit UI

The project includes a Streamlit interface for interacting with the RAG system.

Users can enter questions such as:

```text
What is Amazon EC2?

What is Amazon S3?

What is Amazon VPC?

What is the difference between EC2 and S3?

Why is VPC used with EC2?
```

The application returns:

1. Generated answer
2. Source document
3. Source page number

Example:

```text
Answer

An EC2 instance is a virtual server in the AWS Cloud...

Sources

- ec2_user_guide.pdf — Page 23
```

---

## Project Structure

```text
aws-rag-assistant/
│
├── data/
│   └── documents/
│       ├── ec2_user_guide.pdf
│       ├── s3_user_guide.pdf
│       └── vpc_user_guide.pdf
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── ingest.py
│   ├── rag.py
│   ├── reranker.py
│   └── test_reranker.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

> `venv/`, `chroma_db/`, `.env`, and Python cache files are excluded from version control.

---

## Technologies

### AI / RAG

* OpenAI API
* LangChain
* Sentence Transformers
* Cross-Encoder Reranking

### Vector Database

* ChromaDB

### Document Processing

* PyPDF
* Recursive Character Text Splitting

### Application

* Streamlit

### Programming / Development

* Python
* Git
* GitHub

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/chunchiheng/aws-rag-assistant.git
cd aws-rag-assistant
```

### 2. Create a virtual environment

For Windows PowerShell:

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure OpenAI API Key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 5. Add AWS documentation

Place AWS documentation PDFs inside:

```text
data/documents/
```

For example:

```text
data/documents/
├── ec2_user_guide.pdf
├── s3_user_guide.pdf
└── vpc_user_guide.pdf
```

### 6. Build the vector database

Run:

```powershell
python src/ingest.py
```

This will:

```text
Load PDFs
   ↓
Split documents
   ↓
Generate embeddings
   ↓
Store vectors in ChromaDB
```

### 7. Start the application

From the project root:

```powershell
streamlit run src/app.py
```

The Streamlit application will then open in your browser.

---

## Adding More AWS Services

Additional AWS documentation can be added by placing the corresponding PDF files inside:

```text
data/documents/
```

For example:

```text
data/documents/
├── ec2_user_guide.pdf
├── s3_user_guide.pdf
├── vpc_user_guide.pdf
├── lambda_user_guide.pdf
└── iam_user_guide.pdf
```

Running the ingestion pipeline will process the documents and add their chunks to the vector database.

The deterministic document IDs are generated using the service name, page number, and chunk index to help identify individual chunks.

---

## Why Top 10 → Rerank → Top 3?

A simple approach would be to retrieve the Top 3 results directly from the vector database.

However, semantic similarity does not always guarantee that the retrieved chunk is the most relevant answer.

For example, an EC2 query may retrieve:

* A table of contents
* An introductory section
* An EC2 feature description
* An unrelated EC2 configuration section

Therefore, this project uses a two-stage retrieval strategy:

```text
Fast Retrieval
     ↓
Top 10
     ↓
More Accurate Reranking
     ↓
Top 3
     ↓
LLM Context
```

This balances **retrieval coverage, relevance, and LLM context size**.

---

## Limitations

The current implementation is intentionally designed as a simple RAG demonstration.

Current limitations include:

* No automated retrieval evaluation metrics
* No conversation memory
* No incremental document update detection
* Local ChromaDB storage
* No cloud deployment
* Limited metadata filtering
* Fixed Top 10 → Top 3 retrieval strategy

These areas can be improved in future iterations.

---

## Future Improvements

Potential improvements include:

* Metadata filtering by AWS service
* Incremental document ingestion
* Automatic document update detection
* Hybrid keyword + vector retrieval
* Retrieval evaluation using Recall@K / MRR
* Automated RAG evaluation
* Conversation history
* Additional AWS services such as Lambda, IAM, RDS, and DynamoDB
* Cloud deployment using AWS services
* Authentication and multi-user support

---

## Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation
* Document ingestion and preprocessing
* Text chunking strategies
* Text embeddings
* Vector databases
* Semantic similarity search
* Cross-encoder reranking
* LLM integration
* Prompt-based context grounding
* Source attribution
* Streamlit application development
* Python project structure
* Git and GitHub workflow

---

## Disclaimer

This project is an educational demonstration of a Retrieval-Augmented Generation system using AWS documentation.

AWS documentation is provided by Amazon Web Services and is not part of this project.
