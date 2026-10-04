import os
import docx

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DOCX_IN = os.path.join(BASE_DIR, "Adaptive_Human_Review_Allocation_Review_II_Report.docx")
MD_OUT = os.path.join(BASE_DIR, "Review_II_Report.md")

doc = docx.Document(DOCX_IN)

with open(MD_OUT, "w", encoding="utf-8") as md:
    md.write("# PES UNIVERSITY\n")
    md.write("## DEPARTMENT OF COMPUTER APPLICATIONS\n")
    md.write("### MCA CAPSTONE PROJECT 2025-27 — PHASE I REVIEW II / PRESENTATION-2 REPORT\n\n")
    md.write("**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  \n")
    md.write("**Candidate Name:** Candidate PES1PG25CA101 `[VERIFY BEFORE SUBMISSION: Student Full Name]`  \n")
    md.write("**Candidate SRN:** PES1PG25CA101  \n")
    md.write("**Degree & Track:** Master of Computer Applications (MCA) — AI / ML & Data Analytics  \n")
    md.write("**Course:** UQ25CA741A — Capstone Project Phase-I  \n")
    md.write("**Faculty Guide:** Prof. Dilip Kumar Maripuri, Department of Computer Applications, PES University, Bangalore – 560 085  \n\n")
    md.write("---\n\n")

    in_table_idx = 0
    for block in doc.element.body:
        tag = block.tag.split('}')[-1]
        if tag == 'p':
            p_elem = block
            # find corresponding paragraph in doc.paragraphs
            p_text = "".join(node.text for node in p_elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text).strip()
            if not p_text:
                continue

            # check style or heading
            if p_text.startswith("1. Abstract") or any(p_text.startswith(f"{i}. ") for i in range(1, 21)):
                md.write(f"\n# {p_text}\n\n")
            elif any(p_text.startswith(f"{i}.{j} ") for i in range(1, 21) for j in range(1, 20)):
                md.write(f"\n## {p_text}\n\n")
            elif any(p_text.startswith(f"4.{i} ") for i in range(1, 15)):
                md.write(f"\n### {p_text}\n\n")
            elif p_text.startswith("Figure "):
                md.write(f"\n*{p_text}*\n\n")
            elif p_text.startswith("• "):
                md.write(f"- {p_text[2:]}\n")
            elif "Algorithm 1:" in p_text or "Input:" in p_text or "Output:" in p_text or any(p_text.startswith(f"{i}: ") for i in range(1, 25)):
                md.write(f"    {p_text}\n")
            else:
                md.write(f"{p_text}\n\n")

        elif tag == 'tbl':
            if in_table_idx < len(doc.tables):
                tbl = doc.tables[in_table_idx]
                in_table_idx += 1
                rows = tbl.rows
                if rows:
                    hdr_cells = [c.text.strip().replace('\n', ' ') for c in rows[0].cells]
                    md.write("\n| " + " | ".join(hdr_cells) + " |\n")
                    md.write("| " + " | ".join(["---"] * len(hdr_cells)) + " |\n")
                    for row in rows[1:]:
                        row_cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
                        md.write("| " + " | ".join(row_cells) + " |\n")
                    md.write("\n")

print(f"[SUCCESS] Converted DOCX to Markdown: {MD_OUT}")
print(f"Markdown file size: {os.path.getsize(MD_OUT):,} bytes")
