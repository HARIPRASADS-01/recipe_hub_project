# recipes/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Recipe # Import the Recipe model

class RecipeModelTests(TestCase):

    def setUp(self):
        """
        Set up non-modified objects used by all test methods.
        This runs once before each test method in this class.
        """
        # Create a test user that recipes can be associated with
        self.user = User.objects.create_user(username='testuser', password='testpassword123')

    def test_recipe_creation(self):
        """
        Test that a Recipe object can be created successfully with minimal required fields.
        """
        recipe = Recipe.objects.create(
            title="Test Recipe",
            instructions="Mix and bake.",
            prep_time=10,
            cook_time=20,
            author=self.user # Use the user created in setUp
        )
        # Assertions: Check if the object behaves as expected
        self.assertEqual(recipe.title, "Test Recipe")
        self.assertEqual(recipe.prep_time, 10)
        self.assertEqual(recipe.author.username, 'testuser')
        # Test the __str__ method implicitly by converting the object to string
        self.assertEqual(str(recipe), "Test Recipe")
        # Check if it was actually saved to the database
        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_str_method(self):
        """
        Explicitly test the __str__ method returns the title.
        """
        recipe = Recipe.objects.create(
            title="Another Test Title",
            instructions="Boil water.",
            prep_time=5,
            cook_time=1,
            author=self.user
        )
        self.assertEqual(str(recipe), recipe.title) # Check __str__ output against title

    # Add more tests here later, e.g., for default ordering,
    # testing constraints, or model methods if you add any.