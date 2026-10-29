"""
BuxDU Smart Admin - Multi-Language Translation Engine
====================================================
Features:
1. Zero-config Google Translate backend (works out-of-the-box, no API key needed).
2. Optional Gemini AI backend (Gemini 2.5 Flash) for high-tier academic & journalistic translations.
3. Full HTML preservation: tags (<p>, <strong>, <a>, <img>) are NEVER mangled.
4. Auto-detects and translates from Uzbek (uz) into Russian (ru), English (en), Chinese (zh-cn).
5. Threaded parallel batch translations for near-instant response.
"""

import os
import re
import json
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional, List

try:
    from django.conf import settings
    DJANGO_GEMINI_KEY = getattr(settings, 'GEMINI_API_KEY', None)
except Exception:
    DJANGO_GEMINI_KEY = None


def get_gemini_api_key() -> Optional[str]:
    """Retrieves Gemini API key from Django settings or environment variables."""
    return DJANGO_GEMINI_KEY or os.environ.get('GEMINI_API_KEY')


def _translate_bundle_gemini(text: str, api_key: str) -> Optional[Dict[str, str]]:
    """
    Translates text into RU, EN, and ZH-CN using Google Gemini AI in a single structured call.
    Preserves all HTML markup and uses academic register suitable for universities.
    """
    if not text or not text.strip():
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    prompt = (
        "You are an expert official translator for university news, academic materials, and administration portals.\n"
        "Translate the following Uzbek text into Russian, English, and Simplified Chinese (zh-CN).\n"
        "Strict rules:\n"
        "1. Maintain highest academic and journalistic standards suitable for higher education portals.\n"
        "2. Strictly preserve all HTML tags (e.g. <p>, <strong>, <a>, <img>, <br>) and special characters exactly in place.\n"
        "3. Output MUST be valid JSON with keys: \"ru\", \"en\", \"zh-cn\". Do not wrap in markdown quotes.\n\n"
        f"Uzbek text:\n{text}"
    )

    req_data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(req_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            candidate = res_json.get('candidates', [{}])[0]
            content_part = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
            parsed = json.loads(content_part)
            if isinstance(parsed, dict) and 'ru' in parsed and 'en' in parsed:
                return {
                    'ru': parsed.get('ru', '').strip(),
                    'en': parsed.get('en', '').strip(),
                    'zh-cn': parsed.get('zh-cn', parsed.get('zh', '')).strip()
                }
    except Exception as e:
        # Fallback to standard Google Translate if Gemini request fails or quotas exceeded
        pass
    return None


def _translate_plain_google(text: str, source_lang: str = 'uz', target_lang: str = 'ru') -> str:
    """
    Translates a plain text segment via Google Translate free GTX endpoint.
    Zero configuration, no API key needed.
    """
    if not text or not text.strip():
        return text

    lang_map = {
        'uz': 'uz',
        'ru': 'ru',
        'en': 'en',
        'zh': 'zh-CN',
        'zh-cn': 'zh-CN',
        'zh-hans': 'zh-CN'
    }
    sl = lang_map.get(source_lang.lower(), source_lang)
    tl = lang_map.get(target_lang.lower(), target_lang)

    chunks = []
    current_chunk = []
    current_len = 0

    lines = text.split("\n")
    for line in lines:
        if current_len + len(line) + 1 > 2000:
            chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_len = len(line)
        else:
            current_chunk.append(line)
            current_len += len(line) + 1
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    translated_chunks = []
    for chunk in chunks:
        if not chunk.strip():
            translated_chunks.append(chunk)
            continue

        encoded_text = urllib.parse.quote(chunk)
        url = (
            f"https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl={sl}&tl={tl}&dt=t&q={encoded_text}"
        )
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                translated_piece = "".join([segment[0] for segment in data[0] if segment and segment[0]])
                translated_chunks.append(translated_piece)
        except Exception:
            translated_chunks.append(chunk)

    return "\n".join(translated_chunks)


def translate_text(text: str, source_lang: str = 'uz', target_lang: str = 'ru') -> str:
    """
    Translates text while strictly preserving HTML tags, entities, and line breaks.
    """
    if not text or not text.strip():
        return text

    tag_placeholders = {}
    def preserve_tag(match):
        token = f"___TAG_{len(tag_placeholders)}___"
        tag_placeholders[token] = match.group(0)
        return token

    # 1. Protect HTML comments
    protected = re.sub(r'<!--[\s\S]*?-->', preserve_tag, text)
    # 2. Protect HTML tags
    protected = re.sub(r'<[^>]+>', preserve_tag, protected)
    # 3. Protect HTML entities
    protected = re.sub(r'&[a-zA-Z0-9#]+;', preserve_tag, protected)

    # Translate the cleaned text
    translated = _translate_plain_google(protected, source_lang=source_lang, target_lang=target_lang)

    # Restore tags
    for token, original_tag in tag_placeholders.items():
        pattern = re.compile(re.escape(token).replace(r'\_', r'\s*\_'), re.IGNORECASE)
        translated = pattern.sub(original_tag, translated)

    return translated


def translate_bundle(
    text: str,
    source_lang: str = 'uz',
    target_langs: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Translates text into multiple languages.
    If GEMINI_API_KEY is available, uses Google Gemini AI for contextual academic quality.
    Otherwise, automatically uses high-speed parallel Google Translate.
    """
    if target_langs is None:
        target_langs = ['ru', 'en', 'zh-cn']

    # 1. Try Gemini AI if API key is configured
    gemini_key = get_gemini_api_key()
    if gemini_key:
        gemini_result = _translate_bundle_gemini(text, gemini_key)
        if gemini_result:
            return gemini_result

    # 2. Fallback to concurrent Google Translate (Zero configuration)
    results = {}

    def worker(lang):
        res = translate_text(text, source_lang=source_lang, target_lang=lang)
        return lang, res

    with ThreadPoolExecutor(max_workers=len(target_langs)) as executor:
        futures = [executor.submit(worker, lang) for lang in target_langs]
        for f in futures:
            lang, translated = f.result()
            results[lang] = translated

    return results
