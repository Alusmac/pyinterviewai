import os
import json

from openai import OpenAI
from groq import Groq


# =========================
# Clients
# =========================

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================
# PROMPT (STRICT JSON ONLY)
# =========================

def build_prompt(question, answer):
    return f"""
You are a strict technical interview evaluator.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON (no markdown, no text).

JSON format:
{{
  "level": "Junior | Mid | Senior",
  "score": 0-10,
  "feedback": "short clear explanation",
  "improvement": "how to improve answer"
}}

Rules:
- Be strict
- Be concise
- No extra text
"""


# =========================
# OPENAI CALL
# =========================

def call_openai(question, answer):
    prompt = build_prompt(question, answer)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# =========================
# GROQ FALLBACK
# =========================

def call_groq(question, answer):
    prompt = build_prompt(question, answer)

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# =========================
# SAFE JSON PARSER
# =========================

def safe_parse(text):
    try:
        data = json.loads(text)

        return {
            "level": data.get("level", "Unknown"),
            "score": data.get("score", 0),
            "feedback": data.get("feedback", ""),
            "improvement": data.get("improvement", "")
        }

    except Exception:
        return {
            "level": "Unknown",
            "score": 0,
            "feedback": "AI response parsing failed",
            "improvement": ""
        }


# =========================
# MAIN FUNCTION
# =========================

def get_ai_feedback(question, answer):
    """
    Returns structured AI result for frontend sidebar
    """

    # 1. Try OpenAI
    try:
        response = call_openai(question, answer)
    except Exception as e:
        print("OpenAI failed:", e)

        # 2. fallback Groq
        try:
            response = call_groq(question, answer)
        except Exception as e:
            print("Groq failed:", e)

            return {
                "level": "Unknown",
                "score": 0,
                "feedback": "AI services are unavailable",
                "improvement": ""
            }

    return safe_parse(response)