# urls.py en el proyecto
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# URL patterns without a language prefix (for the default language English)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # For language switching
    path('', RedirectView.as_view(url='articles/'), name='home'),  # Default home
    path('', include('articles.urls')),  # Include URLs from articles app without language prefix
]

# URL patterns with language prefix (for languages other than the default)
urlpatterns += i18n_patterns(
    path('', RedirectView.as_view(url='articles/'), name='home'),
    path('', include('articles.urls')),  # Include URLs from articles app with language prefix
)
