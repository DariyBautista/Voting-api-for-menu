from django.shortcuts import render
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.utils.timezone import now
from django.db import models
from django.utils import timezone
from django.db.models import Count
from .models import Vote
from .serializers import VoteSerializer
from restaurants.models import Menu, Restaurant
from restaurants.serializers import MenuSerializer, RestaurantSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class TodayMenuView(generics.ListAPIView):
    """
    Provides a list of menus for the current day.

    Attributes:
        serializer_class (MenuSerializer): The serializer for the Menu model.

    Methods:
        get_queryset(): Returns the queryset of menus for the current day.
    """

    serializer_class = MenuSerializer

    def get_queryset(self):
        """
        Returns the queryset of menus for the current day.

        Returns:
            QuerySet: A queryset of Menu objects for today.
        """
        today = now().date()
        return Menu.objects.filter(date=today)


class VoteCreateView(generics.CreateAPIView):
    """
    Allows authenticated users to create a vote.

    Attributes:
        queryset (QuerySet): The queryset of all Vote objects.
        serializer_class (VoteSerializer): The serializer for the Vote model.
        permission_classes (list): Permissions required for creating a vote.

    Methods:
        perform_create(serializer): Saves the vote if the user hasn't voted today.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Saves the vote if the user hasn't voted today. Raises an error if the user has already voted.

        Args:
            serializer (VoteSerializer): The serializer instance used to save the vote.

        Raises:
            serializers.ValidationError: If the user has already voted today.
        """
        user = self.request.user
        today = timezone.now().date()
        
        if Vote.objects.filter(user=user, date=today).exists():
            raise serializers.ValidationError("You have already voted today.")
        
        serializer.save(user=user, date=today)        


class TodayMenuResultsView(generics.ListAPIView):
    """
    Provides the results of the votes for the restaurant with the highest votes today.

    Attributes:
        serializer_class (RestaurantSerializer): The serializer for the Restaurant model.
        permission_classes (list): Permissions required to view the results.

    Methods:
        get_queryset(): Returns the queryset of the restaurant with the highest votes for today.
    """

    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset of the restaurant with the highest number of votes for today.

        Returns:
            QuerySet: A queryset containing the Restaurant with the highest votes today.
        """
        today = timezone.now().date()

        votes = Vote.objects.filter(date=today).values('restaurant').annotate(total_votes=Count('restaurant')).order_by('-total_votes')

        if votes.exists():
            restaurant_id = votes.first()['restaurant']
            return Restaurant.objects.filter(id=restaurant_id)

        return Restaurant.objects.none()
