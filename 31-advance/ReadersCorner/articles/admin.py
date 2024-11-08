# articles/admin.py

from django.contrib import admin
from .models import Article, UserFavouriteArticle

# Registra los modelos en el admin
admin.site.register(Article)
admin.site.register(UserFavouriteArticle)
