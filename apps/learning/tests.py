from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.learning.models import LearningPath, Level, Topic, Resource, Bookmark

class LearningResourceModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student_test', password='password123')
        self.path = LearningPath.objects.create(title="Python Path", slug="python-path")
        self.level = Level.objects.create(learning_path=self.path, level_number=1, title="Fundamentals")
        self.topic = Topic.objects.create(
            level=self.level,
            title="Introduction to Python & Setup",
            order=1,
            difficulty="beginner",
            objectives="Learn Python setup and PEP 20.",
            summary_content="Python architecture explanation."
        )

    def test_resource_creation_and_fields(self):
        res = Resource.objects.create(
            topic=self.topic,
            title="The Zen of Python (PEP 20)",
            resource_type="doc",
            url="https://peps.python.org/pep-0020/",
            author_or_source="Python.org",
            duration_or_read_time="5 min read",
            is_recommended=True,
            order=1
        )
        self.assertEqual(res.topic, self.topic)
        self.assertEqual(res.url, "https://peps.python.org/pep-0020/")
        self.assertEqual(res.author_or_source, "Python.org")
        self.assertIn("The Zen of Python (PEP 20)", str(res))
        self.assertTrue(res.is_recommended)

    def test_topic_detail_renders_resources(self):
        res1 = Resource.objects.create(
            topic=self.topic,
            title="The Zen of Python (PEP 20)",
            resource_type="doc",
            url="https://peps.python.org/pep-0020/",
            author_or_source="Python.org",
            duration_or_read_time="5 min read",
            order=1
        )
        res2 = Resource.objects.create(
            topic=self.topic,
            title="Python Tutorial",
            resource_type="doc",
            url="https://docs.python.org/3/tutorial/appetite.html",
            author_or_source="Python.org",
            duration_or_read_time="15 min read",
            order=2
        )

        response = self.client.get(reverse('learning:topic_detail', kwargs={'slug': self.topic.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Zen of Python (PEP 20)")
        self.assertContains(response, "https://peps.python.org/pep-0020/")
        self.assertContains(response, "https://docs.python.org/3/tutorial/appetite.html")

    def test_bookmark_resource_toggle(self):
        self.client.login(username='student_test', password='password123')
        res = Resource.objects.create(
            topic=self.topic,
            title="The Zen of Python (PEP 20)",
            resource_type="doc",
            url="https://peps.python.org/pep-0020/",
            order=1
        )

        # Toggle on
        response = self.client.post(
            reverse('learning:toggle_bookmark', kwargs={'resource_id': res.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertTrue(data['is_bookmarked'])
        self.assertEqual(Bookmark.objects.filter(user=self.user, resource=res).count(), 1)

        # Toggle off
        response = self.client.post(
            reverse('learning:toggle_bookmark', kwargs={'resource_id': res.id}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')
        self.assertFalse(data['is_bookmarked'])
        self.assertEqual(Bookmark.objects.filter(user=self.user, resource=res).count(), 0)
