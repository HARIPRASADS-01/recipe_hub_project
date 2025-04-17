# recipes/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField()
    prep_time = models.PositiveIntegerField(help_text='Preparation time in minutes')
    cook_time = models.PositiveIntegerField(help_text='Cooking time in minutes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    ingredients = models.TextField(help_text='List ingredients, one per line or separated by commas')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']