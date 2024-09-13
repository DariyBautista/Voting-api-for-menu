from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from rest_framework.exceptions import ValidationError
# from utils.version_decorators import check_version

class RestaurantCreateView(generics.CreateAPIView):
    """
    API view for creating a new restaurant.

    Attributes:
        queryset (QuerySet): The queryset of all restaurants.
        serializer_class (Serializer): The serializer used for creating restaurants.
        permission_classes (list): Permissions for accessing this view.

    Methods:
        post(request, *args, **kwargs): Handles POST requests to create a new restaurant.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]  # Change to a custom permission in the future

    # @check_version('1.0')
    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests to create a new restaurant.

    #     Args:
    #         request (Request): The HTTP request object.
    #         *args: Additional positional arguments.
    #         **kwargs: Additional keyword arguments.

    #     Returns:
    #         Response: The response containing the created restaurant data.
    #     """
    #     return super().post(request, *args, **kwargs)

class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API viewset for retrieving, updating, and deleting restaurants.

    Attributes:
        queryset (QuerySet): The queryset of all restaurants.
        serializer_class (Serializer): The serializer used for restaurant data.
        permission_classes (list): Permissions for accessing this viewset.

    Methods:
        create(request, *args, **kwargs): Handles POST requests to create a new restaurant (commented out).
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    # @check_version('1.0')
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

class MenuCreateView(generics.CreateAPIView):
    """
    API view for creating a new menu.

    Attributes:
        queryset (QuerySet): The queryset of all menus.
        serializer_class (Serializer): The serializer used for creating menus.
        permission_classes (list): Permissions for accessing this view.

    Methods:
        post(request, *args, **kwargs): Handles POST requests to create a new menu.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]  # Change to a custom permission in the future
    
    def perform_create(self, serializer):
        date = serializer.validated_data.get('date')
        if date < timezone.now().date():
            raise ValidationError({'date': 'Cannot set a menu for a past date. Please select today or a future date.'})
        super().perform_create(serializer)


class TodayMenuView(generics.ListAPIView):
    """
    API view for listing today's menu items.

    Attributes:
        serializer_class (Serializer): The serializer used for menu data.
        permission_classes (list): Permissions for accessing this view.

    Methods:
        get_queryset(): Returns a queryset of menu items for today.
    """
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns a queryset of menu items for today.

        Returns:
            QuerySet: The queryset of menu items for the current date.
        """
        date = timezone.now().date()
        return Menu.objects.filter(date=date)
