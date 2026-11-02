import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

TEMPLATE_PATH = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx"
BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DOCX_OUT = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_Report.docx")

def populate_report():
    print("Loading original mentor template from:", TEMPLATE_PATH)
    doc = docx.Document(TEMPLATE_PATH)

    # Styling helper for paragraphs inserted into template
    def style_p(p, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=None, space_after=6, line_spacing=1.5):
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        for r in p.runs:
            r.font.name = font_name
            r.font.size = Pt(size_pt)
            r.font.bold = bold
            r.font.italic = italic
            if color_rgb:
                r.font.color.rgb = color_rgb

    def insert_p_after(para, text, bold_prefix=None, italic=False, space_after=6, bullet=False):
        new_p = OxmlElement("w:p")
        para._p.addnext(new_p)
        p = docx.text.paragraph.Paragraph(new_p, para._parent)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        if bullet:
            p.style = 'List Bullet'
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
            r_pre.font.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.italic = italic
        return p

    def insert_image_after(para, img_path, caption, width=Inches(5.8)):
        if os.path.exists(img_path):
            # Caption first (so after reverse order it comes below image)
            p_cap = insert_p_after(para, caption, italic=True, space_after=10)
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.runs[0].font.size = Pt(10)
            
            p_img = insert_p_after(para, "", space_after=4)
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p_img.add_run()
            run.add_picture(img_path, width=width)
            return p_cap
        return para

    print("Populating template cover page...")
    for p in doc.paragraphs:
        if "[Enter Project Title]" in p.text:
            p.text = "Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(14)
                r.font.bold = True
        elif "Student Name : [Student Name]" in p.text:
            p.text = "Student Name : Candidate PES1PG25CA101 [VERIFY BEFORE SUBMISSION: Student Full Name]"
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True
        elif "SRN : [SRN]" in p.text:
            p.text = "SRN : PES1PG25CA101"
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.bold = True

    print("Template cover page updated.")

if __name__ == "__main__":
    populate_report()
