from django.contrib import admin
from .models import AIChatSession, AIChatMessage

class AIChatMessageInline(admin.TabularInline):
    model = AIChatMessage
    extra = 0

@admin.register(AIChatSession)
class AIChatSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'topic_ref', 'updated_at')
    inlines = [AIChatMessageInline]

@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'session', 'created_at')
    list_filter = ('sender', 'created_at')
