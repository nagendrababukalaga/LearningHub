from django.db import models
from django.contrib.auth.models import User
from apps.learning.models import Topic

class AIChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chat_sessions')
    topic_ref = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_sessions')
    title = models.CharField(max_length=200, default="Python Learning Discussion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class AIChatMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'Student'),
        ('assistant', 'LearningHub AI'),
    ]

    session = models.ForeignKey(AIChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES, default='user')
    content = models.TextField()
    context_used = models.TextField(blank=True, help_text="Metadata about student memory injected into this query")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender}] {self.content[:40]}..."
