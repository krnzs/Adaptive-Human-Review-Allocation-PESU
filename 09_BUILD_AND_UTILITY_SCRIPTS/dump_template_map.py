import docx

doc = docx.Document(r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx")
print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

with open("template_map.txt", "w", encoding="utf-8") as f:
    for i, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        f.write(f"P{i:03d} [{p.style.name}] (align={p.alignment}): {txt}\n")

print("Saved template_map.txt")
