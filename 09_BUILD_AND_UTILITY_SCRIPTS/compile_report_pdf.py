import os
import docx
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DOCX_IN = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_FINAL.docx")
PDF_OUT = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_FINAL.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total PDF pages generated: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        if self._pageNumber > 1:
            self.setFont("Times-Roman", 9)
            self.setFillColor(colors.HexColor("#64748B"))
            # Header
            self.drawString(1.0 * inch, 10.25 * inch, "PES University — MCA Capstone Phase-I Review-II Report")
            self.drawRightString(7.5 * inch, 10.25 * inch, "PES1PG25CA101")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(1.0 * inch, 10.15 * inch, 7.5 * inch, 10.15 * inch)
            
            # Footer
            self.line(1.0 * inch, 0.85 * inch, 7.5 * inch, 0.85 * inch)
            self.drawString(1.0 * inch, 0.70 * inch, "Adaptive Human-Review Allocation for Reliable ML Under Distribution Shift")
            self.drawRightString(7.5 * inch, 0.70 * inch, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()

def build_pdf():
    print("=== COMPILING REVIEW-II REPORT PDF VIA REPORTLAB ===")
    doc = docx.Document(DOCX_IN)
    pdf = SimpleDocTemplate(
        PDF_OUT,
        pagesize=letter,
        leftMargin=1.0 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch
    )

    styles = getSampleStyleSheet()
    s_normal = ParagraphStyle('TNormal', parent=styles['Normal'], fontName='Times-Roman', fontSize=10.5, leading=15, textColor=colors.HexColor('#1E293B'), spaceAfter=5)
    s_title = ParagraphStyle('TTitle', parent=styles['Heading1'], fontName='Times-Bold', fontSize=15, leading=19, textColor=colors.HexColor('#0B192C'), alignment=1, spaceAfter=8)
    s_sub = ParagraphStyle('TSub', parent=styles['Normal'], fontName='Times-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#1E40AF'), alignment=1, spaceAfter=12)
    s_h1 = ParagraphStyle('TH1', parent=styles['Heading1'], fontName='Times-Bold', fontSize=12.5, leading=16, textColor=colors.HexColor('#0B192C'), spaceBefore=14, spaceAfter=5, keepWithNext=True)
    s_h2 = ParagraphStyle('TH2', parent=styles['Heading2'], fontName='Times-Bold', fontSize=11.5, leading=15, textColor=colors.HexColor('#1E40AF'), spaceBefore=10, spaceAfter=3, keepWithNext=True)
    s_h3 = ParagraphStyle('TH3', parent=styles['Heading3'], fontName='Times-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#1E293B'), spaceBefore=7, spaceAfter=2, keepWithNext=True)
    s_bullet = ParagraphStyle('TBullet', parent=s_normal, leftIndent=15, bulletIndent=5, spaceAfter=3)
    s_caption = ParagraphStyle('TCaption', parent=s_normal, fontName='Times-Italic', fontSize=9, leading=12, textColor=colors.HexColor('#64748B'), alignment=1, spaceBefore=3, spaceAfter=8)
    s_table_cell = ParagraphStyle('TTblCell', fontName='Times-Roman', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'))
    s_table_hdr = ParagraphStyle('TTblHdr', fontName='Times-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)
    s_code = ParagraphStyle('TCode', fontName='Courier', fontSize=8.5, leading=11, textColor=colors.HexColor('#0B192C'), leftIndent=15, spaceAfter=2)

    story = []
    
    # We iterate through blocks
    tbl_idx = 0
    for block in doc.element.body:
        tag = block.tag.split('}')[-1]
        if tag == 'p':
            p_text = "".join(node.text for node in block.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text).strip()
            if not p_text:
                continue

            # Check if there is an image in this paragraph
            has_image = False
            for blip in block.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
                rId = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                if rId and rId in doc.part.rels:
                    target_part = doc.part.rels[rId].target_part
                    img_bytes = target_part.blob
                    # Save temporary image
                    tmp_img = os.path.join(BASE_DIR, "scratch_pdf_img.png")
                    with open(tmp_img, "wb") as f_img:
                        f_img.write(img_bytes)
                    img_flowable = Image(tmp_img, width=5.5*inch, height=3.0*inch)
                    story.append(Spacer(1, 4))
                    story.append(img_flowable)
                    has_image = True
                    break
            
            if has_image:
                continue

            if p_text.startswith("PES UNIVERSITY") or p_text.startswith("DEPARTMENT OF"):
                story.append(Paragraph(f"<b>{p_text}</b>", s_title))
            elif p_text.startswith("MCA CAPSTONE") or p_text.startswith("PHASE I"):
                story.append(Paragraph(f"<b>{p_text}</b>", s_sub))
            elif p_text.startswith("Adaptive Human-Review"):
                story.append(Paragraph(f"<b>{p_text}</b>", s_title))
                story.append(Spacer(1, 10))
            elif p_text.startswith("1. Abstract") or any(p_text.startswith(f"{i}. ") for i in range(1, 21)):
                if not p_text.startswith("1. Abstract"):
                    story.append(Spacer(1, 8))
                story.append(Paragraph(f"<b>{p_text}</b>", s_h1))
            elif any(p_text.startswith(f"{i}.{j} ") for i in range(1, 21) for j in range(1, 20)):
                story.append(Paragraph(f"<b>{p_text}</b>", s_h2))
            elif any(p_text.startswith(f"4.{i} ") for i in range(1, 15)):
                story.append(Paragraph(f"<b>{p_text}</b>", s_h2))
            elif p_text.startswith("Figure "):
                story.append(Paragraph(p_text, s_caption))
            elif p_text.startswith("• "):
                story.append(Paragraph(f"• {p_text[2:]}", s_bullet))
            elif "Algorithm 1:" in p_text or "Input:" in p_text or "Output:" in p_text or any(p_text.startswith(f"{i}: ") for i in range(1, 25)):
                story.append(Paragraph(p_text, s_code))
            else:
                story.append(Paragraph(p_text, s_normal))

        elif tag == 'tbl':
            if tbl_idx < len(doc.tables):
                t = doc.tables[tbl_idx]
                tbl_idx += 1
                t_data = []
                for r_idx, row in enumerate(t.rows):
                    r_cells = []
                    for c_idx, cell in enumerate(row.cells):
                        cell_txt = cell.text.strip().replace('\n', '<br/>')
                        if r_idx == 0 and len(t.rows) > 4:
                            p_c = Paragraph(cell_txt, s_table_hdr)
                        else:
                            p_c = Paragraph(cell_txt, s_table_cell)
                        r_cells.append(p_c)
                    t_data.append(r_cells)

                # Col widths
                n_cols = len(t.columns)
                avail_w = 6.5 * inch
                if n_cols == 2:
                    col_w = [2.5 * inch, 4.0 * inch]
                elif n_cols == 4:
                    col_w = [0.8*inch, 2.0*inch, 2.5*inch, 1.2*inch]
                elif n_cols == 5:
                    col_w = [1.2*inch, 1.3*inch, 1.3*inch, 1.4*inch, 1.3*inch]
                elif n_cols == 6:
                    col_w = [1.5*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch]
                elif n_cols == 7:
                    col_w = [0.8*inch, 0.9*inch, 1.4*inch, 1.0*inch, 1.1*inch, 0.9*inch, 0.4*inch]
                else:
                    col_w = [avail_w / n_cols] * n_cols

                rep_table = Table(t_data, colWidths=col_w, repeatRows=1)
                t_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ]
                for row_i in range(1, len(t_data)):
                    if row_i % 2 == 1:
                        t_style.append(('BACKGROUND', (0, row_i), (-1, row_i), colors.HexColor('#F8FAFC')))
                rep_table.setStyle(TableStyle(t_style))
                story.append(Spacer(1, 4))
                story.append(rep_table)
                story.append(Spacer(1, 6))

    pdf.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Compiled ReportLab PDF: {PDF_OUT}")
    print(f"PDF file size: {os.path.getsize(PDF_OUT):,} bytes")

if __name__ == "__main__":
    build_pdf()
