from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """class question
    """
    list_display = ("text", "level")
    list_per_page = 20
    search_fields = ("text",)
    list_filter = ("level",)
