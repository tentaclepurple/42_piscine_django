from . import views
from django.urls import path


app_name = "ex05orm"


urlpatterns = [
	path('populate/', views.populate, name='populate'),
	path('display/', views.display, name='display'),
	path('remove/', views.remove, name='remove'),
]
