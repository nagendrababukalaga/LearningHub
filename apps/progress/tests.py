from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.learning.models import LearningPath, Level, Topic
from apps.progress.models import UserTopicProgress, PracticeProblem, UserPractice
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake
from apps.progress.services import RevisionRecommendationEngine, DailyPlanGenerator, calculate_user_analytics

class ProgressAndRevisionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_student', password='testpassword123')
        
        self.path = LearningPath.objects.create(title="Python Path", slug="python-path")
        self.level = Level.objects.create(learning_path=self.path, level_number=1, title="Fundamentals")
        
        self.topic1 = Topic.objects.create(
            level=self.level, title="Variables & Naming", order=1, difficulty="beginner",
            objectives="Learn variables", summary_content="Explanation of variables."
        )
        self.topic2 = Topic.objects.create(
            level=self.level, title="Loops & Control", order=2, difficulty="beginner",
            objectives="Learn loops", summary_content="Explanation of loops."
        )

    def test_daily_plan_generation(self):
        plan = DailyPlanGenerator.get_today_plan(self.user)
        self.assertIsNotNone(plan['next_topic'])
        self.assertEqual(plan['next_topic'].id, self.topic1.id)
        self.assertEqual(len(plan['tasks']), 5)
        self.assertEqual(plan['tasks'][0]['phase'], 'Learn')
        self.assertEqual(plan['tasks'][1]['phase'], 'Understand')
        self.assertEqual(plan['tasks'][2]['phase'], 'Practice')

    def test_revision_recommendation_scoring(self):
        # Topic 1 marked as 'need_revision'
        p1 = UserTopicProgress.objects.create(
            user=self.user, topic=self.topic1,
            understanding_level='need_revision', is_completed=True
        )
        # Topic 1 has an open doubt
        LearningDoubt.objects.create(user=self.user, topic=self.topic1, doubt_text="Why are variables references?")
        # Topic 1 has a logged mistake
        LearningMistake.objects.create(user=self.user, topic=self.topic1, mistake_description="Syntax error in name")

        recommendations = RevisionRecommendationEngine.get_revision_recommendations(self.user)
        self.assertTrue(len(recommendations) > 0)
        top_rec = recommendations[0]
        self.assertEqual(top_rec['topic'].id, self.topic1.id)
        # Score must include 50 (need_revision) + 30 (open doubt) + 25 (mistake) = at least 105
        self.assertGreaterEqual(top_rec['score'], 105)

    def test_user_analytics(self):
        UserTopicProgress.objects.create(
            user=self.user, topic=self.topic1,
            understanding_level='strong', is_completed=True
        )
        analytics = calculate_user_analytics(self.user)
        self.assertEqual(analytics['completed_topics_count'], 1)
        self.assertEqual(analytics['strong_topics_count'], 1)
        self.assertEqual(analytics['overall_progress_pct'], 50.0)

    def test_update_progress_ajax(self):
        self.client.login(username='test_student', password='testpassword123')
        response = self.client.post(reverse('progress:update_progress_ajax', kwargs={'topic_id': self.topic1.id}), {
            'understanding_level': 'strong',
            'is_completed': 'true'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['understanding_level'], 'strong')
        self.assertTrue(data['is_completed'])
