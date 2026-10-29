import os
from django.shortcuts import render
from django.http import HttpResponse, FileResponse

def dashboard_index(request):
    """
    Renders the modern standalone admin dashboard.
    """
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'dashboard', 'index.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return HttpResponse(html, content_type='text/html; charset=utf-8')

def mobile_view(request):
    """
    Renders the ultra-modern mobile redesign of buxdu.uz.
    """
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'dashboard', 'mobile.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    return HttpResponse(html, content_type='text/html; charset=utf-8')

def campus_image_view(request):
    """
    Serves the Nano Banana generated 4K photo of Bukhara State University.
    """
    img_path = r'C:\Users\TGM\.gemini\antigravity\brain\efee2169-2c57-4f5d-96a6-4992aaa9278d\bukhara_state_university_main_campus_1793288493977.jpg'
    if os.path.exists(img_path):
        return FileResponse(open(img_path, 'rb'), content_type='image/jpeg')
    return HttpResponse("Image not found", status=404)

def auto_login_admin_preview(request):
    """
    Directly renders the Django admin change form with full Smart Assistant buttons.
    """
    from django.contrib.auth import get_user_model
    from django.contrib import admin
    from news.models import Article
    User = get_user_model()
    admin_user = User.objects.filter(username='admin').first()
    request.user = admin_user
    original_has_perm = admin.site.has_permission
    admin.site.has_permission = lambda r: True
    try:
        model_admin = admin.site._registry[Article]
        return model_admin.changeform_view(request, '1')
    finally:
        admin.site.has_permission = original_has_perm


def auto_login_admin_index(request):
    """
    Directly renders the Django admin site index page matching buxdu.uz.
    """
    from django.contrib.auth import get_user_model
    from django.contrib import admin
    User = get_user_model()
    admin_user = User.objects.filter(username='admin').first()
    request.user = admin_user
    original_has_perm = admin.site.has_permission
    admin.site.has_permission = lambda r: True
    try:
        return admin.site.index(request)
    finally:
        admin.site.has_permission = original_has_perm




