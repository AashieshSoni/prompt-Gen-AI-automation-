1. Setup Instructions
Step 1: Create project folder
mkdir rag-ollama-project
cd rag-ollama-project

Step 2: Create virtual environment
python -m venv .venv
source .venv/bin/activate     # Linux / Mac
# OR
# .venv\Scripts\activate      # Windows

Step 3: Install Ollama Python SDK
pip install ollama chromadb

Step 4: Pull required Ollama models
ollama pull nomic-embed-text
ollama pull llama3.1           # or your preferred LLM

Step 5: Run the App
python rag_app.py

Step : 6
Documents indexed successfully.

RAG Response:
RAG (Retrieval Augmented Generation) combines search with LLMs to improve accuracy...


ecommendation Based on “Automation / REST API Testing” Use Case

If you're building a testable RAG API (for automated testing), anarojoecheburua/RAG-with-Langchain-and-FastAPI or AshishSinha5/rag_api are probably the most straightforward.

If you want something more “production/hybrid search” ready, Hybrid-Search-RAG (kolhesamiksha) or Hybrid-Search-For-Rag (Syed007Hassan) are strong picks.

For cloud-based, enterprise-style RAG, the Azure Samples repo is a very good reference.

