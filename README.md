# 🧠 PyInterview AI

An AI-powered Python interview training platform that helps users practice coding interviews, receive instant AI feedback, and track their progress over time.

---

## 🚀 Live Demo
*http//*


---

## 📌 Features

### 🧑‍💻 Interview Practice
- Curated Python interview questions
- Difficulty levels: Junior / Mid / Senior
- Clean and distraction-free UI

### 🤖 AI Mentor
- Instant AI evaluation of answers
- Feedback on:
  - Technical correctness
  - Code quality
  - Communication clarity
- AI-powered learning suggestions

### 📊 Performance Tracking
- Correct vs Wrong answers
- Total attempts tracking
- Success rate calculation
- Personal progress history

### 📈 AI Chat Assistant
- Ask Python questions anytime
- Get explanations with examples
- Code snippets included
- Learning tips for improvement

### 🎯 Progress Dashboard
- Modern Notion-style UI card
- Personal performance insights
- Direct access to detailed profile analytics

---

## 🏗️ Tech Stack

### Backend
- Python 3.11+
- Django
- Django ORM
- Django Templates

### AI Integration
- OpenAI API (GPT-4o)
- Groq API (LLaMA 3)

### Frontend
- HTML5
- CSS3 (custom design system)
- Vanilla JavaScript

---

## ⚙️ Installation

1. **Clone repository:**
    ```bash
    git clone https://github.com/alusmac/pyinterviewai.git
    cd pyinterviewai

2. **Create virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows


3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Set environment variables**
    ```bash
    Create .env file:
    OPENAI_API_KEY=your_openai_key
    GROQ_API_KEY=your_groq_key
    SECRET_KEY=your_django_secret
    DEBUG=True

5. **Run migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate

6. **Create superuser (optional)**
    ```bash
    python manage.py createsuperuser

7. **Run server**
    ```bash
    python manage.py runserver
8. **App will be available at:**
    ```bash
    http://127.0.0.1:8000/

