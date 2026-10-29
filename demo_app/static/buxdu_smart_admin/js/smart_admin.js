/**
 * BuxDU Smart Admin Frontend Controller (Django Admin Integration)
 * ================================================================
 * Integrates directly into Django Admin (change_form.html or ModelAdmin.Media)
 * Features:
 * 1. ⚡ One-click 2026 Uzbek Latin reform transliteration (Ö, Ğ, Ş, Ç)
 * 2. 🌐 One-click Automated multi-language translation (RU, EN, ZH)
 * 3. 🎯 Full CKEditor 4 / 5 and django-modeltranslation support
 */

document.addEventListener('DOMContentLoaded', function () {
    console.log("🚀 [BuxDU Smart Admin] Django Admin Paneli integratsiyasi ishga tushdi!");

    // =========================================================================
    // 1. INJECT ACTION BAR IF NOT PRESENT VIA TEMPLATE
    // =========================================================================
    function ensureActionBar() {
        if (document.getElementById('buxdu-smart-bar-injected')) return;

        const targetContainer = document.querySelector('#content-main form') || document.querySelector('#content');
        if (!targetContainer) return;

        const bar = document.createElement('div');
        bar.id = 'buxdu-smart-bar-injected';
        bar.className = 'buxdu-smart-bar';
        bar.innerHTML = `
            <div style="
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #ffffff;
                padding: 12px 18px;
                border-radius: 12px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: space-between;
                gap: 12px;
                border: 1px solid #334155;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            ">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="display: inline-block; width: 10px; height: 10px; background: #10b981; border-radius: 50%; box-shadow: 0 0 8px #10b981;"></span>
                    <strong style="color: #38bdf8; font-size: 14px;">BuxDU Smart Assistant:</strong>
                    <span style="font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.3);">2026 Alifbo & AI Tarjima</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                    <button type="button" id="btn-transliterate-new" style="
                        background: #059669; color: #ffffff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(5, 150, 105, 0.3); transition: all 0.2s;
                    ">
                        ⚡ Yangi Alifboga O'girish (Ö, Ğ, Ş, Ç)
                    </button>
                    <button type="button" id="btn-auto-translate" style="
                        background: #0284c7; color: #ffffff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3); transition: all 0.2s;
                    ">
                        🌐 Tillarga Avto-Tarjima (RU, EN, ZH)
                    </button>
                    <button type="button" id="btn-master-all" style="
                        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: #ffffff; border: none; border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4); transition: all 0.2s;
                    ">
                        🚀 1-Bosishda Hammasi
                    </button>
                </div>
            </div>
            <div id="buxdu-status-message" style="display: none; padding: 10px 14px; border-radius: 8px; margin-bottom: 15px; font-size: 12px; font-weight: 600;"></div>
        `;

        targetContainer.insertBefore(bar, targetContainer.firstChild);
    }

    ensureActionBar();

    // =========================================================================
    // 2. STATUS HELPER
    // =========================================================================
    function showStatus(message, type = 'info', duration = 5000) {
        const statusBox = document.getElementById('buxdu-status-message');
        if (!statusBox) return;

        statusBox.style.display = 'block';
        statusBox.innerHTML = message;

        if (type === 'success') {
            statusBox.style.background = 'rgba(16, 185, 129, 0.15)';
            statusBox.style.color = '#10b981';
            statusBox.style.border = '1px solid rgba(16, 185, 129, 0.3)';
        } else if (type === 'error') {
            statusBox.style.background = 'rgba(239, 68, 68, 0.15)';
            statusBox.style.color = '#ef4444';
            statusBox.style.border = '1px solid rgba(239, 68, 68, 0.3)';
        } else {
            statusBox.style.background = 'rgba(56, 189, 248, 0.15)';
            statusBox.style.color = '#38bdf8';
            statusBox.style.border = '1px solid rgba(56, 189, 248, 0.3)';
        }

        if (duration > 0) {
            setTimeout(() => {
                statusBox.style.display = 'none';
            }, duration);
        }
    }

    // =========================================================================
    // 3. FIELD VALUE GETTER & SETTER (CKEDITOR & TEXTAREA COMPATIBLE)
    // =========================================================================
    function getFieldValue(fieldId) {
        // 1. Try CKEditor 4/5
        if (window.CKEDITOR && window.CKEDITOR.instances) {
            if (window.CKEDITOR.instances[fieldId]) {
                return window.CKEDITOR.instances[fieldId].getData();
            }
            if (window.CKEDITOR.instances[`id_${fieldId}`]) {
                return window.CKEDITOR.instances[`id_${fieldId}`].getData();
            }
        }
        // 2. Standard DOM element
        const el = document.getElementById(fieldId) || document.getElementById(`id_${fieldId}`) || document.querySelector(`[name="${fieldId}"]`);
        return el ? el.value : '';
    }

    function setFieldValue(fieldId, value) {
        let set = false;

        // 1. Set in CKEditor
        if (window.CKEDITOR && window.CKEDITOR.instances) {
            if (window.CKEDITOR.instances[fieldId]) {
                window.CKEDITOR.instances[fieldId].setData(value);
                set = true;
            } else if (window.CKEDITOR.instances[`id_${fieldId}`]) {
                window.CKEDITOR.instances[`id_${fieldId}`].setData(value);
                set = true;
            }
        }

        // 2. Set in DOM
        const el = document.getElementById(fieldId) || document.getElementById(`id_${fieldId}`) || document.querySelector(`[name="${fieldId}"]`);
        if (el) {
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            set = true;
        }

        return set;
    }

    // Auto-discover all Uzbek fields on the page (matching BuxDU models: sarlavha, text, fio, mehnat, etc.)
    function discoverUzbekFields() {
        const found = [];

        // Any field ending in _uz
        document.querySelectorAll('input[id$="_uz"], textarea[id$="_uz"], input[name$="_uz"], textarea[name$="_uz"]').forEach(el => {
            const id = el.id || el.name;
            if (!found.includes(id)) found.push(id);
        });

        // Common default field names if not using _uz suffix
        const commonDefaults = ['sarlavha', 'title', 'fio', 'nomi', 'text', 'content', 'mehnat_faoliyati', 'biografiya', 'annotatsiya'];
        commonDefaults.forEach(name => {
            const el = document.getElementById(`id_${name}`) || document.querySelector(`[name="${name}"]`);
            if (el && !found.includes(el.id || el.name)) {
                found.push(el.id || el.name);
            }
        });

        return found;
    }

    // =========================================================================
    // 4. TRANSLITERATION ENGINE (2026 Uzbek Reform: Ö, Ğ, Ş, Ç)
    // =========================================================================
    const APOS = "['`ʼʻ’‘´\\u02bb\\u02bc\\u2018\\u2019]";

    function transliterateToNew(text) {
        if (!text || typeof text !== 'string') return text;

        // If contains HTML tags, protect them
        if (/<[a-z][\s\S]*>/i.test(text)) {
            return text.replace(/(>|^)([^<]+)(<|$)/g, (match, prefix, content, suffix) => {
                return prefix + convertPlain(content) + suffix;
            });
        }
        return convertPlain(text);
    }

    function convertPlain(str) {
        if (!str) return str;
        let res = str;

        // Protect s'h (e.g. Is'hoq, mus'haf)
        res = res.replace(new RegExp(`([Ss])${APOS}([Hh])`, 'g'), '$1__SEP__$2');

        // G', g' -> Ğ, ğ
        res = res.replace(new RegExp(`G${APOS}`, 'g'), 'Ğ');
        res = res.replace(new RegExp(`g${APOS}`, 'g'), 'ğ');

        // O', o' -> Ö, ö
        res = res.replace(new RegExp(`O${APOS}`, 'g'), 'Ö');
        res = res.replace(new RegExp(`o${APOS}`, 'g'), 'ö');

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

    // =========================================================================
    // 5. TRANSLATION ENGINE (Backend API with Direct Fallback)
    // =========================================================================
    async function translateText(text, targetLang) {
        if (!text || !text.trim()) return "";

        // 1. Try internal Django endpoint first
        try {
            const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
            const res = await fetch('/admin/buxdu_smart_admin/api/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf ? csrf.value : ''
                },
                body: JSON.stringify({
                    text: text,
                    source_lang: 'uz',
                    target_langs: [targetLang]
                })
            });
            if (res.ok) {
                const data = await res.json();
                if (data.success && data.translations && data.translations[targetLang]) {
                    return data.translations[targetLang];
                }
            }
        } catch (e) {
            // Fallback to client-side Google API
        }

        // 2. Direct client-side Google Translate API (Always works without backend setup!)
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
    // 6. EVENT LISTENERS
    // =========================================================================

    // BUTTON 1: Transliterate
    const btnTranslit = document.getElementById('btn-transliterate-new');
    if (btnTranslit) {
        btnTranslit.addEventListener('click', function () {
            const uzFields = discoverUzbekFields();
            let count = 0;

            uzFields.forEach(fieldId => {
                const val = getFieldValue(fieldId);
                if (val && val.trim()) {
                    const converted = transliterateToNew(val);
                    if (converted !== val) {
                        setFieldValue(fieldId, converted);
                        count++;
                    }
                }
            });

            if (count > 0) {
                showStatus(`✅ Muvaffaqiyatli: ${count} ta maydondagi barcha matnlar yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi!`, "success");
            } else {
                showStatus("ℹ️ Barcha matnlar allaqachon to'g'ri yangi alifboda!", "info");
            }
        });
    }

    // BUTTON 2: Auto-Translate to RU, EN, ZH
    const btnTranslate = document.getElementById('btn-auto-translate');
    if (btnTranslate) {
        btnTranslate.addEventListener('click', async function () {
            const btn = this;
            btn.disabled = true;
            btn.innerHTML = "⏳ Tarjima qilinmoqda...";
            showStatus("🌐 Rus, ingliz va xitoy tillariga professional tarjima qilinmoqda, kuting...", "info", 0);

            try {
                const uzFields = discoverUzbekFields();
                let translatedFields = 0;

                for (const fieldId of uzFields) {
                    const uzText = getFieldValue(fieldId);
                    if (!uzText || !uzText.trim()) continue;

                    // Compute target field IDs
                    // e.g., id_sarlavha_uz -> id_sarlavha_ru, id_sarlavha_en, id_sarlavha_zh
                    let baseName = fieldId.replace(/^id_/, '').replace(/_uz$/, '');

                    const [ruText, enText, zhText] = await Promise.all([
                        translateText(uzText, 'ru'),
                        translateText(uzText, 'en'),
                        translateText(uzText, 'zh-CN')
                    ]);

                    if (setFieldValue(`${baseName}_ru`, ruText) || setFieldValue(`id_${baseName}_ru`, ruText)) translatedFields++;
                    if (setFieldValue(`${baseName}_en`, enText) || setFieldValue(`id_${baseName}_en`, enText)) translatedFields++;
                    if (setFieldValue(`${baseName}_zh`, zhText) || setFieldValue(`id_${baseName}_zh`, zhText)) translatedFields++;
                }

                if (translatedFields > 0) {
                    showStatus(`🎉 Muvaffaqiyatli! Barcha tillar (Русский, English, 中文) avtomatik to'ldirildi. Saqlash tugmasini bosing!`, "success");
                } else {
                    showStatus("⚠️ O'zbekcha maydonda matn topilmadi. Avval o'zbekcha kiriting!", "error");
                }
            } catch (err) {
                showStatus("❌ Tarjimada xatolik: " + err.message, "error");
            } finally {
                btn.disabled = false;
                btn.innerHTML = "🌐 Tillarga Avto-Tarjima (RU, EN, ZH)";
            }
        });
    }

    // BUTTON 3: 1-Click Master
    const btnMaster = document.getElementById('btn-master-all');
    if (btnMaster) {
        btnMaster.addEventListener('click', async function () {
            if (btnTranslit) btnTranslit.click();
            if (btnTranslate) await btnTranslate.click();
        });
    }
});
