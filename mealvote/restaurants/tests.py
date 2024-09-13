from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from restaurants.models import Restaurant, Menu
from django.utils import timezone
from datetime import timedelta

class RestaurantSerializerValidationTests(TestCase):
    """
    Tests for validating RestaurantSerializer.

    Methods:
        setUp() : Initializes APIClient for testing.
        test_valid_restaurant_creation() : Tests creation of a valid restaurant.
        test_invalid_phone_number() : Tests creation of a restaurant with an invalid phone number.
        test_non_numeric_phone_number() : Tests creation of a restaurant with a non-numeric phone number.
        test_empty_address() : Tests creation of a restaurant with an empty address.
    """

    def setUp(self):
        """
        Initializes the APIClient for making requests.
        """
        self.client = APIClient()

    def test_valid_restaurant_creation(self):
        """
        Tests that a valid restaurant can be created successfully.
        """
        response = self.client.post('/restaurants/create/', {
            'name': 'Valid Restaurant',
            'address': '123 Valid St',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'Valid Restaurant')

    def test_invalid_phone_number(self):
        """
        Tests that a restaurant with an invalid phone number is rejected.
        """
        response = self.client.post('/restaurants/create/', {
            'name': 'Invalid Phone Restaurant',
            'address': '123 Invalid St',
            'phone_number': '12345'  # Invalid phone number
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertEqual(response.data['phone_number'][0], 'Phone number must be at least 10 digits long and contain only numbers.')

    def test_non_numeric_phone_number(self):
        """
        Tests that a restaurant with a non-numeric phone number is rejected.
        """
        response = self.client.post('/restaurants/create/', {
            'name': 'Non Numeric Phone Restaurant',
            'address': '123 Non-Numeric St',
            'phone_number': '12345abcde'  # Non-numeric phone number
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)
        self.assertEqual(response.data['phone_number'][0], 'Phone number must be at least 10 digits long and contain only numbers.')

    def test_empty_address(self):
        """
        Tests that a restaurant with an empty address is rejected.
        """
        response = self.client.post('/restaurants/create/', {
            'name': 'Test Restaurant',
            'address': '',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('address', response.data)
        self.assertEqual(response.data['address'][0], 'This field may not be blank.')


class MenuCreationTests(TestCase):
    """
    Tests for creating Menu objects.

    Methods:
        setUp() : Initializes APIClient and creates a test restaurant.
        test_valid_menu_creation_today() : Tests creation of a valid menu for today.
        test_valid_menu_creation_future_date() : Tests creation of a valid menu for a future date.
        test_menu_creation_missing_restaurant() : Tests menu creation without specifying a restaurant.
        test_menu_creation_past_date() : Tests menu creation for a past date.
    """

    def setUp(self):
        """
        Initializes the APIClient and creates a test restaurant.
        """
        self.client = APIClient()
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            phone_number='1234567890'
        )

    def test_valid_menu_creation_today(self):
        """
        Tests that a valid menu can be created for today.
        """
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': timezone.now().date(),
            'items': 'Pizza, Pasta'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().restaurant, self.restaurant)

    def test_valid_menu_creation_future_date(self):
        """
        Tests that a valid menu can be created for a future date.
        """
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': future_date,
            'items': 'Burger, Salad'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().restaurant, self.restaurant)
        
    def test_menu_creation_missing_restaurant(self):
        """
        Tests that menu creation fails if no restaurant is specified.
        """
        future_date = timezone.now().date() + timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'date': future_date,
            'items': 'Tacos, Burritos'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('restaurant', response.data)
        self.assertEqual(response.data['restaurant'][0], 'This field is required.')
        
    def test_menu_creation_past_date(self):
        """
        Tests that menu creation fails for a past date.
        """
        past_date = timezone.now().date() - timedelta(days=1)
        response = self.client.post('/restaurants/menu/upload/', {
            'restaurant': self.restaurant.id,
            'date': past_date,
            'items': 'Sushi, Ramen'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)
        self.assertEqual(
            response.data['date'],
            'Cannot set a menu for a past date. Please select today or a future date.'
        )
