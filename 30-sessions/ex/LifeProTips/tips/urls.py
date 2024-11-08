from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('get_user_name/', views.get_user_name, name='getusername'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tip/<int:tip_id>/upvote/', views.upvote_tip, name='upvote_tip'),
    path('tip/<int:tip_id>/downvote/', views.downvote_tip, name='downvote_tip'),
    path('tip/<int:tip_id>/delete/', views.delete_tip, name='delete_tip'),
]
