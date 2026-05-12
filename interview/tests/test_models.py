import pytest
from interview.models import Question, UserScore


@pytest.mark.django_db
def test_question_str() -> None:
    """test the question string function
    """
    q = Question.objects.create(
        text="What is Python?",
        level="junior"
    )
    assert str(q) == "What is Python?"


@pytest.mark.django_db
def test_user_score_calculation() -> None:
    """test the user score calculation
    """
    user = UserScore.objects.create(
        username="testuser",
        correct=3,
        wrong=2
    )

    assert user.score() == 30
