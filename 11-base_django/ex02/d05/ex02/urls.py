# ex02/urls.py
from django.urls import path
from . import views


app_name = 'ex02'
urlpatterns = [
    path('', views.ex02_view, name='ex02_view'),
]
