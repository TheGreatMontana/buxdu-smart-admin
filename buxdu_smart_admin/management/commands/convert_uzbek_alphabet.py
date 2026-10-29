"""
Django Management Command: convert_uzbek_alphabet
=================================================
Bulk converts Uzbek texts in database models into the 2026 New Uzbek Latin Alphabet.

Usage:
    # Dry-run test (does not save changes, just previews):
    python manage.py convert_uzbek_alphabet --dry-run

    # Convert all detected models & text fields:
    python manage.py convert_uzbek_alphabet

    # Convert specific model and fields:
    python manage.py convert_uzbek_alphabet --model article.Article --fields title,content,description
"""

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
from buxdu_smart_admin.uzbek_alphabet import to_new_uzbek_latin


class Command(BaseCommand):
    help = "2026-yilgi yangi o'zbek lotin alifbosiga (ō, ḡ, ş, ç) bazadagi barcha matnlarni o'tkazish"

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help="Aniq model nomi, masalan: 'news.Article' yoki 'main.Post'"
        )
        parser.add_argument(
            '--fields',
            type=str,
            help="Vergul bilan ajratilgan maydonlar ro'yxati, masalan: 'title,content,description'"
        )
        parser.add_argument(
            '--style',
            type=str,
            default='umlaut',
            choices=['umlaut', 'macron', 'tilde'],
            help="Alifbo turi: 'umlaut' (Ö, Ğ, Ş, Ç - rasm bo'yicha), 'macron' (Ō, Ḡ, Ş, Ç) yoki 'tilde' (Õ, Ğ, Ş, Ç)"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Bazani o'zgartirmasdan faqat nechta yozuv o'zgarishini ko'rish"
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        style = options['style']
        target_model_name = options.get('model')
        target_fields_raw = options.get('fields')

        self.stdout.write(self.style.MIGRATE_HEADING("=== BuxDU Smart Admin: Alifbo Konvertatsiyasi ==="))
        if dry_run:
            self.stdout.write(self.style.WARNING("⚠️ REJIM: DRY-RUN (Bazaga hech qanday o'zgarish yozilmaydi)\n"))

        target_models = []
        if target_model_name:
            try:
                target_models.append(apps.get_model(target_model_name))
            except LookupError:
                self.stderr.write(self.style.ERROR(f"❌ Xatolik: '{target_model_name}' modeli topilmadi."))
                return
        else:
            # Scan all models in all installed apps (skip django internal auth/sessions/admin)
            for model in apps.get_models():
                app_label = model._meta.app_label
                if app_label in ['admin', 'auth', 'contenttypes', 'sessions', 'messages']:
                    continue
                target_models.append(model)

        total_converted_records = 0

        for model in target_models:
            model_name = model._meta.label
            text_fields = []

            if target_fields_raw:
                field_names = [f.strip() for f in target_fields_raw.split(',')]
                for fname in field_names:
                    try:
                        f = model._meta.get_field(fname)
                        text_fields.append(f)
                    except Exception:
                        pass
            else:
                # Auto-detect text fields (CharField, TextField)
                for field in model._meta.get_fields():
                    if isinstance(field, (models.CharField, models.TextField)):
                        # Look for common Uzbek or standard text fields
                        name = field.name
                        if any(k in name for k in ['title', 'content', 'description', 'body', 'name', 'text']) and not name.endswith(('_ru', '_en', '_zh')):
                            text_fields.append(field)

            if not text_fields:
                continue

            field_names_str = ", ".join([f.name for f in text_fields])
            self.stdout.write(f"🔍 Tekshirilmoqda: {self.style.SUCCESS(model_name)} (Maydonlar: {field_names_str})")

            queryset = model.objects.all()
            model_converted = 0

            for obj in queryset.iterator():
                obj_changed = False
                for field in text_fields:
                    val = getattr(obj, field.name, None)
                    if val and isinstance(val, str):
                        new_val = to_new_uzbek_latin(val, style=style)
                        if new_val != val:
                            setattr(obj, field.name, new_val)
                            obj_changed = True

                if obj_changed:
                    model_converted += 1
                    if not dry_run:
                        obj.save()

            if model_converted > 0:
                self.stdout.write(self.style.SUCCESS(f"  👉 {model_converted} ta yozuv o'zgartirildi."))
                total_converted_records += model_converted
            else:
                self.stdout.write("  ✓ Barcha matnlar allaqachon to'g'ri alifboda.")

        self.stdout.write("\n" + "=" * 50)
        if dry_run:
            self.stdout.write(self.style.WARNING(f"Jami o'zgartirilishi kerak bo'lgan yozuvlar: {total_converted_records}"))
            self.stdout.write("Haqiqiy o'zgartirishni amalga oshirish uchun buyruqni '--dry-run'siz ishga tushiring.")
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ Bajarildi! Jami yangilangan yozuvlar: {total_converted_records}"))
