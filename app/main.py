from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.query import handle_query
from app.core.metrics import get_metrics_snapshot

app = FastAPI(
    title="ASU Information Agent",
    description="Domain-restricted ASU information system using RAG",
    version="1.0.0"
)

# ✅ CORS configuration (frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For demo; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def query_endpoint(req: QueryRequest):
    return handle_query(req.query)

@app.get("/metrics")
def metrics_endpoint():
    return get_metrics_snapshot()

@app.get("/health")
def health_check():
    return {"status": "ok"}
