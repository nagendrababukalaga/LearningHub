from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import PersonalLearningMemory, TopicNote, LearningDoubt, LearningMistake
from apps.learning.models import Topic, Level

@login_required
def memory_hub(request):
    """
    Personal Learning Memory Hub: View all conceptual models,
    analogies, and explanations captured by the student.
    """
    memories = PersonalLearningMemory.objects.filter(
        user=request.user
    ).select_related('topic', 'topic__level').order_by('-updated_at')

    # Filter out completely empty memories
    active_memories = [m for m in memories if m.is_filled]

    levels = Level.objects.filter(learning_path__is_active=True).prefetch_related('topics')
    
    return render(request, 'memory/memory_hub.html', {
        'memories': active_memories,
        'total_memories_count': len(active_memories),
        'levels': levels,
    })


@login_required
def save_memory_ajax(request, topic_id):
    """
    AJAX endpoint to save or update Personal Learning Memory fields.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)

    topic = get_object_or_404(Topic, id=topic_id)
    memory, _ = PersonalLearningMemory.objects.get_or_create(user=request.user, topic=topic)

    memory.what_i_understood = request.POST.get('what_i_understood', memory.what_i_understood).strip()
    memory.my_own_explanation = request.POST.get('my_own_explanation', memory.my_own_explanation).strip()
    memory.real_life_analogy = request.POST.get('real_life_analogy', memory.real_life_analogy).strip()
    memory.my_code_example = request.POST.get('my_code_example', memory.my_code_example).strip()
    memory.what_confused_me = request.POST.get('what_confused_me', memory.what_confused_me).strip()
    memory.what_helped_me = request.POST.get('what_helped_me', memory.what_helped_me).strip()
    memory.save()

    return JsonResponse({
        'status': 'ok',
        'message': 'Personal Learning Memory updated successfully!',
        'updated_at': memory.updated_at.strftime('%b %d, %H:%M')
    })


@login_required
def doubts_list(request):
    """
    Doubt tracker: review active vs resolved doubts across all topics.
    """
    filter_status = request.GET.get('status', 'all')
    doubts = LearningDoubt.objects.filter(user=request.user).select_related('topic', 'topic__level')

    if filter_status == 'open':
        doubts = doubts.filter(is_resolved=False)
    elif filter_status == 'resolved':
        doubts = doubts.filter(is_resolved=True)

    topics = Topic.objects.filter(is_active=True).select_related('level')

    return render(request, 'memory/doubts_list.html', {
        'doubts': doubts,
        'filter_status': filter_status,
        'topics': topics,
        'open_count': LearningDoubt.objects.filter(user=request.user, is_resolved=False).count(),
        'resolved_count': LearningDoubt.objects.filter(user=request.user, is_resolved=True).count(),
    })


@login_required
def create_doubt(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        doubt_text = request.POST.get('doubt_text', '').strip()
        topic = get_object_or_404(Topic, id=topic_id)

        if doubt_text:
            LearningDoubt.objects.create(
                user=request.user,
                topic=topic,
                doubt_text=doubt_text
            )
            messages.success(request, f"Doubt logged for {topic.title}. You can review and resolve it anytime.")
        else:
            messages.error(request, "Please enter your doubt description.")

    return redirect(request.META.get('HTTP_REFERER', 'memory:doubts_list'))


@login_required
def toggle_doubt_resolve(request, doubt_id):
    doubt = get_object_or_404(LearningDoubt, id=doubt_id, user=request.user)
    
    if request.method == 'POST':
        resolution_notes = request.POST.get('resolution_notes', '').strip()
        if not doubt.is_resolved:
            doubt.mark_resolved(resolution_notes)
            messages.success(request, f"Doubt on {doubt.topic.title} marked as resolved! Great job understanding it.")
        else:
            doubt.is_resolved = False
            doubt.resolved_at = None
            doubt.save()
            messages.info(request, "Doubt re-opened for further review.")

    return redirect(request.META.get('HTTP_REFERER', 'memory:doubts_list'))


@login_required
def mistakes_list(request):
    """
    Mistake tracker: review syntax, logic, and runtime mistakes made during practice.
    """
    error_filter = request.GET.get('type', 'all')
    mistakes = LearningMistake.objects.filter(user=request.user).select_related('topic', 'topic__level')

    if error_filter != 'all':
        mistakes = mistakes.filter(error_type=error_filter)

    topics = Topic.objects.filter(is_active=True).select_related('level')

    return render(request, 'memory/mistakes_list.html', {
        'mistakes': mistakes,
        'topics': topics,
        'error_filter': error_filter,
        'error_types': LearningMistake.ERROR_TYPES,
        'total_mistakes_count': mistakes.count()
    })


@login_required
def create_mistake(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        mistake_desc = request.POST.get('mistake_description', '').strip()
        correction = request.POST.get('correction_or_lesson', '').strip()
        error_type = request.POST.get('error_type', 'syntax')
        code_snippet = request.POST.get('code_snippet', '').strip()

        topic = get_object_or_404(Topic, id=topic_id)

        if mistake_desc and correction:
            LearningMistake.objects.create(
                user=request.user,
                topic=topic,
                mistake_description=mistake_desc,
                correction_or_lesson=correction,
                error_type=error_type,
                code_snippet=code_snippet
            )
            messages.success(request, f"Mistake logged for {topic.title}. Tracking your mistakes turns errors into mastery.")
        else:
            messages.error(request, "Please fill in both the mistake description and the correction rule.")

    return redirect(request.META.get('HTTP_REFERER', 'memory:mistakes_list'))


@login_required
def delete_mistake(request, mistake_id):
    mistake = get_object_or_404(LearningMistake, id=mistake_id, user=request.user)
    if request.method == 'POST':
        mistake.delete()
        messages.info(request, "Mistake log deleted.")
    return redirect('memory:mistakes_list')
