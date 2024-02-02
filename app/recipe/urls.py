"""
URL MAPPINGS FOR TEH RECIPE APP
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet) #creates a new endpoint

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]