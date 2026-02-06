'''chromadb long term memory
agent/vectorstore_client.py

'''
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("api_rlaif_memory")

def store_learning(spec, results, reward, insights):
    collection.add(
        documents=[results],
        metadatas=[{
            "reward": reward,
            "insights": insights,
            "spec_hash": hash(spec)
        }],
        ids=[str(hash(results))]
    )
