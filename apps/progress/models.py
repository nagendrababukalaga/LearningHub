from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.learning.models import Topic, LearningPath

class UserTopicProgress(models.Model):
    UNDERSTANDING_LEVELS = [
        ('not_started', 'Not Started'),
        ('learning', 'Learning (Getting familiar)'),
        ('need_revision', 'Need Revision (Shaky / Confused)'),
        ('comfortable', 'Comfortable (Can use in code)'),
        ('strong', 'Strong (Can teach to others)'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    understanding_level = models.CharField(max_length=20, choices=UNDERSTANDING_LEVELS, default='not_started')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_reviewed_at = models.DateTimeField(default=timezone.now)
    times_reviewed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')
        ordering = ['topic__level__level_number', 'topic__order']

    def __str__(self):
        return f"{self.user.username} - {self.topic.title} ({self.get_understanding_level_display()})"

    def mark_completed(self):
        self.is_completed = True
        self.status = 'completed'
        if not self.completed_at:
            self.completed_at = timezone.now()
        if self.understanding_level == 'not_started':
            self.understanding_level = 'comfortable'
        self.last_reviewed_at = timezone.now()
        self.save()


class DailyTask(models.Model):
    TASK_TYPES = [
        ('learn', 'Learn Concept'),
        ('understand', 'Personal Understanding'),
        ('practice', 'Coding Practice'),
        ('review', 'Revision & Doubts'),
        ('complete', 'Milestone Checkoff'),
    ]

    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='daily_tasks')
    topic_ref = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='daily_tasks')
    day_number = models.PositiveIntegerField(default=1, help_text="Curriculum day index")
    title = models.CharField(max_length=255)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='learn')
    description = models.TextField()
    estimated_minutes = models.PositiveIntegerField(default=20)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['day_number', 'order', 'id']

    def __str__(self):
        return f"Day {self.day_number} [{self.get_task_type_display()}]: {self.title}"


class UserDailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_daily_tasks')
    daily_task = models.ForeignKey(DailyTask, on_delete=models.CASCADE, related_name='user_instances')
    is_completed = models.BooleanField(default=False)
    date_assigned = models.DateField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'daily_task', 'date_assigned')
        ordering = ['daily_task__order']

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"{self.user.username} - {self.daily_task.title} ({status})"

    def toggle(self):
        self.is_completed = not self.is_completed
        self.completed_at = timezone.now() if self.is_completed else None
        self.save()


class PracticeProblem(models.Model):
    PLATFORM_CHOICES = [
        ('learninghub', 'LearningHub Practice'),
        ('leetcode', 'LeetCode'),
        ('hackerrank', 'HackerRank'),
        ('codewars', 'Codewars'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='practice_problems')
    title = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='learninghub')
    problem_url = models.URLField(max_length=500, blank=True)
    prompt_description = models.TextField()
    starter_code = models.TextField(blank=True, default="# Write your solution here\n")
    solution_hint = models.TextField(blank=True)
    solution_code = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['topic__level__level_number', 'topic__order', 'order']

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title} ({self.topic.title})"


class UserPractice(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_submissions')
    problem = models.ForeignKey(PracticeProblem, on_delete=models.CASCADE, related_name='user_attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    my_solution_code = models.TextField(blank=True)
    reflection_notes = models.TextField(blank=True, help_text="Key takeaways, time complexity, or tricks learned")
    time_spent_minutes = models.PositiveIntegerField(default=0)
    solved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'problem')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} [{self.get_status_display()}]"
