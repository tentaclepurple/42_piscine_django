# account/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.account_view, name='account_view'),
    path('ajax_login/', views.ajax_login, name='ajax_login'),
    path('ajax_logout/', views.ajax_logout, name='ajax_logout'),
]
