from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .uzbek_alphabet import to_new_uzbek_latin
from .translator import translate_bundle


class SmartMultilingualAdmin(admin.ModelAdmin):
    """
    Drop-in Admin class for any multilingual model (Article, Employee, Book, Category, etc.).
    Provides:
    1. Header Smart Action Bar on both Changeform and Changelist.
    2. Django Admin 'Harakat' actions for bulk transliteration and translation.
    """
    change_form_template = 'admin/buxdu_smart_admin/change_form.html'
    actions = ['action_convert_to_new_uzbek', 'action_auto_translate_all', 'action_master_all']

    class Media:
        css = {
            'all': (
                'buxdu_smart_admin/css/smart_admin.css',
            )
        }
        js = (
            'buxdu_smart_admin/js/smart_admin.js',
        )

    def _get_model_target_fields(self, obj):
        fields = []
        for f in obj._meta.get_fields():
            name = getattr(f, 'name', '')
            if name.endswith('_uz') or name in ('sarlavha', 'title', 'fio', 'nomi', 'text', 'content', 'annotatsiya'):
                fields.append(name)
        return fields

    @admin.action(description="⚡ Tanlanganlarni yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazish")
    def action_convert_to_new_uzbek(self, request, queryset):
        """
        Bulk action to convert selected records' Uzbek text fields into the new Latin alphabet.
        """
        count = 0
        for obj in queryset:
            updated = False
            target_fields = self._get_model_target_fields(obj)
            for field in target_fields:
                if hasattr(obj, field):
                    val = getattr(obj, field, None)
                    if val and isinstance(val, str):
                        new_val = to_new_uzbek_latin(val)
                        if new_val != val:
                            setattr(obj, field, new_val)
                            updated = True
            if updated:
                obj.save()
                count += 1

        self.message_user(
            request,
            f"✅ Muvaffaqiyatli: {count} ta yozuv 2026-yilgi yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi!",
            messages.SUCCESS
        )

    @admin.action(description="🌐 Tanlanganlarni barcha tillarga (RU, EN, ZH) avto-tarjima qilish")
    def action_auto_translate_all(self, request, queryset):
        """
        Bulk action to auto-translate empty RU/EN/ZH fields from UZ.
        """
        count = 0
        for obj in queryset:
            changed = False
            target_fields = self._get_model_target_fields(obj)
            for field in target_fields:
                if field.endswith('_uz'):
                    val = getattr(obj, field, None)
                    if val and isinstance(val, str) and val.strip():
                        base = field[:-3]
                        ru_f, en_f, zh_f = f"{base}_ru", f"{base}_en", f"{base}_zh"
                        if hasattr(obj, ru_f) or hasattr(obj, en_f) or hasattr(obj, zh_f):
                            trans = translate_bundle(val, source_lang='uz', target_langs=['ru', 'en', 'zh-cn'])
                            if hasattr(obj, ru_f) and trans.get('ru'):
                                setattr(obj, ru_f, trans['ru'])
                                changed = True
                            if hasattr(obj, en_f) and trans.get('en'):
                                setattr(obj, en_f, trans['en'])
                                changed = True
                            if hasattr(obj, zh_f) and trans.get('zh-cn'):
                                setattr(obj, zh_f, trans['zh-cn'])
                                changed = True
            if changed:
                obj.save()
                count += 1

        self.message_user(
            request,
            f"🎉 Ajoyib: {count} ta yozuv rus, ingliz va xitoy tillariga tarjima qilindi!",
            messages.SUCCESS
        )

    @admin.action(description="🚀 1-Bosishda Hammasi (Yangi Alifbo + 3 Tilda Tarjima)")
    def action_master_all(self, request, queryset):
        """
        Bulk master action: both transliterate and translate.
        """
        self.action_convert_to_new_uzbek(request, queryset)
        self.action_auto_translate_all(request, queryset)
