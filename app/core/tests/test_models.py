"""
Testing the custom add user Model
"""
from decimal import Decimal #storing one of the values of the recipe object
from django.test import TestCase
from django.contrib.auth import get_user_model #get user helper function in case we want to change the user model
from core import models

class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com' #example.com is a reserved domain used for testing --> recommanded
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )#create user : method from the model manager

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password)) #hashed password

    def test_new_user_email_normalized(self):
        """test email is normalized for new users by creating a sample lists of the normalized emails"""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            #['Test2@EXAMPLE.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
        )

        self.assertEqual(str(recipe), recipe.title) #checks the string rep of the recipe, returns a title when getting the string representation of the model