from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .forms import CommentForm
from .models import Post, Comment
from . import models
from django.db.models import Count
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]
        authors = models.Post.objects.published().get_authors().order_by('first_name')

        context.update({'latest_posts': latest_posts, 'authors': authors,})
        return context

class AboutView(TemplateView):
    template_name = 'blog/about.html'

def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions.html')

class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')


class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset().published()
        if 'pk' in self.kwargs:
            return queryset

        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )
class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset =  models.Topic.objects.order_by('name')

class TopicDetailView(DetailView):
    model = models.Topic
    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()
        if 'pk' in self.kwargs:
            return queryset

        return queryset.filter(
        )

class PostDisplay(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk}) + '#comments'
