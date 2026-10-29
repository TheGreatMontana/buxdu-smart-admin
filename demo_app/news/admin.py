from django.contrib import admin
from buxdu_smart_admin.admin import SmartMultilingualAdmin
from .models import (
    Article, Employee, Book, Category, Position, 
    TypeArticle, Menu, PhotoContent
)


class PhotoContentInline(admin.TabularInline):
    model = PhotoContent
    extra = 1


@admin.register(Article)
class ArticleAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'category', 'slug', 'owner', 'author', 'views_count', 'sana')
    list_filter = ('category', 'material_turi', 'is_featured')
    search_fields = ('sarlavha_uz', 'sarlavha_ru', 'sarlavha_en', 'text_uz')
    inlines = [PhotoContentInline]
    fieldsets = (
        ("🇺🇿 O'zbek tili (Asosiy)", {
            'fields': ('category', 'material_turi', 'sarlavha_uz', 'text_uz'),
            'description': "O'zbek tilida yozing. Yuqoridagi 'Yangi Alifbo (Ö, Ğ, Ş, Ç)' va 'Avto-Tarjima' tugmalarini bosing."
        }),
        ("🇷🇺 Русский", {
            'fields': ('sarlavha_ru', 'text_ru'),
        }),
        ("🇬🇧 Ingliz tili (English)", {
            'fields': ('sarlavha_en', 'text_en'),
        }),
        ("🇨🇳 Xitoycha (中文)", {
            'fields': ('sarlavha_zh', 'text_zh'),
        }),
        ("⚙️ Parametrlar va Rasm", {
            'fields': ('image', 'is_featured', 'owner', 'author', 'xodimlar_info', 'uniwork_id', 'views_count', 'slug'),
        }),
    )


@admin.register(Employee)
class EmployeeAdmin(SmartMultilingualAdmin):
    list_display = ('fio_uz', 'category', 'lavozim', 'slug', 'id')
    list_filter = ('category', 'lavozim')
    search_fields = ('fio_uz', 'fio_ru', 'fio_en', 'ilmiy_unvoni_uz')
    fieldsets = (
        ("🇺🇿 O'zbek tili", {
            'fields': ('category', 'lavozim', 'fio_uz', 'ilmiy_unvoni_uz', 'address_uz', 'qabul_vaqti_uz', 'mehnat_faoliyati_uz', 'malaka_oshirish_uz', 'oqitadigan_fanlari_uz', 'ilmiy_faoliyati_uz'),
        }),
        ("🇷🇺 Русский", {
            'fields': ('fio_ru', 'ilmiy_unvoni_ru', 'address_ru', 'qabul_vaqti_ru', 'mehnat_faoliyati_ru', 'malaka_oshirish_ru', 'oqitadigan_fanlari_ru', 'ilmiy_faoliyati_ru'),
            'classes': ('collapse',),
        }),
        ("🇬🇧 Ingliz tili (English)", {
            'fields': ('fio_en', 'ilmiy_unvoni_en', 'address_en', 'qabul_vaqti_en', 'mehnat_faoliyati_en', 'malaka_oshirish_en', 'oqitadigan_fanlari_en', 'ilmiy_faoliyati_en'),
            'classes': ('collapse',),
        }),
        ("🇨🇳 Xitoycha (中文)", {
            'fields': ('fio_zh', 'ilmiy_unvoni_zh', 'address_zh', 'qabul_vaqti_zh', 'mehnat_faoliyati_zh', 'malaka_oshirish_zh', 'oqitadigan_fanlari_zh', 'ilmiy_faoliyati_zh'),
            'classes': ('collapse',),
        }),
        ("Aloqa va Profil", {
            'fields': ('photo', 'phone_number', 'fax', 'email', 'owner', 'web_site', 'google_scholar', 'orcid', 'scopus', 'ad_index', 'slug'),
        }),
    )


@admin.register(Book)
class BookAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'category', 'url', 'nashr_yili', 'sahifalar_soni')
    list_filter = ('category', 'nashr_yili')
    search_fields = ('sarlavha_uz', 'mualliflar', 'text_uz')
    fieldsets = (
        ("🇺🇿 O'zbek tili", {
            'fields': ('category', 'sarlavha_uz', 'text_uz', 'mualliflar', 'nashriyot', 'nashr_yili', 'sahifalar_soni', 'tili', 'url', 'image', 'file'),
        }),
        ("🇷🇺 Русский", {
            'fields': ('sarlavha_ru', 'text_ru'),
            'classes': ('collapse',),
        }),
        ("🇬🇧 Ingliz tili", {
            'fields': ('sarlavha_en', 'text_en'),
            'classes': ('collapse',),
        }),
        ("🇨🇳 Xitoycha", {
            'fields': ('sarlavha_zh', 'text_zh'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Category)
class CategoryAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'slug', 'parent', 'folder_path')
    search_fields = ('sarlavha_uz', 'slug')


@admin.register(Position)
class PositionAdmin(SmartMultilingualAdmin):
    list_display = ('title_uz', 'level')
    search_fields = ('title_uz',)


@admin.register(TypeArticle)
class TypeArticleAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'slug')
    search_fields = ('sarlavha_uz',)


@admin.register(Menu)
class MenuAdmin(SmartMultilingualAdmin):
    list_display = ('sarlavha_uz', 'slug', 'parent', 'type', 'position', 'category', 'article', 'url')
    list_filter = ('type', 'position', 'visible')
    search_fields = ('sarlavha_uz', 'url')


@admin.register(PhotoContent)
class PhotoContentAdmin(SmartMultilingualAdmin):
    list_display = ('id', 'sarlavha_uz', 'article', 'photo')
    search_fields = ('sarlavha_uz',)
