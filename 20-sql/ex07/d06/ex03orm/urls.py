from . import views
from django.urls import path


urlpatterns = [
	path('populate/', views.populate, name='populate'),
	path('display/', views.display, name='display'),
]
