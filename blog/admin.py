from django.contrib import admin
from . import models
from .models import Post, Comment

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    list_filter = (
        'status',
        'topics',
    )
    inlines = [
        CommentInline,
    ]
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'approve',
    )
    search_fields = (
        'email',
        'comment',
        'name',
    )
    list_filter = (
        'approve',
    )
admin.site.register(models.Post, PostAdmin)
