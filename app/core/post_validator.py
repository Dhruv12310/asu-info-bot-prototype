# app/core/post_validator.py

OVERCONFIDENT_PHRASES = [
    "always",
    "never",
    "guaranteed",
    "definitely",
    "must",
    "will ensure",
    "100%",
    "required to",
]

EXTERNAL_KNOWLEDGE_HINTS = [
    "generally",
    "in most cases",
    "typically",
    "usually",
    "according to law",
    "federal law",
    "state law",
]

def validate_answer(answer: str) -> bool:
    """
    Returns True if answer is safe to return.
    Returns False if answer should be rejected.
    """

    text = answer.lower()

    # 1️⃣ Overconfidence / authoritative tone
    for phrase in OVERCONFIDENT_PHRASES:
        if phrase in text:
            return False

    # 2️⃣ External / generalized knowledge hints
    for phrase in EXTERNAL_KNOWLEDGE_HINTS:
        if phrase in text:
            return False

    # 3️⃣ Empty or suspiciously short answers
    if len(text.strip()) < 5:
        return False

    return True
