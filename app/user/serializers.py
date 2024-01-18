"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate
)
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    """
    This class is where we tell the Django Rest Framework, the model and the fields and any additional arguments
    that we want to pass to the serialize set and the serialized needs to know which model it's representing.
    """

    class Meta:
        model = get_user_model()  # this serializer is going to be for our user model
        fields = ['email', 'password',
                  'name']  # list of fields that we want to make available through the serialization
        # This fields must be only the ones that the user will be able to change through the API

        # Dictionary that allows us to provide extra metadata to provide different fields, by telling DRF things like we
        # do want the fields to be write only or read only, ...
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        """
        The Create method allows us to override the behavior that the serializer does when you create a new user object
        out of that serialize. By doing this the create method will be called after validation and it will only be called 
        after the validation was successful. If the validation error, i.e., the minimum wasn't provided the min length,
        then would just raise a validation error.
        """

        def create(self, validated_data):
            """Create and return a user encrypted password."""
            return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type', 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unabled to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
