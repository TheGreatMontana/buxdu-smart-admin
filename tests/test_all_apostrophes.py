import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\TGM\.gemini\antigravity\scratch\buxdu_smart_admin')
from buxdu_smart_admin.uzbek_alphabet import to_new_uzbek_latin

# Test various apostrophes
samples = [
    "O'", "O‘", "O’", "O`", "Oʻ", "Oʼ",
    "o'", "o‘", "o’", "o`", "oʻ", "oʼ",
    "G'", "G‘", "G’", "G`", "Gʻ", "Gʼ",
    "g'", "g‘", "g’", "g`", "gʻ", "gʼ",
    "Sh", "sh", "SH", "Ch", "ch", "CH"
]

for s in samples:
    converted = to_new_uzbek_latin(s, style='umlaut')
    print(f"{s:5} -> {converted}")
