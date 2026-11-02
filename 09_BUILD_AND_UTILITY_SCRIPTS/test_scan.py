import docx

doc = docx.Document(r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx")

current_heading = "COVER"
sections = {}
for i, p in enumerate(doc.paragraphs):
    txt = p.text.strip()
    is_h = False
    if p.style.name in ('Heading 1', 'Heading 2') or any(txt.startswith(f"{n}.") for n in range(1, 21)):
        current_heading = txt
        sections[current_heading] = []
        is_h = True
    elif current_heading in sections:
        sections[current_heading].append((i, txt))

print(f"Total sections tracked: {len(sections)}")
for h in list(sections.keys())[:15]:
    print(f'Heading: "{h}" -> {len(sections[h])} paragraphs: {[t[1][:30] for t in sections[h]]}')
