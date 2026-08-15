from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import LearningPath, Level, Topic, Resource, Bookmark
from apps.progress.models import UserTopicProgress, PracticeProblem, UserPractice
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake, TopicNote

def path_overview(request):
    """
    Displays the full structured Python Learning Path (Levels 1 to 7).
    """
    primary_path = LearningPath.objects.filter(is_active=True).first()
    if not primary_path:
        return render(request, 'learning/empty_path.html')

    levels = primary_path.levels.prefetch_related('topics').all()
    
    # Pre-fetch user progress if authenticated
    user_progress_map = {}
    completed_topic_ids = set()
    if request.user.is_authenticated:
        progresses = UserTopicProgress.objects.filter(user=request.user)
        user_progress_map = {p.topic_id: p for p in progresses}
        completed_topic_ids = {p.topic_id for p in progresses if p.is_completed}

    # Enhance level data with user statistics
    level_list = []
    for level in levels:
        level_topics = level.topics.filter(is_active=True)
        total_in_level = level_topics.count()
        completed_in_level = sum(1 for t in level_topics if t.id in completed_topic_ids)
        pct = round((completed_in_level / total_in_level * 100) if total_in_level else 0)

        topics_data = []
        for t in level_topics:
            prog = user_progress_map.get(t.id)
            topics_data.append({
                'topic': t,
                'progress': prog,
                'is_completed': t.id in completed_topic_ids,
                'understanding': prog.understanding_level if prog else 'not_started',
            })

        level_list.append({
            'level': level,
            'topics_data': topics_data,
            'total_topics': total_in_level,
            'completed_topics': completed_in_level,
            'progress_pct': pct,
        })

    return render(request, 'learning/path_overview.html', {
        'path': primary_path,
        'level_list': level_list,
    })


def topic_detail(request, slug):
    """
    Comprehensive topic study page with conceptual explanation, resources,
    Personal Learning Memory editor, doubts, mistakes, and practice challenges.
    """
    topic = get_object_or_404(Topic.objects.select_related('level', 'level__learning_path'), slug=slug)
    resources = topic.resources.all()
    practice_problems = topic.practice_problems.all()
    
    # Progress & memory state for logged-in user
    progress = None
    memory = None
    doubts = []
    mistakes = []
    bookmarked_ids = set()
    user_practices = {}

    if request.user.is_authenticated:
        # Record streak activity
        if hasattr(request.user, 'profile'):
            request.user.profile.record_activity()

        progress, created = UserTopicProgress.objects.get_or_create(
            user=request.user,
            topic=topic,
            defaults={'status': 'in_progress'}
        )
        if not created and progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.save()

        memory, _ = PersonalLearningMemory.objects.get_or_create(user=request.user, topic=topic)
        doubts = LearningDoubt.objects.filter(user=request.user, topic=topic)
        mistakes = LearningMistake.objects.filter(user=request.user, topic=topic)
        bookmarked_ids = set(Bookmark.objects.filter(
            user=request.user, resource__in=resources
        ).values_list('resource_id', flat=True))

        user_practices = {
            up.problem_id: up for up in UserPractice.objects.filter(user=request.user, problem__in=practice_problems)
        }

    practice_data = []
    for prob in practice_problems:
        practice_data.append({
            'problem': prob,
            'user_attempt': user_practices.get(prob.id)
        })

    return render(request, 'learning/topic_detail.html', {
        'topic': topic,
        'level': topic.level,
        'path': topic.level.learning_path,
        'resources': resources,
        'practice_data': practice_data,
        'progress': progress,
        'memory': memory,
        'doubts': doubts,
        'mistakes': mistakes,
        'bookmarked_ids': bookmarked_ids,
        'prev_topic': topic.get_previous_topic(),
        'next_topic': topic.get_next_topic(),
    })


@login_required
def toggle_bookmark(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    bookmark = Bookmark.objects.filter(user=request.user, resource=resource).first()
    
    if bookmark:
        bookmark.delete()
        is_bookmarked = False
        msg = f"Removed '{resource.title}' from bookmarks."
    else:
        Bookmark.objects.create(user=request.user, resource=resource)
        is_bookmarked = True
        msg = f"Saved '{resource.title}' to your bookmarks."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({'status': 'ok', 'is_bookmarked': is_bookmarked, 'message': msg})
    
    messages.info(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'learning:path_overview'))


@login_required
def bookmarks_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('resource', 'resource__topic', 'resource__topic__level')
    return render(request, 'learning/bookmarks_list.html', {
        'bookmarks': bookmarks
    })
