import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_core.settings')
django.setup()

from news.models import Material, Xodim, Book, Document, Kategoriya

# Kategoriyalar
k_ilmiy, _ = Kategoriya.objects.get_or_create(nomi_uz="Ilmiy-tadqiqot institutlari", slug="ilmiy-institutlar")
k_fakultet, _ = Kategoriya.objects.get_or_create(nomi_uz="Fakultetlar va Kafedralar", slug="fakultetlar")
k_yangilik, _ = Kategoriya.objects.get_or_create(nomi_uz="Universitet yangiliklari", slug="yangiliklar")

# Materiallar
if Material.objects.count() == 0:
    Material.objects.create(
        title_uz="Tabiiy fanlar va agroinnovatsiyalar ilmiy-tadqiqot instituti",
        content_uz="Buxoro davlat universiteti huzuridagi Tabiiy fanlar va agroinnovatsiyalar ilmiy-tadqiqot institutida yangi ilmiy ishlanmalar va innovatsion loyihalar ustida ish olib borilmoqda. Institut olimlari xalqaro grantlar g'olibi bo'lishdi.",
        turi="institut",
        kategoriya=k_ilmiy,
        is_published=True
    )
    Material.objects.create(
        title_uz="Aniq fanlar va intellektual muhandislik texnologiyalari ilmiy-tadqiqot instituti",
        content_uz="Institutda axborot xavfsizligi, sun'iy intellekt va robototexnika yo'nalishlarida ilmiy-amaliy tadqiqotlar o'tkazilmoqda.",
        turi="institut",
        kategoriya=k_ilmiy,
        is_published=True
    )
    Material.objects.create(
        title_uz="Buxoro davlat universiteti rektori delegatsiyasi xalqaro hamkorlik uchrashuvida",
        content_uz="Universitet rahbariyati xalqaro ta'lim sifatini oshirish va xorijiy OTMlar bilan hamkorlik aloqalarini kengaytirish bo'yicha uchrashuv o'tkazdi.",
        turi="yangilik",
        kategoriya=k_yangilik,
        is_published=True
    )
    print("✅ Materiallar yaratildi.")

# Xodimlar
if Xodim.objects.count() == 0:
    Xodim.objects.create(
        fio_uz="Barakayev Ixtiyor Rajabovich",
        lavozim_uz="Direktor o'rinbosari | Tabiiy fanlar va agrobiotexnologiya fakulteti",
        telefon="+998 65 221-29-14",
        email="i.barakayev@buxdu.uz",
        qabul_vaqti="Dushanba - Chorshanba, 14:00 - 17:00",
        tartib=1
    )
    Xodim.objects.create(
        fio_uz="Qobilov Komiljon Hamidovich",
        lavozim_uz="Direktor o'rinbosari | Fakultetlar",
        telefon="+998 65 221-30-00",
        email="k.qobilov@buxdu.uz",
        qabul_vaqti="Seshanba - Juma, 10:00 - 13:00",
        tartib=2
    )
    print("✅ Xodimlar yaratildi.")

# Kitoblar
if Book.objects.count() == 0:
    Book.objects.create(
        nomi_uz="BUXORO TARIXI MASALALARI (eng qadimgi zamonlardan hozirgacha)",
        muallif_uz="BuxDU Tarix fakulteti professor-o'qituvchilari",
        annotatsiya_uz="Xalqaro ilmiy-amaliy anjuman materiallari to'plami.",
        yil=2026
    )
    Book.objects.create(
        nomi_uz="Zamonaviy axborot texnologiyalari va raqamli ta'lim",
        muallif_uz="I.R. Barakayev, K.H. Qobilov",
        annotatsiya_uz="Oliy o'quv yurtlari talabalari uchun darslik.",
        yil=2025
    )
    print("✅ Kitoblar yaratildi.")

# Hujjatlar
if Document.objects.count() == 0:
    Document.objects.create(
        nomi_uz="Buxoro davlat universitetining 2026-yilgi Jamoa shartnomasi",
        raqami="№ 14-A, 15.01.2026",
        turi="Jamoa shartnomasi"
    )
    Document.objects.create(
        nomi_uz="O'zbekiston Respublikasi Prezidentining Oliy ta'lim tizimini rivojlantirish to'g'risidagi Farmoni",
        raqami="PF-60-son",
        turi="Prezident Farmoni"
    )
    print("✅ Hujjatlar yaratildi.")
