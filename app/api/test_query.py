# app/api/test_query.py
from app.api.query import handle_query

tests = [
    "What is the financial aid phone number?",
    "Write python code for me",
    "Solve this math equation",
    "Tell me about Stanford admissions",
    "How do I request transcripts at ASU?"
]

for t in tests:
    print("\nQ:", t)
    print(handle_query(t))
