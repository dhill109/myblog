from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
from django.db.models import Count
from blog.models import Post, Comment

User = get_user_model()

def question_1_return_active_users():
    """
    Return the results of a query which returns a list of all
    active users in the database.
    """
    User = get_user_model()
    return User.objects.filter(is_active="True").all()


def question_2_return_regular_users():
    """
    Return the results of a query which returns a list of users that
    are *not* staff and *not* superusers
    """
    User = get_user_model()
    return User.objects.all()

def question_3_return_all_posts_for_user(user):
    """
    Return all the Posts authored by the user provided. Posts should
    be returned in reverse chronological order from when they
    were created.
    """
    user = User.objects.get(username='jas')
    return Post.objects.filter(author=user)



def question_4_return_all_posts_ordered_by_title():
    """
    Return all Post objects, ordered by their title.
    """
    return Post.objects.order_by('title')

def question_5_return_all_post_comments(post):
    """
    Return all the comments made for the post provided in order
    of last created.
    """
    return Comment.objects.all()


def question_6_return_the_post_with_the_most_comments():
    """
    Return the Post object containing the most comments in
    the database. Do not concern yourself with approval status;
    return the object which has generated the most activity.
    """
    return Post.objects.annotate(Count('comment')).values('title','comment__count')


def question_7_create_a_comment(post):
    """
    Create and return a comment for the post object provided.
    """
    pos = Post.objects.get(title='first blog post')
    return Comment.objects.create(post=pos, name = 'SINGH',email ='sa@gmail.com', comment ='okay')



def question_8_set_approved_to_false(comment):
    """
    Update the comment record provided and set approved=False
    """
    com = Comment.objects.get(name = 'SINGH')
    com.approve = False
    return com.appove


def question_9_delete_post_and_all_related_comments(post):
    """
    Delete the post object provided, and all related comments.
    """
    return Post.objects.filter(title__contains='fifth blog').delete()
