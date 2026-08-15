from django.contrib import admin
from .models import PersonalLearningMemory, TopicNote, LearningDoubt, LearningMistake

@admin.register(PersonalLearningMemory)
class PersonalLearningMemoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'is_filled', 'updated_at')
    list_filter = ('updated_at', 'topic__level')
    search_fields = ('user__username', 'topic__title', 'what_i_understood', 'real_life_analogy')

@admin.register(TopicNote)
class TopicNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'topic', 'updated_at')
    search_fields = ('title', 'content', 'user__username', 'topic__title')

@admin.register(LearningDoubt)
class LearningDoubtAdmin(admin.ModelAdmin):
    list_display = ('doubt_text', 'user', 'topic', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('doubt_text', 'resolution_notes', 'user__username', 'topic__title')

@admin.register(LearningMistake)
class LearningMistakeAdmin(admin.ModelAdmin):
    list_display = ('mistake_description', 'user', 'topic', 'error_type', 'created_at')
    list_filter = ('error_type', 'created_at')
    search_fields = ('mistake_description', 'correction_or_lesson', 'user__username', 'topic__title')
