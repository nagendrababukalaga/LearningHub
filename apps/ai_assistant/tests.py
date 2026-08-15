from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.learning.models import LearningPath, Level, Topic
from apps.memory.models import PersonalLearningMemory
from apps.ai_assistant.services import ContextualAIService

class AIAssistantTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='ai_student', password='password123')
        self.path = LearningPath.objects.create(title="Python Path", slug="python-path")
        self.level = Level.objects.create(learning_path=self.path, level_number=1, title="Fundamentals")
        self.topic = Topic.objects.create(level=self.level, title="Python Loops", order=1, difficulty="beginner")

    def test_ai_offline_fallback_generator(self):
        # 1. Simplify mode
        resp_simplify = ContextualAIService.generate_response(
            user=self.user, prompt_text="", topic_id=self.topic.id, action_mode='simplify'
        )
        self.assertIn("Simplified Breakdown", resp_simplify)

        # 2. Analogy mode
        resp_analogy = ContextualAIService.generate_response(
            user=self.user, prompt_text="", topic_id=self.topic.id, action_mode='analogy'
        )
        self.assertIn("Real-World Analogies", resp_analogy)

        # 3. Practice challenge mode
        resp_practice = ContextualAIService.generate_response(
            user=self.user, prompt_text="", topic_id=self.topic.id, action_mode='practice'
        )
        self.assertIn("Coding Challenges", resp_practice)

    def test_ai_chat_api_endpoint(self):
        self.client.login(username='ai_student', password='password123')
        response = self.client.post(reverse('ai_assistant:api_query'), {
            'prompt': 'How do while loops work in Python?',
            'topic_id': self.topic.id,
            'action_mode': 'general'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('LearningHub AI Assistant', data['response'])
