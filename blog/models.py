from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class PostQueryset(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)
    def get_authors(self):
        User = get_user_model()
        return User.objects.filter(blog_posts__in=self).distinct()

class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True  # No duplicates!
    )
    slug = models.SlugField(unique=True, null=False)
    objects = PostQueryset.as_manager()

    def get_absolute_url(self):
        if self.name:
            kwargs = {
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}
        return reverse('topic-detail', kwargs=kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
class Post(models.Model):

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(max_length=255)
    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',  # Slug is unique for publication date
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    content = models.TextField()
    published = models.DateTimeField(
        null=False,
        blank=False,
        help_text='The date & time this article was published',
    )
    objects = PostQueryset.as_manager()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    content = RichTextUploadingField()

    class Meta:
        ordering = ['created']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

class PostManager(models.Manager):
    """
    PostManger to exclude the unchecked check box
    """
    def get_queryset(self):
        queryset = super().get_queryset()  # Get the initial queryset
        return queryset.exclude(approve=False)  # Exclude deleted records

class Comment(models.Model):
    """
    CLass Comment MODEL
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(
    max_length=100,
    null=False,
    blank=False)
    comment = models.TextField(max_length=100, null=False, blank=False)
    approve = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    objects = PostManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.comment[:60]
class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'
class Contest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    photo = models.FileField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Photo Contest Submissions'
        ordering = ['-submitted']

    def __str__(self):
        return f''
