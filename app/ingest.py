import os
import json
import faiss
import markdown
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/raw"
INDEX_DIR = "vector_store"
CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

os.makedirs(INDEX_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_markdown_files():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md"):
            path = os.path.join(DATA_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({
                "source": filename,
                "content": text
            })
    return docs


def chunk_text(text):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + CHUNK_SIZE
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def main():
    documents = load_markdown_files()
    all_chunks = []
    metadata = []

    for doc in documents:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({
                "source": doc["source"]
            })

    print(f"Total chunks: {len(all_chunks)}")

    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, os.path.join(INDEX_DIR, "asu_index.faiss"))

    with open(os.path.join(INDEX_DIR, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print("Ingestion complete. FAISS index created.")


if __name__ == "__main__":
    main()
