from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'


class CustomLoginView(LoginView):
    template_name = 'articles/login.html'
    redirect_authenticated_user = True
