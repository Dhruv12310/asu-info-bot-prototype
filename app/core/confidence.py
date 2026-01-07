# app/core/confidence.py

# Empirically safe for MiniLM + L2
SIMILARITY_THRESHOLD = 1.2

def is_confident(distances):
    """
    distances: numpy array shape (1, k)
    Lower distance = better match
    """
    best_distance = distances[0][0]
    return best_distance <= SIMILARITY_THRESHOLD
