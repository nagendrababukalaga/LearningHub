from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.learning.models import LearningPath, Level, Topic
from apps.memory.models import PersonalLearningMemory, LearningDoubt, LearningMistake

class MemoryAndDoubtTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alex_learner', password='password123')
        self.path = LearningPath.objects.create(title="Python Path", slug="python-path")
        self.level = Level.objects.create(learning_path=self.path, level_number=1, title="Fundamentals")
        self.topic = Topic.objects.create(level=self.level, title="Strings", order=1, difficulty="beginner")

    def test_save_personal_learning_memory(self):
        self.client.login(username='alex_learner', password='password123')
        response = self.client.post(reverse('memory:save_memory_ajax', kwargs={'topic_id': self.topic.id}), {
            'what_i_understood': 'Strings are immutable Unicode sequences.',
            'my_own_explanation': 'Like letters etched in stone.',
            'real_life_analogy': 'A printed newspaper.',
        })
        self.assertEqual(response.status_code, 200)
        
        memory = PersonalLearningMemory.objects.get(user=self.user, topic=self.topic)
        self.assertEqual(memory.real_life_analogy, 'A printed newspaper.')
        self.assertTrue(memory.is_filled)

    def test_create_and_resolve_doubt(self):
        doubt = LearningDoubt.objects.create(
            user=self.user, topic=self.topic, doubt_text="Can we index strings with negative numbers?"
        )
        self.assertFalse(doubt.is_resolved)

        doubt.mark_resolved("Yes, -1 starts from the rightmost character.")
        self.assertTrue(doubt.is_resolved)
        self.assertIn("-1 starts from the rightmost", doubt.resolution_notes)

    def test_mistake_tracking(self):
        mistake = LearningMistake.objects.create(
            user=self.user, topic=self.topic,
            mistake_description="Tried s[0] = 'H' on immutable string.",
            correction_or_lesson="Strings are immutable. Create a new string with slicing or replace.",
            error_type="type"
        )
        self.assertEqual(mistake.error_type, 'type')
        self.assertEqual(LearningMistake.objects.filter(user=self.user).count(), 1)
