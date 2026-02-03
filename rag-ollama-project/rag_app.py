import ollama
from embedder import embed_text
from vector_store import add_document, search_docs

# -----------------------------
# INDEXING DOCUMENTS
# -----------------------------
def index_documents():
    docs = {
        "doc1": "Python is a high-level programming language.",
        "doc2": "Ollama provides local LLM inference on your machine.",
        "doc3": "RAG improves LLM output by retrieving relevant context."
    }

    for doc_id, content in docs.items():
        emb = embed_text(content)
        add_document(doc_id, content, emb)

    print("Documents indexed successfully.")

# -----------------------------
# RAG QUERY ENGINE
# -----------------------------
def rag_query(query):
    query_emb = embed_text(query)
    results = search_docs(query_emb)

    retrieved_docs = "\n".join(results["documents"][0])

    prompt = f"""
    You are an AI assistant with knowledge from the following documents:

    {retrieved_docs}

    Based on the above context, answer the question:
    {query}
    """

    response = ollama.generate(
        model="llama3.1",
        prompt=prompt
    )

    print("\nRAG Response:\n", response["response"])

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    index_documents()
    rag_query("What is RAG and why is it useful?")
