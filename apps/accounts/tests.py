from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_student_registration(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'new_coder',
            'email': 'coder@example.com',
            'first_name': 'Sam',
            'last_name': 'Miller',
            'primary_goal': 'internship',
            'experience_level': 'zero',
            'password': 'strongpassword123',
            'confirm_password': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='new_coder').exists())
        user = User.objects.get(username='new_coder')
        self.assertEqual(user.profile.primary_goal, 'internship')

    def test_login_and_streak_recording(self):
        user = User.objects.create_user(username='streak_user', password='password123')
        self.assertEqual(user.profile.current_streak, 1)

        response = self.client.post(reverse('accounts:login'), {
            'username': 'streak_user',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
