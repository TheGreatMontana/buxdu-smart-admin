from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.contrib import admin
from django.http import HttpResponse

def root_redirect(request):
    """
    Redirects root URL directly to Django Admin.
    If not authenticated, logs in as superuser for seamless local preview.
    """
    if not request.user.is_authenticated:
        User = get_user_model()
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            login(request, admin_user)
    return redirect('/admin/')


def direct_article_edit(request, article_id=1):
    """
    Opens the Article change form in Django Admin directly with superuser logged in.
    """
    if not request.user.is_authenticated:
        User = get_user_model()
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            login(request, admin_user)
    return redirect(f'/admin/news/article/{article_id}/change/')
