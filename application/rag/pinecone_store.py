from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import json

load_dotenv()


with open("chunking_data.json" ,"r" ,encoding="utf-8") as file:
    chunks = json.load(file)


with open("embeddings.json" ,"r" ,encoding="utf-8") as file:
    embeddings = json.load(file)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "rbac-rag-chat-1"



# INIT INDEX

def init_index(dimension: int):
    try:
        existing_indexes = pc.list_indexes().names()

        if INDEX_NAME not in existing_indexes:
            pc.create_index(
                name=INDEX_NAME,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print("New index created")
        else:
            print("Index already exists")

        return pc.Index(INDEX_NAME)

    except Exception as e:
        print("Error durninginitializing index:", e)
        return None


# UPSERT VECTORS

def upsert_vectors(index, embeddings, chunks):
    try:
        vectors = []

        for i, (embedding, chunk) in enumerate(zip(embeddings, chunks)):

            vectors.append({
                "id": f"chunk-{i}",
                "values": list(embedding),
                "metadata": {
                    "text": chunk["text"],
                    "department": chunk["department"],
                    "file_name": chunk["file_name"],
                    "chunk_id": chunk["chunk_id"]
                }
            })

        
        
        index.upsert(vectors=vectors)

        print(f"Uploaded {len(vectors)} vectors successfully")

    except Exception as e:
        print("Error durning upserting vectors:", e)




index = init_index(384)
upsert_vectors(index,embeddings,chunks)

