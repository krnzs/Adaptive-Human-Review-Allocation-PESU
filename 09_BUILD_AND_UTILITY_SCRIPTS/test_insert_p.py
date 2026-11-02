import docx
from docx.shared import Pt, Inches
from docx.oxml import OxmlElement

doc = docx.Document(r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\test_template_mod.docx")

# Find '1. Abstract'
for idx, p in enumerate(doc.paragraphs):
    if p.text.strip() == "1. Abstract":
        print(f"Found '1. Abstract' at index {idx}")
        p_next = doc.paragraphs[idx+1]
        print(f"Next paragraph: {p_next.text}")
        p_next.text = "This is the replacement abstract paragraph 1."
        
        # Add paragraph 2 after p_next
        new_p = OxmlElement('w:p')
        p_next._p.addnext(new_p)
        p2 = docx.text.paragraph.Paragraph(new_p, doc)
        p2.text = "This is the replacement abstract paragraph 2."
        p2.style = doc.styles['Normal']
        break

doc.save(r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\test_template_mod2.docx")
print("Saved test_template_mod2.docx successfully.")
