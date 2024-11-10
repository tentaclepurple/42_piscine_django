from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django import forms
from django.http import HttpResponseRedirect
from .models import Article, UserFavouriteArticle



class AddToFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []  # No visible fields in the form
    template_name = 'articles/add_to_favourite.html'

    def form_valid(self, form):
        user = self.request.user
        article_id = self.kwargs['pk']
        
        # Check if the favorite already exists
        if UserFavouriteArticle.objects.filter(user=user, article_id=article_id).exists():
            messages.info(self.request, "This article is already in your favourites.")
            return HttpResponseRedirect(self.get_success_url())
        
        form.instance.user = user
        form.instance.article_id = article_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_detail', args=[self.kwargs['pk']])  # Redirect to article detail


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'synopsis', 'content'] 


class PublishArticleView(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'articles/publish_article.html'
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'articles/register.html'
    success_url = '/articles/' 

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    ordering = ['-created']


class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'articles/login.html'
    redirect_authenticated_user = True


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'


class FavouritesListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'articles/favourites_list.html'
    context_object_name = 'favourites'

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user)


class CustomLogoutView(LogoutView):
    next_page = 'home'
