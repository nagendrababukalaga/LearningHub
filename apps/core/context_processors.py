from apps.learning.models import LearningPath
from apps.progress.models import UserTopicProgress
from apps.memory.models import LearningDoubt

def global_context(request):
    """
    Context processor to supply global variables to all templates.
    """
    context = {
        'APP_NAME': 'LearningHub',
        'APP_TAGLINE': 'Learn Python with direction, not confusion.',
        'primary_path': LearningPath.objects.filter(is_active=True).first(),
    }
    
    if request.user.is_authenticated:
        # Calculate pending revision count for navbar badge
        need_revision_count = UserTopicProgress.objects.filter(
            user=request.user,
            understanding_level='need_revision'
        ).count()
        
        open_doubts_count = LearningDoubt.objects.filter(
            user=request.user,
            is_resolved=False
        ).count()
        
        context['nav_revision_badge'] = need_revision_count
        context['nav_doubts_badge'] = open_doubts_count
        context['user_profile'] = getattr(request.user, 'profile', None)
    
    return context
