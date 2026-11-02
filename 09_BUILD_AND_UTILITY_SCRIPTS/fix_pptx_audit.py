"""
Surgical corrections to the existing PPTX based on audit findings.
Preserves all design, fonts, colors, layout. Only fixes factual issues.
"""
import copy
from pptx import Presentation
from pptx.util import Pt

PPTX = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\Adaptive_Human_Review_Allocation_PESU.pptx"

prs = Presentation(PPTX)
changes = []

def fix_text_in_shape(shape, old, new, slide_num):
    """Replace text in a shape while preserving formatting."""
    if not shape.has_text_frame:
        return False
    found = False
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)
                changes.append(f"  Slide {slide_num}: '{old}' -> '{new}'")
                found = True
    return found

def fix_table_cell(table, row, col, new_text, slide_num, desc=""):
    """Replace text in a table cell while preserving formatting."""
    cell = table.cell(row, col)
    old = cell.text.strip()
    if old != new_text:
        for para in cell.text_frame.paragraphs:
            for run in para.runs:
                run.text = ""
        cell.text_frame.paragraphs[0].runs[0].text = new_text if cell.text_frame.paragraphs[0].runs else new_text
        # If no runs, set directly
        if not cell.text_frame.paragraphs[0].runs:
            cell.text_frame.paragraphs[0].text = new_text
        changes.append(f"  Slide {slide_num} table [{row},{col}]: '{old[:50]}...' -> '{new_text[:50]}...' ({desc})")

def set_cell_text_preserve_format(cell, new_text):
    """Set cell text while trying to preserve the first run's formatting."""
    tf = cell.text_frame
    if tf.paragraphs and tf.paragraphs[0].runs:
        # Save format from first run
        first_run = tf.paragraphs[0].runs[0]
        font_size = first_run.font.size
        font_bold = first_run.font.bold
        try:
            font_color = first_run.font.color.rgb
        except (AttributeError, TypeError):
            font_color = None
        font_name = first_run.font.name
        # Clear all runs
        for p in tf.paragraphs:
            for r in p.runs:
                r.text = ""
        first_run.text = new_text
        # Restore format
        if font_size: first_run.font.size = font_size
        if font_bold is not None: first_run.font.bold = font_bold
        if font_color: first_run.font.color.rgb = font_color
        if font_name: first_run.font.name = font_name
    else:
        cell.text = new_text

# ====================================================================
# SLIDE 4: Fix Literature Survey table to match final reference list
# ====================================================================
slide4 = prs.slides[3]
for shape in slide4.shapes:
    if shape.has_table:
        tbl = shape.table
        n_rows = len(tbl.rows)
        print(f"Slide 4 table: {n_rows} rows x {len(tbl.columns)} cols")

        # Current rows (1-indexed, row 0 is header):
        # Row 1: BigFlow-NIDS - KEEP
        # Row 2: Mozannar & Sontag - KEEP
        # Row 3: Wei et al. - KEEP
        # Row 4: Geifman & El-Yaniv - KEEP
        # Row 5: Guo et al. - KEEP but fix "Proves" -> "Demonstrates"
        # Row 6: Angelopoulos/Bates -> REPLACE with Kim et al.
        # Row 7: Yang et al. IJCV - KEEP
        # Row 8: Lee et al. -> REPLACE with Liu et al.
        # Row 9: Koh et al. WILDS - KEEP (but now becomes Koh)
        # Row 10: Charusaie -> REPLACE with He et al. OR Cao et al.

        # But we need 10 papers matching the user's final list:
        # [1] Mozannar (row 2) ✓
        # [2] Wei et al. (row 3) ✓
        # [3] Geifman (row 4) ✓
        # [4] Guo et al. (row 5) ✓ - fix "Proves"
        # [5] Kim et al. 2024 - NEED TO ADD (replace row 6)
        # [6] Liu et al. 2022 - NEED TO ADD (replace row 8)
        # [7] Yang et al. IJCV (row 7) ✓
        # [8] Koh et al. WILDS (row 9) ✓
        # [9] He et al. 2023 - NEED TO ADD (new)
        # [10] Cao et al. 2023 - NEED TO ADD (replace row 10)
        # BigFlow-NIDS (row 1) ✓ (dataset, separate)

        # FIX Row 5 (Guo et al.): "Proves" -> "Demonstrates"
        if n_rows > 5:
            cell_text = tbl.cell(5, 3).text
            if "Proves" in cell_text or "proves" in cell_text:
                new_summary = cell_text.replace("Proves", "Demonstrates").replace("proves", "demonstrates")
                set_cell_text_preserve_format(tbl.cell(5, 3), new_summary)
                changes.append("  Slide 4: Guo et al. summary: 'Proves' -> 'Demonstrates'")

        # FIX Row 6: Replace Angelopoulos/Bates with Kim et al.
        if n_rows > 6:
            set_cell_text_preserve_format(tbl.cell(6, 0),
                "Human-in-the-Loop Cyber Intrusion Detection Using Active Learning")
            set_cell_text_preserve_format(tbl.cell(6, 1),
                "Y. Kim, G. Dan, Q. Zhu")
            set_cell_text_preserve_format(tbl.cell(6, 2),
                "IEEE TIFS, vol. 19, 2024")
            set_cell_text_preserve_format(tbl.cell(6, 3),
                "Active learning for NIDS with human-in-the-loop. Directly relevant to human-review allocation in intrusion detection.")
            changes.append("  Slide 4: Replaced Angelopoulos/Bates (row 6) with Kim et al. 2024")

        # FIX Row 8: Replace Lee et al. with Liu et al.
        if n_rows > 8:
            set_cell_text_preserve_format(tbl.cell(8, 0),
                "Incorporating Uncertainty in Learning to Defer for Safe Computer-Aided Diagnosis")
            set_cell_text_preserve_format(tbl.cell(8, 1),
                "J. Liu, B. Gallego, S. Barbieri")
            set_cell_text_preserve_format(tbl.cell(8, 2),
                "Scientific Reports, vol. 12, 2022")
            set_cell_text_preserve_format(tbl.cell(8, 3),
                "Incorporates uncertainty into learning-to-defer. Motivates combining uncertainty with deferral decisions.")
            changes.append("  Slide 4: Replaced Lee et al. (row 8) with Liu et al. 2022")

        # FIX Row 10: Replace Charusaie with He et al.
        if n_rows > 10:
            set_cell_text_preserve_format(tbl.cell(10, 0),
                "Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey")
            set_cell_text_preserve_format(tbl.cell(10, 1),
                "K. He, D. D. Kim, M. R. Asghar")
            set_cell_text_preserve_format(tbl.cell(10, 2),
                "IEEE Commun. Surveys, vol. 25, 2023")
            set_cell_text_preserve_format(tbl.cell(10, 3),
                "Comprehensive survey of adversarial ML for NIDS. Provides context for robustness challenges in network intrusion detection.")
            changes.append("  Slide 4: Replaced Charusaie (row 10) with He et al. 2023")

        # We need an 11th row for Cao et al. but can't easily add table rows
        # Instead, let's check if there's space. The user needs exactly 10 papers.
        # Current: BigFlow(1) + 9 papers = 10 rows. We need BigFlow + 10 papers = 11 data rows.
        # But we have exactly 11 rows (header + 10 data). BigFlow takes one.
        # So we have space for 10 papers including BigFlow, which means 9 research papers + BigFlow.
        # The user's list has 10 research papers + BigFlow = 11 total.
        # We can't fit 11 data rows in a 10-data-row table.
        # Solution: BigFlow is a dataset, not a research paper. We can keep it on the dataset slide
        # and replace its row with Cao et al.

        # Actually, let's check: the user's requirement says "minimum 10 IEEE/Scopus-indexed research papers"
        # BigFlow is a dataset publication. So we need to fit all 10 research papers.
        # Currently we have BigFlow + 9 papers = 10 rows. We need to replace BigFlow row (row 1)
        # with one of the missing papers, and move BigFlow to the dataset slide or references.

        # Let's replace BigFlow (row 1) with Cao et al., since BigFlow is already covered
        # extensively on the Dataset slide (Slide 6).
        if n_rows > 1:
            set_cell_text_preserve_format(tbl.cell(1, 0),
                "Anomaly Detection Under Distribution Shift")
            set_cell_text_preserve_format(tbl.cell(1, 1),
                "T. Cao, J. Zhu, G. Pang")
            set_cell_text_preserve_format(tbl.cell(1, 2),
                "IEEE/CVF ICCV, 2023")
            set_cell_text_preserve_format(tbl.cell(1, 3),
                "Addresses anomaly detection under distribution shift. Directly relevant to our shifted-test evaluation setting.")
            changes.append("  Slide 4: Replaced BigFlow row (row 1) with Cao et al. ICCV 2023 (BigFlow is covered on Dataset slide)")

print(f"\nSlide 4: Literature survey table fixed ({len(changes)} changes so far)")

# ====================================================================
# SLIDE 7: Fix "Softmax", "Robust Scaler", "Streamlit GUI"
# ====================================================================
slide7 = prs.slides[6]
for shape in slide7.shapes:
    fix_text_in_shape(shape, "Confidence (Softmax)", "Prediction Probability", 7)
    fix_text_in_shape(shape, "Softmax", "Prediction Probability", 7)
    fix_text_in_shape(shape, "Robust Scaler (Train)", "StandardScaler (LR only)", 7)
    fix_text_in_shape(shape, "Robust Scaler", "StandardScaler", 7)
    fix_text_in_shape(shape, "XGBoost (ROC 0.92)", "XGBoost (val ROC-AUC 0.9228)", 7)
    fix_text_in_shape(shape, "ROC 0.92", "val ROC-AUC 0.9228", 7)
    fix_text_in_shape(shape, "Streamlit GUI", "Evaluation Pipeline", 7)
    fix_text_in_shape(shape, "High-Risk \u27a8 Human Audit", "High-Risk \u27a8 Simulated Review", 7)
    fix_text_in_shape(shape, "Human Audit", "Simulated Review", 7)
    fix_text_in_shape(shape, "Auto AI", "Automated Decision", 7)

# ====================================================================
# SLIDE 8: Fix Tools & Technologies
# ====================================================================
slide8 = prs.slides[7]
for shape in slide8.shapes:
    # Fix Streamlit claims
    fix_text_in_shape(shape, "Interactive Streamlit dashboard with real-time parameter tuning and graphical plots", 
                      "Modular pipeline with configurable parameters and reproducible evaluation", 8)
    fix_text_in_shape(shape, "real-time parameter tuning", "configurable parameters", 8)
    fix_text_in_shape(shape, "Streamlit (Live interactive research dashboard)",
                      "joblib (Model serialization and persistence)", 8)
    fix_text_in_shape(shape, "Streamlit", "joblib", 8)
    
    # Fix PyArrow
    fix_text_in_shape(shape, "Pandas, PyArrow (High-throughput Parquet serialization)",
                      "Pandas (DataFrame operations, CSV I/O)", 8)
    fix_text_in_shape(shape, "PyArrow", "pathlib", 8)
    
    # Fix Seaborn
    fix_text_in_shape(shape, "Matplotlib, Seaborn (Publication-grade performance plots)",
                      "hashlib (Data integrity verification via SHA-256)", 8)
    fix_text_in_shape(shape, "Seaborn", "hashlib", 8)
    
    # Fix throughput claim
    fix_text_in_shape(shape, "Vectorized throughput (<15s for 75K rows), full reproducibility (fixed seeds), modular architecture, input schema guards",
                      "Full reproducibility (fixed seeds, deterministic splits), modular architecture (26 sequential scripts), data integrity verification (SHA-256)", 8)
    fix_text_in_shape(shape, "Vectorized throughput (<15s for 75K rows)",
                      "Full reproducibility (fixed seeds)", 8)

# ====================================================================
# SLIDE 9: Fix Streamlit claim
# ====================================================================
slide9 = prs.slides[8]
for shape in slide9.shapes:
    fix_text_in_shape(shape, "Streamlit Research UI: Interactive parameter tuning, dynamic budget slider (1%\u201310%), and real-time metric cards",
                      "Evaluation Pipeline: Configurable review budgets (1%-10%), automated strategy comparison, and CSV-based results reporting", 9)
    fix_text_in_shape(shape, "Streamlit Research UI", "Evaluation Pipeline", 9)
    fix_text_in_shape(shape, "Streamlit", "Evaluation", 9)

# ====================================================================
# SLIDE 10: Fix overclaim about OOD effectiveness
# ====================================================================
slide10 = prs.slides[9]
for shape in slide10.shapes:
    # Fix the "uncovering severe OOD and drift errors" overclaim
    fix_text_in_shape(shape,
        "Multi-factor adaptive allocation outperforms single-signal confidence by uncovering severe OOD and drift errors",
        "At 1-2% budgets, multi-factor allocation captures more errors than confidence alone in this experiment. Note: OOD-only performed worse than random (0.03% at 1%)", 10)
    fix_text_in_shape(shape,
        "uncovering severe OOD and drift errors",
        "combining complementary signals (though OOD alone was ineffective on this dataset)", 10)

# ====================================================================
# SLIDE 12: Fix "IEEE References" -> "References", add BigFlow ref
# ====================================================================
slide12 = prs.slides[11]
for shape in slide12.shapes:
    fix_text_in_shape(shape, "IEEE References", "References", 12)
    fix_text_in_shape(shape, "KEY IEEE REFERENCES", "REFERENCES", 12)
    
    # Check if BigFlow dataset reference is present
    if shape.has_text_frame:
        full_text = " ".join(p.text for p in shape.text_frame.paragraphs)
        if "[10]" in full_text and "BigFlow" not in full_text:
            # Add BigFlow reference after [10]
            for para in shape.text_frame.paragraphs:
                if "[10]" in para.text:
                    # Add new paragraph after this one
                    new_p = shape.text_frame.add_paragraph()
                    new_p.text = '[11] M. B. Uddin and M. S. Arefin, "BigFlow-NIDS: Large-Scale Benchmark Dataset," Data in Brief, Elsevier, 2026, doi: 10.1016/j.dib.2026.112530.'
                    # Copy format from existing reference
                    if para.runs:
                        for r in new_p.runs:
                            r.font.size = para.runs[0].font.size
                            try:
                                r.font.color.rgb = para.runs[0].font.color.rgb
                            except (AttributeError, TypeError):
                                pass
                    changes.append("  Slide 12: Added BigFlow-NIDS dataset reference [11]")
                    break

# ====================================================================
# SAVE
# ====================================================================
prs.save(PPTX)
print(f"\n{'='*60}")
print(f"AUDIT CORRECTIONS APPLIED: {len(changes)} changes")
print(f"{'='*60}")
for c in changes:
    print(c)
print(f"\nSaved to: {PPTX}")

import os
print(f"File size: {os.path.getsize(PPTX):,} bytes")
