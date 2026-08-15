from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.learning.models import Topic

class PersonalLearningMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_memories')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_memories')
    
    what_i_understood = models.TextField(
        blank=True,
        help_text="Summarize the concept in your own natural words."
    )
    my_own_explanation = models.TextField(
        blank=True,
        help_text="Explain this concept as if you were teaching it to a 10-year-old."
    )
    real_life_analogy = models.TextField(
        blank=True,
        help_text="What real-world comparison makes this click for you?"
    )
    my_code_example = models.TextField(
        blank=True,
        help_text="Your own custom Python snippet demonstrating this topic."
    )
    what_confused_me = models.TextField(
        blank=True,
        help_text="What parts felt tricky, confusing, or easy to mix up?"
    )
    what_helped_me = models.TextField(
        blank=True,
        help_text="What unlocked the 'aha!' moment for you?"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}'s Memory on {self.topic.title}"

    @property
    def is_filled(self):
        return bool(
            self.what_i_understood or
            self.my_own_explanation or
            self.real_life_analogy or
            self.my_code_example or
            self.what_confused_me
        )


class TopicNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255, default="Quick Note")
    content = models.TextField()
    tags = models.CharField(max_length=150, blank=True, help_text="Comma-separated tags (e.g. syntax, trick, interview)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.topic.title})"


class LearningDoubt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='doubts')
    doubt_text = models.TextField(help_text="What question or doubt do you still have about this topic?")
    resolution_notes = models.TextField(blank=True, help_text="How was this doubt resolved? What was the answer?")
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['is_resolved', '-created_at']

    def __str__(self):
        status = "Resolved" if self.is_resolved else "Open"
        return f"[{status}] {self.doubt_text[:50]}..."

    def mark_resolved(self, notes=""):
        self.is_resolved = True
        if notes:
            self.resolution_notes = notes
        self.resolved_at = timezone.now()
        self.save()


class LearningMistake(models.Model):
    ERROR_TYPES = [
        ('syntax', 'Syntax Error'),
        ('logic', 'Logic / Off-by-one Bug'),
        ('runtime', 'Runtime / Exception'),
        ('type', 'Type Mismatch / Conversion'),
        ('conceptual', 'Conceptual Misunderstanding'),
        ('name', 'NameError / Scope Mistake'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mistakes')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='mistakes')
    mistake_description = models.TextField(help_text="What mistake or error did you make while writing or practicing?")
    correction_or_lesson = models.TextField(help_text="What is the fix or rule to avoid this in the future?")
    error_type = models.CharField(max_length=30, choices=ERROR_TYPES, default='syntax')
    code_snippet = models.TextField(blank=True, help_text="The broken vs corrected code snippet")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_error_type_display()}] {self.mistake_description[:50]}..."
