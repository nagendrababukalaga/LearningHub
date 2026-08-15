from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Bootcamp, BootcampDay, UserBootcampProgress

def bootcamp_index(request):
    """
    30-Day Python Bootcamp curriculum roadmap with 4 weekly milestones.
    """
    bootcamp = Bootcamp.objects.filter(is_active=True).first()
    if not bootcamp:
        return render(request, 'bootcamp/empty.html')

    days = bootcamp.days.select_related('topic_ref', 'topic_ref__level').all()

    completed_day_ids = set()
    if request.user.is_authenticated:
        completed_day_ids = set(UserBootcampProgress.objects.filter(
            user=request.user, is_completed=True
        ).values_list('bootcamp_day_id', flat=True))

    days_data = []
    for day in days:
        days_data.append({
            'day': day,
            'is_completed': day.id in completed_day_ids,
            'week_number': ((day.day_number - 1) // 7) + 1
        })

    completed_count = len(completed_day_ids)
    total_days = len(days_data) or 30
    progress_pct = round((completed_count / total_days) * 100)

    return render(request, 'bootcamp/bootcamp_index.html', {
        'bootcamp': bootcamp,
        'days_data': days_data,
        'completed_count': completed_count,
        'total_days': total_days,
        'progress_pct': progress_pct,
    })


def bootcamp_day_detail(request, day_number):
    day = get_object_or_404(BootcampDay.objects.select_related('bootcamp', 'topic_ref'), day_number=day_number)
    user_progress = None

    if request.user.is_authenticated:
        user_progress, _ = UserBootcampProgress.objects.get_or_create(
            user=request.user, bootcamp_day=day
        )
        if request.method == 'POST':
            user_progress.submission_notes = request.POST.get('submission_notes', '').strip()
            user_progress.save()
            messages.success(request, f"Notes updated for Day {day.day_number}!")

    prev_day = BootcampDay.objects.filter(bootcamp=day.bootcamp, day_number=day_number - 1).first()
    next_day = BootcampDay.objects.filter(bootcamp=day.bootcamp, day_number=day_number + 1).first()

    return render(request, 'bootcamp/bootcamp_day_detail.html', {
        'day': day,
        'user_progress': user_progress,
        'prev_day': prev_day,
        'next_day': next_day,
    })


@login_required
def toggle_day_complete(request, day_number):
    day = get_object_or_404(BootcampDay, day_number=day_number)
    user_prog, _ = UserBootcampProgress.objects.get_or_create(user=request.user, bootcamp_day=day)
    user_prog.toggle()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'status': 'ok',
            'is_completed': user_prog.is_completed,
            'message': f"Day {day.day_number} marked as {'Completed' if user_prog.is_completed else 'In Progress'}!"
        })

    msg = f"Day {day.day_number} marked as {'Completed' if user_prog.is_completed else 'In Progress'}!"
    messages.success(request, msg)
    return redirect('bootcamp:day_detail', day_number=day_number)
