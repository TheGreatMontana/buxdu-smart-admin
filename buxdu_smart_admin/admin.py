from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from .uzbek_alphabet import to_new_uzbek_latin
from .translator import translate_bundle


class SmartMultilingualAdmin(admin.ModelAdmin):
    """
    Drop-in Admin class for any multilingual model (Article, News, Announcement, etc.).
    
    Usage:
        from buxdu_smart_admin.admin import SmartMultilingualAdmin
        
        @admin.register(Article)
        class ArticleAdmin(SmartMultilingualAdmin):
            # Your normal settings (list_display, search_fields, etc.)
            pass
    """
    change_form_template = 'admin/buxdu_smart_admin/change_form.html'
    actions = ['action_convert_to_new_uzbek', 'action_auto_translate_all']

    class Media:
        css = {
            'all': (
                'buxdu_smart_admin/css/smart_admin.css',
            )
        }
        js = (
            'buxdu_smart_admin/js/smart_admin.js',
        )

    @admin.action(description="⚡ Tanlanganlarni yangi o'zbek alifbosiga o'tkazish")
    def action_convert_to_new_uzbek(self, request, queryset):
        """
        Bulk action to convert selected records' Uzbek text fields into the new Latin alphabet.
        """
        count = 0
        text_fields = ['title', 'title_uz', 'content', 'content_uz', 'description', 'description_uz', 'body', 'body_uz']

        for obj in queryset:
            updated = False
            for field in text_fields:
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
            f"✅ Muvaffaqiyatli: {count} ta maqola yangi alifboga o'tkazildi!",
            messages.SUCCESS
        )

    @admin.action(description="🌐 Tanlanganlarni barcha tillarga (RU, EN, ZH) avto-tarjima qilish")
    def action_auto_translate_all(self, request, queryset):
        """
        Bulk action to auto-translate empty RU/EN/ZH fields from UZ.
        """
        count = 0
        for obj in queryset:
            # Detect title
            uz_title = getattr(obj, 'title_uz', None) or getattr(obj, 'title', None)
            if uz_title:
                translations = translate_bundle(uz_title, source_lang='uz', target_langs=['ru', 'en', 'zh-cn'])
                if hasattr(obj, 'title_ru') and not obj.title_ru:
                    obj.title_ru = translations.get('ru', '')
                if hasattr(obj, 'title_en') and not obj.title_en:
                    obj.title_en = translations.get('en', '')
                if hasattr(obj, 'title_zh') and not obj.title_zh:
                    obj.title_zh = translations.get('zh-cn', '')
                if hasattr(obj, 'title_zh_cn') and not obj.title_zh_cn:
                    obj.title_zh_cn = translations.get('zh-cn', '')

            # Detect content
            uz_content = getattr(obj, 'content_uz', None) or getattr(obj, 'content', None) or getattr(obj, 'body_uz', None)
            if uz_content:
                translations = translate_bundle(uz_content, source_lang='uz', target_langs=['ru', 'en', 'zh-cn'])
                for f_prefix in ['content', 'body']:
                    ru_f = f"{f_prefix}_ru"
                    en_f = f"{f_prefix}_en"
                    zh_f = f"{f_prefix}_zh"
                    zh_cn_f = f"{f_prefix}_zh_cn"

                    if hasattr(obj, ru_f) and not getattr(obj, ru_f):
                        setattr(obj, ru_f, translations.get('ru', ''))
                    if hasattr(obj, en_f) and not getattr(obj, en_f):
                        setattr(obj, en_f, translations.get('en', ''))
                    if hasattr(obj, zh_f) and not getattr(obj, zh_f):
                        setattr(obj, zh_f, translations.get('zh-cn', ''))
                    if hasattr(obj, zh_cn_f) and not getattr(obj, zh_cn_f):
                        setattr(obj, zh_cn_f, translations.get('zh-cn', ''))

            obj.save()
            count += 1

        self.message_user(
            request,
            f"✅ {count} ta maqola rus, ingliz va xitoy tillariga avtomatik tarjima qilindi!",
            messages.SUCCESS
        )
