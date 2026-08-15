from django.contrib import admin
from .models import UserTopicProgress, DailyTask, UserDailyTask, PracticeProblem, UserPractice

@admin.register(UserTopicProgress)
class UserTopicProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'status', 'understanding_level', 'is_completed', 'last_reviewed_at')
    list_filter = ('status', 'understanding_level', 'is_completed')
    search_fields = ('user__username', 'topic__title')

@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'title', 'task_type', 'estimated_minutes', 'topic_ref')
    list_filter = ('task_type', 'day_number')
    search_fields = ('title', 'description')

@admin.register(PracticeProblem)
class PracticeProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'difficulty', 'platform', 'order')
    list_filter = ('difficulty', 'platform', 'topic__level')
    search_fields = ('title', 'prompt_description', 'topic__title')

@admin.register(UserPractice)
class UserPracticeAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'status', 'solved_at')
    list_filter = ('status', 'solved_at')
    search_fields = ('user__username', 'problem__title')
