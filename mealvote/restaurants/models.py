from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    """
    Represents a restaurant.

    Attributes:
        name (str): The name of the restaurant.
        address (str): The address of the restaurant.
        phone_number (str): The phone number of the restaurant.
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        """
        Returns a string representation of the restaurant.

        Returns:
            str: The name of the restaurant.
        """
        return self.name

class Menu(models.Model):
    """
    Represents a menu for a specific restaurant on a specific date.

    Attributes:
        restaurant (Restaurant): The restaurant associated with the menu.
        date (date): The date of the menu.
        items (str): The items included in the menu.
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    items = models.TextField()

    class Meta:
        unique_together = ('restaurant', 'date')

    def __str__(self):
        """
        Returns a string representation of the menu.

        Returns:
            str: A string combining the restaurant name and menu date.
        """
        return f"{self.restaurant.name} - {self.date}"
