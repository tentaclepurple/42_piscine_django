from . import views
from django.urls import path


urlpatterns = [
	path('display/', views.display, name='display'),
]
