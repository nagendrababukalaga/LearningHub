from django.shortcuts import render, get_object_or_404
from .models import MentorArticle, MentorTip

def guidance_home(request):
    """
    Mentor guidance library: articles, tips, and roadmaps from senior engineers.
    """
    category_filter = request.GET.get('category', 'all')
    articles = MentorArticle.objects.all()

    if category_filter != 'all':
        articles = articles.filter(category=category_filter)

    tips = MentorTip.objects.all()
    categories = MentorArticle.CATEGORY_CHOICES

    return render(request, 'guidance/guidance_home.html', {
        'articles': articles,
        'tips': tips,
        'categories': categories,
        'selected_category': category_filter,
    })


def article_detail(request, slug):
    article = get_object_or_404(MentorArticle, slug=slug)
    related_articles = MentorArticle.objects.filter(category=article.category).exclude(id=article.id)[:2]

    return render(request, 'guidance/article_detail.html', {
        'article': article,
        'related_articles': related_articles,
    })


def pricing_concept(request):
    """
    Freemium / Pro Mentorship concept page demonstrating business scalability.
    """
    return render(request, 'guidance/pricing_concept.html')
