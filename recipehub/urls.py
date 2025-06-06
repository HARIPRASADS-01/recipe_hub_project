# recipehub/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('recipes:recipe_list'), permanent=False), name='home'),
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('accounts/', include('recipehub.accounts_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)