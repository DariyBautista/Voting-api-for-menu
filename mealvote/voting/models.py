from django.db import models
from django.conf import settings
from restaurants.models import Restaurant  

class Vote(models.Model):
    """
    Represents a vote made by a user for a restaurant's menu on a specific date.

    Attributes:
        user (ForeignKey): The user who made the vote.
        restaurant (ForeignKey): The restaurant being voted for.
        date (DateField): The date on which the vote was cast.

    Meta:
        unique_together (list): Ensures that a user can only vote once per restaurant per day.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        unique_together = ['user', 'restaurant', 'date']
        """
        Ensures that each combination of user, restaurant, and date is unique.
        This constraint prevents a user from voting more than once for the same restaurant on the same day.
        """

    def __str__(self):
        """
        Returns a string representation of the vote.

        Returns:
            str: A description of the vote including user, restaurant, and date.
        """
        return f"{self.user} voted for {self.restaurant} on {self.date}"
