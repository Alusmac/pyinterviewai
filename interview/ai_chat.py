import os
import json

from django.http import HttpResponse
from openai import OpenAI
from groq import Groq

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_chat_prompt(message: str) -> str:
    """Prompt building for AI"""
    return f"""
You are iChat, a senior AI programming mentor.

Your role:
- Teach Python, system design, algorithms
- Explain concepts simply
- Give examples and code
- Help interview preparation
- NEVER grade or score answers

User message:
{message}

Return ONLY valid JSON:

{{
  "response": "main explanation",
  "example": "code example if needed",
  "tip": "short learning tip"
}}

Rules:
- Be clear and structured
- Always give practical examples
- Focus on learning, not evaluation
"""


def call_openai_chat(prompt: str) -> HttpResponse:
    """Call OpenAI Chat
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def call_groq_chat(prompt: str) -> HttpResponse:
    """Call GroQ Chat
    """
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def safe_parse(text: str) -> str:
    """Safely parse text
    """
    try:
        return json.loads(text)
    except Exception:
        return {
            "response": text,
            "example": "",
            "tip": ""
        }


def get_ai_chat(message: str):
    """aiChat assistant for learning + explanations
    """

    prompt = build_chat_prompt(message)

    try:
        response = call_groq_chat(prompt)
        return safe_parse(response)

    except Exception as e:
        print("Groq chat failed:", e)

    try:
        response = call_openai_chat(prompt)
        return safe_parse(response)

    except Exception as e:
        print("OpenAI chat failed:", e)

    return {
        "response": "AI chat is currently unavailable",
        "example": "",
        "tip": ""
    }
