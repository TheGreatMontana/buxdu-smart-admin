# 🏛️ BuxDU Smart Django Admin (2026 Alifbo & Ko'p Tilli Tarjima)

[![Django](https://img.shields.io/badge/Django-5.2+-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Uzbek Latin 2026](https://img.shields.io/badge/2026_Alifbo-Ö_%7C_Ğ_%7C_Ş_%7C_Ç-2b7a59?style=for-the-badge)](https://buxdu.uz)

> **Buxoro davlat universiteti (`buxdu.uz`) Django admin paneli uchun maxsus ishlab chiqilgan tayyor plagin.**
> Sayt administratori uchun birgina tugma bilan o'zbekcha matnlarni 2026-yilgi yangi lotin alifbosiga (`Ö, Ğ, Ş, Ç`) o'tkazadi va rus, ingliz hamda xitoy tillariga professional darajada avtomatik tarjima qiladi.

---

## ⚡ Asosiy Imkoniyatlar (Django Admin Ichida)

Django ma'muriyat panelidagi har bir maqola, yangilik, kitob yoki xodim formasining yuqori qismida 100% Django dizayniga moslashgan aqlli boshqaruv paneli joylashgan:

1. **⚡ Yangi Alifboga O'tkazish (Ö, Ğ, Ş, Ç)**:
   - `O‘ / o‘` ➔ `Ö / ö` (*O'zbekiston* ➔ *Özbekiston*, *o'quv* ➔ *öquv*)
   - `G‘ / g‘` ➔ `Ğ / ğ` (*yig'ilish* ➔ *yiğiliş*, *to'g'risida* ➔ *töğrisida*)
   - `Sh / sh` ➔ `Ş / ş` (*sharafli* ➔ *şarafli*, *qatnashdi* ➔ *qatnaşdi*)
   - `Ch / ch` ➔ `Ç / ç` (*ochilish* ➔ *oçiliş*, *o'qituvchilar* ➔ *öqituvçilar*)
   - `Is'hoq`, `mus'haf` kabi so'zlardagi tutuq belgisi xavfsiz saqlanadi.
   - Kirill alifbosida kiritilgan matnlarni ham avtomatik aniqlab yangi lotinga o'giradi.
   - CKEditor 4 va TinyMCE ichidagi HTML teglarni (`<p>`, `<a>`, `<strong>`, `<img>`) buzmaydi.

2. **🌐 Tillarga Avto-Tarjima (RU, EN, ZH)**:
   - O'zbek tilidagi sarlavha va to'liq matnni bir zumda **Rus**, **Ingliz** va **Xitoy** tillariga akademik standartda tarjima qiladi.
   - `django-modeltranslation` maydonlarini (`sarlavha_ru`, `text_ru`, `sarlavha_en`, `text_en`, `sarlavha_zh`, `text_zh`) avtomatik to'ldiradi.

3. **🚀 1-Bosishda Hammasi**:
   - Yangi alifboga o'tkazish va 3 ta tilga tarjima qilishni bir vaqtda bajaradi.

---

## 🚀 Loyihani Lokal Ishga Tushirish

### 1. Repozitoriyni yuklab olish:
```bash
git clone https://github.com/TheGreatMontana/buxdu-smart-admin.git
cd buxdu-smart-admin
```

### 2. Virtual muhit va kutubxonalarni o'rnatish:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Serverni ishga tushirish:
```bash
cd demo_app
python manage.py runserver 127.0.0.1:8000
```

---

## 🔗 Kerakli Havolalar (Links)

Server yongandan so'ng brauzeringizda quyidagi havolalarni oching:

* 🏛️ **Django Admin Bosh Sahifasi**:  
  👉 **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**  
  *(Login: `admin` | Parol: `admin123`)*

* ⚡ **To'g'ridan-to'g'ri Maqolani Tahrirlash (Smart Tugmalar bilan)**:  
  👉 **[http://127.0.0.1:8000/edit-demo/](http://127.0.0.1:8000/edit-demo/)**  
  *(Hech qanday login terish shart emas — avtomatik ochiladi va tugmalarni darhol sinab ko'rish mumkin)*

* 🌐 **Bosh sahifa (Avtomatik Adminga Yo'naltiradi)**:  
  👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📦 O'z loyihangizga (`buxdu.uz` ga) o'rnatish

1. `buxdu_smart_admin` jildini loyihangizga ko'chiring.
2. `settings.py` fayliga qo'shing:
```python
INSTALLED_APPS = [
    'buxdu_smart_admin',
    'django.contrib.admin',
    # ... boshqa ilovalaringiz
]
```
3. `admin.py` faylida modelingiz uchun `SmartMultilingualAdmin` dan foydalaning:
```python
from django.contrib import admin
from buxdu_smart_admin.admin import SmartMultilingualAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'sana')
```
Tayyor! Endi sizning Django adminingizda aqlli tugmalar paydo bo'ladi.
