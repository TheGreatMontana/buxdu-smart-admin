/**
 * BuxDU Smart Admin Frontend Controller
 * =====================================
 * Handles:
 * 1. 2026 New Uzbek Latin transliteration (client-side + backend API fallback)
 * 2. Automated parallel translation to RU, EN, ZH
 * 3. Language tab switching & clean UX
 * 4. Telegram & Google live preview
 * 5. WYSIWYG editor integration (CKEditor, TinyMCE, standard textareas)
 */

document.addEventListener('DOMContentLoaded', function () {
    // CSRF Helper for Django AJAX
    function getCsrfToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }

    // Status message helper
    const statusBox = document.getElementById('buxdu-status-message');
    function showStatus(message, type = 'info', duration = 4000) {
        if (!statusBox) return;
        statusBox.className = `buxdu-status ${type}`;
        statusBox.innerHTML = message;
        statusBox.classList.remove('hidden');

        if (duration > 0) {
            setTimeout(() => {
                statusBox.classList.add('hidden');
            }, duration);
        }
    }

    // Helper: Read field value (supports CKEditor / textarea / input)
    function getFieldValue(fieldName) {
        // Try CKEditor first if present
        if (window.CKEDITOR && window.CKEDITOR.instances && window.CKEDITOR.instances[`id_${fieldName}`]) {
            return window.CKEDITOR.instances[`id_${fieldName}`].getData();
        }
        // Try TinyMCE
        if (window.tinymce && window.tinymce.get(`id_${fieldName}`)) {
            return window.tinymce.get(`id_${fieldName}`).getContent();
        }
        // Standard input or textarea
        const el = document.querySelector(`[name="${fieldName}"]`) || document.getElementById(`id_${fieldName}`);
        return el ? el.value : '';
    }

    // Helper: Set field value (supports CKEditor / textarea / input)
    function setFieldValue(fieldName, value) {
        if (window.CKEDITOR && window.CKEDITOR.instances && window.CKEDITOR.instances[`id_${fieldName}`]) {
            window.CKEDITOR.instances[`id_${fieldName}`].setData(value);
            return true;
        }
        if (window.tinymce && window.tinymce.get(`id_${fieldName}`)) {
            window.tinymce.get(`id_${fieldName}`).setContent(value);
            return true;
        }
        const el = document.querySelector(`[name="${fieldName}"]`) || document.getElementById(`id_${fieldName}`);
        if (el) {
            el.value = value;
            // Trigger change event for listeners
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
        }
        return false;
    }

    // Client-side quick transliterator (instant without network latency)
    function clientTransliterateToNew(text) {
        if (!text) return text;
        const apostrophes = "['`ʼʻ’‘]";
        let res = text;
        
        // Protect s'h
        res = res.replace(new RegExp(`([Ss])${apostrophes}([Hh])`, 'g'), '$1__SEP__$2');

        // G', g' -> Ğ, ğ
        res = res.replace(new RegExp(`G${apostrophes}`, 'g'), 'Ğ');
        res = res.replace(new RegExp(`g${apostrophes}`, 'g'), 'ğ');

        // O', o' -> Ö, ö
        res = res.replace(new RegExp(`O${apostrophes}`, 'g'), 'Ö');
        res = res.replace(new RegExp(`o${apostrophes}`, 'g'), 'ö');

        // Sh, sh -> Ş, ş
        res = res.replace(/\bSH\b/g, 'Ş');
        res = res.replace(/Sh/g, 'Ş');
        res = res.replace(/sh/g, 'ş');

        // Ch, ch -> Ç, ç
        res = res.replace(/\bCH\b/g, 'Ç');
        res = res.replace(/Ch/g, 'Ç');
        res = res.replace(/ch/g, 'ç');

        // Restore s'h
        res = res.replace(/__SEP__/g, "'");
        return res;
    }

    // Find all primary Uzbek fields
    function getUzbekFieldNames() {
        const candidates = ['title_uz', 'title', 'content_uz', 'content', 'description_uz', 'description', 'body_uz', 'body', 'text_uz', 'text'];
        const found = [];
        candidates.forEach(name => {
            const el = document.querySelector(`[name="${name}"]`) || document.getElementById(`id_${name}`);
            if (el) found.push(name);
        });
        return found;
    }

    // =========================================================================
    // 1. ACTION: Transliterate to 2026 New Uzbek Latin
    // =========================================================================
    const btnTranslit = document.getElementById('btn-transliterate-new');
    if (btnTranslit) {
        btnTranslit.addEventListener('click', async function () {
            const uzFields = getUzbekFieldNames();
            if (uzFields.length === 0) {
                showStatus("⚠️ O'zbekcha maydonlar (title, content) topilmadi.", "error");
                return;
            }

            btnTranslit.disabled = true;
            btnTranslit.innerHTML = "⏳ Alifbo o'zgartirilmoqda...";
            let convertedCount = 0;

            for (const field of uzFields) {
                const currentVal = getFieldValue(field);
                if (currentVal && currentVal.trim()) {
                    const newVal = clientTransliterateToNew(currentVal);
                    if (newVal !== currentVal) {
                        setFieldValue(field, newVal);
                        convertedCount++;
                    }
                }
            }

            btnTranslit.disabled = false;
            btnTranslit.innerHTML = '<span class="btn-icon">⚡</span> Yangi Alifboga O\'girish';

            if (convertedCount > 0) {
                showStatus(`✅ Muvaffaqiyatli: ${convertedCount} ta maydondagi matnlar yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi!`, "success", 5000);
            } else {
                showStatus("ℹ️ Barcha o'zbekcha matnlar allaqachon yangi alifboda yoki matn kiritilmagan.", "info", 4000);
            }
        });
    }

    // =========================================================================
    // 2. ACTION: Automated Parallel Translation to RU, EN, ZH
    // =========================================================================
    const btnTranslate = document.getElementById('btn-auto-translate');
    if (btnTranslate) {
        btnTranslate.addEventListener('click', async function () {
            // Find Uzbek title & content
            const titleField = ['title_uz', 'title'].find(f => getFieldValue(f));
            const contentField = ['content_uz', 'content', 'description_uz', 'description', 'body_uz', 'body'].find(f => getFieldValue(f));

            const titleText = titleField ? getFieldValue(titleField) : '';
            const contentText = contentField ? getFieldValue(contentField) : '';

            if (!titleText && !contentText) {
                showStatus("⚠️ Avval o'zbekcha sarlavha yoki matnni kiriting!", "error");
                return;
            }

            btnTranslate.disabled = true;
            btnTranslate.innerHTML = "⏳ Sun'iy intellekt tarjima qilmoqda...";
            showStatus("🌐 Rus, ingliz va xitoy tillariga professional tarjima qilinmoqda, kuting...", "info", 0);

            try {
                // Function to call translation API or fallback endpoint
                async function callTranslateApi(text) {
                    const response = await fetch('/admin/buxdu_smart_admin/api/translate/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCsrfToken()
                        },
                        body: JSON.stringify({
                            text: text,
                            source_lang: 'uz',
                            target_langs: ['ru', 'en', 'zh-cn']
                        })
                    });
                    if (response.ok) {
                        const data = await response.json();
                        return data.translations;
                    }
                    throw new Error("Tarjima serverida xatolik yuz berdi");
                }

                // Translate Title
                let titleTrans = {};
                if (titleText) {
                    titleTrans = await callTranslateApi(titleText);
                }

                // Translate Content
                let contentTrans = {};
                if (contentText) {
                    contentTrans = await callTranslateApi(contentText);
                }

                // Insert into RU fields
                if (titleTrans['ru']) {
                    setFieldValue('title_ru', titleTrans['ru']);
                }
                if (contentTrans['ru']) {
                    setFieldValue('content_ru', contentTrans['ru']) ||
                    setFieldValue('description_ru', contentTrans['ru']) ||
                    setFieldValue('body_ru', contentTrans['ru']);
                }

                // Insert into EN fields
                if (titleTrans['en']) {
                    setFieldValue('title_en', titleTrans['en']);
                }
                if (contentTrans['en']) {
                    setFieldValue('content_en', contentTrans['en']) ||
                    setFieldValue('description_en', contentTrans['en']) ||
                    setFieldValue('body_en', contentTrans['en']);
                }

                // Insert into ZH fields
                const zhText = titleTrans['zh-cn'] || titleTrans['zh'];
                if (zhText) {
                    setFieldValue('title_zh', zhText) || setFieldValue('title_zh_cn', zhText);
                }
                const zhContent = contentTrans['zh-cn'] || contentTrans['zh'];
                if (zhContent) {
                    setFieldValue('content_zh', zhContent) ||
                    setFieldValue('content_zh_cn', zhContent) ||
                    setFieldValue('description_zh', zhContent) ||
                    setFieldValue('body_zh', zhContent);
                }

                showStatus("🎉 Ajoyib! Rus, ingliz va xitoy tillari avtomatik to'ldirildi. Tekshirib 'Saqlash' tugmasini bosing.", "success", 7000);
            } catch (err) {
                console.error(err);
                showStatus("⚠️ Tarjima qilishda xatolik yuz berdi: " + err.message, "error", 6000);
            } finally {
                btnTranslate.disabled = false;
                btnTranslate.innerHTML = '<span class="btn-icon">🌐</span> Tillarga Avto-Tarjima (RU, EN, ZH)';
            }
        });
    }

    // =========================================================================
    // 3. ACTION: Language Tabs Filtering
    // =========================================================================
    const tabButtons = document.querySelectorAll('.lang-tab');
    if (tabButtons.length > 0) {
        tabButtons.forEach(btn => {
            btn.addEventListener('click', function () {
                tabButtons.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const lang = this.getAttribute('data-lang');
                const formRows = document.querySelectorAll('.form-row, .fieldBox, .unfold-field');

                formRows.forEach(row => {
                    if (lang === 'all') {
                        row.style.display = '';
                        return;
                    }

                    // Check if row has class or input matching current language
                    const input = row.querySelector('input, textarea, select');
                    const name = input ? input.getAttribute('name') : '';
                    const isLangMatch = name && (name.endsWith(`_${lang}`) || (lang === 'uz' && !name.includes('_')));

                    // Keep general fields visible (like image, category, date, is_published)
                    const isSystemField = name && ['image', 'photo', 'file', 'category', 'status', 'created_at', 'date', 'is_active', 'is_published'].some(s => name.includes(s));

                    if (isLangMatch || isSystemField) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });
        });
    }

    // =========================================================================
    // 4. ACTION: Telegram & Google Preview Modal
    // =========================================================================
    const btnPreview = document.getElementById('btn-seo-preview');
    const modal = document.getElementById('buxdu-preview-modal');
    const btnClose = document.getElementById('btn-close-preview');

    if (btnPreview && modal) {
        btnPreview.addEventListener('click', function () {
            const title = getFieldValue('title_uz') || getFieldValue('title') || 'Sarlavha kiritilmagan';
            const rawContent = getFieldValue('content_uz') || getFieldValue('content') || getFieldValue('description') || 'Matn kiritilmagan';
            
            // Strip HTML tags for clean text preview
            const cleanText = rawContent.replace(/<[^>]*>/g, '').trim();

            document.getElementById('tg-preview-title').textContent = title;
            document.getElementById('tg-preview-body').textContent = cleanText.substring(0, 280) + (cleanText.length > 280 ? '...' : '');

            document.getElementById('google-preview-title').textContent = title + ' - Buxoro davlat universiteti';
            document.getElementById('google-preview-desc').textContent = cleanText.substring(0, 160) + '...';

            modal.classList.remove('hidden');
        });

        if (btnClose) {
            btnClose.addEventListener('click', function () {
                modal.classList.add('hidden');
            });
        }

        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });
    }
});
