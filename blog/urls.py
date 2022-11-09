# blog/urls.py
from django.contrib import admin
from django.urls import path
from blog import views
from .views import PostListView, PostDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Set root to home view
]
