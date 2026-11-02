import sys
print("Python executable:", sys.executable)
import docx
print("python-docx version:", docx.__version__)

template_path = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx"
doc = docx.Document(template_path)
print("Successfully loaded template. Total paragraphs:", len(doc.paragraphs), "Total tables:", len(doc.tables))
