# recipes/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe

# --- User Registration Form ---
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. A valid email address, please.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists(): # Case-insensitive check
            raise forms.ValidationError("An account with this email address already exists.")
        return email

# --- Recipe Add/Edit Form ---
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'ingredients',
            'instructions',
            'prep_time',
            'cook_time',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Recipe Title'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A short description...'}),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'placeholder': 'e.g.\n1 cup flour\n2 eggs\n1 tsp salt'}),
            'instructions': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Step-by-step instructions...'}),
            'prep_time': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'min': '0', 'placeholder': 'Minutes'}),
        }
        help_texts = {
             'ingredients': '', # Clear default help text
             'image': 'Optional: Upload a picture of the finished dish.',
             'prep_time': '', # Clear default help text
             'cook_time': '', # Clear default help text
        }
        labels = {
            'prep_time': 'Prep Time (minutes)', # More descriptive labels
            'cook_time': 'Cook Time (minutes)',
        }