# 🏛️ BuxDU Smart Admin & Modern Mobile CMS (2026 Edition)

[![Django](https://img.shields.io/badge/Django-5.2+-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38bdf8?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Tampermonkey](https://img.shields.io/badge/Tampermonkey-Userscript-00485B?style=for-the-badge&logo=tampermonkey&logoColor=white)](https://www.tampermonkey.net/)
[![Google DeepMind](https://img.shields.io/badge/Nano_Banana-4K_Visuals-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/)

> **Professional raqamli transformatsiya loyihasi**: Buxoro davlat universiteti (`buxdu.uz`) uchun 2026-yilgi yangi lotin alifbosi reformasi (`Ö, Ğ, Ş, Ç`), ko'p tilli avtomatik tarjima (RU, EN, ZH), Tampermonkey brauzer yordamchisi va zamonaviy mobil sayt redesigni.

---

## 📌 Loyiha tarkibidagi 2 ta asosiy yechim

### 1️⃣ Yechim: BuxDU Admin Smart Helper (Tampermonkey Userscript)
> **Jonli sayt (`buxdu.uz/admin/*`) uchun darhol ishlaydigan brauzer kengaytmasi.**

Universitet dasturchilarini kutish shart emas! Sayt administratori o'z brauzeriga 1 daqiqada o'rnatib, hoziroq foydalanishi mumkin:
* **🚀 1-BOSISHDA HAMMASI**: O'zbekcha yozilgan maqolani yangi alifboga o'tkazadi va bir vaqtning o'zida rus, ingliz va xitoy tillariga tarjima qiladi.
* **⚡ 2026 Yangi Alifbo Reformasi**: `O‘/o‘` ➔ `Ö/ö`, `G‘/g‘` ➔ `Ğ/ğ`, `Sh/sh` ➔ `Ş/ş`, `Ch/ch` ➔ `Ç/ç`.
* **CKEditor 4 va Modeltranslation integratsiyasi**: Matn ichidagi HTML teglarni (`<p>`, `<a>`, `<img>`) saqlagan holda tahrirlaydi va Django tillar tablarini avtomatik to'ldiradi.
* **O'rnatish**: [`userscript/buxdu_admin_helper.user.js`](userscript/buxdu_admin_helper.user.js) faylini Tampermonkey'ga import qiling.

---

### 2️⃣ Yechim: Zamonaviy Mustaqil CMS & Mobil Redesign (`admin.buxdu.uz` & `buxdu.uz`)
> **Eski Django admin o'rniga zamonaviy SPA boshqaruv paneli va yangilangan mobil versiya.**

* **8 ta model (`MAIN` bo'limi)**:
  1. `Article` (**Materiallar**) — yangiliklar, e'lonlar, fotogalereyalar.
  2. `Employee` (**Xodimlar**) — rektorat, dekanlar, kafedra mudirlari, professorlar.
  3. `Book` (**Books**) — konferensiya to'plamlari, avtoreferatlar.
  4. `Category` (**Kategoriyalar**) — fakultetlar va bo'limlar.
  5. `Position` (**Lavozimlar**) — iyerarxiya va darajalar.
  6. `TypeArticle` (**Material turilari**) — sport, tadbirlar, grantlar.
  7. `Menu` (**Menu**) — sayt navigatsiyasi.
  8. `PhotoContent` (**Photo contents**) — foto-albomlar.
* **📱 Ultra-zamonaviy Mobil Sayt (`/mobile/`)**:
  - Matnni to'sib turgan 5 ta noqulay ijtimoiy tugmalar o'rniga qulay **Speed-Dial Floating Action Button (Share)**.
  - Tezkor xizmatlar (HEMIS, Rektorat, Kutubxona, Qabul-2027) doirachalari.
  - Google DeepMind **Nano Banana** orqali yaratilgan 4K fotorealistik BuxDU bosh binosi surati.
  - Ilova uslubidagi **Bottom Navigation Bar** (`Asosiy`, `Yangiliklar`, `HEMIS`, `Kitoblar`, `Menyu`).
  - Dark / Light rejimi va ko'p tilli interfeys.
* **⚡ Ommaviy Alifbo Yangilash (Bulk Transliterate)**: Butun ma'lumotlar bazasidagi minglab eski maqolalarni 1 tugma bilan yangi alifboga o'tkazish imkoniyati.

---

## 📸 Skrinshotlar va Vizual

| BuxDU Bosh Binosi (Nano Banana 4K) | Zamonaviy Mobil Redesign |
|:---:|:---:|
| ![BuxDU Campus](buxdu_campus_hero.jpg) | ![Mobile Redesign](demo_app/dashboard/templates/dashboard/mobile.html) |

---

## 🚀 Tezkor Ishga Tushirish (Quick Start)

### 1. Repozitoriyni klonlash:
```bash
git clone https://github.com/TheGreatMontana/buxdu-smart-admin.git
cd buxdu-smart-admin
```

### 2. Virtual muhit yaratish va kutubxonalarni o'rnatish:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install django
```

### 3. Ma'lumotlar bazasini tayyorlash va test ma'lumotlarini yuklash:
```bash
cd demo_app
python manage.py migrate
python apply_and_seed.py
```

### 4. Serverni yoqish:
```bash
python manage.py runserver 127.0.0.1:8000
```

* 🖥️ **Boshqaruv paneli (Desktop/Tablet)**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* 📱 **Zamonaviy Mobil Sayt**: [http://127.0.0.1:8000/mobile/](http://127.0.0.1:8000/mobile/)
* ⚙️ **REST API Dok**: [http://127.0.0.1:8000/api/stats/](http://127.0.0.1:8000/api/stats/)
* 🔑 **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Login: `admin` / Parol: `admin123`)

---

## 🛠️ API Qo'llanmasi

| Metod | Endpoint | Tavsif |
|---|---|---|
| `GET` | `/api/stats/` | Barcha 8 ta model bo'yicha jonli hisoblagichlar |
| `POST` | `/api/tools/transliterate/` | Matnni 2026 yangi alifbosiga o'tkazish (`Ö, Ğ, Ş, Ç`) |
| `POST` | `/api/tools/bulk_transliterate/` | Butun bazadagi yozuvlarni ommaviy alifboga o'tkazish |
| `POST` | `/api/tools/translate/` | Matnni bir vaqtning o'zida RU, EN, ZH tillariga tarjima qilish |
| `GET/POST` | `/api/<model_name>/` | Generic CRUD ro'yxat va yangi yozuv yaratish |
| `GET/PUT/DELETE` | `/api/<model_name>/<id>/` | Yozuvni olish, tahrirlash yoki o'chirish |

---

## 📄 Litsenziya
MIT License © 2026 TheGreatMontana. Buxoro davlat universiteti (BuxDU) raqamli infratuzilmasini rivojlantirish uchun ochiq manbali loyiha.
