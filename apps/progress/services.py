from django.utils import timezone
from datetime import timedelta
from apps.learning.models import Topic, LearningPath
from apps.progress.models import UserTopicProgress, DailyTask, UserDailyTask, PracticeProblem, UserPractice
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake
from apps.bootcamp.models import BootcampDay, UserBootcampProgress

class RevisionRecommendationEngine:
    """
    Rule-based intelligent revision engine that inspects student's
    personal learning memory, logged mistakes, open doubts, and understanding levels.
    """

    @staticmethod
    def get_revision_recommendations(user, limit=5):
        recommendations = []
        user_progress_map = {
            p.topic_id: p for p in UserTopicProgress.objects.filter(user=user).select_related('topic', 'topic__level')
        }
        
        # Get all active topics
        active_topics = Topic.objects.filter(is_active=True).select_related('level', 'level__learning_path')
        
        for topic in active_topics:
            progress = user_progress_map.get(topic.id)
            score = 0
            reasons = []

            # Check open doubts
            open_doubts = LearningDoubt.objects.filter(user=user, topic=topic, is_resolved=False)
            open_doubts_count = open_doubts.count()
            if open_doubts_count > 0:
                score += 30 * min(open_doubts_count, 3)
                reasons.append(f"You have {open_doubts_count} unresolved doubt{'s' if open_doubts_count > 1 else ''} recorded.")

            # Check mistakes
            mistakes = LearningMistake.objects.filter(user=user, topic=topic)
            mistakes_count = mistakes.count()
            if mistakes_count > 0:
                score += 25 * min(mistakes_count, 2)
                reasons.append(f"You logged {mistakes_count} mistake{'s' if mistakes_count > 1 else ''} during practice.")

            # Check understanding level
            if progress:
                if progress.understanding_level == 'need_revision':
                    score += 50
                    reasons.append("You manually marked this topic as 'Need Revision'.")
                elif progress.understanding_level == 'learning':
                    score += 20
                    reasons.append("You are currently learning this concept.")
                
                # Check days since last review
                if progress.is_completed and progress.last_reviewed_at:
                    days_ago = (timezone.now() - progress.last_reviewed_at).days
                    if days_ago >= 5:
                        score += 15
                        reasons.append(f"It has been {days_ago} days since you last reviewed this topic.")

            # Check if memory is empty for a completed topic
            if progress and progress.is_completed:
                has_memory = PersonalLearningMemory.objects.filter(user=user, topic=topic).exists()
                if not has_memory:
                    score += 15
                    reasons.append("You haven't recorded your own mental model / analogy for this topic yet.")

            if score > 0:
                recommendations.append({
                    'topic': topic,
                    'progress': progress,
                    'score': score,
                    'reasons': reasons,
                    'open_doubts_count': open_doubts_count,
                    'mistakes_count': mistakes_count,
                    'level': topic.level,
                })

        # Sort descending by priority score
        recommendations.sort(key=lambda r: r['score'], reverse=True)
        return recommendations[:limit] if limit else recommendations


class DailyPlanGenerator:
    """
    Generates a clear, actionable daily learning routine for the student.
    Eliminates decision fatigue: answers 'What should I do today?'
    """

    @staticmethod
    def get_today_plan(user):
        today = timezone.now().date()
        
        # 1. Determine next recommended topic
        completed_topic_ids = set(UserTopicProgress.objects.filter(
            user=user, is_completed=True
        ).values_list('topic_id', flat=True))

        next_topic = Topic.objects.filter(
            is_active=True
        ).exclude(
            id__in=completed_topic_ids
        ).order_by('level__level_number', 'order').first()

        # If all completed, cycle back to revision
        if not next_topic:
            next_topic = Topic.objects.filter(is_active=True).first()

        # 2. Check top revision item
        revision_items = RevisionRecommendationEngine.get_revision_recommendations(user, limit=1)
        top_revision = revision_items[0] if revision_items else None

        # 3. Build today's structured task list
        tasks = []

        # Step 1: Learn
        tasks.append({
            'step_number': 1,
            'phase': 'Learn',
            'type': 'learn',
            'title': f"Study: {next_topic.title}",
            'description': f"Read the conceptual breakdown and explore recommended resources for {next_topic.title}.",
            'estimated_minutes': next_topic.estimated_minutes or 30,
            'topic': next_topic,
            'action_url': f"/topics/{next_topic.slug}/",
            'is_completed': False
        })

        # Step 2: Understand (Personal Learning Memory)
        tasks.append({
            'step_number': 2,
            'phase': 'Understand',
            'type': 'understand',
            'title': "Formulate Personal Mental Model",
            'description': f"Write down your own explanation and a real-world analogy for {next_topic.title}.",
            'estimated_minutes': 15,
            'topic': next_topic,
            'action_url': f"/topics/{next_topic.slug}/#memory-section",
            'is_completed': False
        })

        # Step 3: Practice
        practice_prob = PracticeProblem.objects.filter(topic=next_topic).first()
        tasks.append({
            'step_number': 3,
            'phase': 'Practice',
            'type': 'practice',
            'title': f"Solve Practice Challenge: {practice_prob.title if practice_prob else next_topic.title}",
            'description': "Write clean Python code without looking up the solution. Track any mistakes made.",
            'estimated_minutes': 20,
            'topic': next_topic,
            'action_url': f"/practice/?topic={next_topic.id}",
            'is_completed': False
        })

        # Step 4: Review / Revision
        if top_revision:
            rev_topic = top_revision['topic']
            tasks.append({
                'step_number': 4,
                'phase': 'Review',
                'type': 'review',
                'title': f"10-Minute Active Revision: {rev_topic.title}",
                'description': f"Priority Revision: {top_revision['reasons'][0]}",
                'estimated_minutes': 10,
                'topic': rev_topic,
                'action_url': f"/topics/{rev_topic.slug}/",
                'is_completed': False
            })
        else:
            tasks.append({
                'step_number': 4,
                'phase': 'Review',
                'type': 'review',
                'title': "Review Mistakes & Doubts Log",
                'description': "Check your logged mistakes log and reinforce key takeaways.",
                'estimated_minutes': 10,
                'topic': next_topic,
                'action_url': "/memory/mistakes/",
                'is_completed': False
            })

        # Step 5: Complete
        tasks.append({
            'step_number': 5,
            'phase': 'Complete',
            'type': 'complete',
            'title': f"Mark {next_topic.title} Understanding Level",
            'description': "Update your progress to Comfortable or Strong and celebrate daily consistency!",
            'estimated_minutes': 5,
            'topic': next_topic,
            'action_url': f"/topics/{next_topic.slug}/",
            'is_completed': False
        })

        # Calculate total estimated study time
        total_time = sum(t['estimated_minutes'] for t in tasks)

        return {
            'next_topic': next_topic,
            'top_revision': top_revision,
            'tasks': tasks,
            'total_time_minutes': total_time,
            'date': today
        }


def calculate_user_analytics(user):
    """
    Computes real-time progress percentages and mastery metrics for student dashboard.
    """
    total_topics = Topic.objects.filter(is_active=True).count() or 1
    
    progress_qs = UserTopicProgress.objects.filter(user=user)
    completed_topics_count = progress_qs.filter(is_completed=True).count()
    strong_topics_count = progress_qs.filter(understanding_level='strong').count()
    comfortable_topics_count = progress_qs.filter(understanding_level='comfortable').count()
    need_revision_count = progress_qs.filter(understanding_level='need_revision').count()
    
    overall_progress_pct = round((completed_topics_count / total_topics) * 100, 1)

    # Practice stats
    total_practice_problems = PracticeProblem.objects.count() or 1
    solved_practice_count = UserPractice.objects.filter(user=user, status='solved').count()
    practice_progress_pct = round((solved_practice_count / total_practice_problems) * 100, 1)

    # Memory & Doubts
    memories_count = PersonalLearningMemory.objects.filter(user=user).count()
    open_doubts_count = LearningDoubt.objects.filter(user=user, is_resolved=False).count()
    resolved_doubts_count = LearningDoubt.objects.filter(user=user, is_resolved=True).count()
    mistakes_count = LearningMistake.objects.filter(user=user).count()

    # Bootcamp stats
    total_bootcamp_days = BootcampDay.objects.count() or 30
    completed_bootcamp_days = UserBootcampProgress.objects.filter(user=user, is_completed=True).count()
    bootcamp_progress_pct = round((completed_bootcamp_days / total_bootcamp_days) * 100, 1)

    return {
        'total_topics': total_topics,
        'completed_topics_count': completed_topics_count,
        'overall_progress_pct': overall_progress_pct,
        'strong_topics_count': strong_topics_count,
        'comfortable_topics_count': comfortable_topics_count,
        'need_revision_count': need_revision_count,
        'total_practice_problems': total_practice_problems,
        'solved_practice_count': solved_practice_count,
        'practice_progress_pct': practice_progress_pct,
        'memories_count': memories_count,
        'open_doubts_count': open_doubts_count,
        'resolved_doubts_count': resolved_doubts_count,
        'mistakes_count': mistakes_count,
        'total_bootcamp_days': total_bootcamp_days,
        'completed_bootcamp_days': completed_bootcamp_days,
        'bootcamp_progress_pct': bootcamp_progress_pct,
    }
