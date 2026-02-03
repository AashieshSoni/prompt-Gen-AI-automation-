import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="rag_documents"
)

def add_document(doc_id, content, embedding):
    collection.add(
        ids=[doc_id],
        documents=[content],
        embeddings=[embedding]
    )

def search_docs(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results
