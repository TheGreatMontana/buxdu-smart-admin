import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from news.models import Article

User = get_user_model()

# Create superuser if not exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@buxdu.uz', 'admin123')
    print("✅ Superuser yaratildi: Login: 'admin', Parol: 'admin123'")
else:
    print("ℹ️ Superuser 'admin' allaqachon mavjud.")

# Populate test article with old Latin
if Article.objects.count() == 0:
    Article.objects.create(
        title_uz="Buxoro davlat universiteti o'qituvchilari xalqaro grant g'olibi bo'lishdi",
        content_uz="Buxoro davlat universiteti jamoasi navbatdagi katta yutuqqa erishdi. Universitet o'qituvchilari va talabalari shahar miqyosidagi ilmiy tanlovda g'olib deb topildi. Choyxona va kutubxona majmuasida taqdirlash marosimi bo'lib o'tdi. Is'hoq ota nomidagi maxsus mukofot topshirildi.",
        category="Xalqaro aloqalar",
        is_published=True
    )
    Article.objects.create(
        title_uz="Universitetda yangi o'quv yili uchun qabul boshlandi",
        content_uz="BuxDU rektori boshchiligida kengaytirilgan yig'ilish o'tkazildi. Yoshlar bilan ishlash bo'yicha prorektor yangi o'quv rejalari bilan tanishtirdi.",
        category="Qabul 2026",
        is_published=True
    )
    print("✅ 2 ta namunaviy maqola yaratildi (eski o'zbek lotin alifbosida).")
