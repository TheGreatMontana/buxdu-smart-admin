# 🏛️ BuxDU Smart Django Admin

[![Django](https://img.shields.io/badge/Django-3.2_|_4.2_|_5.x-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![2026 Reform](https://img.shields.io/badge/2026_Alifbo-Ö_%7C_Ğ_%7C_Ş_%7C_Ç-2b7a59?style=for-the-badge)](https://buxdu.uz)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **Plug-and-play Django-плагин для админ-панели сайтов университетов и организаций.**  
> Обеспечивает мгновенный переход узбекских текстов на **новый алфавит 2026 года (`Ö, Ğ, Ş, Ç`)** и **автоматический синхронный перевод** на русский, английский и китайский языки прямо в Django Admin.

---

## ⚡ Основные возможности

1. **⚡ Перевод на новый алфавит 2026 года (`Ö, Ğ, Ş, Ç`)**:
   - `O‘ / o‘` ➔ `Ö / ö` (*O'zbekiston* ➔ *Özbekiston*, *o'quv* ➔ *öquv*)
   - `G‘ / g‘` ➔ `Ğ / ğ` (*yig'ilish* ➔ *yiğiliş*, *to'g'risida* ➔ *töğrisida*)
   - `Sh / sh` ➔ `Ş / ş` (*sharafli* ➔ *şarafli*, *qatnashdi* ➔ *qatnaşdi*)
   - `Ch / ch` ➔ `Ç / ç` (*ochilish* ➔ *oçiliş*, *o'qituvchilar* ➔ *öqituvçilar*)
   - Автоматически сохраняет апострофы в именах и терминах (*Is'hoq*, *mus'haf*).
   - Поддерживает автоматический перевод текста, вставленного на кириллице.
   - Бережно сохраняет всю разметку HTML внутри визуального редактора **CKEditor 4** и TinyMCE.

2. **🌐 Мультиязычный авто-перевод (RU, EN, ZH)**:
   - В 1 клик переводит узбекский заголовок и тело статьи на **русский**, **английский** и **китайский** языки.
   - Автоматически заполняет соответствующие поля модели (`sarlavha_ru`, `text_ru`, `sarlavha_en`, `text_en`, `sarlavha_zh`, `text_zh`).

3. **🚀 Пакетная обработка в общем списке (Changelist)**:
   - Кнопки работают как внутри отдельного материала, так и в общей таблице: можно выделить 10–50 статей и в 1 клик обновить их в базе данных.

---

## 📖 Руководство по установке / O'rnatish qo'llanmasi

### Шаг 1. Добавление приложения в проект
Скопируйте директорию `buxdu_smart_admin` в корень вашего Django-проекта (рядом с `manage.py`):
```bash
cp -r /path/to/buxdu_smart_admin ./buxdu_smart_admin
```

---

### Шаг 2. Регистрация в `settings.py`
Добавьте `'buxdu_smart_admin'` в список установленных приложений `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'buxdu_smart_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    # ... остальные приложения
]
```

---

### Шаг 3. Подключение URL-маршрутов в `urls.py`
В основном файле маршрутизации проекта подключите эндпоинты плагина:

```python
from django.urls import path, include

urlpatterns = [
    # API эндпоинты для транслитерации и перевода
    path('admin/buxdu_smart_admin/', include('buxdu_smart_admin.urls')),
    
    path('admin/', admin.site.urls),
]
```

---

### Шаг 4. Подключение к моделям в `admin.py`
Для любой модели (статьи, сотрудники, книги, новости) используйте готовый класс `SmartMultilingualAdmin`:

```python
from django.contrib import admin
from buxdu_smart_admin.admin import SmartMultilingualAdmin
from .models import Article

@admin.register(Article)
class ArticleAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'sana')
    # Все ваши прежние поля и настройки сохраняются без изменений
```

> **Если у вас уже используется собственный базовый класс ModelAdmin:**  
> Достаточно добавить в ваш класс админки:
> ```python
> change_form_template = 'admin/buxdu_smart_admin/change_form.html'
> actions = ['action_convert_to_new_uzbek', 'action_auto_translate_all', 'action_master_all']
> ```

---

### Шаг 5. Сборка статики и перезапуск веб-сервера
Выполните стандартную команду сбора статических файлов и перезапустите службу:

```bash
python manage.py collectstatic --noinput

# При использовании systemd / Gunicorn:
sudo systemctl restart gunicorn

# Либо через supervisor:
sudo supervisorctl restart all
```

---

## 🧩 Альтернативный вариант (Tampermonkey Userscript)
Если требуется использовать функционал прямо сейчас на работающем сайте **без внесения изменений в код бэкенда**:
1. Установите расширение [Tampermonkey](https://www.tampermonkey.net/) в браузер администратора.
2. Добавьте скрипт [`userscript/buxdu_admin_helper.user.js`](userscript/buxdu_admin_helper.user.js).
3. При открытии `buxdu.uz/admin` кнопки транслитерации и перевода появятся на странице автоматически.

---

## 🧪 Локальный запуск демо-проекта

```bash
git clone https://github.com/TheGreatMontana/buxdu-smart-admin.git
cd buxdu-smart-admin

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # На Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Инициализация и запуск
cd demo_app
python init_db.py
python manage.py runserver 127.0.0.1:8000
```

* 🔑 **Админ-панель**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (Логин: `admin` | Пароль: `admin123`)
* ⚡ **Прямой переход к редактированию**: [http://127.0.0.1:8000/edit-demo/](http://127.0.0.1:8000/edit-demo/)
