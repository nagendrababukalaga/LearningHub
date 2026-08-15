from django.db import models

class StudentStory(models.Model):
    name = models.CharField(max_length=100)
    role_or_college = models.CharField(max_length=150, default="Computer Science Student")
    avatar_color = models.CharField(max_length=20, default="#3B82F6")
    initials = models.CharField(max_length=5, default="JD")
    quote = models.TextField()
    outcome = models.CharField(max_length=150, help_text="e.g. 'Cracked Python Internship at TechCorp'")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Student Story"
        verbose_name_plural = "Student Stories"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.role_or_college})"
