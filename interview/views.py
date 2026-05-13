import json
from datetime import timedelta
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Avg
from django.db.models.functions import TruncDate

from .models import Question, UserScore, InterviewAttempt
from .ai import get_ai_feedback
from .ai_chat import get_ai_chat


def home(request: HttpRequest) -> HttpResponse:
    """ home view
     """
    username = request.session.get("username")
    questions = Question.objects.filter(level="Junior")

    user_score = None
    if username:
        user_score, _ = UserScore.objects.get_or_create(username=username)

    return render(request, "home.html", {
        "questions": questions,
        "username": username,
        "user_score": user_score,
        "current_level": "Junior"
    })


def questions_by_level(request: HttpRequest, level: str) -> HttpResponse:
    """ filter for level  (URL: /level/junior/ )
    """
    username = request.session.get("username")
    questions = Question.objects.filter(level=level)

    user_score = None
    if username:
        user_score, _ = UserScore.objects.get_or_create(username=username)

    return render(request, "home.html", {
        "questions": questions,
        "username": username,
        "user_score": user_score,
        "current_level": level
    })


def question_view(request: HttpRequest, id: int) -> HttpResponse:
    """ Question page with an editor and a timer
     """
    question = get_object_or_404(Question, id=id)
    return render(request, "question.html", {
        "question": question,
        "timer": 60
    })


def result(request: HttpRequest) -> HttpResponse:
    """  Processing the AI's response and saving it to the history
    """
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        answer = request.POST.get("answer", "")
        username = request.session.get("username")

        question = get_object_or_404(Question, id=question_id)
        result_data = get_ai_feedback(question.text, answer)

        score = int(result_data.get("score", 0))
        is_correct = score >= 7

        if username:
            update_score(username, is_correct)

            InterviewAttempt.objects.create(
                username=username,
                question=question,
                score=score
            )

        return JsonResponse({
            "score": score,
            "feedback": result_data.get("feedback"),
            "improvement": result_data.get("improvement"),
            "level": result_data.get("level")
        })

    return JsonResponse({"error": "POST only"}, status=405)


def profile_view(request: HttpRequest) -> HttpResponse:
    """profile view
    """
    username = request.session.get("username")
    if not username:
        return redirect("home")

    last_week = timezone.now() - timedelta(days=7)
    stats_query = (
        InterviewAttempt.objects.filter(username=username, date__gte=last_week)
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(avg_score=Avg('score'))
        .order_by('day')
    )

    stats_data = [
        {"day": item['day'].strftime('%d.%m'), "avg_score": float(item['avg_score'])}
        for item in stats_query
    ]

    history = InterviewAttempt.objects.filter(username=username).order_by('-date')[:10]
    user_stats, _ = UserScore.objects.get_or_create(username=username)

    return render(request, "profile.html", {
        "username": username,
        "stats": json.dumps(stats_data),
        "history": history,
        "user_stats": user_stats
    })


def set_user(request: HttpRequest) -> HttpResponse:
    """set username
    """
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            request.session["username"] = username
            UserScore.objects.get_or_create(username=username)
    return redirect("home")


def update_score(username: str, is_correct: bool):
    """update score
     """
    user, _ = UserScore.objects.get_or_create(username=username)
    if is_correct:
        user.correct += 1
    else:
        user.wrong += 1
    user.save()


def ai_chat(request: HttpRequest) -> HttpResponse:
    """ Chat with AI
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")
        except json.JSONDecodeError:
            message = request.POST.get("message", "")

        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)

        result = get_ai_chat(message)
        return JsonResponse(result)

    return render(request, "ai_chat.html")
