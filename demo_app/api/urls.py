from django.urls import path
from . import views

urlpatterns = [
    # Tools & Stats
    path('tools/transliterate/', views.tool_transliterate, name='api_tool_transliterate'),
    path('tools/bulk_transliterate/', views.tool_bulk_transliterate, name='api_tool_bulk_transliterate'),
    path('tools/translate/', views.tool_translate, name='api_tool_translate'),
    path('stats/', views.dashboard_stats, name='api_dashboard_stats'),

    # Generic Model endpoints (materials, xodimlar, books, kategoriyalar, lavozimlar, materialturlari, menus, photos)
    path('<str:model_name>/', views.api_generic_list_create, name='api_model_list_create'),
    path('<str:model_name>/<int:pk>/', views.api_generic_detail_update_delete, name='api_model_detail'),
]
