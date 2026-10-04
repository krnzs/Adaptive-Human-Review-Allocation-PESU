import docx
import shutil
import os

src_template = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx"
test_target = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\test_template_mod.docx"

shutil.copyfile(src_template, test_target)
doc = docx.Document(test_target)

# Modify title
for p in doc.paragraphs:
    if "[Enter Project Title]" in p.text:
        p.text = p.text.replace("[Enter Project Title]", "Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift")
    if "[Student Name]" in p.text:
        p.text = p.text.replace("[Student Name]", "Candidate PES1PG25CA101 [VERIFY BEFORE SUBMISSION: Student Full Name]")
    if "[SRN]" in p.text:
        p.text = p.text.replace("[SRN]", "PES1PG25CA101")

doc.save(test_target)
print("Successfully modified test template. Target size:", os.path.getsize(test_target))
