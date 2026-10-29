from django.db import models


# =============================================================================
# 1. CATEGORY (Kategoriyalar) - matches /admin/main/category/
# =============================================================================
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories', verbose_name="Parent")
    folder_path = models.CharField("Folder path", max_length=255, default="category", blank=True)
    
    # Multilingual fields
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=250)
    sarlavha_ru = models.CharField("Заголовок (Русский)", max_length=250, blank=True)
    sarlavha_en = models.CharField("Title (English)", max_length=250, blank=True)
    sarlavha_zh = models.CharField("标题 (中文)", max_length=250, blank=True)
    
    slug = models.SlugField("Slug", max_length=255, unique=True, blank=True)
    tartib = models.PositiveIntegerField("Tartib", default=1)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['tartib', 'sarlavha_uz']

    def __str__(self):
        return self.sarlavha_uz

    # Backwards compatibility property
    @property
    def nomi_uz(self):
        return self.sarlavha_uz


# =============================================================================
# 2. POSITION (Lavozimlar) - matches /admin/main/position/
# =============================================================================
class Position(models.Model):
    level = models.IntegerField("Level", default=0)
    
    # Multilingual fields
    title_uz = models.CharField("Title (O'zbekcha)", max_length=250)
    title_ru = models.CharField("Должность (Русский)", max_length=250, blank=True)
    title_en = models.CharField("Title (English)", max_length=250, blank=True)
    title_zh = models.CharField("职务 (中文)", max_length=250, blank=True)

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"
        ordering = ['level', 'title_uz']

    def __str__(self):
        return self.title_uz

    @property
    def nomi_uz(self):
        return self.title_uz


# =============================================================================
# 3. TYPE ARTICLE (Material turilari) - matches /admin/main/typearticle/
# =============================================================================
class TypeArticle(models.Model):
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=200)
    sarlavha_ru = models.CharField("Тип материала (Русский)", max_length=200, blank=True)
    sarlavha_en = models.CharField("Type (English)", max_length=200, blank=True)
    sarlavha_zh = models.CharField("类别 (中文)", max_length=200, blank=True)
    slug = models.SlugField("Slug", max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Material turi"
        verbose_name_plural = "Material turilari"
        ordering = ['sarlavha_uz']

    def __str__(self):
        return self.sarlavha_uz

    @property
    def nomi_uz(self):
        return self.sarlavha_uz


# =============================================================================
# 4. ARTICLE (Materiallar) - matches /admin/main/article/
# =============================================================================
class Article(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subarticles', verbose_name="Parent")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    material_turi = models.ForeignKey(TypeArticle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Material turi")
    
    image = models.FileField("Image", upload_to="article/images/", blank=True, null=True)
    is_featured = models.BooleanField("Избранные", default=False)
    
    owner = models.CharField("Owner", max_length=150, default="buxdu-press", blank=True)
    author = models.CharField("Author", max_length=150, default="buxdu-press", blank=True)
    xodimlar_info = models.CharField("Xodimlar", max_length=300, blank=True)
    uniwork_id = models.CharField("Uniwork id", max_length=100, blank=True, null=True)
    
    views_count = models.PositiveIntegerField("Ko'rishlar soni", default=0)
    sana = models.DateTimeField("Sana", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)
    slug = models.SlugField("Slug", max_length=350, blank=True)

    # Multilingual fields (O'zbek tili, Русский, Ingliz tili, Xitoycha)
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=350)
    sarlavha_ru = models.CharField("Заголовок (Русский)", max_length=350, blank=True)
    sarlavha_en = models.CharField("Title (English)", max_length=350, blank=True)
    sarlavha_zh = models.CharField("标题 (中文)", max_length=350, blank=True)

    text_uz = models.TextField("Text (O'zbekcha)")
    text_ru = models.TextField("Текст (Русский)", blank=True)
    text_en = models.TextField("Text (English)", blank=True)
    text_zh = models.TextField("内容 (中文)", blank=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiallar"
        ordering = ['-sana']

    def __str__(self):
        return self.sarlavha_uz or f"Material #{self.id}"

    # Aliases
    @property
    def title_uz(self):
        return self.sarlavha_uz
    @property
    def content_uz(self):
        return self.text_uz


# =============================================================================
# 5. BOOK (Books) - matches /admin/main/book/
# =============================================================================
class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    image = models.FileField("Image", upload_to="books/images/", blank=True, null=True)
    nashr_yili = models.PositiveIntegerField("Nashr yili", default=2026)
    sahifalar_soni = models.PositiveIntegerField("Sahifalar soni", default=100)
    tili = models.CharField("Tili", max_length=50, default="O'zbekcha")
    url = models.CharField("Url", max_length=300, default="#", blank=True)

    # Multilingual fields
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=350)
    sarlavha_ru = models.CharField("Название книги (Русский)", max_length=350, blank=True)
    sarlavha_en = models.CharField("Book Title (English)", max_length=350, blank=True)
    sarlavha_zh = models.CharField("书名 (中文)", max_length=350, blank=True)

    text_uz = models.TextField("Text (O'zbekcha)", blank=True)
    text_ru = models.TextField("Описание (Русский)", blank=True)
    text_en = models.TextField("Description (English)", blank=True)
    text_zh = models.TextField("简介 (中文)", blank=True)

    mualliflar = models.CharField("Mualliflar", max_length=350, default="Buxoro davlat universiteti")
    nashriyot = models.CharField("Nashriyot", max_length=250, default="Buxoro", blank=True)
    file = models.FileField("File", upload_to="konf_journal/", blank=True, null=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-nashr_yili', 'sarlavha_uz']

    def __str__(self):
        return f"{self.sarlavha_uz} ({self.nashr_yili})"

    @property
    def nomi_uz(self):
        return self.sarlavha_uz


# =============================================================================
# 6. EMPLOYEE (Xodimlar) - matches /admin/main/employee/
# =============================================================================
class Employee(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    lavozim = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Lavozim")
    photo = models.FileField("Photo", upload_to="person/", blank=True, null=True)
    phone_number = models.CharField("Phone number", max_length=60, blank=True)
    fax = models.CharField("Fax", max_length=60, blank=True)
    email = models.EmailField("Email", blank=True)
    owner = models.CharField("Owner", max_length=100, default="admin", blank=True)
    
    web_site = models.CharField("Web site", max_length=255, blank=True)
    google_scholar = models.CharField("Google scholar", max_length=255, blank=True)
    orcid = models.CharField("Orcid", max_length=100, blank=True)
    scopus = models.CharField("Scopus", max_length=100, blank=True)
    ad_index = models.CharField("Ad index", max_length=100, blank=True)
    slug = models.SlugField("Slug", max_length=255, blank=True)

    # Multilingual fields
    fio_uz = models.CharField("Fio (O'zbekcha)", max_length=250)
    fio_ru = models.CharField("Ф.И.О (Русский)", max_length=250, blank=True)
    fio_en = models.CharField("Full Name (English)", max_length=250, blank=True)
    fio_zh = models.CharField("姓名 (中文)", max_length=250, blank=True)

    ilmiy_unvoni_uz = models.CharField("Ilmiy unvoni (O'zbekcha)", max_length=250, blank=True)
    ilmiy_unvoni_ru = models.CharField("Ученое звание (Русский)", max_length=250, blank=True)
    ilmiy_unvoni_en = models.CharField("Academic Degree (English)", max_length=250, blank=True)
    ilmiy_unvoni_zh = models.CharField("职称/学位 (中文)", max_length=250, blank=True)

    address_uz = models.CharField("Address (O'zbekcha)", max_length=300, blank=True)
    address_ru = models.CharField("Адрес (Русский)", max_length=300, blank=True)
    address_en = models.CharField("Address (English)", max_length=300, blank=True)
    address_zh = models.CharField("地址 (中文)", max_length=300, blank=True)

    qabul_vaqti_uz = models.CharField("Qabul vaqti (O'zbekcha)", max_length=200, blank=True)
    qabul_vaqti_ru = models.CharField("Время приема (Русский)", max_length=200, blank=True)
    qabul_vaqti_en = models.CharField("Reception Hours (English)", max_length=200, blank=True)
    qabul_vaqti_zh = models.CharField("接待时间 (中文)", max_length=200, blank=True)

    mehnat_faoliyati_uz = models.TextField("Mehnat faoliyati (O'zbekcha)", blank=True)
    mehnat_faoliyati_ru = models.TextField("Трудовая деятельность (Русский)", blank=True)
    mehnat_faoliyati_en = models.TextField("Work Experience (English)", blank=True)
    mehnat_faoliyati_zh = models.TextField("工作经历 (中文)", blank=True)

    malaka_oshirish_uz = models.TextField("Malaka oshirish (O'zbekcha)", blank=True)
    malaka_oshirish_ru = models.TextField("Повышение квалификации (Русский)", blank=True)
    malaka_oshirish_en = models.TextField("Professional Development (English)", blank=True)
    malaka_oshirish_zh = models.TextField("进修培训 (中文)", blank=True)

    oqitadigan_fanlari_uz = models.TextField("O'qitadigan fanlari (O'zbekcha)", blank=True)
    oqitadigan_fanlari_ru = models.TextField("Преподаваемые предметы (Русский)", blank=True)
    oqitadigan_fanlari_en = models.TextField("Taught Subjects (English)", blank=True)
    oqitadigan_fanlari_zh = models.TextField("任教课程 (中文)", blank=True)

    ilmiy_faoliyati_uz = models.TextField("Ilmiy faoliyati (O'zbekcha)", blank=True)
    ilmiy_faoliyati_ru = models.TextField("Научная деятельность (Русский)", blank=True)
    ilmiy_faoliyati_en = models.TextField("Scientific Activities (English)", blank=True)
    ilmiy_faoliyati_zh = models.TextField("科研活动 (中文)", blank=True)

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"
        ordering = ['id']

    def __str__(self):
        return f"{self.fio_uz} ({self.lavozim or 'Xodim'})"


# =============================================================================
# 7. MENU (Menu) - matches /admin/main/menu/
# =============================================================================
class Menu(models.Model):
    TYPE_CHOICES = [
        ('all_categories', 'Список всех категорий'),
        ('material', 'Материал'),
        ('external', 'Внешние ссылки'),
    ]

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='submenus', verbose_name="Parent")
    type = models.CharField("Type", max_length=50, choices=TYPE_CHOICES, default='material')
    position = models.CharField("Position", max_length=50, default='top')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Article")
    mob_icon = models.FileField("Mob icon", upload_to="menu/icons/", blank=True, null=True)
    visible = models.BooleanField("Visible", default=True)
    level = models.IntegerField("Level", default=0)

    # Multilingual fields
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=200)
    sarlavha_ru = models.CharField("Название (Русский)", max_length=200, blank=True)
    sarlavha_en = models.CharField("Title (English)", max_length=200, blank=True)
    sarlavha_zh = models.CharField("名称 (中文)", max_length=200, blank=True)

    slug = models.SlugField("Slug", max_length=200, blank=True)
    url = models.CharField("Url", max_length=300, default="#", blank=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menu"
        ordering = ['level', 'sarlavha_uz']

    def __str__(self):
        return self.sarlavha_uz

    @property
    def nomi_uz(self):
        return self.sarlavha_uz


# =============================================================================
# 8. PHOTO CONTENT (Photo contents) - matches /admin/main/photocontent/
# =============================================================================
class PhotoContent(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='photos', verbose_name="Article", null=True, blank=True)
    photo = models.FileField("Photo", upload_to="photocontents/")
    sarlavha_uz = models.CharField("Sarlavha (O'zbekcha)", max_length=300, blank=True)

    class Meta:
        verbose_name = "Photo content"
        verbose_name_plural = "Photo contents"

    def __str__(self):
        return f"Photo content #{self.id} for {self.article or 'Gallery'}"

    @property
    def nomi_uz(self):
        return self.sarlavha_uz or f"Photo #{self.id}"


# Aliases for backward compatibility
Material = Article
Xodim = Employee
Kategoriya = Category
Lavozim = Position
MaterialTuri = TypeArticle
