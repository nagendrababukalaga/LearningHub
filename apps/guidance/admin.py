from django.contrib import admin
from .models import MentorArticle, MentorTip

@admin.register(MentorArticle)
class MentorArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MentorTip)
class MentorTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_filter = ('category',)
