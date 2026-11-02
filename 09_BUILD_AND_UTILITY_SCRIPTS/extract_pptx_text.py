"""Extract all text from PPTX for audit purposes."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
prs = Presentation(r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\Adaptive_Human_Review_Allocation_PESU.pptx")

out = os.path.join(os.environ['TEMP'], 'pptx_audit.txt')
with open(out, 'w', encoding='utf-8') as f:
    for i, slide in enumerate(prs.slides, 1):
        f.write(f'\n=== SLIDE {i} ===\n')
        for shape in slide.shapes:
            if shape.has_text_frame:
                for p in shape.text_frame.paragraphs:
                    t = p.text.strip()
                    if t:
                        f.write(f'  TEXT: {t}\n')
            if shape.has_table:
                tbl = shape.table
                for r in range(len(tbl.rows)):
                    cells = [tbl.cell(r, c).text.strip() for c in range(len(tbl.columns))]
                    f.write(f'  ROW: {cells}\n')
        if slide.has_notes_slide:
            n = slide.notes_slide.notes_text_frame.text.strip()
            if n:
                f.write(f'  NOTES: {n}\n')
print(f"Written to {out}")
