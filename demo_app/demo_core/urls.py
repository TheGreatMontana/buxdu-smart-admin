from django.contrib import admin
from django.urls import path, include
from .views import root_redirect, direct_article_create

urlpatterns = [
    # Root redirects straight to Django Admin with automatic login
    path('', root_redirect, name='root_admin'),

    # Direct link to create an article with the Smart Buttons
    path('edit-demo/', direct_article_create, name='direct_create_demo'),

    # BuxDU Smart Assistant endpoints
    path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),

    # Official Django Administration
    path('admin/', admin.site.urls),
]
