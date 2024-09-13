from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import CustomUser
from .validators import CustomUserValidator

class BasePasswordSerializer(serializers.ModelSerializer):
    """
    Base serializer for handling password validation.

    Methods:
        validate_passwords(password, password2): Checks if the passwords match and validates the password strength.
    """

    def validate_passwords(self, password, password2):
        """
        Validates that the passwords match and meets the strength requirements.

        Args:
            password (str): The password to validate.
            password2 (str): The confirmation password to validate.

        Raises:
            ValidationError: If passwords do not match or do not meet strength requirements.
        """
        if password != password2:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        try:
            CustomUserValidator.validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.detail})

class UserRegisterSerializer(BasePasswordSerializer):
    """
    Serializer for user registration.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The password for the user account.
        password2 (str): The confirmation password.
        phone_number (str): The phone number of the user.

    Methods:
        validate(attrs): Validates the user registration data.
        create(validated_data): Creates a new user with the validated data.
    """

    first_name = serializers.CharField(required=True, max_length=20)
    last_name = serializers.CharField(required=True, max_length=20)
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'password2', 'phone_number']

    def validate(self, attrs):
        """
        Validates the user registration data.

        Args:
            attrs (dict): The user registration data.

        Returns:
            dict: The validated data.

        Raises:
            ValidationError: If the data does not meet validation requirements.
        """
        self.validate_passwords(attrs.get('password'), attrs.get('password2'))

        try:
            CustomUserValidator.validate_phone_number(attrs.get('phone_number'))
        except ValidationError as error:
            raise serializers.ValidationError(error.detail)

        return attrs

    def create(self, validated_data):
        """
        Creates a new user with the validated data.

        Args:
            validated_data (dict): The validated user registration data.

        Returns:
            CustomUser: The newly created user.
        """
        user = CustomUser.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user
