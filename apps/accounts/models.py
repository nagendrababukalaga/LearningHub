from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    GOAL_CHOICES = [
        ('beginner', 'Python from Absolute Zero'),
        ('internship', 'Internship & Job Interview Prep'),
        ('software_eng', 'Software Engineering Fundamentals'),
        ('data_science', 'Data Science & Automation Foundation'),
        ('college_exam', 'College Coursework & Lab Prep'),
    ]

    EXPERIENCE_CHOICES = [
        ('zero', 'Complete Beginner (No prior coding)'),
        ('some', 'Know basic programming (C/C++/Java)'),
        ('rusty', 'Used Python before, need structured refresher'),
        ('intermediate', 'Intermediate, want to master core concepts'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, help_text="What are you aiming to build with Python?")
    primary_goal = models.CharField(max_length=50, choices=GOAL_CHOICES, default='beginner')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='zero')
    daily_goal_minutes = models.PositiveIntegerField(default=45, help_text="Target minutes per day")
    current_streak = models.PositiveIntegerField(default=1)
    longest_streak = models.PositiveIntegerField(default=1)
    last_active_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def record_activity(self):
        """Update student streak on daily activity."""
        today = timezone.now().date()
        if self.last_active_date == today:
            return
        
        if self.last_active_date == today - timedelta(days=1):
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        elif self.last_active_date < today - timedelta(days=1):
            self.current_streak = 1
            
        self.last_active_date = today
        self.save()


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, full_name=instance.username)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
