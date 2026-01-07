# ASU Information Agent (RAG Prototype)

A **domain-restricted ASU information chatbot** that answers using only **verified ASU documents** via **Retrieval-Augmented Generation (RAG)**.

 No “ChatGPT wrapper” behavior  
 Refuses coding/math/external-university questions  
 Answers are **context-only** + **post-validated**  
 Shows **sources** for every answer  
 Built-in **cache + metrics** for demo and auditing  
 Clean API with Swagger docs (`/docs`) and lightweight ChatGPT-like UI

---

## Demo Screenshot (UI)
> Add your screenshot here later (optional): `docs/ui.png`

---

## What This Project Is (and Isn’t)

### Is
- A governed ASU-only information assistant
- RAG pipeline: Markdown → embeddings → FAISS index → retrieval → answer formatting
- Built to scale toward production architecture (pgvector later)

### Is not
- A general-purpose assistant
- A code tutor / math solver / external admissions guide
- A “free-form” LLM chat

---

## Architecture (Current Prototype)

Student Browser UI (frontend)
|
| POST /query
v
FastAPI API (app/main.py)
|
| Intent Filter + Cache + Retrieval + Confidence Gate
v
FAISS Vector Index (vector_store/asu_index.faiss)
|
v
Top-K Context (from data/raw/*.md)
|
v
OpenAI GPT-3.5 (formatter only)
|
v
Post-Answer Validator (fail closed)
|
v
Response + Sources

yaml
Copy code

---

## Project Structure

asu-info-bot/
├── app/
│   ├── api/
│   │   ├── query.py            # main guarded query pipeline
│   │   └── test_query.py       # local CLI tests
│   │
│   ├── core/
│   │   ├── intent_filter.py    # blocks non-ASU / coding / math
│   │   ├── confidence.py       # similarity threshold gating
│   │   ├── generator.py        # GPT formatter (context-only)
│   │   ├── post_validator.py   # rejects unsafe / ungrounded answers
│   │   ├── cache.py            # memoizes responses
│   │   └── metrics.py          # counters + unanswered questions
│   │
│   ├── ingest.py               # builds FAISS + metadata from markdown
│   └── main.py                 # FastAPI entrypoint + endpoints
│
├── data/
│   └── raw/                    # ASU knowledge base files (markdown)
│
├── vector_store/
│   ├── asu_index.faiss         # generated FAISS index
│   └── metadata.json           # generated metadata for retrieval
│
├── frontend/
│   ├── index.html              # ChatGPT-style UI
│   ├── style.css
│   └── app.js
│
├── .env                        # NOT committed (OpenAI key)
├── requirements.txt
├── README.md
└── .gitignore


yaml
Copy code

---

## Endpoints

### ✅ API Docs
- `GET /docs` → Swagger UI
- `GET /openapi.json` → OpenAPI schema

### ✅ Core Endpoints
- `POST /query` → ask a question
- `GET /health` → health check
- `GET /metrics` → usage counters (privacy-safe)

---

## Setup (Windows / macOS / Linux)

### 1) Create virtual environment
```bash
python -m venv venv

## 2) Activate the Virtual Environment

### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
macOS / Linux
bash
Copy code
source venv/bin/activate
3) Install Dependencies
bash
Copy code
pip install -r requirements.txt
Configure OpenAI Key (.env)
Create a file named .env in the project root:

env
Copy code
OPENAI_API_KEY=your_key_here
✅ The .gitignore prevents committing this file.

Build the Vector Index (Ingestion)
This step reads data/raw/*.md, chunks the documents, generates embeddings, and writes:

vector_store/asu_index.faiss

vector_store/metadata.json

Run:

bash
Copy code
python app/ingest.py
Run Backend (FastAPI)
bash
Copy code
uvicorn app.main:app --reload
Open:

Swagger Docs: http://127.0.0.1:8000/docs

Metrics: http://127.0.0.1:8000/metrics

Run Frontend
Option A (double-click)
Open:

bash
Copy code
frontend/index.html
Option B (recommended – avoids browser quirks)
bash
Copy code
cd frontend
python -m http.server 5500
Then open:

cpp
Copy code
http://127.0.0.1:5500
Example Queries (For Demo)
✅ ASU Questions (Should Answer)
csharp
Copy code
What is the financial aid phone number?
How do I request transcripts at ASU?
How do I contact the Dean of Students office?
❌ Non-ASU / Disallowed (Should Refuse)
kotlin
Copy code
Write python code for me
Solve this math equation
Tell me about Stanford admissions
How Safety Works
This system is designed to fail closed.

Intent Filter
kotlin
Copy code
Blocks coding / math / external-university questions
Similarity Threshold
csharp
Copy code
If retrieval confidence is low → refuses
Context-only LLM
css
Copy code
GPT is used as a formatter, not a knowledge source
Post-answer Validator
python
Copy code
Rejects anything that looks ungrounded or overconfident
Metrics (Observability)
GET /metrics returns:

nginx
Copy code
total_queries
cache_hits
refusals
successful_answers
top_unanswered_questions
This helps iterate and improve the dataset based on real usage.

Roadmap (Production Scale)
Prototype → Production plan:

pgsql
Copy code
- Upgrade from file-based FAISS to Postgres + pgvector
- Add admin tooling for data ingestion / updates
- Add ASU SSO integration (if deployed officially)
- Add monitoring + dashboards + rate limiting
