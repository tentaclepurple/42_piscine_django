from django.urls import path
from .views import ArticleListView, CustomLoginView
from django.views.generic import RedirectView
from django.urls import reverse_lazy


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('articles')), name='home'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
