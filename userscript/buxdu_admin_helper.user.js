// ==UserScript==
// @name         BuxDU Admin Smart Helper (2026 Alifbo & Avto-Tarjima)
// @namespace    http://tampermonkey.net/
// @version      2.0.0
// @description  Buxoro davlat universiteti (buxdu.uz/admin/) uchun yangi o'zbek lotin alifbosi (Ö, Ğ, Ş, Ç) va rus, ingliz, xitoy tillariga avtomatik professional tarjima
// @author       Senior AI Engineering Team
// @match        https://buxdu.uz/admin/*
// @match        http://buxdu.uz/admin/*
// @match        https://*.buxdu.uz/admin/*
// @match        http://127.0.0.1:8000/admin/*
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// @connect      translate.googleapis.com
// @run-at       document-end
// ==/UserScript==

(function () {
    'use strict';

    console.log("🚀 [BuxDU Admin Smart Helper v2.0] yuklandi!");

    // =========================================================================
    // 1. TRANSLITERATION ENGINE (2026 Reform: Ö, Ğ, Ş, Ç)
    // =========================================================================
    const APOS = "['`ʼʻ’‘´\\u02bb\\u02bc\\u2018\\u2019]";

    function transliterateText(text) {
        if (!text || typeof text !== 'string') return text;

        // If text contains HTML tags, only transliterate the text nodes
        if (/<[a-z][\s\S]*>/i.test(text)) {
            return text.replace(/(>|^)([^<]+)(<|$)/g, (match, prefix, content, suffix) => {
                return prefix + convertPlainUzbek(content) + suffix;
            });
        }
        return convertPlainUzbek(text);
    }

    function convertPlainUzbek(str) {
        if (!str) return str;
        let res = str;

        // Protect s'h (e.g., Is'hoq, mus'haf)
        res = res.replace(new RegExp(`([Ss])${APOS}([Hh])`, 'g'), '$1__PROTECTED_APOS__$2');

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

        // Restore s'h
        res = res.replace(/__PROTECTED_APOS__/g, "'");

        return res;
    }

    // =========================================================================
    // 2. MULTI-LANGUAGE TRANSLATOR (GTX API)
    // =========================================================================
    function translateApi(text, targetLang) {
        return new Promise((resolve, reject) => {
            if (!text || !text.trim()) {
                resolve("");
                return;
            }

            // Protect HTML tags if present
            const tags = [];
            let cleanText = text;
            if (/<[a-z][\s\S]*>/i.test(text)) {
                cleanText = text.replace(/<[^>]+>/g, match => {
                    tags.push(match);
                    return ` ___TAG_${tags.length - 1}___ `;
                });
            }

            const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=uz&tl=${targetLang}&dt=t&q=${encodeURIComponent(cleanText)}`;

            GM_xmlhttpRequest({
                method: "GET",
                url: url,
                onload: function (resp) {
                    try {
                        const data = JSON.parse(resp.responseText);
                        let result = "";
                        if (data && data[0]) {
                            data[0].forEach(seg => {
                                if (seg && seg[0]) result += seg[0];
                            });
                        }
                        // Restore HTML tags
                        tags.forEach((t, i) => {
                            result = result.replace(new RegExp(`___TAG_${i}___|___ TAG_${i} ___|___TAG_ ${i}___`, 'gi'), t);
                        });
                        resolve(result.trim());
                    } catch (e) {
                        reject(e);
                    }
                },
                onerror: function (err) {
                    reject(err);
                }
            });
        });
    }

    // =========================================================================
    // 3. DOM & CKEDITOR CONTROLLER
    // =========================================================================
    function getFieldValue(fieldId) {
        // Try CKEditor first
        if (window.CKEDITOR && window.CKEDITOR.instances && window.CKEDITOR.instances[fieldId]) {
            return window.CKEDITOR.instances[fieldId].getData();
        }
        const el = document.getElementById(fieldId) || document.querySelector(`[name="${fieldId}"]`);
        return el ? el.value : '';
    }

    function setFieldValue(fieldId, value) {
        let updated = false;

        // Try CKEditor
        if (window.CKEDITOR && window.CKEDITOR.instances && window.CKEDITOR.instances[fieldId]) {
            window.CKEDITOR.instances[fieldId].setData(value);
            updated = true;
        }

        const el = document.getElementById(fieldId) || document.querySelector(`[name="${fieldId}"]`);
        if (el) {
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            updated = true;
        }

        return updated;
    }

    // Discover all Uzbek translation fields on the current Django admin form
    function findUzbekFields() {
        const found = [];
        // Matches inputs, textareas with _uz suffix
        const elements = document.querySelectorAll('input[id$="_uz"], textarea[id$="_uz"], [id$="_uz_ifr"]');
        elements.forEach(el => {
            const rawId = el.id.replace('_ifr', '');
            if (!found.includes(rawId)) {
                found.push(rawId);
            }
        });

        // Also check by name
        document.querySelectorAll('input[name$="_uz"], textarea[name$="_uz"]').forEach(el => {
            const rawId = el.id || el.name;
            if (!found.includes(rawId)) {
                found.push(rawId);
            }
        });

        return found;
    }

    // =========================================================================
    // 4. FLOATING SMART DASHBOARD WIDGET
    // =========================================================================
    function injectUI() {
        if (document.getElementById('buxdu-senior-helper')) return;

        // Styles
        const css = `
            #buxdu-senior-helper {
                position: fixed;
                bottom: 20px;
                right: 25px;
                z-index: 9999999;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: #ffffff;
                padding: 12px 16px;
                border-radius: 16px;
                box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                display: flex;
                flex-direction: column;
                gap: 10px;
                min-width: 330px;
                transition: all 0.3s ease;
            }
            .buxdu-header {
                display: flex;
                align-items: center;
                justify-content: space-between;
                font-size: 13px;
                font-weight: 700;
                color: #38bdf8;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                padding-bottom: 8px;
            }
            .buxdu-btn-group {
                display: flex;
                flex-direction: column;
                gap: 8px;
            }
            .buxdu-btn {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                text-decoration: none;
            }
            .buxdu-btn:hover {
                transform: translateY(-1px);
                filter: brightness(1.1);
            }
            .buxdu-btn:active {
                transform: translateY(0);
            }
            .buxdu-btn-all {
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                color: #ffffff;
                box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            }
            .buxdu-btn-translit {
                background: #059669;
                color: #ffffff;
            }
            .buxdu-btn-trans {
                background: #0284c7;
                color: #ffffff;
            }
            .buxdu-toast {
                font-size: 11px;
                padding: 6px 10px;
                border-radius: 8px;
                background: rgba(16, 185, 129, 0.2);
                color: #34d399;
                border: 1px solid rgba(16, 185, 129, 0.3);
                display: none;
                line-height: 1.4;
            }
        `;

        if (typeof GM_addStyle !== 'undefined') {
            GM_addStyle(css);
        } else {
            const style = document.createElement('style');
            style.textContent = css;
            document.head.appendChild(style);
        }

        const container = document.createElement('div');
        container.id = 'buxdu-senior-helper';
        container.innerHTML = `
            <div class="buxdu-header">
                <span>🏛️ BuxDU Admin Smart AI</span>
                <span style="font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 7px; border-radius: 10px;">v2.0 Pro</span>
            </div>
            <div class="buxdu-btn-group">
                <button type="button" class="buxdu-btn buxdu-btn-all" id="btn-buxdu-all">
                    🚀 1-BOSISHDA HAMMASI (Alifbo + 3 Tilga Tarjima)
                </button>
                <div style="display: flex; gap: 8px;">
                    <button type="button" class="buxdu-btn buxdu-btn-translit" id="btn-buxdu-translit" style="flex: 1;">
                        ⚡ Alifbo (Ö, Ğ, Ş, Ç)
                    </button>
                    <button type="button" class="buxdu-btn buxdu-btn-trans" id="btn-buxdu-translate" style="flex: 1;">
                        🌐 3 Tilda Tarjima
                    </button>
                </div>
            </div>
            <div id="buxdu-toast" class="buxdu-toast"></div>
        `;

        document.body.appendChild(container);

        // Toast Helper
        function showToast(msg, isSuccess = true) {
            const toast = document.getElementById('buxdu-toast');
            toast.style.display = 'block';
            toast.innerHTML = msg;
            toast.style.color = isSuccess ? '#34d399' : '#f87171';
            toast.style.borderColor = isSuccess ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)';
            toast.style.background = isSuccess ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 6000);
        }

        // =====================================================================
        // ACTION 1: TRANSLITERATE ALL UZBEK FIELDS
        // =====================================================================
        async function runTransliteration() {
            const uzFields = findUzbekFields();
            if (uzFields.length === 0) {
                // Fallback check standard field IDs without _uz
                const fallbackFields = ['id_sarlavha', 'id_title', 'id_text', 'id_content', 'id_fio', 'id_nomi'];
                fallbackFields.forEach(f => {
                    const val = getFieldValue(f);
                    if (val) uzFields.push(f);
                });
            }

            let modified = 0;
            uzFields.forEach(fid => {
                const current = getFieldValue(fid);
                if (current && current.trim()) {
                    const converted = transliterateText(current);
                    if (converted !== current) {
                        setFieldValue(fid, converted);
                        modified++;
                    }
                }
            });

            return modified;
        }

        document.getElementById('btn-buxdu-translit').addEventListener('click', async () => {
            const count = await runTransliteration();
            showToast(count > 0 
                ? `✅ ${count} ta maydon yangi lotin alifbosiga (Ö, Ğ, Ş, Ç) o'tkazildi!` 
                : "✅ Barcha matnlar allaqachon to'g'ri yangi alifboda!");
        });

        // =====================================================================
        // ACTION 2: AUTO-TRANSLATE TO RU, EN, ZH
        // =====================================================================
        async function runTranslation() {
            const uzFields = findUzbekFields();
            let translatedCount = 0;

            for (const fid of uzFields) {
                const val = getFieldValue(fid);
                if (!val || !val.trim()) continue;

                const baseName = fid.replace(/_uz$/, '');
                const ruId = `${baseName}_ru`;
                const enId = `${baseName}_en`;
                const zhId = `${baseName}_zh`;

                const [ruText, enText, zhText] = await Promise.all([
                    translateApi(val, 'ru'),
                    translateApi(val, 'en'),
                    translateApi(val, 'zh-CN')
                ]);

                if (setFieldValue(ruId, ruText)) translatedCount++;
                if (setFieldValue(enId, enText)) translatedCount++;
                if (setFieldValue(zhId, zhText)) translatedCount++;
            }

            return translatedCount;
        }

        document.getElementById('btn-buxdu-translate').addEventListener('click', async function () {
            const btn = this;
            btn.disabled = true;
            btn.textContent = "⏳ Tarjima...";
            showToast("⏳ Rus, ingliz va xitoy tillariga tarjima qilinmoqda...");

            try {
                const count = await runTranslation();
                if (count > 0) {
                    showToast(`🎉 Muvaffaqiyatli! ${count} ta til maydonlari (RU, EN, ZH) to'ldirildi!`);
                } else {
                    showToast("⚠️ O'zbekcha maydonda matn topilmadi. Avval o'zbekcha kiriting!", false);
                }
            } catch (err) {
                showToast("❌ Tarjimada xatolik: " + err.message, false);
            } finally {
                btn.disabled = false;
                btn.textContent = "🌐 3 Tilda Tarjima";
            }
        });

        // =====================================================================
        // ACTION 3: MASTER 1-CLICK ALL
        // =====================================================================
        document.getElementById('btn-buxdu-all').addEventListener('click', async function () {
            const btn = this;
            btn.disabled = true;
            btn.textContent = "⏳ Bajarilmoqda...";
            showToast("⚡ 1-qadam: Yangi alifboga o'tkazilmoqda...");

            try {
                // 1. Transliterate
                const translitCount = await runTransliteration();
                showToast("🌐 2-qadam: Rus, Ingliz va Xitoy tillariga tarjima qilinmoqda...");

                // 2. Translate
                const transCount = await runTranslation();

                showToast(`🎉 Qoyilmaqom! Alifbo yangilandi va ${transCount} ta maydon 3 tilda to'ldirildi! Endi Saqlash ("Saqlash" / Save) tugmasini bosing.`);
            } catch (err) {
                showToast("❌ Xatolik: " + err.message, false);
            } finally {
                btn.disabled = false;
                btn.textContent = "🚀 1-BOSISHDA HAMMASI (Alifbo + 3 Tilga Tarjima)";
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', injectUI);
    } else {
        injectUI();
    }
})();
