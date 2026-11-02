"""
PES UNIVERSITY - DEPARTMENT OF COMPUTER APPLICATIONS
MCA CAPSTONE PROJECT 2025-27 - PHASE I REVIEW II REPORT
MASTER BUILDER: POPULATES THE EXACT UNIVERSITY MENTOR TEMPLATE DIRECTLY
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from report_content_dict import get_all_section_content

TEMPLATE_PATH = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx"
BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DOCX_OUT = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_FINAL.docx")

COLOR_NAVY = RGBColor(11, 25, 44)       # #0B192C
COLOR_BLUE = RGBColor(30, 64, 175)      # #1E40AF
COLOR_DARK = RGBColor(30, 41, 59)       # #1E293B
COLOR_MUTED = RGBColor(100, 116, 139)   # #64748B

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, val in edge_data.items():
                element.set(qn(f'w:{key}'), str(val))

def format_table(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for r_idx, row in enumerate(table.rows):
        is_header = (r_idx == 0)
        bg = "1E3A8A" if is_header else ("F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, cell in enumerate(row.cells):
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            set_cell_border(cell,
                            top=dict(val='single', sz=4, color='CBD5E1'),
                            bottom=dict(val='single', sz=4, color='CBD5E1'),
                            left=dict(val='single', sz=4, color='CBD5E1'),
                            right=dict(val='single', sz=4, color='CBD5E1'))
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if is_header:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(30, 41, 59)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                if i < len(row.cells):
                    row.cells[i].width = Inches(w)

def populate_table_data(tbl, headers, rows, col_widths=None):
    for c_idx, h in enumerate(headers):
        tbl.rows[0].cells[c_idx].text = h
    existing_data_rows = len(tbl.rows) - 1
    for r_idx, row_vals in enumerate(rows):
        if r_idx < existing_data_rows:
            target_row = tbl.rows[r_idx + 1]
        else:
            target_row = tbl.add_row()
        for c_idx, val in enumerate(row_vals):
            target_row.cells[c_idx].text = str(val)
    while len(tbl.rows) > len(rows) + 1:
        row_to_del = tbl.rows[-1]
        tbl._tbl.remove(row_to_del._tr)
    format_table(tbl, col_widths)

def format_run(run, bold=False, italic=False, size=12, color=COLOR_DARK):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color

def set_p_text(p, text, bold_prefix=None, italic=False, space_after=6, bullet=False):
    p.text = ""
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    if bullet:
        p.paragraph_format.left_indent = Inches(0.25)
        r_bul = p.add_run("• ")
        format_run(r_bul, bold=True, color=COLOR_NAVY)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, bold=True, color=COLOR_NAVY)
    r = p.add_run(text)
    format_run(r, italic=italic, color=COLOR_DARK)
    return p

def insert_p_after(cursor, doc, text, bold_prefix=None, italic=False, space_after=6, bullet=False):
    new_p_elem = OxmlElement("w:p")
    cursor.addnext(new_p_elem)
    new_p = docx.text.paragraph.Paragraph(new_p_elem, doc._body)
    set_p_text(new_p, text, bold_prefix=bold_prefix, italic=italic, space_after=space_after, bullet=bullet)
    return new_p_elem

def insert_image_after(cursor, doc, img_path, caption, width=Inches(5.8), space_after=10):
    if not os.path.exists(img_path):
        print(f"  [WARN] Image not found: {img_path}")
        return cursor
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    run = p_img.add_run()
    run.add_picture(img_path, width=width)
    cursor.addnext(p_img._p)
    cursor = p_img._p

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(space_after)
    r = p_cap.add_run(caption)
    format_run(r, italic=True, size=10, color=COLOR_MUTED)
    cursor.addnext(p_cap._p)
    return p_cap._p

def insert_table_after(cursor, doc, headers, rows, col_widths=None):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    for c_idx, h in enumerate(headers):
        tbl.rows[0].cells[c_idx].text = h
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            tbl.rows[r_idx + 1].cells[c_idx].text = str(val)
    format_table(tbl, col_widths)
    cursor.addnext(tbl._tbl)
    return tbl._tbl

def build_mentor_report():
    print("=== POPULATING EXACT UNIVERSITY MENTOR TEMPLATE DIRECTLY ===")
    print(f"Loading template: {TEMPLATE_PATH}")
    doc = docx.Document(TEMPLATE_PATH)
    builtin_tables = list(doc.tables)
    print(f"  Captured {len(builtin_tables)} built-in tables from template.")

    # STRIP INSTRUCTIONS TO STUDENTS
    delete_mode = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt == "Instructions to Students":
            delete_mode = True
        
        if delete_mode:
            # We stop deleting once we see something looking like a main heading like "1. TITLE" or the cover page
            if "Project Title" in txt or txt == "1. TITLE" or "Abstract" in txt:
                delete_mode = False
            else:
                p._p.getparent().remove(p._p)
                continue
                
        # Targeted deletions of other boilerplate
        if "[VERIFY BEFORE SUBMISSION" in txt or "where applicable" in txt or "For every research paper include" in txt or "[Enter Project Title]" in txt:
            try:
                p._p.getparent().remove(p._p)
            except Exception:
                pass

    # Re-fetch paragraphs after deletion
    paragraphs = doc.paragraphs

    
    # 1. Update Cover Page
    print("  Updating Cover Page details...")
    for p in doc.paragraphs[:15]:
        if "[Enter Project Title]" in p.text:
            p.text = "Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift"
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(14)
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
        elif "[Student Name]" in p.text:
            p.text = p.text.replace("[Student Name]", "Karan Shetty K N")
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
        elif "[SRN]" in p.text:
            p.text = p.text.replace("[SRN]", "PES1PG25CA101")
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)

    # 2. Get Section Content
    all_content = get_all_section_content()
    print(f"  Loaded {len(all_content)} section definitions.")

    # 3. Identify Headings and their placeholder paragraphs in the template
    print("  Mapping headings and placeholder paragraphs...")
    sections = {}
    current_heading = None

    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt in all_content:
            current_heading = txt
            sections[current_heading] = {"heading_p": p, "placeholders": []}
        elif current_heading is not None:
            # Check if this paragraph starts another recognized heading
            if any(p.style.name in ('Heading 1', 'Heading 2') for _ in [1]):
                if txt in all_content:
                    current_heading = txt
                    sections[current_heading] = {"heading_p": p, "placeholders": []}
                    continue
            sections[current_heading]["placeholders"].append(p)

    print(f"  Mapped {len(sections)} sections in document.")

    # 4. Populate each section
    for heading_title, data in sections.items():
        items = all_content.get(heading_title, [])
        placeholders = data["placeholders"]
        heading_p = data["heading_p"]

        if not items:
            continue

        # Start cursor at heading or first placeholder
        if placeholders:
            first_p = placeholders[0]
            first_item = items[0]
            
            # Populate first item
            if first_item[0] == "p":
                text = first_item[1]
                bold_prefix = first_item[2] if len(first_item) > 2 else None
                italic = first_item[3] if len(first_item) > 3 else False
                set_p_text(first_p, text, bold_prefix=bold_prefix, italic=italic)
                cursor = first_p._p
                start_idx = 1
            elif first_item[0] == "bullet":
                text = first_item[1]
                bold_prefix = first_item[2] if len(first_item) > 2 else None
                set_p_text(first_p, text, bold_prefix=bold_prefix, bullet=True)
                cursor = first_p._p
                start_idx = 1
            elif first_item[0] == "builtin_table":
                # Builtin table: populate it, clear first_p
                tbl_idx, headers, rows, col_w = first_item[1], first_item[2], first_item[3], first_item[4]
                populate_table_data(builtin_tables[tbl_idx], headers, rows, col_w)
                cursor = heading_p._p
                first_p._p.getparent().remove(first_p._p)
                start_idx = 1
            else:
                cursor = first_p._p
                start_idx = 0
                
            # Process remaining items
            for item in items[start_idx:]:
                itype = item[0]
                if itype == "p":
                    text = item[1]
                    bold_prefix = item[2] if len(item) > 2 else None
                    italic = item[3] if len(item) > 3 else False
                    cursor = insert_p_after(cursor, doc, text, bold_prefix=bold_prefix, italic=italic)
                elif itype == "bullet":
                    text = item[1]
                    bold_prefix = item[2] if len(item) > 2 else None
                    cursor = insert_p_after(cursor, doc, text, bold_prefix=bold_prefix, bullet=True)
                elif itype == "image":
                    cursor = insert_image_after(cursor, doc, item[1], item[2], item[3])
                elif itype == "table":
                    cursor = insert_table_after(cursor, doc, item[1], item[2], item[3])
                elif itype == "builtin_table":
                    tbl_idx, headers, rows, col_w = item[1], item[2], item[3], item[4]
                    populate_table_data(builtin_tables[tbl_idx], headers, rows, col_w)

            # Clean up any remaining placeholder paragraphs
            for extra_p in placeholders[1:]:
                # Only remove if it contains bracketed text or is empty instructional text
                p_txt = extra_p.text.strip()
                if p_txt.startswith("[") or p_txt == "" or any(p_txt.startswith(w) for w in ["Paper title", "Authors", "Publication year", "Journal", "DOI", "Research problem", "Method", "Dataset", "Key findings", "Limitations", "Relevance"]):
                    extra_p._p.getparent().remove(extra_p._p)
        else:
            # No placeholders under heading, insert after heading
            cursor = heading_p._p
            for item in items:
                itype = item[0]
                if itype == "p":
                    text = item[1]
                    bold_prefix = item[2] if len(item) > 2 else None
                    italic = item[3] if len(item) > 3 else False
                    cursor = insert_p_after(cursor, doc, text, bold_prefix=bold_prefix, italic=italic)
                elif itype == "bullet":
                    text = item[1]
                    bold_prefix = item[2] if len(item) > 2 else None
                    cursor = insert_p_after(cursor, doc, text, bold_prefix=bold_prefix, bullet=True)
                elif itype == "image":
                    cursor = insert_image_after(cursor, doc, item[1], item[2], item[3])
                elif itype == "table":
                    cursor = insert_table_after(cursor, doc, item[1], item[2], item[3])
                elif itype == "builtin_table":
                    tbl_idx, headers, rows, col_w = item[1], item[2], item[3], item[4]
                    populate_table_data(builtin_tables[tbl_idx], headers, rows, col_w)

    print("  Saving populated document...")
    doc.save(DOCX_OUT)
    print(f"[SUCCESS] Saved populated DOCX to: {DOCX_OUT}")
    print(f"File size: {os.path.getsize(DOCX_OUT):,} bytes")

if __name__ == "__main__":
    build_mentor_report()
