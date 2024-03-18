from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from customers.models import CustomerProfile, AgentProfile, BlockedAgent, User
from customers.serializers import UserSerializer
from messages_user.models import Message  # Assuming this is your model for messages

User = get_user_model()

class UserSerializerVisibilityTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        
        self.customer = User.objects.create_user(username='customerUser', password='testpass', is_customer=True)
        self.customer_profile = CustomerProfile.objects.get_or_create(user=self.customer)[0]  # Ensure profile is created

        self.agent = User.objects.create_user(username='agentUser', password='testpass', is_agent=True)
        self.agent_profile = AgentProfile.objects.get_or_create(user=self.agent)[0]  # Ensure profile is created

        self.other_customer = User.objects.create_user(username='otherCustomer', password='testpass', is_customer=True)
        self.other_customer_profile = CustomerProfile.objects.get_or_create(user=self.other_customer)[0]  # Ensure profile is created

        # BlockedAgent and other necessary setup

        BlockedAgent.objects.create(customer=self.customer, agent=self.agent)

    def test_customer_sees_agent_info_public_profile_true(self):
        self.agent.public_profile = True
        self.agent.save()

        request = self.factory.get('/fake-url')
        request.user = self.customer
        serializer = UserSerializer(instance=self.agent, context={'request': request})
        data = serializer.data

        self.assertIn('username', data)
        # Assuming 'email' should not be visible according to your model's privacy logic
        self.assertNotIn('email', data)

    def test_agent_sees_limited_customer_info_after_interaction_public_profile_false(self):
        self.customer.public_profile = False
        self.customer.save()

        # Simulating an interaction
        Message.objects.create(sender=self.customer, recipient=self.agent, content="Hello")

        request = self.factory.get('/fake-url')
        request.user = self.agent
        serializer = UserSerializer(instance=self.customer, context={'request': request})
        data = serializer.data

        # Adjust based on your visibility logic
        self.assertNotIn('phone_number', data)
        self.assertIn('nickname', data)  # Assuming 'nickname' is visible after interaction

    def test_customer_cannot_see_other_customer_info_public_profile_true(self):
        self.other_customer.public_profile = True
        self.other_customer.save()

        request = self.factory.get('/fake-url')
        request.user = self.customer
        serializer = UserSerializer(instance=self.other_customer, context={'request': request})
        data = serializer.data

        # Expecting empty data as customers should not see other customer's info
        self.assertEqual(data, {})

    # Adjust this test to match your review visibility logic
    def test_visibility_of_reviewer_info(self):
        # This test would need a Review model instance linked to a user
        # and verification of its visibility based on the logic you've implemented.
        pass
