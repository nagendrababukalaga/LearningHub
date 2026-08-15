from django.db import models
from django.utils.text import slugify

class MentorArticle(models.Model):
    CATEGORY_CHOICES = [
        ('strategy', 'Learning Strategy & Consistency'),
        ('debugging', 'Debugging & Problem Solving'),
        ('interview', 'Python Internship & Interview Prep'),
        ('mistakes', 'Avoiding Beginner Pitfalls'),
        ('projects', 'Resume Projects & Building Things'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='strategy')
    author_name = models.CharField(max_length=100, default="LearningHub Senior Mentors")
    read_time_minutes = models.PositiveIntegerField(default=5)
    summary = models.TextField()
    content = models.TextField(help_text="Full article guide content")
    actionable_rules = models.TextField(help_text="Key actionable rules separated by newlines")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    def get_rules_list(self):
        return [line.strip() for line in self.actionable_rules.split('\n') if line.strip()]


class MentorTip(models.Model):
    title = models.CharField(max_length=150)
    short_tip = models.TextField()
    category = models.CharField(max_length=50, default="Daily Wisdom")
    icon = models.CharField(max_length=50, default="lightbulb")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title
