# customers/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import AgentProfile, CustomerProfile, BlockedAgent

User = get_user_model()

class UserModelTests(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create_user(username='testuser', email='user@test.com', password='testpass123')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_agent)  # Assuming default is False

    def test_agent_profile_creation(self):
        AgentProfile.objects.create(user=self.user)
        self.assertTrue(hasattr(self.user, 'agent_profile'))

    # Add more tests as needed
