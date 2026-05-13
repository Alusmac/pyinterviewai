from django.db import models
from django.utils import timezone


class Question(models.Model):
    """questions table
    """
    LEVEL_CHOICES = [
        ("junior", "Junior"),
        ("mid", "Mid"),
        ("senior", "Senior"),
    ]

    text = models.TextField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="junior")

    def __str__(self):
        return f"[{self.level.upper()}] {self.text[:50]}..."


class UserScore(models.Model):
    """user scores table
    """
    username = models.CharField(max_length=50, unique=True)  # Додано unique=True для надійності
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.username}"

    @property
    def total_attempts(self):
        return self.correct + self.wrong

    @property
    def success_rate(self):
        if self.total_attempts == 0:
            return 0
        return round((self.correct / self.total_attempts) * 100, 1)


class InterviewAttempt(models.Model):
    """The history of each response for creating a progress chart
    """
    username = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.username} - {self.score}/10 on {self.date.strftime('%Y-%m-%d')}"
