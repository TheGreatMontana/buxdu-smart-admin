# 🏛️ BuxDU Smart Django Admin (2026 Alifbo & Ko'p Tilli Tarjima)

[![Django](https://img.shields.io/badge/Django-3.2_|_4.2_|_5.x-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![2026 Alifbo Reformasi](https://img.shields.io/badge/2026_Alifbo-Ö_%7C_Ğ_%7C_Ş_%7C_Ç-2b7a59?style=for-the-badge)](https://buxdu.uz)

> **Buxoro davlat universiteti (`buxdu.uz`) Django admin paneli uchun tayyor plagin.**  
> Sayt administratori uchun 1 bosishda o'zbekcha matnlarni 2026-yilgi yangi lotin alifbosiga (`Ö, Ğ, Ş, Ç`) o'tkazadi va rus, ingliz hamda xitoy tillariga professional darajada avtomatik tarjima qilib beradi.

---

## 👨‍💻 BuxDU Dasturchisi ("Programmer Boy") Uchun O'rnatish Qo'llanmasi

Ushbu plagin mavjud `buxdu.uz` Django loyihasiga **3 daqiqada**, hech qanday mavjud kodni buzmasdan, oson ulanadi.

---

### 🛠️ 1-QADAM: Loyihaga qo'shish
Ushbu repozitoriydagi `buxdu_smart_admin/` papkasini serveringizdagi Django loyihangiz ildiziga (`manage.py` turgan joyga) nusxalang:
```bash
# buxdu.uz loyihangiz papkasida:
cp -r /path/to/buxdu_smart_admin ./buxdu_smart_admin
```

---

### ⚙️ 2-QADAM: `settings.py` sozlamasi
`settings.py` faylingizdagi `INSTALLED_APPS` ro'yxatiga `buxdu_smart_admin` ni qo'shing:

```python
INSTALLED_APPS = [
    'buxdu_smart_admin',       # 👈 Shuni qo'shing (django.contrib.admin dan oldin yoki keyin)
    'django.contrib.admin',
    'django.contrib.auth',
    # ... qolgan ilovalaringiz
]
```

---

### 🌐 3-QADAM: `urls.py` sozlamasi
Loyihangizning asosiy `urls.py` fayliga API marshrutini ulang:

```python
from django.urls import path, include

urlpatterns = [
    # BuxDU Smart Assistant endpoints (Alifbo va Avto-tarjima uchun)
    path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),  # 👈 Shuni qo'shing
    
    path('admin/', admin.site.urls),
    # ... qolgan yo'llaringiz
]
```

---

### 📝 4-QADAM: `admin.py` da faollashtirish
Kerakli modelingiz (masalan, `Article`, `Xodimlar`, `Books` va h.k.) admin klassiga ulaymiz.

#### Usul A (Eng osoni — 1 qator o'zgarish):
`admin.ModelAdmin` o'rniga `SmartMultilingualAdmin` dan meros oling:

```python
from django.contrib import admin
from buxdu_smart_admin.admin import SmartMultilingualAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(SmartMultilingualAdmin):    # 👈 admin.ModelAdmin o'rniga
    list_display = ('sarlavha_uz', 'sana')
    # Sizning avvalgi barcha sozlamalaringiz o'zgarishsiz qoladi!
```

#### Usul B (Agar sizda allaqachon o'z maxsus BaseAdmin bo'lsa):
Mavjud admin modelingizga quyidagi 2 ta parametrni qo'shib qo'ysangiz kifoya:

```python
@admin.register(Article)
class ArticleAdmin(YourExistingBaseAdmin):
    change_form_template = 'admin/buxdu_smart_admin/change_form.html'
    
    class Media:
        css = {'all': ('buxdu_smart_admin/css/smart_admin.css',)}
        js = ('buxdu_smart_admin/js/smart_admin.js',)
```

---

### 📦 5-QADAM: Statik fayllarni yig'ish va serverni qayta yuklash
Server konsolida statik fayllarni yig'ing va Gunicorn / Nginx xizmatini yangilang:

```bash
python manage.py collectstatic --noinput

# Agar Gunicorn ishlatilsa:
sudo systemctl restart gunicorn
# yoki
sudo supervisorctl restart all
```

**Bo'ldi, tayyor! 🎉**  
Endi `buxdu.uz/admin/` sahifasiga kirganingizda:
1. **Ro'yxat sahifasida (Changelist)**: Barcha yoki tanlangan maqolalarni 1 tugma bilan bazada yangi alifboga o'tkazish va tarjima qilish imkoniyati paydo bo'ladi.
2. **Tahrirlash sahifasida (Changeform)**: Yuqorida qulay tugmalar paydo bo'ladi (CKEditor 4 bilan to'liq ishlaydi).
3. **Standart «Harakat:» (Actions)** menyusida ham ommaviy alifbo va tarjima buyruqlari qo'shiladi.

---

<br>

## 💡 0-VARIANT: Dasturchini kutmasdan darhol ishlatish (Tampermonkey Userscript)

Agar server dasturchisi hozir band bo'lsa va sizga **hoziroq jonli `buxdu.uz` saytida** natija kerak bo'lsa:

1. Brauzeringizga [Tampermonkey](https://www.tampermonkey.net/) kengaytmasini o'rnating.
2. Ushbu repozitoriydagi [`userscript/buxdu_admin_helper.user.js`](userscript/buxdu_admin_helper.user.js) skriptini Tampermonkey'ga qo'shing.
3. `buxdu.uz/admin` saytini oching — **serverga umuman teginmasdan**, to'g'ridan-to'g'ri brauzeringizda barcha tugmalar avtomatik paydo bo'ladi va ishlaydi!

---

<br>

---

## 🇷🇺 Руководство по установке (Для программиста бэкенда)

### Шаг 1: Скопируйте папку
Положите папку `buxdu_smart_admin` в корень вашего Django-проекта (рядом с `manage.py`).

### Шаг 2: Добавьте в `INSTALLED_APPS` (`settings.py`):
```python
INSTALLED_APPS = [
    'buxdu_smart_admin',
    'django.contrib.admin',
    ...
]
```

### Шаг 3: Подключите маршруты в `urls.py`:
```python
path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),
```

### Шаг 4: Наследуйте `SmartMultilingualAdmin` в `admin.py`:
```python
from buxdu_smart_admin.admin import SmartMultilingualAdmin

@admin.register(Article)
class ArticleAdmin(SmartMultilingualAdmin):
    ...
```

### Шаг 5: Соберите статику и перезапустите:
```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

---

## ⚡ Что делают кнопки:
* **`⚡ Yangi Alifboga O'tkazish (Ö, Ğ, Ş, Ç)`**: 
  - `O‘/o‘` ➔ `Ö/ö`
  - `G‘/g‘` ➔ `Ğ/ğ`
  - `Sh/sh` ➔ `Ş/ş`
  - `Ch/ch` ➔ `Ç/ç`
  - Бережно сохраняет апострофы в именах вроде *Is'hoq*, *mus'haf*.
  - Поддерживает автоматическую конвертацию с кириллицы на новую латиницу.
  - Корректно сохраняет HTML-теги внутри визуального редактора CKEditor 4.
* **`🌐 Tillarga Avto-Tarjima (RU, EN, ZH)`**: 
  - Автоматически переводит узбекские тексты на русский, английский и китайский языки.
  - Заполняет мультиязычные поля модели (`_ru`, `_en`, `_zh`).
* **`🚀 1-Bosishda Hammasi`**: 
  - Выполняет и перевод на новый алфавит, и перевод на 3 языка одновременно.
