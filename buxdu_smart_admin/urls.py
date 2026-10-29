from django.urls import path
from . import views

app_name = 'buxdu_smart_admin'

urlpatterns = [
    path('api/transliterate/', views.api_transliterate, name='api_transliterate'),
    path('api/translate/', views.api_translate, name='api_translate'),
]
