# ex03/urls.py
from django.urls import path
from . import views


app_name = 'ex03'
urlpatterns = [
    path('', views.shades_table, name='shades_table'),
]
