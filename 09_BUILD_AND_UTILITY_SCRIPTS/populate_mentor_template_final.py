"""
PES UNIVERSITY - DEPARTMENT OF COMPUTER APPLICATIONS
MCA CAPSTONE PROJECT 2025-27 - PHASE I REVIEW II REPORT
POPULATES THE EXACT UNIVERSITY MENTOR TEMPLATE
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

TEMPLATE_PATH = r"C:\Users\Admin CDS\Downloads\MCA Capstone Project 2025-27 – Review II Report Template.docx"
BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DOCX_OUT = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_Report.docx")
MD_OUT = os.path.join(BASE_DIR, "Review_II_Report.md")
PDF_OUT = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_Report.pdf")

print("Initializing Exact Mentor Template Populator...")
