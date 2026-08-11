from pathlib import Path
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# ============================================================
# 1. Find all PDF files
# ============================================================

DOCUMENTS_PATH = Path("data/documents")

pdf_files = list(DOCUMENTS_PATH.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files:")

for pdf_file in pdf_files:
    print(f"- {pdf_file.name}")


# ============================================================
# 2. Load all PDFs
# ============================================================

all_documents = []

for pdf_file in pdf_files:

    print(f"\nLoading: {pdf_file.name}")

    loader = PyPDFLoader(str(pdf_file))
    documents = loader.load()

    print(f"Number of pages: {len(documents)}")

    # Add service metadata
    filename = pdf_file.name.lower()

    if filename.startswith("ec2_"):
        service = "EC2"

    elif filename.startswith("s3_"):
        service = "S3"

    elif filename.startswith("vpc_"):
        service = "VPC"

    else:
        service = "Unknown"

    for document in documents:
        document.metadata["service"] = service

    all_documents.extend(documents)


print(
    f"\nTotal number of pages across all PDFs: "
    f"{len(all_documents)}"
)


# ============================================================
# 3. Create text splitter
# ============================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)


# ============================================================
# 4. Split all documents into chunks
# ============================================================

chunks = text_splitter.split_documents(all_documents)

print(f"Total number of chunks: {len(chunks)}")


# ============================================================
# 5. Create embedding model
# ============================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ============================================================
# 6. Create deterministic IDs
# ============================================================

chunk_ids = []

service_chunk_counters = {}

for chunk in chunks:

    source = chunk.metadata.get("source", "unknown")
    page = chunk.metadata.get("page", "unknown")
    service = chunk.metadata.get("service", "unknown")

    # Keep track of chunk number separately for each service
    if service not in service_chunk_counters:
        service_chunk_counters[service] = 0

    chunk_number = service_chunk_counters[service]

    chunk_id = (
        f"{service.lower()}_"
        f"page_{page}_"
        f"chunk_{chunk_number}"
    )

    chunk_ids.append(chunk_id)

    service_chunk_counters[service] += 1


# Print some example IDs

print("\nFirst 10 chunk IDs:")

for chunk_id in chunk_ids[:10]:
    print(chunk_id)


# ============================================================
# 7. Create ChromaDB
# ============================================================

vectorstore = Chroma(
    collection_name="aws_documents",
    embedding_function=embeddings,
    persist_directory="chroma_db",
)


# ============================================================
# 8. Add chunks to ChromaDB in batches
# ============================================================

BATCH_SIZE = 1000

for i in range(0, len(chunks), BATCH_SIZE):

    batch_chunks = chunks[i:i + BATCH_SIZE]
    batch_ids = chunk_ids[i:i + BATCH_SIZE]

    vectorstore.add_documents(
        documents=batch_chunks,
        ids=batch_ids,
    )

    print(
        f"Added chunks "
        f"{i} - "
        f"{i + len(batch_chunks) - 1}"
    )


# ============================================================
# 9. Finished
# ============================================================

print("\nSuccessfully added all documents to ChromaDB.")