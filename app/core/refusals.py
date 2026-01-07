# app/core/refusals.py
def out_of_scope():
    return {
        "answer": "I can help with official Arizona State University information only.",
        "sources": []
    }

def insufficient_info():
    return {
        "answer": "I don’t have verified ASU information on that topic.",
        "sources": []
    }
