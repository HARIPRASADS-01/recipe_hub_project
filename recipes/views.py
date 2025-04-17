# recipes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Recipe
from .forms import CustomUserCreationForm, RecipeForm

# --- Recipe List View (with Search & Pagination) ---
def recipe_list(request):
    """ Displays all recipes with search and pagination. """
    all_recipes_list = Recipe.objects.all() # Base queryset

    # Apply search filtering if 'q' parameter exists
    search_query = request.GET.get('q')
    if search_query:
        all_recipes_list = all_recipes_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query) |
            Q(instructions__icontains=search_query) |
            Q(author__username__icontains=search_query)
        ).distinct()

    # Apply pagination
    items_per_page = 8 # Increased items per page slightly
    paginator = Paginator(all_recipes_list, items_per_page)
    page_number = request.GET.get('page')

    try:
        recipes_page = paginator.page(page_number)
    except PageNotAnInteger:
        recipes_page = paginator.page(1) # Default to first page
    except EmptyPage:
        recipes_page = paginator.page(paginator.num_pages) # Default to last page

    context = {
        'recipes_page': recipes_page,
        'page_title': 'Recipes', # Simplified title
        'search_query': search_query,
    }
    return render(request, 'recipes/recipe_list.html', context)

# --- Recipe Detail View ---
def recipe_detail(request, pk):
    """ Displays the full details of a single recipe. """
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
        'page_title': recipe.title
    }
    return render(request, 'recipes/recipe_detail.html', context)

# --- User Signup View ---
def signup(request):
    """ Handles new user registration. """
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}! Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    context = {'form': form, 'page_title': 'Create an Account'}
    return render(request, 'registration/signup.html', context)

# --- Add Recipe View ---
@login_required
def add_recipe(request):
    """ Allows logged-in users to add a new recipe. """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, f'Recipe "{recipe.title}" added successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = RecipeForm()

    context = {
        'form': form,
        'page_title': 'Add Your Recipe'
    }
    return render(request, 'recipes/recipe_form.html', context)

# --- Edit Recipe View ---
@login_required
def edit_recipe(request, pk):
    """ Allows the author of a recipe to edit it. """
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        raise PermissionDenied("You cannot edit a recipe you didn't create.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, f'Recipe "{recipe.title}" updated.')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, 'Please check the form for errors.')
    else:
        form = RecipeForm(instance=recipe) # Pre-populate with existing data

    context = {
        'form': form,
        'recipe': recipe,
        'page_title': f'Edit Recipe: {recipe.title}'
    }
    return render(request, 'recipes/recipe_form.html', context)

# --- Delete Recipe View ---
@login_required
def delete_recipe(request, pk):
    """ Allows the author of a recipe to delete it after confirmation. """
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        raise PermissionDenied("You cannot delete a recipe you didn't create.")

    if request.method == 'POST':
        recipe_title = recipe.title
        recipe.delete()
        messages.success(request, f'Recipe "{recipe_title}" was deleted.')
        return redirect('recipes:recipe_list')
    else:
        # Show confirmation page on GET request
        context = {
            'recipe': recipe,
            'page_title': f'Confirm Delete: {recipe.title}'
        }
        return render(request, 'recipes/recipe_confirm_delete.html', context)

# --- My Recipes View ---
@login_required
def my_recipes(request):
    """ Displays a list of recipes created by the logged-in user. """
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-created_at')
    # Simple pagination for My Recipes (optional)
    items_per_page = 10
    paginator = Paginator(user_recipes, items_per_page)
    page_number = request.GET.get('page')
    try:
        recipes_page = paginator.page(page_number)
    except PageNotAnInteger:
        recipes_page = paginator.page(1)
    except EmptyPage:
        recipes_page = paginator.page(paginator.num_pages)

    context = {
        'recipes_page': recipes_page, # Pass Page object
        'page_title': 'My Added Recipes'
    }
    return render(request, 'recipes/my_recipes.html', context)