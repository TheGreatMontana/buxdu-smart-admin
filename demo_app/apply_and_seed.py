import os
import sys
import django

# Setup Django environment
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin\demo_app')
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')

django.setup()

from django.core.management import call_command
from news.models import Article, Employee, Book, Category, Position, TypeArticle, Menu, PhotoContent

print("Running makemigrations...")
call_command('makemigrations', 'news')
print("Running migrate...")
call_command('migrate')

print("Seeding exact real data from buxdu screenshots...")

# 1. Categories
cat_gender, _ = Category.objects.get_or_create(
    slug="191-gender-tenglik-markazi",
    defaults={"sarlavha_uz": "Gender tenglik markazi", "folder_path": "category"}
)
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
cat_konf, _ = Category.objects.get_or_create(
    slug="173-konferensiya-toplamlari",
    defaults={"sarlavha_uz": "Konferensiya to'plamlari", "folder_path": "konf_journal"}
)
cat_avtoreferat, _ = Category.objects.get_or_create(
    slug="avtoreferat",
    defaults={"sarlavha_uz": "Avtoreferat", "folder_path": "category"}
)
cat_xotin, _ = Category.objects.get_or_create(
    slug="188-xotin-qizlar-bilan-ishlash-bolimi",
    defaults={"sarlavha_uz": "Xotin-qizlar bilan ishlash bo'limi", "folder_path": "category"}
)
cat_rahbariyat, _ = Category.objects.get_or_create(
    slug="rahbariyat",
    defaults={"sarlavha_uz": "Rahbariyat", "folder_path": "category"}
)

# 2. Positions
pos_it, _ = Position.objects.get_or_create(
    title_uz="Rektorning axborot texnologiyalari bo'yicha maslahatchisi",
    defaults={"level": 0, "title_ru": "Советник ректора по ИТ", "title_en": "Advisor to the Rector on IT"}
)
pos_rector, _ = Position.objects.get_or_create(
    title_uz="Rektor",
    defaults={"level": 0, "title_ru": "Ректор", "title_en": "Rector"}
)
pos_prorector_sci, _ = Position.objects.get_or_create(
    title_uz="Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
    defaults={"level": 1, "title_ru": "Проректор по научной работе и инновациям", "title_en": "Vice-Rector for Research and Innovation"}
)
pos_head, _ = Position.objects.get_or_create(
    title_uz="Bo'lim boshlig'i",
    defaults={"level": 0, "title_ru": "Начальник отдела", "title_en": "Head of Department"}
)

# 3. Material Types
type_sport, _ = TypeArticle.objects.get_or_create(
    slug="8-sport",
    defaults={"sarlavha_uz": "Sport", "sarlavha_ru": "Спорт", "sarlavha_en": "Sport"}
)
type_grant, _ = TypeArticle.objects.get_or_create(
    slug="6-talim-granti",
    defaults={"sarlavha_uz": "Ta'lim granti", "sarlavha_ru": "Образовательный грант", "sarlavha_en": "Educational grant"}
)
type_hamkorlik, _ = TypeArticle.objects.get_or_create(
    slug="5-hamkorlik",
    defaults={"sarlavha_uz": "Xalqaro hamkorlik", "sarlavha_ru": "Международное сотрудничество", "sarlavha_en": "International cooperation"}
)
type_tadbirlar, _ = TypeArticle.objects.get_or_create(
    slug="3-tadbirlar",
    defaults={"sarlavha_uz": "Tadbirlar", "sarlavha_ru": "Мероприятия", "sarlavha_en": "Events"}
)

# 4. Articles
art1, _ = Article.objects.get_or_create(
    slug="9315-maxmudova-sadoqat-xolmatovnaning-filologiya-fanlari",
    defaults={
        "category": cat_elonlar,
        "material_turi": type_tadbirlar,
        "sarlavha_uz": "Maxmudova Sadoqat Xolmatovnaning filologiya fanlari doktori (DSc) dissertatsiya ishi himoyasi to'g'risida",
        "text_uz": "<p>“Yangi o‘zbek ijtimoiy she’riyatining poetik taraqqiyot xususiyatlari (Vatan haqidagi asarlar misolida)” mavzusida doktorlik dissertatsiyasi himoyasi bo‘lib o‘tadi.</p><p><strong>Manzil:</strong> 200118, Buxoro shahri, M.Iqbol ko‘chasi, 11-uy.</p>",
        "views_count": 56,
        "owner": "buxdu-press",
        "author": "buxdu-press",
        "is_featured": True,
    }
)
art2, _ = Article.objects.get_or_create(
    slug="9312-buxduda-dual-talim-nazariya-va-amaliyot-uygunligi",
    defaults={
        "category": cat_yangiliklar,
        "material_turi": type_tadbirlar,
        "sarlavha_uz": "BuxDUda dual ta'lim: nazariya va amaliyot uyg'unligi",
        "text_uz": "<p>Buxoro davlat universitetida talabalarning nazariy bilimlarini amaliyot bilan bog‘lash bo‘yicha yangi tizim joriy etilmoqda.</p>",
        "views_count": 19,
        "owner": "buxdu-press",
        "author": "buxdu-press",
    }
)
art3, _ = Article.objects.get_or_create(
    slug="9307-buxoro-xalqaro-ilmiy-tafakkur-markazida",
    defaults={
        "category": cat_yangiliklar,
        "material_turi": type_hamkorlik,
        "sarlavha_uz": "Buxoro xalqaro ilmiy tafakkur markazida: Yusuf Qorabog'iy merosi O'zbekiston va Ozarbayjon olimlarini birlashtirdi",
        "text_uz": "<p>Xalqaro ilmiy anjumanda O‘zbekiston va Ozarbayjon olimlari buyuk alloma merosini o‘rganish bo‘yicha ma’ruzalar qildilar.</p>",
        "views_count": 180,
        "owner": "buxdu-press",
        "author": "buxdu-press",
    }
)

# 5. Employees
emp1, _ = Employee.objects.get_or_create(
    slug="1266-xaydarova-lobar-xalimovna",
    defaults={
        "category": cat_xotin,
        "lavozim": pos_head,
        "fio_uz": "Xaydarova Lobar Xalimovna",
        "phone_number": "+998973005020",
        "email": "lobar.haydarova0305@gmail.com",
        "ilmiy_unvoni_uz": "Pedagogika fanlari bo'yicha falsafa doktori (PhD)",
        "address_uz": "Buxoro shahar M.Iqbol ko'chasi 11 uy",
        "qabul_vaqti_uz": "Har kuni 9.00-17.00 (shanbadan tashqari)",
        "mehnat_faoliyati_uz": "<p>2001-2005 yy. - Buxoro shahar 2-maktab boshlang'ich guruhlarida mehnat fani o'qituvchisi<br>2005-2009 yy. - Buxoro davlat universiteti talabasi<br>2019-2026 yy. - Xotin-qizlar bilan ishlash bo'limi boshlig'i</p>",
    }
)
emp2, _ = Employee.objects.get_or_create(
    slug="1-xamidov-obidjon-xafizovich",
    defaults={
        "category": cat_rahbariyat,
        "lavozim": pos_rector,
        "fio_uz": "Xamidov Obidjon Xafizovich",
        "phone_number": "+998652212914",
        "email": "rektor@buxdu.uz",
        "ilmiy_unvoni_uz": "Iqtisodiyot fanlari doktori, professor",
        "address_uz": "Buxoro shahar, M.Iqbol ko'chasi, 11-uy",
        "qabul_vaqti_uz": "Dushanba: 14:00 - 17:00",
    }
)

# 6. Books
book1, _ = Book.objects.get_or_create(
    sarlavha_uz="BUXORO TARIXI MASALALARI (eng qadimgi zamonlardan hozirgacha)",
    defaults={
        "category": cat_konf,
        "mualliflar": "Buxoro davlat universiteti",
        "nashriyot": "Buxoro - 2025",
        "nashr_yili": 2025,
        "sahifalar_soni": 310,
        "tili": "O'zbekcha",
        "url": "#",
        "text_uz": "BUXORO TARIXI MASALALARI (eng qadimgi zamonlardan hozirgacha) nomli xalqaro ilmiy-amaliy konferensiya to'plami."
    }
)
book2, _ = Book.objects.get_or_create(
    sarlavha_uz="Mimemik matnlarda muloqotning modellari: pragmalingvistik va psixolingvistik yondashuvlar",
    defaults={
        "category": cat_avtoreferat,
        "mualliflar": "Filologiya fakulteti",
        "nashriyot": "Buxoro",
        "nashr_yili": 2026,
        "sahifalar_soni": 68,
        "tili": "O'zbekcha",
        "url": "#",
        "text_uz": "Filologiya fanlari bo'yicha falsafa doktori dissertatsiyasi avtoreferati."
    }
)

# 7. Menu
menu1, _ = Menu.objects.get_or_create(
    slug="412-gender-tenglik",
    defaults={
        "sarlavha_uz": "Gender tenglik markazi",
        "type": "all_categories",
        "position": "top",
        "category": cat_gender,
        "url": "#",
        "visible": True
    }
)
menu2, _ = Menu.objects.get_or_create(
    slug="401-davlat-auditi-fakulteti",
    defaults={
        "sarlavha_uz": "Davlat auditi fakulteti",
        "type": "material",
        "position": "top",
        "url": "#",
        "visible": True
    }
)

print("Seeding completed successfully!")
