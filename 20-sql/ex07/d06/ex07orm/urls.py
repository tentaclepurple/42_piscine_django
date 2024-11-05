from . import views
from django.urls import path


app_name = "ex07orm"


urlpatterns = [
	path('populate/', views.populate, name='populate'),
	path('display/', views.display, name='display'),
	path('remove/', views.remove, name='remove'),
    path("update/", views.update, name="update"),

]
