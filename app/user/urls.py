"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user' #is going to be used for the reverse mapping defined in the test user api

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView, name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]