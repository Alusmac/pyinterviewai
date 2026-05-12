from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('question/<int:id>/', views.question_view, name='question'),
    path('result/', views.result, name='result'),
    path('level/<str:level>/', views.questions_by_level, name='questions_by_level'),
    path('set-user/', views.set_user, name='set_user'),
    path('ai-chat/', views.ai_chat, name='ai_chat'),
]
