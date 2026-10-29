from django.contrib import admin
from django.urls import path, include
from .views import root_redirect, direct_article_edit

urlpatterns = [
    # Root redirects straight to Django Admin with automatic login
    path('', root_redirect, name='root_admin'),

    # Direct 1-click link to edit an article with the Smart Buttons
    path('edit-demo/', direct_article_edit, name='direct_edit_demo'),
    path('edit-demo/<int:article_id>/', direct_article_edit, name='direct_edit_demo_id'),

    # BuxDU Smart Assistant endpoints
    path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),

    # Official Django Administration
    path('admin/', admin.site.urls),
]
