# app/core/generator.py

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an Arizona State University information agent.

Rules:
- Answer ONLY using the provided context.
- Do NOT use external knowledge.
- Do NOT guess or assume.
- If the answer is not explicitly stated in the context, say:
  "I do not have verified ASU information on that topic."
- Keep answers short, factual, and neutral.
"""

def generate_answer(question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n".join(context_chunks)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Context:
{context_text}

Question:
{question}
"""
            }
        ],
        temperature=0,
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()
