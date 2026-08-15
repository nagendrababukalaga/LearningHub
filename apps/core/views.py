from django.shortcuts import render
from django.db.models import Q
from apps.learning.models import LearningPath, Level, Topic, Resource
from apps.guidance.models import MentorArticle
from apps.progress.models import PracticeProblem
from .models import StudentStory

def landing_page(request):
    """
    Startup-quality Landing Page for LearningHub.
    """
    path = LearningPath.objects.filter(is_active=True).first()
    levels = Level.objects.filter(learning_path=path).prefetch_related('topics') if path else []
    stories = StudentStory.objects.all()
    sample_topics = Topic.objects.filter(is_active=True)[:6]

    return render(request, 'core/landing.html', {
        'path': path,
        'levels': levels,
        'stories': stories,
        'sample_topics': sample_topics,
    })


def search_view(request):
    """
    Global search across topics, practice exercises, and mentor articles.
    """
    query = request.GET.get('q', '').strip()
    topics = []
    practice_problems = []
    articles = []

    if query:
        topics = Topic.objects.filter(
            Q(title__icontains=query) |
            Q(objectives__icontains=query) |
            Q(summary_content__icontains=query) |
            Q(key_takeaways__icontains=query)
        ).select_related('level')

        practice_problems = PracticeProblem.objects.filter(
            Q(title__icontains=query) |
            Q(prompt_description__icontains=query)
        ).select_related('topic')

        articles = MentorArticle.objects.filter(
            Q(title__icontains=query) |
            Q(summary__icontains=query) |
            Q(content__icontains=query)
        )

    total_results = len(topics) + len(practice_problems) + len(articles)

    return render(request, 'core/search_results.html', {
        'query': query,
        'topics': topics,
        'practice_problems': practice_problems,
        'articles': articles,
        'total_results': total_results,
    })


def handler404(request, exception):
    return render(request, 'core/404.html', status=404)


def handler500(request):
    return render(request, 'core/500.html', status=500)
