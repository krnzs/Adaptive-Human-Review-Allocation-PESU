"""
Third pass: fix remaining issues with substring-based approach.
"""
from pptx import Presentation

PPTX = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\Adaptive_Human_Review_Allocation_PESU.pptx"
prs = Presentation(PPTX)
changes = []

# SLIDE 7: Fix remaining "Streamlit GUI" in the box that contains vertical-tab separated text
slide7 = prs.slides[6]
for shape in slide7.shapes:
    if not shape.has_text_frame: continue
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if "Streamlit GUI" in run.text:
                run.text = run.text.replace("Streamlit GUI", "Evaluation Pipeline")
                changes.append("  Slide 7: Replaced 'Streamlit GUI' in decision box")

# SLIDE 8: Fix FR13-FR14 description
slide8 = prs.slides[7]
for shape in slide8.shapes:
    if not shape.has_text_frame: continue
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if "Interactive joblib dashboard" in run.text:
                run.text = run.text.replace(
                    "Interactive joblib dashboard with configurable parameters and graphical plots",
                    "Modular evaluation pipeline with configurable budgets and CSV-based reporting"
                )
                changes.append("  Slide 8: Fixed FR13-FR14 description")
            if "High-throughput Parquet serialization" in run.text:
                run.text = run.text.replace(
                    "Pandas, pathlib (High-throughput Parquet serialization)",
                    "Pandas (DataFrame operations, CSV I/O), pathlib (Cross-platform paths)"
                )
                changes.append("  Slide 8: Fixed Data Handling description")
            if "joblib (Live interactive research dashboard)" in run.text:
                run.text = run.text.replace(
                    "joblib (Live interactive research dashboard)",
                    "joblib (Model serialization and persistence)"
                )
                changes.append("  Slide 8: Fixed joblib description")

prs.save(PPTX)
import os
print(f"\nThird-pass corrections: {len(changes)} changes")
for c in changes: print(c)
print(f"\nSaved: {PPTX} ({os.path.getsize(PPTX):,} bytes)")
