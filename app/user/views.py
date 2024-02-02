"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions #baseclasses
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView): #creating objects
    """Create a new user in the system."""
    serializer_class = UserSerializer

#when we make an http request, it maps through the url, then it gets passed into the createUserView class that calls the serializer, creates the object and returns a response

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        print("CreateTokenView - post method called")
        response = super().post(request, *args, **kwargs)
        print("Response:", response.data)
        return response


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user