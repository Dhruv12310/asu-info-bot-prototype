# app/api/query.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.intent_filter import allow_query
from app.core.confidence import is_confident
from app.core.refusals import out_of_scope, insufficient_info
from app.core.generator import generate_answer
from app.core.post_validator import validate_answer
from app.core.cache import get_cached_response, set_cached_response
from app.core.metrics import (
    log_query,
    log_cache_hit,
    log_refusal,
    log_success,
)

INDEX_DIR = "vector_store"
DATA_DIR = "data/raw"
TOP_K = 3

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and metadata
index = faiss.read_index(f"{INDEX_DIR}/asu_index.faiss")
with open(f"{INDEX_DIR}/metadata.json", encoding="utf-8") as f:
    metadata = json.load(f)


def handle_query(query: str):
    """
    Full guarded query pipeline:
    0) Metrics logging
    1) Cache check
    2) Intent & scope filter
    3) Semantic retrieval
    4) Confidence gate
    5) Context-only LLM answer
    6) Post-answer validation (fail closed)
    7) Cache + success logging
    """

    # 0️⃣ Log incoming query
    log_query()

    # 1️⃣ Cache check (fast path)
    cached = get_cached_response(query)
    if cached:
        log_cache_hit()
        return cached

    # 2️⃣ Intent & scope filter
    if not allow_query(query):
        log_refusal(query)
        return out_of_scope()

    # 3️⃣ Retrieval
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, TOP_K)

    # Debug (safe during development / demo)
    print("DEBUG distance:", distances[0][0])

    # 4️⃣ Confidence gate (fail closed)
    if not is_confident(distances):
        log_refusal(query)
        return insufficient_info()

    # 5️⃣ Load context from retrieved documents
    context_chunks = []
    source_files = set()

    for idx in indices[0]:
        source = metadata[idx]["source"]
        source_files.add(source)

        with open(f"{DATA_DIR}/{source}", encoding="utf-8") as f:
            context_chunks.append(f.read())

    # 6️⃣ Generate answer (LLM = formatter only)
    answer = generate_answer(query, context_chunks)

    # 7️⃣ Post-answer validation (final safety layer)
    if not validate_answer(answer):
        log_refusal(query)
        return insufficient_info()

    # 8️⃣ Successful response
    response = {
        "answer": answer,
        "sources": sorted(source_files)
    }

    log_success()
    set_cached_response(query, response)

    return response
