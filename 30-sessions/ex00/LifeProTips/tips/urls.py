from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get_user_name/', views.get_user_name, name='getusername'),
]
