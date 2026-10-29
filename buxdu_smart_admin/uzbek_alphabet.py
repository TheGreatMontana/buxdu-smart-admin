"""
BuxDU Smart Admin - Uzbek Alphabet Reform Engine
================================================
Transliteration module supporting:
1. Old Uzbek Latin -> New Uzbek Latin (Reform)
   - Oʻ, oʻ -> Ō, ō (or Õ, õ)
   - Gʻ, gʻ -> Ḡ, ḡ (or Ğ, ğ)
   - Sh, sh -> Ş, ş
   - Ch, ch -> Ç, ç
   - Handles edge cases like `s'h` -> `s'h` (Is'hoq, Mus'haf)
   - Handles all variants of apostrophes: ', `, ’, ‘, ʻ, ʼ
2. Uzbek Cyrillic -> New Uzbek Latin
3. Reversible mode (New Latin -> Old Latin)
"""

import re
from typing import Literal

# Variants of apostrophes used in Uzbek Latin
APOSTROPHES = r"['`ʼʻ’‘\u02bb\u02bc]"

# Cyrillic to Latin mapping
CYRILLIC_VOWELS = set("аеёиоуэюяАЕЁИОУЭЮЯ")

CYRILLIC_MAP = {
    'А': 'A', 'а': 'a',
    'Б': 'B', 'б': 'b',
    'В': 'V', 'в': 'v',
    'Г': 'G', 'г': 'g',
    'Д': 'D', 'д': 'd',
    'Ж': 'J', 'ж': 'j',
    'З': 'Z', 'з': 'z',
    'И': 'I', 'и': 'i',
    'Й': 'Y', 'й': 'y',
    'К': 'K', 'к': 'k',
    'Л': 'L', 'л': 'l',
    'М': 'M', 'м': 'm',
    'Н': 'N', 'н': 'n',
    'О': 'O', 'о': 'o',
    'П': 'P', 'п': 'p',
    'Р': 'R', 'р': 'r',
    'С': 'S', 'с': 's',
    'Т': 'T', 'т': 't',
    'У': 'U', 'у': 'u',
    'Ф': 'F', 'ф': 'f',
    'Х': 'X', 'х': 'x',
    'Ҳ': 'H', 'ҳ': 'h',
    'Қ': 'Q', 'қ': 'q',
    'Ъ': "'", 'ъ': "'",
    'Ь': "",  'ь': "",
}


def to_new_uzbek_latin(text: str, style: Literal['umlaut', 'macron', 'tilde'] = 'umlaut') -> str:
    """
    Converts text written in old Uzbek Latin or Cyrillic into the new Uzbek Latin alphabet.
    
    style='umlaut': Ö, ö, Ğ, ğ, Ş, ş, Ç, ç (official standard shown in reform graphics)
    style='macron': Ō, ō, Ḡ, ḡ, Ş, ş, Ç, ç
    style='tilde':  Õ, õ, Ğ, ğ, Ş, ş, Ç, ç
    """
    if not text:
        return text

    # First, detect if text has Cyrillic characters
    if re.search(r'[\u0400-\u04FF]', text):
        text = cyrillic_to_new_latin(text, style=style)

    # Choose replacement characters based on style
    if style == 'macron':
        O_UPPER, o_LOWER = 'Ō', 'ō'
        G_UPPER, g_LOWER = 'Ḡ', 'ḡ'
    elif style == 'tilde':
        O_UPPER, o_LOWER = 'Õ', 'õ'
        G_UPPER, g_LOWER = 'Ğ', 'ğ'
    else: # default: 'umlaut' (Ö, ö, Ğ, ğ)
        O_UPPER, o_LOWER = 'Ö', 'ö'
        G_UPPER, g_LOWER = 'Ğ', 'ğ'

    SH_UPPER, sh_LOWER = 'Ş', 'ş'
    CH_UPPER, ch_LOWER = 'Ç', 'ç'

    # Protect HTML tags and entities so we don't mangle attributes like `class="...""`
    html_placeholders = {}
    def preserve_html(match):
        token = f"__HTML_TOKEN_{len(html_placeholders)}__"
        html_placeholders[token] = match.group(0)
        return token

    # Preserve HTML tags
    text = re.sub(r'<[^>]+>', preserve_html, text)
    # Preserve HTML entities
    text = re.sub(r'&[a-zA-Z0-9#]+;', preserve_html, text)

    # Edge case protection: s'h (e.g. Is'hoq, mus'haf) should NOT turn into ş
    def protect_sh_edge_cases(match):
        return match.group(1) + '__SEP_SH__' + match.group(2)

    text = re.sub(rf'([Ss]){APOSTROPHES}([Hh])', protect_sh_edge_cases, text)

    # 1. Replace Oʻ / oʻ with macron/tilde
    text = re.sub(rf'O{APOSTROPHES}', O_UPPER, text)
    text = re.sub(rf'o{APOSTROPHES}', o_LOWER, text)

    # 2. Replace Gʻ / gʻ with macron/tilde
    text = re.sub(rf'G{APOSTROPHES}', G_UPPER, text)
    text = re.sub(rf'g{APOSTROPHES}', g_LOWER, text)

    # 3. Replace Sh / SH / sh with Ş / ş
    text = re.sub(r'SH\b', SH_UPPER, text)
    text = re.sub(r'Sh', SH_UPPER, text)
    text = re.sub(r'sh', sh_LOWER, text)

    # 4. Replace Ch / CH / ch with Ç / ç
    text = re.sub(r'CH\b', CH_UPPER, text)
    text = re.sub(r'Ch', CH_UPPER, text)
    text = re.sub(r'ch', ch_LOWER, text)

    # Restore protected s'h
    text = text.replace('__SEP_SH__', "'")

    # Restore preserved HTML
    for token, original in html_placeholders.items():
        text = text.replace(token, original)

    return text


def to_old_uzbek_latin(text: str) -> str:
    """
    Converts new Uzbek Latin back to standard old Latin (o', g', sh, ch).
    Useful for backward compatibility or exporting data.
    """
    if not text:
        return text

    replacements = [
        ('Ö', "Oʻ"), ('ö', "oʻ"),
        ('Ō', "Oʻ"), ('ō', "oʻ"),
        ('Õ', "Oʻ"), ('õ', "oʻ"),
        ('Ğ', "Gʻ"), ('ğ', "gʻ"),
        ('Ḡ', "Gʻ"), ('ḡ', "gʻ"),
        ('Ş', "Sh"), ('ş', "sh"),
        ('Ç', "Ch"), ('ç', "ch"),
    ]

    for new_char, old_char in replacements:
        text = text.replace(new_char, old_char)

    return text


def cyrillic_to_new_latin(text: str, style: Literal['umlaut', 'macron', 'tilde'] = 'umlaut') -> str:
    """
    Transliterates Uzbek Cyrillic into the new Uzbek Latin alphabet.
    Handles contextual rules for Е/е, Ц/ц, Ё/ё, Ю/ю, Я/я, Ў/ў, Ғ/ғ, Ш/ш, Ч/ч.
    """
    if not text:
        return text

    if style == 'macron':
        o_char, O_char = 'ō', 'Ō'
        g_char, G_char = 'ḡ', 'Ḡ'
    elif style == 'tilde':
        o_char, O_char = 'õ', 'Õ'
        g_char, G_char = 'ğ', 'Ğ'
    else: # 'umlaut' (Ö, ö, Ğ, ğ)
        o_char, O_char = 'ö', 'Ö'
        g_char, G_char = 'ğ', 'Ğ'

    result = []
    length = len(text)
    i = 0

    while i < length:
        char = text[i]
        prev_char = text[i - 1] if i > 0 else ' '
        next_char = text[i + 1] if i + 1 < length else ' '

        # Contextual 'E' / 'e' -> 'Ye' / 'ye' at start of word or after vowels
        if char == 'Е':
            if prev_char in ' \t\n\r"\'([{' or prev_char in CYRILLIC_VOWELS:
                result.append('YE' if next_char.isupper() else 'Ye')
            else:
                result.append('E')
            i += 1
            continue
        elif char == 'е':
            if prev_char in ' \t\n\r"\'([{' or prev_char in CYRILLIC_VOWELS:
                result.append('ye')
            else:
                result.append('e')
            i += 1
            continue

        # Contextual 'Ц' / 'ц'
        if char == 'Ц':
            result.append('TS' if next_char.isupper() else 'Ts')
            i += 1
            continue
        elif char == 'ц':
            result.append('ts')
            i += 1
            continue

        # Specific Uzbek Cyrillic letters
        if char == 'Ў':
            result.append(O_char)
            i += 1
            continue
        elif char == 'ў':
            result.append(o_char)
            i += 1
            continue
        elif char == 'Ғ':
            result.append(G_char)
            i += 1
            continue
        elif char == 'ғ':
            result.append(g_char)
            i += 1
            continue
        elif char == 'Ш':
            result.append('Ş')
            i += 1
            continue
        elif char == 'ш':
            result.append('ş')
            i += 1
            continue
        elif char == 'Ч':
            result.append('Ç')
            i += 1
            continue
        elif char == 'ч':
            result.append('ç')
            i += 1
            continue
        elif char == 'Ё':
            result.append('YO' if next_char.isupper() else 'Yo')
            i += 1
            continue
        elif char == 'ё':
            result.append('yo')
            i += 1
            continue
        elif char == 'Ю':
            result.append('YU' if next_char.isupper() else 'Yu')
            i += 1
            continue
        elif char == 'ю':
            result.append('yu')
            i += 1
            continue
        elif char == 'Я':
            result.append('YA' if next_char.isupper() else 'Ya')
            i += 1
            continue
        elif char == 'я':
            result.append('ya')
            i += 1
            continue

        # Standard 1-to-1 mappings
        if char in CYRILLIC_MAP:
            result.append(CYRILLIC_MAP[char])
        else:
            result.append(char)

        i += 1

    return "".join(result)
