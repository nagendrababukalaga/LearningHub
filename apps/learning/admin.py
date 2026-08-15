from django.contrib import admin
from .models import LearningPath, Level, Topic, Resource, Bookmark

class LevelInline(admin.TabularInline):
    model = Level
    extra = 1

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ('order', 'title', 'difficulty', 'estimated_minutes', 'is_active')

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'order', 'total_topics')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [LevelInline]

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level_number', 'title', 'learning_path', 'topics_count')
    list_filter = ('learning_path',)
    inlines = [TopicInline]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'order', 'difficulty', 'estimated_minutes', 'is_active')
    list_filter = ('level__learning_path', 'level', 'difficulty', 'is_active')
    search_fields = ('title', 'summary_content', 'objectives')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ResourceInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'resource_type', 'author_or_source', 'is_recommended')
    list_filter = ('resource_type', 'is_recommended')
    search_fields = ('title', 'author_or_source', 'topic__title')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'created_at')
    list_filter = ('created_at',)
