"""
myblog/First views
views.py

"""
from django.http import HttpResponse


def index(request):
    """accepting and returning the http request and response
    """
    return HttpResponse('Hello world! This is my first Online blog')
