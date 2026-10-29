from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.contrib import admin

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


def direct_article_create(request):
    """
    Opens the Add Article form in Django Admin with superuser logged in.
    """
    if not request.user.is_authenticated:
        User = get_user_model()
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            login(request, admin_user)
    return redirect('/admin/news/article/add/')
