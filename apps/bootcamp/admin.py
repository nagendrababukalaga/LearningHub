from django.contrib import admin
from .models import Bootcamp, BootcampDay, UserBootcampProgress

class BootcampDayInline(admin.TabularInline):
    model = BootcampDay
    extra = 1
    fields = ('day_number', 'title', 'topic_ref', 'estimated_minutes')

@admin.register(Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_days', 'is_active')
    inlines = [BootcampDayInline]

@admin.register(BootcampDay)
class BootcampDayAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'title', 'bootcamp', 'topic_ref', 'estimated_minutes')
    list_filter = ('bootcamp',)
    search_fields = ('title', 'concept_summary', 'practice_assignment')

@admin.register(UserBootcampProgress)
class UserBootcampProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'bootcamp_day', 'is_completed', 'completed_at')
    list_filter = ('is_completed',)
