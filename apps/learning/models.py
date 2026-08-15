from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class LearningPath(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=255, default="Master Python from zero to job-ready")
    description = models.TextField()
    icon = models.CharField(max_length=50, default="code", help_text="Icon identifier (e.g., terminal, code, cpu)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def total_topics(self):
        return Topic.objects.filter(level__learning_path=self, is_active=True).count()


class Level(models.Model):
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='levels')
    level_number = models.PositiveIntegerField(default=1)
    title = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['level_number', 'order']
        unique_together = ('learning_path', 'level_number')

    def __str__(self):
        return f"Level {self.level_number}: {self.title}"

    @property
    def topics_count(self):
        return self.topics.filter(is_active=True).count()


class Topic(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    order = models.PositiveIntegerField(default=1)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_minutes = models.PositiveIntegerField(default=30)
    objectives = models.TextField(help_text="Bullet points separated by newlines")
    summary_content = models.TextField(help_text="In-depth conceptual explanation for students")
    code_snippet = models.TextField(blank=True, help_text="Clean Python code example demonstrating the topic")
    key_takeaways = models.TextField(blank=True, help_text="Key takeaways separated by newlines")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['level__level_number', 'order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.level.level_number}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"L{self.level.level_number}.{self.order} — {self.title}"

    def get_objectives_list(self):
        return [line.strip() for line in self.objectives.split('\n') if line.strip()]

    def get_takeaways_list(self):
        return [line.strip() for line in self.key_takeaways.split('\n') if line.strip()]

    def get_previous_topic(self):
        return Topic.objects.filter(
            level__learning_path=self.level.learning_path,
            is_active=True
        ).filter(
            models.Q(level__level_number__lt=self.level.level_number) |
            models.Q(level__level_number=self.level.level_number, order__lt=self.order)
        ).order_by('-level__level_number', '-order').first()

    def get_next_topic(self):
        return Topic.objects.filter(
            level__learning_path=self.level.learning_path,
            is_active=True
        ).filter(
            models.Q(level__level_number__gt=self.level.level_number) |
            models.Q(level__level_number=self.level.level_number, order__gt=self.order)
        ).order_by('level__level_number', 'order').first()


class Resource(models.Model):
    TYPE_CHOICES = [
        ('video', 'Video Tutorial'),
        ('doc', 'Official Documentation'),
        ('article', 'In-Depth Article'),
        ('practice', 'Interactive Practice'),
        ('cheatsheet', 'Cheat Sheet / Reference'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='doc')
    url = models.URLField(max_length=500)
    author_or_source = models.CharField(max_length=150, default="Python Official Docs")
    duration_or_read_time = models.CharField(max_length=50, default="10 min read")
    is_recommended = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"[{self.get_resource_type_display()}] {self.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
