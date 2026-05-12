import pytest


@pytest.fixture
def user_data() -> dict:
    """user_data fixture"""
    return {
        "username": "testuser",
        "correct": 3,
        "wrong": 1
    }
