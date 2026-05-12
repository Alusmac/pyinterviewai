import os
import re

from openai import OpenAI
from groq import Groq

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_prompt(question: str, answer: str) -> str:
    """prompt building for AI
    """
    return f"""
You are a strict Python technical interviewer.

Question: {question}

Candidate answer: {answer}

Evaluate the answer and respond EXACTLY in this format:

Level: Junior / Mid / Senior
Score: 0-10
Feedback: short explanation of the answer quality
Improvement: how to improve the answer

Rules:
- Junior = basic understanding, missing key concepts
- Mid = solid understanding, minor gaps
- Senior = deep understanding, best practices, clear reasoning
"""


def call_openai(question: str, answer: str) -> str:
    """ Call OpenAI
    """
    prompt = build_prompt(question, answer)

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def call_groq(question: str, answer: str) -> str:
    """ Call GroQ
    """
    prompt = build_prompt(question, answer)

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def parse_ai_response(text: str) -> dict:
    """ Parse AI
    """
    level_match = re.search(r"Level:\s*(Junior|Mid|Senior)", text)
    score_match = re.search(r"Score:\s*(\d+)", text)

    return {
        "level": level_match.group(1) if level_match else "Unknown",
        "score": score_match.group(1) if score_match else "N/A",
        "raw": text
    }


def get_ai_feedback(question: str, answer: str) -> str:
    """ Get AI
    """

    try:
        response = call_openai(question, answer)
    except Exception as e:
        print("OpenAI failed:", e)

        try:
            response = call_groq(question, answer)
        except Exception as e:
            print("Groq failed:", e)

            return {
                "level": "Unknown",
                "score": "N/A",
                "raw": "AI services are currently unavailable."
            }

    return parse_ai_response(response)
