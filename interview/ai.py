import os
import re
import json
from openai import OpenAI
from groq import Groq

# Clients initialization
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question: str, answer: str) -> str:
    """
    Constructs an English-only prompt for the AI.
    Includes instructions for analyzing technical accuracy and speech confidence.
    """
    return f"""
You are a Senior Python Technical Interviewer and Communication Coach.
Analyze the candidate's response provided below. 

Note: The answer was captured via voice-to-text, so it might contain filler words or minor transcription errors. Evaluate both technical knowledge and communication confidence.

Context:
- Interview Question: {question}
- Candidate's Answer: {answer}

Your Task:
1. Technical Evaluation: Assess the correctness of the Python-specific concepts.
2. Communication Analysis: Identify filler words (e.g., 'um', 'like', 'well', 'kind of') and assess if the candidate sounds confident or hesitant.
3. Formatting: Respond EXACTLY in the format below.

Response Format:
Level: Junior / Mid / Senior
Score: 0-10
Feedback: [Provide a comprehensive evaluation. If the answer is incorrect or incomplete, explain the 'why' and provide the CORRECT Python code snippet as a solution.]
Improvement: [Suggest actionable steps for technical growth and tips to reduce speech fillers or improve verbal delivery.]

Strict Rules:
- If the answer is empty or irrelevant, the score must be 0-2.
- If the answer is correct but sounds very hesitant (lots of fillers), penalize the score by 1-2 points.
- ALWAYS include a correct code example in the Feedback section if the candidate's logic is flawed.
"""

def parse_ai_response(text: str) -> dict:
    """Extracts all fields using robust regular expressions."""
    # Using flags=re.IGNORECASE and re.DOTALL for safer parsing
    level_match = re.search(r"Level:\s*(.*)", text, re.IGNORECASE)
    score_match = re.search(r"Score:\s*(\d+)", text, re.IGNORECASE)
    feedback_match = re.search(r"Feedback:\s*(.*?)(?=Improvement:|$)", text, re.DOTALL | re.IGNORECASE)
    improvement_match = re.search(r"Improvement:\s*(.*)", text, re.DOTALL | re.IGNORECASE)

    return {
        "level": level_match.group(1).strip() if level_match else "Unknown",
        "score": score_match.group(1).strip() if score_match else "0",
        "feedback": feedback_match.group(1).strip() if feedback_match else "No feedback provided.",
        "improvement": improvement_match.group(1).strip() if improvement_match else "No improvement tips.",
        "raw": text
    }

def call_openai(question: str, answer: str) -> str:
    prompt = build_prompt(question, answer)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a professional technical interviewer."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def call_groq(question: str, answer: str) -> str:
    prompt = build_prompt(question, answer)
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_ai_feedback(question: str, answer: str) -> dict:
    """Main entry point for getting feedback with fallback logic."""
    try:
        response = call_openai(question, answer)
    except Exception as e:
        print(f"OpenAI failed: {e}")
        try:
            response = call_groq(question, answer)
        except Exception as e:
            print(f"Groq failed: {e}")
            return {
                "level": "N/A",
                "score": "0",
                "feedback": "AI Mentor is currently offline. Please check your API keys or connection.",
                "improvement": "Check the server logs for more details.",
                "raw": "Error"
            }

    return parse_ai_response(response)

def get_ai_chat(message: str) -> dict:
    """Generic chat helper for the AI Mentor assistant."""
    try:
        # Using Groq for faster chat responses
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful and concise Python Mentor."},
                {"role": "user", "content": message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception:
        return {"reply": "I'm sorry, I'm having trouble responding right now. Let's try again in a moment!"}