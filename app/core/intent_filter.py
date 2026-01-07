# app/core/intent_filter.py
import re

BLOCKED_KEYWORDS = [
    "code", "program", "python", "java", "c++",
    "homework", "assignment", "solve", "derivative",
    "integral", "math", "equation", "proof",
    "essay", "story", "poem", "write a"
]

ASU_HINTS = [
    "asu", "arizona state", "sun devil",
    "registrar", "financial aid", "dean",
    "housing", "campus", "advising", "it help"
]

def is_blocked(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in BLOCKED_KEYWORDS)

def is_asu_related(query: str) -> bool:
    q = query.lower()
    return any(h in q for h in ASU_HINTS)

def allow_query(query: str) -> bool:
    if is_blocked(query):
        return False
    if not is_asu_related(query):
        return False
    return True
