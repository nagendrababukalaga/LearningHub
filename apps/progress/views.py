from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import UserTopicProgress, PracticeProblem, UserPractice, DailyTask, UserDailyTask
from .services import RevisionRecommendationEngine, DailyPlanGenerator, calculate_user_analytics
from apps.learning.models import Topic, Level, LearningPath
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake

@login_required
def dashboard_view(request):
    """
    Main student dashboard answering: 'What should I do today?'
    """
    # 1. Update streak
    if hasattr(request.user, 'profile'):
        request.user.profile.record_activity()

    # 2. Get today's actionable learning plan
    today_plan = DailyPlanGenerator.get_today_plan(request.user)

    # 3. Get user mastery analytics
    stats = calculate_user_analytics(request.user)

    # 4. Get top revision recommendations
    revision_items = RevisionRecommendationEngine.get_revision_recommendations(request.user, limit=3)

    # 5. Level curriculum overview
    levels = Level.objects.filter(learning_path__is_active=True).prefetch_related('topics')
    user_progress_map = {
        p.topic_id: p for p in UserTopicProgress.objects.filter(user=request.user)
    }

    levels_summary = []
    for lvl in levels:
        lvl_topics = lvl.topics.filter(is_active=True)
        tot = lvl_topics.count()
        comp = sum(1 for t in lvl_topics if user_progress_map.get(t.id) and user_progress_map[t.id].is_completed)
        levels_summary.append({
            'level': lvl,
            'total': tot,
            'completed': comp,
            'pct': round((comp / tot * 100) if tot else 0)
        })

    # 6. Recent memories
    recent_memories = PersonalLearningMemory.objects.filter(
        user=request.user
    ).exclude(what_i_understood="").select_related('topic')[:3]

    return render(request, 'progress/dashboard.html', {
        'today_plan': today_plan,
        'stats': stats,
        'revision_items': revision_items,
        'levels_summary': levels_summary,
        'recent_memories': recent_memories,
    })


@login_required
def update_progress_ajax(request, topic_id):
    """
    AJAX endpoint to update understanding level or mark topic completed.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)

    topic = get_object_or_404(Topic, id=topic_id)
    progress, _ = UserTopicProgress.objects.get_or_create(user=request.user, topic=topic)

    understanding = request.POST.get('understanding_level')
    if understanding in dict(UserTopicProgress.UNDERSTANDING_LEVELS):
        progress.understanding_level = understanding

    is_completed_str = request.POST.get('is_completed')
    if is_completed_str is not None:
        is_completed = is_completed_str.lower() in ('true', '1', 'yes')
        progress.is_completed = is_completed
        if is_completed:
            progress.status = 'completed'
            if not progress.completed_at:
                progress.completed_at = timezone.now()
            progress.last_reviewed_at = timezone.now()
        else:
            progress.status = 'in_progress'

    progress.save()

    return JsonResponse({
        'status': 'ok',
        'understanding_level': progress.understanding_level,
        'understanding_label': progress.get_understanding_level_display(),
        'is_completed': progress.is_completed,
        'message': f"Progress updated for {topic.title}!"
    })


@login_required
def practice_list(request):
    """
    Interactive practice tracker with problem filter by level, difficulty, and status.
    """
    topic_id = request.GET.get('topic')
    difficulty = request.GET.get('difficulty', 'all')
    status_filter = request.GET.get('status', 'all')

    problems = PracticeProblem.objects.select_related('topic', 'topic__level').all()

    if topic_id:
        problems = problems.filter(topic_id=topic_id)
    if difficulty != 'all':
        problems = problems.filter(difficulty=difficulty)

    user_submissions = {
        up.problem_id: up for up in UserPractice.objects.filter(user=request.user)
    }

    problem_cards = []
    for prob in problems:
        attempt = user_submissions.get(prob.id)
        current_status = attempt.status if attempt else 'not_started'
        
        if status_filter != 'all' and current_status != status_filter:
            continue

        problem_cards.append({
            'problem': prob,
            'attempt': attempt,
            'status': current_status
        })

    topics = Topic.objects.filter(is_active=True).select_related('level')

    return render(request, 'progress/practice_list.html', {
        'problem_cards': problem_cards,
        'topics': topics,
        'selected_topic_id': int(topic_id) if topic_id and topic_id.isdigit() else None,
        'selected_difficulty': difficulty,
        'selected_status': status_filter,
        'total_count': len(problem_cards),
        'solved_count': sum(1 for p in problem_cards if p['status'] == 'solved'),
    })


@login_required
def practice_submit_ajax(request, problem_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)

    problem = get_object_or_404(PracticeProblem, id=problem_id)
    attempt, _ = UserPractice.objects.get_or_create(user=request.user, problem=problem)

    new_status = request.POST.get('status', attempt.status)
    if new_status in dict(UserPractice.STATUS_CHOICES):
        attempt.status = new_status
        if new_status == 'solved' and not attempt.solved_at:
            attempt.solved_at = timezone.now()

    attempt.my_solution_code = request.POST.get('solution_code', attempt.my_solution_code)
    attempt.reflection_notes = request.POST.get('reflection_notes', attempt.reflection_notes)
    attempt.save()

    return JsonResponse({
        'status': 'ok',
        'problem_status': attempt.status,
        'message': f"Saved practice submission for '{problem.title}'!"
    })


@login_required
def revision_hub(request):
    """
    Rule-based Revision Hub: surfaces topics prioritized by mistakes,
    open doubts, understanding level, and days since last review.
    """
    recommendations = RevisionRecommendationEngine.get_revision_recommendations(request.user, limit=None)
    stats = calculate_user_analytics(request.user)

    return render(request, 'progress/revision_hub.html', {
        'recommendations': recommendations,
        'stats': stats,
        'total_revision_count': len(recommendations),
    })
