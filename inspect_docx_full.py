import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 - Review II Report Template.docx"
if not os.path.exists(docx_path):
    # Try finding it in Downloads
    for f in os.listdir(r"C:\Users\Admin CDS\Downloads"):
        if "Review II" in f and f.endswith(".docx"):
            docx_path = os.path.join(r"C:\Users\Admin CDS\Downloads", f)
            break

print("Using template at:", docx_path)

with zipfile.ZipFile(docx_path, 'r') as z:
    xml_content = z.read('word/document.xml')

root = ET.fromstring(xml_content)
namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

paragraphs = []
for p in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
    if texts:
        paragraphs.append(''.join(texts))

out_txt = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\template_parsed.txt"
with open(out_txt, 'w', encoding='utf-8') as f:
    for i, p in enumerate(paragraphs):
        f.write(f"P{i:03d}: {p}\n")

print(f"Parsed {len(paragraphs)} paragraphs to {out_txt}")
