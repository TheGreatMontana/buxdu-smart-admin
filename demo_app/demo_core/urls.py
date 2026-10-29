from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_index, mobile_view, campus_image_view

urlpatterns = [
    # 1. Modern Standalone Admin Dashboard (admin.buxdu.uz style)
    path('', dashboard_index, name='dashboard_home'),
    path('dashboard/', dashboard_index, name='dashboard_index'),

    # 2. Modern Mobile Redesign of buxdu.uz
    path('mobile/', mobile_view, name='mobile_home'),
    path('campus-hero.jpg', campus_image_view, name='campus_hero_img'),

    # 3. REST API for Standalone Dashboard
    path('api/', include('api.urls')),

    # 4. BuxDU Smart Assistant endpoints
    path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),

    # 5. Classic Django Admin (still accessible for backward compatibility)
    path('admin/', admin.site.urls),
]
