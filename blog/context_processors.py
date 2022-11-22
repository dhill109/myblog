from . import models
from django.db.models import Count

def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    topics = models.Post.objects.values_list('topics__name', flat=True) \
    .annotate(num = Count('id')).order_by('-num')

    return {'authors': authors, 'topics': topics}
