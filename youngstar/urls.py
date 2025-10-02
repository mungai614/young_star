# CORRECT way — project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('youngstarapp.urls')),  # include the urls.py inside the app!
]
