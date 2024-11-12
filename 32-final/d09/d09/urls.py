from django.urls import path, include
from django.contrib import admin
from django.views.generic import RedirectView



urlpatterns = [
	path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
	path('chat/', include('chat.urls'), name='chat'),
	path('', RedirectView.as_view(url='chat/')),
]
