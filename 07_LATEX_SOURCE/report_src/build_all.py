import os
import sys

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
sys.path.insert(0, BASE_DIR)

from report_src.docx_helper import init_document, add_title_block
from report_src.sections_part1 import build_section_1_abstract, build_section_2_introduction, build_section_3_review1
from report_src.sections_part2 import build_section_4_literature_survey
from report_src.sections_part3 import build_section_5_synthesis, build_section_6_comparative_study, build_section_7_contributions, build_section_8_tools
from report_src.sections_part4 import build_section_9_functional, build_section_10_non_functional, build_section_11_system_design
from report_src.sections_part5 import build_section_12_database, build_section_13_methodology, build_section_14_implementation
from report_src.sections_part6 import build_section_15_ml_methodology, build_section_16_testing, build_section_17_genai, build_section_18_challenges, build_section_19_work_planned, build_section_20_references

def generate_docx():
    print("=== BUILDING REVIEW-II DOCX REPORT ===")
    doc = init_document()

    title = "Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift"
    student_name = "Candidate PES1PG25CA101 [VERIFY BEFORE SUBMISSION: Student Full Name]"
    srn = "PES1PG25CA101"
    guide_name = "Prof. Dilip Kumar Maripuri"
    department = "Department of Computer Applications"
    university = "PES University, Bangalore – 560 085"

    print("  Adding Title Block & Front Matter...")
    add_title_block(doc, title, student_name, srn, guide_name, department, university)

    print("  Building Section 1: Abstract...")
    build_section_1_abstract(doc)

    print("  Building Section 2: Introduction...")
    build_section_2_introduction(doc)

    print("  Building Section 3: Review-I Recommendations...")
    build_section_3_review1(doc)

    print("  Building Section 4: Detailed Literature Survey (10 Papers)...")
    build_section_4_literature_survey(doc)

    print("  Building Section 5: Literature Review Synthesis...")
    build_section_5_synthesis(doc)

    print("  Building Section 6: Comparative Study...")
    build_section_6_comparative_study(doc)

    print("  Building Section 7: Proposed Contribution / Distinguishing Features...")
    build_section_7_contributions(doc)

    print("  Building Section 8: Tools and Technologies Used...")
    build_section_8_tools(doc)

    print("  Building Section 9: Functional Requirements...")
    build_section_9_functional(doc)

    print("  Building Section 10: Non-Functional Requirements...")
    build_section_10_non_functional(doc)

    print("  Building Section 11: System / Software Design...")
    build_section_11_system_design(doc)

    print("  Building Section 12: Database / Data Design...")
    build_section_12_database(doc)

    print("  Building Section 13: Detailed Methodology...")
    build_section_13_methodology(doc)

    print("  Building Section 14: Current Implementation...")
    build_section_14_implementation(doc)

    print("  Building Section 15: ML / DL / AI Methodology & Results...")
    build_section_15_ml_methodology(doc)

    print("  Building Section 16: Testing / Evaluation...")
    build_section_16_testing(doc)

    print("  Building Section 17: External GenAI / API Usage Disclosure...")
    build_section_17_genai(doc)

    print("  Building Section 18: Current Challenges...")
    build_section_18_challenges(doc)

    print("  Building Section 19: Work Planned Before Review-III...")
    build_section_19_work_planned(doc)

    print("  Building Section 20: References...")
    build_section_20_references(doc)

    out_docx = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_Report.docx")
    doc.save(out_docx)
    print(f"\n[SUCCESS] Saved submission-ready DOCX to: {out_docx}")
    print(f"File size: {os.path.getsize(out_docx):,} bytes")

if __name__ == "__main__":
    generate_docx()
