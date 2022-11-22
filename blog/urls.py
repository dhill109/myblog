# blog/urls.py
from django.contrib import admin
from django.urls import path, include
from blog import views
from .views import PostListView, PostDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),

]
