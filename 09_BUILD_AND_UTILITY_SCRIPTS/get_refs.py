import re
with open('build_full_v2_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()
refs = re.findall(r'\[\d+\].*?\]', text)
for r in set(refs): print(r)
