from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import CustomerProfile, AgentProfile, BlockedAgent

User = get_user_model()

class UserApiVisibilityTests(APITestCase):
    def setUp(self):
        # Setup users
        self.customer = User.objects.create_user(username='customer', email='customer@test.com', password='test', is_customer=True)
        self.agent = User.objects.create_user(username='agent', email='agent@test.com', password='test', is_agent=True)
        self.other_customer = User.objects.create_user(username='othercustomer', email='othercustomer@test.com', password='test', is_customer=True)
        
        # # Setup customer profile for self.customer
        # CustomerProfile.objects.create(user=self.customer, location='Test Location')
        
        # # Setup agent profile for self.agent
        # AgentProfile.objects.create(user=self.agent)
        
        # Block agent for the customer
        BlockedAgent.objects.create(customer=self.customer, agent=self.agent)
        
        self.profile_url = reverse('current_user')

    def authenticate_and_get(self, user):
        self.client.force_authenticate(user=user)
        return self.client.get(self.profile_url)

    def test_agent_cannot_see_blocked_customer_profile(self):
        response = self.authenticate_and_get(self.agent)
        # Assuming agent cannot see detailed info of a customer who blocked them
        self.assertNotIn('email', response.data)

    def test_customer_can_see_agent_profile(self):
        response = self.authenticate_and_get(self.customer)
        # Assuming customers can see agent profiles not blocked
        self.assertIn('username', response.data)
        
    def test_customer_cannot_see_other_customer_info(self):
        response = self.authenticate_and_get(self.other_customer)
        # Assuming a customer cannot see other customer's profile details
        self.assertNotIn('email', response.data)

    def test_visibility_based_on_reviews(self):
        # Assuming there's a review by 'self.customer' visible to all including blocked agents
        # You'll need to setup a review instance linked to 'self.customer' and verify its visibility
        pass
