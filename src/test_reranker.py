from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from reranker import rerank_documents


# -------------------------
# Load embedding model
# -------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------
# Load ChromaDB
# -------------------------

vectorstore = Chroma(
    collection_name="aws_documents",
    embedding_function=embeddings,
    persist_directory="chroma_db",
)


# -------------------------
# User query
# -------------------------

query = "What is Amazon S3?"


# -------------------------
# Retrieve Top 10
# -------------------------

results = vectorstore.similarity_search_with_score(
    query,
    k=10
)


documents = [
    document
    for document, score in results
]


print(f"\nQuery: {query}")
print(f"Initial retrieval: {len(documents)} documents")


# -------------------------
# Rerank Top 10 → Top 3
# -------------------------

reranked_results = rerank_documents(
    query,
    documents,
    top_k=3
)


# -------------------------
# Display results
# -------------------------

print("\nReranked Top 3:\n")


for i, (document, score) in enumerate(
    reranked_results,
    start=1
):

    print(f"--- Result {i} ---")

    print(f"Reranker score: {score}")

    print("\nContent:")
    print(
        document.page_content[:500]
    )

    print("\nMetadata:")

    metadata = {
        "source": document.metadata.get("source"),
        "page": document.metadata.get("page"),
    }

    print(metadata)

    print()