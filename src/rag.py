import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from openai import OpenAI

from reranker import rerank_documents


load_dotenv()


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
# OpenAI client
# -------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_question(query):

    # -------------------------
    # Retrieve Top 10
    # -------------------------

    retrieved_documents = vectorstore.similarity_search(
        query,
        k=10,
    )


    # -------------------------
    # Rerank Top 10 → Top 3
    # -------------------------

    reranked_results = rerank_documents(
        query,
        retrieved_documents,
        top_k=3,
    )


    # -------------------------
    # Extract Top 3 documents
    # -------------------------

    top_documents = [
        document
        for document, score in reranked_results
    ]


    # -------------------------
    # Build context
    # -------------------------

    context = "\n\n".join(
        document.page_content
        for document in top_documents
    )


    # -------------------------
    # Build sources
    # -------------------------

    sources = []

    for document in top_documents:

        source = document.metadata.get("source")
        page = document.metadata.get("page")

        filename = os.path.basename(source)

        sources.append(
            f"{filename} — Page {page + 1}"
        )


    # -------------------------
    # Prompt
    # -------------------------

    prompt = f"""
You are an AWS documentation assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context,
say that you don't have enough information.

Context:
{context}

Question:
{query}
"""


    # -------------------------
    # Call OpenAI
    # -------------------------

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )


    answer = response.output_text


    return answer, sources