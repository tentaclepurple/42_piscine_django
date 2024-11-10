from django.urls import path, include
from django.contrib import admin


urlpatterns = [
	path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
	path('chat/', include('chat.urls'), name='chat'),
]
