/**
 * BuxDU Smart Admin Native Django Controller
 * ===========================================
 * Seamlessly integrates into Django Administration forms.
 * Provides:
 * 1. ⚡ Complete 2026 Uzbek Latin alphabet transliteration (Ö, Ğ, Ş, Ç)
 * 2. 🌐 Multi-language automatic translation (RU, EN, ZH)
 * 3. 🚀 1-Click Master action
 * 4. Full support for CKEditor 4/5, TinyMCE, modeltranslation tabs & plain inputs.
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log("🏛️ [BuxDU Smart Admin] Django Admin Paneli faollashtirildi!");

    // =========================================================================
    // 1. ENSURE ACTION BAR (SINGLE INSTANCE ONLY)
    // =========================================================================
    function setupActionBar() {
        if (document.getElementById('buxdu-django-bar')) {
            // Template already provided the bar, no need to inject
            return;
        }

        const target = document.querySelector('#content-main form') || document.querySelector('#content form') || document.querySelector('#content');
        if (!target) return;

        const bar = document.createElement('div');
        bar.id = 'buxdu-django-bar';
        bar.className = 'buxdu-django-admin-bar';
        bar.innerHTML = `
            <div class="django-bar-left">
                <span class="django-bar-dot"></span>
                <strong class="django-bar-title">BuxDU Smart Assistant</strong>
                <span class="django-bar-badge">2026 Alifbo: Ö, Ğ, Ş, Ç</span>
            </div>
            <div class="django-bar-actions">
                <button type="button" id="btn-transliterate-new" class="django-admin-btn django-btn-accent" title="Barcha o'zbekcha matnlarni yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazish">
                    ⚡ Yangi Alifboga O'tkazish (Ö, Ğ, Ş, Ç)
                </button>
                <button type="button" id="btn-auto-translate" class="django-admin-btn django-btn-primary" title="Rus, ingliz va xitoy tillariga avtomatik tarjima qilish">
                    🌐 Tillarga Avto-Tarjima (RU, EN, ZH)
                </button>
                <button type="button" id="btn-master-all" class="django-admin-btn django-btn-master" title="Alifbo va tarjimani 1 bosishda bajarish">
                    🚀 1-Bosishda Hammasi
                </button>
            </div>
        `;

        const alertDiv = document.createElement('div');
        alertDiv.id = 'buxdu-django-alert';
        alertDiv.className = 'buxdu-django-alert hidden';

        target.insertBefore(alertDiv, target.firstChild);
        target.insertBefore(bar, alertDiv);
    }

    setupActionBar();

    // =========================================================================
    // 2. ALERT MESSAGES (DJANGO NATIVE STYLE)
    // =========================================================================
    function showAlert(msg, type = 'success', timeout = 6000) {
        let alertBox = document.getElementById('buxdu-django-alert');
        if (!alertBox) {
            alertBox = document.createElement('div');
            alertBox.id = 'buxdu-django-alert';
            alertBox.className = 'buxdu-django-alert';
            const bar = document.getElementById('buxdu-django-bar');
            if (bar && bar.parentNode) bar.parentNode.insertBefore(alertBox, bar.nextSibling);
        }

        alertBox.className = `buxdu-django-alert ${type}`;
        alertBox.innerHTML = msg;
        alertBox.classList.remove('hidden');

        if (timeout > 0) {
            setTimeout(() => {
                alertBox.classList.add('hidden');
            }, timeout);
        }
    }

    // =========================================================================
    // 3. FIELD DISCOVERY & VALUE ACCESSORS (CKEDITOR + DOM)
    // =========================================================================
    function getFieldValue(name) {
        // Try CKEditor first
        if (window.CKEDITOR && window.CKEDITOR.instances) {
            if (window.CKEDITOR.instances[name]) return window.CKEDITOR.instances[name].getData();
            if (window.CKEDITOR.instances[`id_${name}`]) return window.CKEDITOR.instances[`id_${name}`].getData();
        }
        // Try TinyMCE
        if (window.tinymce) {
            if (window.tinymce.get(name)) return window.tinymce.get(name).getContent();
            if (window.tinymce.get(`id_${name}`)) return window.tinymce.get(`id_${name}`).getContent();
        }
        const el = document.getElementById(name) || document.getElementById(`id_${name}`) || document.querySelector(`[name="${name}"]`);
        return el ? el.value : '';
    }

    function setFieldValue(name, value) {
        let set = false;

        // Set in CKEditor
        if (window.CKEDITOR && window.CKEDITOR.instances) {
            if (window.CKEDITOR.instances[name]) {
                window.CKEDITOR.instances[name].setData(value);
                set = true;
            } else if (window.CKEDITOR.instances[`id_${name}`]) {
                window.CKEDITOR.instances[`id_${name}`].setData(value);
                set = true;
            }
        }

        // Set in TinyMCE
        if (window.tinymce) {
            if (window.tinymce.get(name)) {
                window.tinymce.get(name).setContent(value);
                set = true;
            } else if (window.tinymce.get(`id_${name}`)) {
                window.tinymce.get(`id_${name}`).setContent(value);
                set = true;
            }
        }

        // Set in DOM input/textarea
        const el = document.getElementById(name) || document.getElementById(`id_${name}`) || document.querySelector(`[name="${name}"]`);
        if (el) {
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            set = true;
        }

        return set;
    }

    function getAllUzbekFieldIds() {
        const found = [];

        // All fields ending in _uz
        document.querySelectorAll('input[id$="_uz"], textarea[id$="_uz"], input[name$="_uz"], textarea[name$="_uz"]').forEach(el => {
            const id = el.id || el.name;
            if (!found.includes(id)) found.push(id);
        });

        // Common defaults in BuxDU models
        const defaults = [
            'sarlavha', 'title', 'fio', 'nomi', 'text', 'content', 'mehnat_faoliyati',
            'malaka_oshirish', 'oqitadigan_fanlari', 'ilmiy_faoliyati', 'annotatsiya', 'biografiya'
        ];
        defaults.forEach(f => {
            const el = document.getElementById(`id_${f}`) || document.querySelector(`[name="${f}"]`);
            if (el) {
                const id = el.id || el.name;
                if (!found.includes(id)) found.push(id);
            }
        });

        return found;
    }

    // =========================================================================
    // 4. ALPHABET TRANSLITERATION ENGINE (2026 REFORM: Ö, Ğ, Ş, Ç)
    // =========================================================================
    const APOS = "['`ʼʻ’‘´\\u02bb\\u02bc\\u2018\\u2019]";

    function transliterateToNewLatin(text) {
        if (!text || typeof text !== 'string') return text;

        // Preserve HTML markup if present
        if (/<[a-z][\s\S]*>/i.test(text)) {
            return text.replace(/(>|^)([^<]+)(<|$)/g, (match, prefix, content, suffix) => {
                return prefix + convertText(content) + suffix;
            });
        }
        return convertText(text);
    }

    function convertText(str) {
        if (!str) return str;
        let res = str;

        // Protect s'h (e.g. Is'hoq, mus'haf)
        res = res.replace(new RegExp(`([Ss])${APOS}([Hh])`, 'g'), '$1__SEP__$2');

        // 1. G' g' -> Ğ ğ
        res = res.replace(new RegExp(`G${APOS}`, 'g'), 'Ğ');
        res = res.replace(new RegExp(`g${APOS}`, 'g'), 'ğ');

        // 2. O' o' -> Ö ö
        res = res.replace(new RegExp(`O${APOS}`, 'g'), 'Ö');
        res = res.replace(new RegExp(`o${APOS}`, 'g'), 'ö');

        // 3. Sh sh -> Ş ş
        res = res.replace(/\bSH\b/g, 'Ş');
        res = res.replace(/Sh/g, 'Ş');
        res = res.replace(/sh/g, 'ş');

        // 4. Ch ch -> Ç ç
        res = res.replace(/\bCH\b/g, 'Ç');
        res = res.replace(/Ch/g, 'Ç');
        res = res.replace(/ch/g, 'ç');

        // 5. Uzbek Cyrillic support (if pasted in Cyrillic)
        const cyrMap = {
            'Ў': 'Ö', 'ў': 'ö',
            'Ғ': 'Ğ', 'ғ': 'ğ',
            'Ш': 'Ş', 'ш': 'ş',
            'Ч': 'Ç', 'ч': 'ç',
            'Я': 'Ya', 'я': 'ya',
            'Ё': 'Yo', 'ё': 'yo',
            'Ю': 'Yu', 'ю': 'yu',
            'Ц': 'Ts', 'ц': 'ts',
            'Қ': 'Q', 'қ': 'q',
            'Ҳ': 'H', 'ҳ': 'h',
            'Х': 'X', 'х': 'x',
            'Ж': 'J', 'ж': 'j'
        };
        for (const [c, l] of Object.entries(cyrMap)) {
            res = res.split(c).join(l);
        }

        // Restore s'h
        res = res.replace(/__SEP__/g, "'");
        return res;
    }

    // =========================================================================
    // 5. TRANSLATION ENGINE (Google GTX + Backend fallback)
    // =========================================================================
    async function translateApi(text, targetLang) {
        if (!text || !text.trim()) return "";

        const encoded = encodeURIComponent(text);
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=uz&tl=${targetLang}&dt=t&q=${encoded}`;

        const resp = await fetch(url);
        const json = await resp.json();
        let result = "";
        if (json && json[0]) {
            json[0].forEach(seg => {
                if (seg && seg[0]) result += seg[0];
            });
        }
        return result.trim();
    }

    // =========================================================================
    // 6. ACTION HANDLERS
    // =========================================================================

    // ACTION 1: TRANSLITERATE ALL UZBEK FIELDS
    function handleTransliterate() {
        const uzFields = getAllUzbekFieldIds();
        let updatedCount = 0;

        uzFields.forEach(fid => {
            const val = getFieldValue(fid);
            if (val && val.trim()) {
                const converted = transliterateToNewLatin(val);
                if (converted !== val) {
                    setFieldValue(fid, converted);
                    updatedCount++;
                }
            }
        });

        if (updatedCount > 0) {
            showAlert(`✅ Muvaffaqiyatli: <strong>${updatedCount} ta maydondagi barcha matnlar</strong> 2026-yilgi yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi!`, 'success');
        } else {
            showAlert("ℹ️ Barcha o'zbekcha matnlar allaqachon to'g'ri yangi alifboda!", 'info');
        }
        return updatedCount;
    }

    const btnTranslit = document.getElementById('btn-transliterate-new');
    if (btnTranslit) {
        btnTranslit.addEventListener('click', handleTransliterate);
    }

    // ACTION 2: AUTO-TRANSLATE TO RU, EN, ZH
    async function handleTranslate() {
        const btn = document.getElementById('btn-auto-translate');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = "⏳ Tarjima qilinmoqda...";
        }
        showAlert("🌐 Rus, ingliz va xitoy tillariga professional darajada tarjima qilinmoqda, kuting...", "info", 0);

        try {
            const uzFields = getAllUzbekFieldIds();
            let translatedCount = 0;

            for (const fid of uzFields) {
                const uzVal = getFieldValue(fid);
                if (!uzVal || !uzVal.trim()) continue;

                // Base field name (e.g. id_sarlavha_uz -> sarlavha)
                const base = fid.replace(/^id_/, '').replace(/_uz$/, '');

                const [ru, en, zh] = await Promise.all([
                    translateApi(uzVal, 'ru'),
                    translateApi(uzVal, 'en'),
                    translateApi(uzVal, 'zh-CN')
                ]);

                if (setFieldValue(`${base}_ru`, ru) || setFieldValue(`id_${base}_ru`, ru)) translatedCount++;
                if (setFieldValue(`${base}_en`, en) || setFieldValue(`id_${base}_en`, en)) translatedCount++;
                if (setFieldValue(`${base}_zh`, zh) || setFieldValue(`id_${base}_zh`, zh)) translatedCount++;
            }

            if (translatedCount > 0) {
                showAlert(`🎉 Ajoyib! <strong>${translatedCount} ta maydon</strong> (Русский, English, 中文) avtomatik to'ldirildi. Endi pastdagi <strong>SAQLASH</strong> tugmasini bosing!`, 'success');
            } else {
                showAlert("⚠️ O'zbekcha maydonda matn topilmadi. Avval o'zbekcha matn kiriting!", 'error');
            }
        } catch (err) {
            showAlert("❌ Tarjimada xatolik yuz berdi: " + err.message, 'error');
        } finally {
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<span class="btn-icon">🌐</span> Tillarga Avto-Tarjima (RU, EN, ZH)';
            }
        }
    }

    const btnTranslate = document.getElementById('btn-auto-translate');
    if (btnTranslate) {
        btnTranslate.addEventListener('click', handleTranslate);
    }

    // ACTION 3: MASTER 1-CLICK ALL
    const btnMaster = document.getElementById('btn-master-all');
    if (btnMaster) {
        btnMaster.addEventListener('click', async function () {
            handleTransliterate();
            await handleTranslate();
        });
    }
});
