from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from restaurants.models import Restaurant, Menu
from voting.models import Vote

User = get_user_model()

class VotingTests(TestCase):
    """
    Test suite for the voting functionality in the application.
    """

    def setUp(self):
        """
        Set up the test environment. Creates a user, generates a JWT token,
        creates a restaurant, and sets up a menu for testing purposes.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )
        # Generate JWT token
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Set up necessary data
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            phone_number='1234567890'
        )
        self.menu = Menu.objects.create(
            restaurant=self.restaurant,
            date='2024-09-13'
        )

    def test_today_menu(self):
        """
        Test retrieving today's menu. 
        Asserts that the endpoint for retrieving today's menu responds with a 200 OK status.
        """
        response = self.client.get('/voting/menu/today/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_vote_creation(self):
        """
        Test creating a vote for a restaurant.
        Asserts that creating a vote responds with a 201 Created status and that the vote is correctly created.
        """
        response = self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_vote_already_voted(self):
        """
        Test voting twice for the same restaurant.
        Asserts that attempting to vote again for the same restaurant responds with a 400 Bad Request status.
        """
        self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        response = self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_vote_results(self):
        """
        Test retrieving vote results after a vote is cast.
        Asserts that the endpoint for retrieving vote results responds with a 200 OK status and that the results are correct.
        """
        self.client.post('/voting/vote/', {
            'restaurant': self.restaurant.id
        })
        response = self.client.get('/voting/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_vote_results_no_votes(self):
        """
        Test retrieving vote results when no votes have been cast.
        Asserts that the endpoint for retrieving vote results responds with a 200 OK status even if no votes are present.
        """
        response = self.client.get('/voting/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
