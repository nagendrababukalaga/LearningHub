from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'primary_goal', 'experience_level', 'current_streak', 'daily_goal_minutes', 'last_active_date')
    list_filter = ('primary_goal', 'experience_level')
    search_fields = ('user__username', 'full_name', 'user__email')
