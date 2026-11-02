"""
Second-pass corrections for remaining issues after first audit fix.
"""
from pptx import Presentation

PPTX = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\Adaptive_Human_Review_Allocation_PESU.pptx"
prs = Presentation(PPTX)
changes = []

def fix(shape, old, new, sn):
    if not shape.has_text_frame: return False
    found = False
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)
                changes.append(f"  Slide {sn}: '{old[:60]}' -> '{new[:60]}'")
                found = True
    return found

# SLIDE 7: remaining "Streamlit GUI"
for shape in prs.slides[6].shapes:
    fix(shape, "Streamlit GUI", "Evaluation Pipeline", 7)

# SLIDE 8: "fit robust scalers" -> "fit scalers"
for shape in prs.slides[7].shapes:
    fix(shape, "fit robust scalers", "fit scalers (StandardScaler for LR)", 8)
    
    # Fix the nonsensical tool descriptions after first-pass replacement
    fix(shape, "Interactive joblib dashboard with configurable parameters and graphical plots",
        "Modular evaluation pipeline with configurable budgets and CSV-based reporting", 8)
    fix(shape, "Pandas, pathlib (High-throughput Parquet serialization)",
        "Pandas (DataFrame operations, CSV I/O), pathlib (Cross-platform paths)", 8)
    fix(shape, "joblib (Live interactive research dashboard)",
        "joblib (Model serialization and persistence)", 8)
    fix(shape, "hashlib (Data integrity verification via SHA-256)",
        "hashlib (Data integrity verification, SHA-256 checksums)", 8)

# SLIDE 9: Fix unverifiable Streamlit-like UI claims
for shape in prs.slides[8].shapes:
    fix(shape, "Evaluation Research UI: Interactive parameter tuning, dynamic budget slider (1%\u201310%), and real-time metric cards",
        "Evaluation Pipeline: Configurable review budgets (1%-10%), automated strategy comparison, and CSV-based results reporting", 9)
    # Fallback if the exact match above didn't work due to encoding
    fix(shape, "Interactive parameter tuning, dynamic budget slider", 
        "Configurable review budgets, automated strategy comparison", 9)
    fix(shape, "real-time metric cards",
        "CSV-based results reporting", 9)

# SLIDE 7: Fix "autonomous AI decision" in pseudocode  
for shape in prs.slides[6].shapes:
    fix(shape, "autonomous AI decision", "automated model decision", 7)

# SAVE
prs.save(PPTX)
import os
print(f"\nSecond-pass corrections: {len(changes)} changes")
for c in changes: print(c)
print(f"\nSaved: {PPTX}")
print(f"Size: {os.path.getsize(PPTX):,} bytes")
