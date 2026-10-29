import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin')

from buxdu_smart_admin.translator import translate_bundle

text = "Buxoro davlat universiteti rektori xalqaro konferensiyada nutq so'zladi."
print("Original (UZ):", text)

print("\nTranslating into RU, EN, ZH...")
res = translate_bundle(text, source_lang='uz', target_langs=['ru', 'en', 'zh-cn'])

for lang, tr in res.items():
    print(f"[{lang.upper()}]: {tr}")
