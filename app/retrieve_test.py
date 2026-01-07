import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = "vector_store"

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index(f"{INDEX_DIR}/asu_index.faiss")
with open(f"{INDEX_DIR}/metadata.json") as f:
    metadata = json.load(f)


def search(query, k=3):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for idx in indices[0]:
        results.append(metadata[idx]["source"])

    return results


if __name__ == "__main__":
    while True:
        q = input("\nAsk a test question (or 'exit'): ")
        if q.lower() == "exit":
            break
        print(search(q))
