from django.contrib import admin
from .models import StudentStory

@admin.register(StudentStory)
class StudentStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_or_college', 'outcome', 'order')
