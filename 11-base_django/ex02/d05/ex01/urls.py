# ex01/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('django/', views.django_page, name='django_page'),
    path('display/', views.display_process_page, name='display_process_page'),
    path('templates/', views.template_engine_page, name='template_engine_page'),
]
