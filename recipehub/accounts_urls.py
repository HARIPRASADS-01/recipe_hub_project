# recipehub/accounts_urls.py
from django.urls import path, include
from recipes import views as recipe_views

urlpatterns = [
    path('signup/', recipe_views.signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
]