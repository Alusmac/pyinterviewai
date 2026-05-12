from django.db import models


class Question(models.Model):
    """question table """
    LEVEL_CHOICES = [
        ("junior", "Junior"),
        ("mid", "Mid"),
        ("senior", "Senior"),
    ]

    text = models.TextField()

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="junior")

    def __str__(self):
        return self.text


class UserScore(models.Model):
    """user score table"""
    username = models.CharField(max_length=50)

    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    def score(self):
        return self.correct * 10
