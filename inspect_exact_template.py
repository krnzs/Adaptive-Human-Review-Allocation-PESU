import docx

doc = docx.Document(r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx")
print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

for i in range(min(40, len(doc.paragraphs))):
    p = doc.paragraphs[i]
    runs_info = []
    for r in p.runs:
        runs_info.append(f"'{r.text}'(font={r.font.name}, size={r.font.size}, bold={r.font.bold})")
    print(f"P{i:03d} [{p.style.name}] align={p.alignment}: {' '.join(runs_info)}")
