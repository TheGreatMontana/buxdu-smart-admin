import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')
django.setup()

from django.contrib.auth import get_user_model
from news.models import (
    Kategoriya, Lavozim, MaterialTuri, Material, 
    Xodim, Book, Menu, PhotoContent
)

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@buxdu.uz', 'admin123')
    print("Superuser created: admin / admin123")

# 1. Kategoriyalar
k_yangilik, _ = Kategoriya.objects.get_or_create(nomi_uz="Universitet yangiliklari", slug="yangiliklar", tartib=1)
k_ilmiy, _ = Kategoriya.objects.get_or_create(nomi_uz="Ilmiy-tadqiqot institutlari", slug="ilmiy-institutlar", tartib=2)
k_fakultet, _ = Kategoriya.objects.get_or_create(nomi_uz="Fakultetlar va kafedralar", slug="fakultetlar", tartib=3)

# 2. Lavozimlar
l_rektor, _ = Lavozim.objects.get_or_create(nomi_uz="Rektor", daraja="Rektorat")
l_prorektor, _ = Lavozim.objects.get_or_create(nomi_uz="Prorektor", daraja="Rektorat")
l_dekan, _ = Lavozim.objects.get_or_create(nomi_uz="Fakultet dekani", daraja="Dekanat")
l_direktor, _ = Lavozim.objects.get_or_create(nomi_uz="Direktor o'rinbosari", daraja="Institut")

# 3. Material turlari
t_yangilik, _ = MaterialTuri.objects.get_or_create(nomi_uz="Yangilik", slug="yangilik")
t_maqola, _ = MaterialTuri.objects.get_or_create(nomi_uz="Ilmiy maqola", slug="maqola")
t_elon, _ = MaterialTuri.objects.get_or_create(nomi_uz="E'lon", slug="elon")
t_institut, _ = MaterialTuri.objects.get_or_create(nomi_uz="Institut sahifasi", slug="institut")

# 4. Materiallar (Yangiliklar & Institutlar)
Material.objects.create(
    title_uz="Tabiiy fanlar va agroinnovatsiyalar ilmiy-tadqiqot instituti",
    content_uz="Buxoro davlat universiteti huzuridagi Tabiiy fanlar va agroinnovatsiyalar ilmiy-tadqiqot institutida zamonaviy biotexnologiyalar, tuproq unumdorligi va organik dehqonchilik yo'nalishlarida chuqur ilmiy izlanishlar olib borilmoqda. Institut olimlari xalqaro grantlar g'olibi bo'lishdi.",
    turi=t_institut,
    kategoriya=k_ilmiy,
    korishlar_soni=1420,
    is_published=True
)

Material.objects.create(
    title_uz="Aniq fanlar va intellektual muhandislik texnologiyalari ilmiy-tadqiqot instituti",
    content_uz="Institutda raqamli iqtisodiyot, sun'iy intellekt, axborot xavfsizligi va robototexnika sohasida xalqaro ilmiy laboratoriyalar tashkil etilgan.",
    turi=t_institut,
    kategoriya=k_ilmiy,
    korishlar_soni=980,
    is_published=True
)

Material.objects.create(
    title_uz="BuxDU professor-o'qituvchilari xalqaro simpoziumda nutq so'zlashdi",
    content_uz="Universitet jamoasi xalqaro ta'lim sifatini oshirish va xorijiy OTMlar bilan hamkorlik aloqalarini kengaytirish bo'yicha ilmiy ma'ruza qildi.",
    turi=t_yangilik,
    kategoriya=k_yangilik,
    korishlar_soni=540,
    is_published=True
)

# 5. Xodimlar
Xodim.objects.create(
    fio_uz="Barakayev Ixtiyor Rajabovich",
    lavozim=l_direktor,
    lavozim_uz="Direktor o'rinbosari | Tabiiy fanlar va agrobiotexnologiya fakulteti",
    telefon="+998 65 221-29-14",
    email="i.barakayev@buxdu.uz",
    qabul_vaqti="Dushanba - Chorshanba, 14:00 - 17:00",
    biografiya_uz="Texnika fanlari bo'yicha falsafa doktori (PhD), dotsent.",
    tartib=1
)

Xodim.objects.create(
    fio_uz="Qobilov Komiljon Hamidovich",
    lavozim=l_direktor,
    lavozim_uz="Direktor o'rinbosari | Fakultetlar",
    telefon="+998 65 221-30-00",
    email="k.qobilov@buxdu.uz",
    qabul_vaqti="Seshanba - Juma, 10:00 - 13:00",
    biografiya_uz="Pedagogika fanlari doktori, professor.",
    tartib=2
)

# 6. Books
Book.objects.create(
    nomi_uz="BUXORO TARIXI MASALALARI (eng qadimgi zamonlardan hozirgacha)",
    muallif_uz="BuxDU Tarix fakulteti professor-o'qituvchilari",
    annotatsiya_uz="Konferensiya to'plamlari: Xalqaro ilmiy-amaliy anjuman materiallari to'plami.",
    yil=2026
)

Book.objects.create(
    nomi_uz="Avtoreferat | Matematik modellash va zamonaviy dasturiy vositalar",
    muallif_uz="I.R. Barakayev",
    annotatsiya_uz="Doktorlik dissertatsiyasi avtoreferati.",
    yil=2025
)

# 7. Menu
m_asosiy, _ = Menu.objects.get_or_create(nomi_uz="Universitet", havola="/universitet/", tartib=1)
Menu.objects.get_or_create(nomi_uz="Universitet nizomi", havola="/universitet-nizomi/", yuqori_menyu=m_asosiy, tartib=1)
Menu.objects.get_or_create(nomi_uz="Rahbariyat", havola="/rahbariyat/", yuqori_menyu=m_asosiy, tartib=2)
Menu.objects.get_or_create(nomi_uz="Fakultetlar", havola="/fakultetlar/", tartib=2)
Menu.objects.get_or_create(nomi_uz="Ilmiy faoliyat", havola="/ilmiy/", tartib=3)

# 8. Photo contents
PhotoContent.objects.create(
    nomi_uz="Universitetda yangi o'quv yili ochilish tantanasi",
    tavsif_uz="2026-yilgi qabul talabalari bilan tantanali uchrashuvdan lavhalar."
)

print("✅ Barcha 8 ta model bo'yicha ma'lumotlar muvaffaqiyatli yuklandi!")
