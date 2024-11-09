# articles/admin.py

from django.contrib import admin
from .models import Article, UserFavouriteArticle


class UserFavouriteArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')  # Display user and article in the list view
    search_fields = ('user__username', 'article__title')  # Enable search by username and article title


admin.site.register(Article)
admin.site.register(UserFavouriteArticle, UserFavouriteArticleAdmin)
