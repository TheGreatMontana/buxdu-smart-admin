import os
import sys
from pathlib import Path
import django

# Setup cross-platform paths
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from news.models import Article, Employee, Book, Category, Position, TypeArticle, Menu, PhotoContent

print("1. Running database migrations...")
call_command('makemigrations', 'news')
call_command('migrate')

print("2. Ensuring Superuser (admin / admin123)...")
User = get_user_model()
admin_user = User.objects.filter(username='admin').first()
if not admin_user:
    User.objects.create_superuser('admin', 'admin@buxdu.uz', 'admin123')
    print("   Created superuser: admin / admin123")
else:
    admin_user.set_password('admin123')
    admin_user.save()
    print("   Superuser 'admin' password updated to 'admin123'")

print("3. Seeding models matching buxdu.uz...")

# 1. Categories
cat_elonlar, _ = Category.objects.get_or_create(
    slug="elonlar",
    defaults={"sarlavha_uz": "E'lonlar", "folder_path": "category"}
)
cat_yangiliklar, _ = Category.objects.get_or_create(
    slug="yangiliklar",
    defaults={"sarlavha_uz": "Yangiliklar", "folder_path": "category"}
)
cat_psixolog, _ = Category.objects.get_or_create(
    slug="psixolog-maslahati",
    defaults={"sarlavha_uz": "Psixolog maslahati", "folder_path": "category"}
)

# 2. TypeArticle
type_tadbir, _ = TypeArticle.objects.get_or_create(
    slug="tadbirlar",
    defaults={"sarlavha_uz": "Tadbirlar"}
)
type_sport, _ = TypeArticle.objects.get_or_create(
    slug="sport",
    defaults={"sarlavha_uz": "Sport"}
)

# 3. Position
pos_rektor, _ = Position.objects.get_or_create(
    title_uz="Rektor",
    defaults={"level": 1, "title_ru": "Ректор", "title_en": "Rector"}
)
pos_dekan, _ = Position.objects.get_or_create(
    title_uz="Fakultet dekani",
    defaults={"level": 2, "title_ru": "Декан факультета", "title_en": "Faculty Dean"}
)

# 4. Sample Articles (with old Latin Uzbek text needing reform)
if Article.objects.count() == 0:
    Article.objects.create(
        sarlavha_uz="O'zbekiston Respublikasi Fanlar akademiyasi ilmiy anjumani to'g'risida",
        text_uz="<p>Buxoro davlat universitetida yangi o'quv yili ochilish marosimi bo'lib o'tdi. Unda xalqaro mehmonlar va o'qituvchilar qatnashdilar. Shuningdek, ilmiy hamkorlik to'g'risida memorandum imzolandi.</p>",
        category=cat_yangiliklar,
        material_turi=type_tadbir,
        slug="9307-buxoro-xalqaro-ilmiy-tafakkur-markazida",
        views_count=180
    )
    Article.objects.create(
        sarlavha_uz="Maxmudova Sadoqat Xolmatovnaning filologiya fanlari doktori (DSc) dissertatsiya ishi himoyasi to'g'risida",
        text_uz="<p>“Yangi o'zbek ijtimoiy she'riyatining poetik taraqqiyot xususiyatlari” mavzusida doktorlik dissertatsiyasi himoyasi bo'lib o'tadi. Manzil: Buxoro shahri, M.Iqbol ko'chasi, 11-uy.</p>",
        category=cat_elonlar,
        material_turi=type_tadbir,
        slug="9315-maxmudova-sadoqat-xolmatovnaning-filologiya-fanlari",
        views_count=56
    )

print("✅ Barcha test ma'lumotlari muvaffaqiyatli yuklandi!")
