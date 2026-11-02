with open('report_content_part1.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('(("p",', '("p",')

with open('report_content_part1.py', 'w', encoding='utf-8') as f:
    f.write(text)
