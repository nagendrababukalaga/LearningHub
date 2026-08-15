from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.learning.models import Topic

class Bootcamp(models.Model):
    title = models.CharField(max_length=150, default="Python 30-Day Intensive Bootcamp")
    slug = models.SlugField(unique=True, default="python-30-day-bootcamp")
    tagline = models.CharField(max_length=255, default="Go from absolute beginner to building real Python projects in 30 days")
    description = models.TextField()
    total_days = models.PositiveIntegerField(default=30)
    icon = models.CharField(max_length=50, default="rocket")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BootcampDay(models.Model):
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE, related_name='days')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    topic_ref = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='bootcamp_days')
    concept_summary = models.TextField()
    learning_goals = models.TextField(help_text="Bullet points separated by newlines")
    practice_assignment = models.TextField(help_text="The practical challenge for today")
    code_starter = models.TextField(blank=True)
    estimated_minutes = models.PositiveIntegerField(default=60)
    resource_url = models.URLField(max_length=500, blank=True)

    class Meta:
        ordering = ['day_number']
        unique_together = ('bootcamp', 'day_number')

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"

    def get_goals_list(self):
        return [line.strip() for line in self.learning_goals.split('\n') if line.strip()]


class UserBootcampProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bootcamp_progress')
    bootcamp_day = models.ForeignKey(BootcampDay, on_delete=models.CASCADE, related_name='user_progress')
    is_completed = models.BooleanField(default=False)
    submission_notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'bootcamp_day')
        ordering = ['bootcamp_day__day_number']

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.user.username} - Day {self.bootcamp_day.day_number} ({status})"

    def toggle(self):
        self.is_completed = not self.is_completed
        self.completed_at = timezone.now() if self.is_completed else None
        self.save()
