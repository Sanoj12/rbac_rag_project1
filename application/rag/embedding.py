from sentence_transformers import SentenceTransformer
import os
import json



with open("chunking_data.json" ,"r" ,encoding="utf-8") as file:
    chunks = json.load(file)

texts = [ch["text"] for ch in chunks]

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(texts: list):
    try:
        embeddings = model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    except Exception as e:
        print("Embedding error:", e)
        return []

embeddings = create_embeddings(texts)


with open("embeddings.json", "w", encoding="utf-8") as file:
    json.dump(embeddings, file, indent=2)
    print("embeddings.json successfully created")