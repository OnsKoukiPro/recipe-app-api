"""
Views for the user API.
"""
from rest_framework import generics #baseclasses

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView): #creating objects
    """Create a new user in the system."""
    serializer_class = UserSerializer

#when we make an http request, it maps through the url, then it gets passed into the createUserView class that calls the serializer, creates the object and returns a response