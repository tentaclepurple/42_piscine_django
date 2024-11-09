# urls.py en la app articles
from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('publish/', views.PublishArticleView.as_view(), name='publish_article'),
    path('favourites/', views.FavouritesListView.as_view(), name='favourites'),
    path('articles/<int:pk>/add_to_favourite/', views.AddToFavouriteView.as_view(), name='add_to_favourite'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
