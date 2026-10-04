with open('generate_v2_diagrams.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('(\"Interactive Dashboard / UI\", \"?\", \"0%\", RED)', '(\"Interactive Dashboard / UI\", \"app.py\", \"50%\", AMBER)')
text = text.replace('13 of 14 modules fully implemented (93%). Interactive UI: Phase-2.', '13 fully implemented + FR14 partially impl. (50%) = 96.4%.')

with open('generate_v2_diagrams.py', 'w', encoding='utf-8') as f:
    f.write(text)
