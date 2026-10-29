import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin')
from buxdu_smart_admin.uzbek_alphabet import to_new_uzbek_latin, to_old_uzbek_latin

text = "G' g', O' o', Sh sh, Ch ch"
new_text = to_new_uzbek_latin(text)
print("Original:", text)
print("New:     ", new_text)

sentence = "Buxoro davlat universiteti o'qituvchilari g'olib bo'lishdi, shahar va choyxona. Is'hoq."
print("\nFull sentence test:")
print("Original:", sentence)
print("New:     ", to_new_uzbek_latin(sentence))
