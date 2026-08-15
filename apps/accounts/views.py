from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, ProfileUpdateForm
from apps.progress.services import calculate_user_analytics

def register_view(request):
    if request.user.is_authenticated:
        return redirect('progress:dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Profile is created via post_save signal; update additional fields
            profile = user.profile
            profile.primary_goal = form.cleaned_data.get('primary_goal', 'beginner')
            profile.experience_level = form.cleaned_data.get('experience_level', 'zero')
            profile.full_name = f"{user.first_name} {user.last_name}".strip() or user.username
            profile.save()

            login(request, user)
            messages.success(request, f"Welcome to LearningHub, {user.username}! Your structured Python learning path is ready.")
            return redirect('progress:dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('progress:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Update user streak
            if hasattr(user, 'profile'):
                user.profile.record_activity()
                
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next', 'progress:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. Keep up the consistency next time!")
    return redirect('core:landing')


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your learning profile has been updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    stats = calculate_user_analytics(request.user)
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile,
        'stats': stats,
    })
