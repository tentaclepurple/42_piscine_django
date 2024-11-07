from django.urls import path
from . import views


app_name = 'ex06sql'


urlpatterns = [
    path('init/', views.init, name='init'),
	path('populate/', views.populate, name='populate'),
	path('display/', views.display, name='display'),
	path('remove/', views.remove, name='remove'),
	path('update/', views.update, name='update'),
]
