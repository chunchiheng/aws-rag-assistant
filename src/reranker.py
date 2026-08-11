from sentence_transformers import CrossEncoder


# Load reranker model
model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(query, documents, top_k=3):
    """
    Rerank retrieved documents using a Cross-Encoder.

    Args:
        query: User's question.
        documents: List of LangChain Document objects.
        top_k: Number of documents to return.

    Returns:
        Top-k reranked documents with their scores.
    """

    # Create query-document pairs
    pairs = [
        (query, document.page_content)
        for document in documents
    ]

    # Calculate relevance scores
    scores = model.predict(pairs)

    # Combine documents with their scores
    scored_documents = list(zip(documents, scores))

    # Sort by relevance score (highest first)
    scored_documents.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Return top-k documents
    return scored_documents[:top_k]