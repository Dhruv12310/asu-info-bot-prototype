# app/core/metrics.py

from collections import Counter
from datetime import datetime

metrics = {
    "total_queries": 0,
    "cache_hits": 0,
    "refusals": 0,
    "successful_answers": 0,
}

unanswered_questions = Counter()


def log_query():
    metrics["total_queries"] += 1


def log_cache_hit():
    metrics["cache_hits"] += 1


def log_refusal(query: str):
    metrics["refusals"] += 1
    unanswered_questions[query.lower()] += 1


def log_success():
    metrics["successful_answers"] += 1


def get_metrics_snapshot():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "metrics": metrics,
        "top_unanswered_questions": unanswered_questions.most_common(5),
    }
