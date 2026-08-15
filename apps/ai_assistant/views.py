from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import ContextualAIService
from .models import AIChatSession, AIChatMessage
from apps.learning.models import Topic

@login_required
def ai_assistant_page(request):
    """
    Dedicated AI Learning Assistant workspace.
    """
    topic_id = request.GET.get('topic')
    selected_topic = None
    if topic_id:
        selected_topic = Topic.objects.filter(id=topic_id).first()

    topics = Topic.objects.filter(is_active=True).select_related('level')
    
    return render(request, 'ai_assistant/ai_chat.html', {
        'topics': topics,
        'selected_topic': selected_topic,
    })


@login_required
def ai_chat_api(request):
    """
    JSON API endpoint for AI assistant queries with context injection.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=400)

    prompt = request.POST.get('prompt', '').strip()
    topic_id = request.POST.get('topic_id')
    action_mode = request.POST.get('action_mode', 'general')

    if not prompt and action_mode == 'general':
        return JsonResponse({'status': 'error', 'message': 'Prompt cannot be empty.'}, status=400)

    # Set default prompts for action modes if blank
    if not prompt:
        topic_obj = Topic.objects.filter(id=topic_id).first() if topic_id else None
        t_name = topic_obj.title if topic_obj else "this Python concept"
        if action_mode == 'simplify':
            prompt = f"Can you simplify and explain {t_name} clearly?"
        elif action_mode == 'analogy':
            prompt = f"Give me real-world analogies to understand {t_name}."
        elif action_mode == 'practice':
            prompt = f"Generate 2 practical coding challenges for {t_name}."
        elif action_mode == 'debug':
            prompt = f"What are common bugs and mistakes beginners make with {t_name}?"
        elif action_mode == 'study_plan':
            prompt = f"Create a 15-minute quick study routine for {t_name}."

    response_text = ContextualAIService.generate_response(
        user=request.user,
        prompt_text=prompt,
        topic_id=topic_id,
        action_mode=action_mode
    )

    return JsonResponse({
        'status': 'ok',
        'prompt': prompt,
        'response': response_text,
        'action_mode': action_mode,
    })
