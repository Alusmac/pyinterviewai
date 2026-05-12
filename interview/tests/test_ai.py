import pytest
from unittest.mock import patch

from interview.ai import get_ai_feedback, parse_ai_response
from interview.ai_chat import get_ai_chat, safe_parse


def test_parse_ai_response() -> None:
    """test the AI response parsing
    """
    text = """
    Level: Mid
    Score: 8
    Feedback: good
    Improvement: better naming
    """

    result = parse_ai_response(text)

    assert result["level"] == "Mid"
    assert result["score"] == "8"


@patch("interview.ai.call_openai")
def test_get_ai_feedback_openai(mock_openai) -> None:
    """test to get AI feedback openai
    """
    mock_openai.return_value = """
    Level: Senior
    Score: 9
    Feedback: great
    Improvement: none
    """

    result = get_ai_feedback("Q", "A")

    assert result["level"] == "Senior"
    assert result["score"] == "9"


@patch("interview.ai.call_openai", side_effect=Exception("fail"))
@patch("interview.ai.call_groq")
def test_get_ai_feedback_fallback(mock_groq, mock_openai) -> None:
    """test to get AI feedback fallback
    """
    mock_groq.return_value = """
    Level: Junior
    Score: 5
    Feedback: ok
    Improvement: practice more
    """

    result = get_ai_feedback("Q", "A")

    assert result["level"] == "Junior"
    assert result["score"] == "5"


def test_safe_parse_valid_json() -> None:
    """test the safe_parse valid function
    """
    text = '{"response": "hello", "example": "code", "tip": "learn"}'

    result = safe_parse(text)

    assert result["response"] == "hello"


def test_safe_parse_invalid_json() -> None:
    """test the safe_parse invalid json
    """
    text = "NOT JSON STRING"

    result = safe_parse(text)

    assert "NOT JSON STRING" in result["response"]


@patch("interview.ai_chat.call_groq_chat")
def test_get_ai_chat_success(mock_groq) -> None:
    """test the AI chat success
    """
    mock_groq.return_value = '{"response": "hi", "example": "", "tip": "t"}'

    result = get_ai_chat("hello")

    assert result["response"] == "hi"
