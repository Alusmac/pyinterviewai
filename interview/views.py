from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Question, UserScore
from .ai import get_ai_feedback

from django.http import JsonResponse
from .ai_chat import get_ai_chat


def home(request: HttpRequest) -> HttpResponse:
    """ home view
    """
    username = request.session.get("username")

    questions = Question.objects.filter(level="junior")

    user_score = None
    if username:
        user_score, _ = UserScore.objects.get_or_create(username=username)

    return render(request, "home.html", {
        "questions": questions,
        "username": username,
        "user_score": user_score
    })


def question_view(request: HttpRequest, id: int) -> HttpResponse:
    """ question view
    """
    question = get_object_or_404(Question, id=id)

    return render(request, "question.html", {
        "question": question
    })


def result(request: HttpRequest) -> HttpResponse:
    """ result view
    """
    if request.method == "POST":

        question_id = request.POST.get("question_id")
        answer = request.POST.get("answer")
        username = request.session.get("username")

        question = get_object_or_404(Question, id=question_id)

        result_data = get_ai_feedback(question.text, answer)

        score = int(result_data.get("score", 0))
        is_correct = score >= 7

        if username:
            update_score(username, is_correct)

        return JsonResponse({
            "level": result_data.get("level"),
            "score": score,
            "feedback": result_data.get("feedback"),
            "improvement": result_data.get("improvement")
        })

    return JsonResponse({"error": "POST only"})


def questions_by_level(request: HttpRequest, level: int) -> HttpResponse:
    """ questions_by_level view
    """
    questions = Question.objects.filter(level=level)

    username = request.session.get("username")
    user_score = None

    if username:
        user_score, _ = UserScore.objects.get_or_create(username=username)

    return render(request, "home.html", {
        "questions": questions,
        "level": level,
        "username": username,
        "user_score": user_score
    })


def set_user(request: HttpRequest) -> HttpResponse:
    """ set_user view
    """
    if request.method == "POST":
        username = request.POST.get("username")

        request.session["username"] = username
        UserScore.objects.get_or_create(username=username)

    return redirect("home")


def update_score(username: str | int, is_correct: bool) -> bool:
    """ update_score view
    """
    user, _ = UserScore.objects.get_or_create(username=username)

    if is_correct:
        user.correct += 1
    else:
        user.wrong += 1

    user.save()


def ai_chat(request: HttpRequest) -> HttpResponse:
    """ ai_chat view
    """
    if request.method == "POST":
        message = request.POST.get("message")

        if not message:
            return JsonResponse({"error": "empty message"})

        result = get_ai_chat(message)

        return JsonResponse(result)

    return JsonResponse({"error": "POST only"})
