import os
import re
import sys

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
sys.path.insert(0, BASE_DIR)

from report_content_part1 import get_part1_content
from report_content_part2 import get_part2_content

all_content = {}
all_content.update(get_part1_content())
all_content.update(get_part2_content())

OUT_DIR = os.path.join(BASE_DIR, "PES1PG25CA101-KARANSHETTYKN-Report")
CH_DIR = os.path.join(OUT_DIR, "chapters")
FIG_DIR = os.path.join(OUT_DIR, "figures")
TBL_DIR = os.path.join(OUT_DIR, "tables")

os.makedirs(CH_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TBL_DIR, exist_ok=True)

def tex_escape(text):
    if not isinstance(text, str):
        text = str(text)
    # Remove instructions/residue
    text = re.sub(r'\[VERIFY BEFORE SUBMISSION.*?\]', '', text, flags=re.IGNORECASE)
    text = text.replace('Instructions to Students', '')
    
    # Specific project phrasing fixes
    text = text.replace('13 of 14 requirements complete (93%)', '13 of 14 functional requirements are fully implemented; FR14 is partially implemented.')
    text = text.replace('13.5 of 14 Modules Implemented (96.4%)', '13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).')
    text = text.replace('96.4%', '92.9%')
    
    # Character cleanups
    text = text.replace('—', '---').replace('–', '--')
    text = text.replace('•', '')
    text = text.replace('“', '``').replace('”', "''").replace('‘', '`').replace('’', "'")
    text = text.replace('≥', '$\\ge$').replace('≤', '$\\le$').replace('±', '$\\pm$')
    text = text.replace('×', '$\\times$').replace('→', '$\\rightarrow$')
    
    # Standard LaTeX escapes
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{').replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('\\textbackslash\\{\\}', '\\textbackslash{}')
    return text.strip()

def format_table_tex(headers, rows, caption=""):
    n_cols = len(headers)
    if n_cols == 0:
        return ""
    
    # Choose column widths based on number of columns
    if n_cols == 2:
        col_spec = "p{0.3\\textwidth} p{0.65\\textwidth}"
    elif n_cols == 3:
        col_spec = "p{0.18\\textwidth} p{0.44\\textwidth} p{0.32\\textwidth}"
    elif n_cols == 4:
        col_spec = "p{0.1\\textwidth} p{0.28\\textwidth} p{0.38\\textwidth} p{0.16\\textwidth}"
    elif n_cols == 5:
        col_spec = "p{0.14\\textwidth} p{0.16\\textwidth} p{0.14\\textwidth} p{0.18\\textwidth} p{0.28\\textwidth}"
    else:
        col_spec = " ".join(["p{0.15\\textwidth}"] * n_cols)
    
    lines = [
        "\\begin{table}[H]",
        "\\centering",
        "\\small",
        f"\\begin{{tabular}}{{{col_spec}}}",
        "\\toprule"
    ]
    
    # Header row
    hdr_cells = [f"\\textbf{{{tex_escape(h)}}}" for h in headers]
    lines.append(" & ".join(hdr_cells) + " \\\\")
    lines.append("\\midrule")
    
    # Rows
    for r in rows:
        row_cells = [tex_escape(str(c)) for c in r]
        while len(row_cells) < n_cols:
            row_cells.append("")
        lines.append(" & ".join(row_cells[:n_cols]) + " \\\\")
        
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    if caption:
        lines.append(f"\\caption{{{tex_escape(caption)}}}")
    lines.append("\\end{table}")
    return "\n".join(lines) + "\n\n"

def render_section_content(sec_key, items):
    sec_title = sec_key.split('. ', 1)[1] if '. ' in sec_key else sec_key
    out = []
    
    num_part = sec_key.split(' ', 1)[0] if ' ' in sec_key else ''
    dots = num_part.count('.')
    if dots == 0 or (dots == 1 and num_part.endswith('.')):
        out.append(f"\\section{{{tex_escape(sec_title)}}}\n\n")
    elif dots == 1 or (dots == 2 and num_part.endswith('.')):
        out.append(f"\\subsection{{{tex_escape(sec_title)}}}\n\n")
    else:
        out.append(f"\\subsubsection{{{tex_escape(sec_title)}}}\n\n")
        
    in_bullet_list = False
    
    for item in items:
        itype = item[0]
        
        if itype != 'bullet' and in_bullet_list:
            out.append("\\end{itemize}\n\n")
            in_bullet_list = False
            
        if itype == 'p':
            text = item[1]
            prefix = item[2] if len(item) > 2 and item[2] else None
            is_italic = item[3] if len(item) > 3 else False
            
            # Check if this is code / terminal trace
            if text.startswith('[INFO]') or 'src/25_final_strategy_comparison.py' in text:
                out.append("\\begin{verbatim}\n" + text + "\n\\end{verbatim}\n\n")
            elif 'Algorithm 1:' in text or 'Input:' in text or 'Output:' in text or text.strip().startswith('1: ') or text.strip().startswith('2: '):
                out.append("\\texttt{" + tex_escape(text).replace('\n', '\\\\ ') + "}\n\n")
            else:
                p_str = ""
                if prefix:
                    p_str += f"\\textbf{{{tex_escape(prefix)}}} "
                if is_italic:
                    p_str += f"\\textit{{{tex_escape(text)}}}"
                else:
                    p_str += tex_escape(text)
                out.append(p_str + "\n\n")
                
        elif itype == 'bullet':
            if not in_bullet_list:
                out.append("\\begin{itemize}\n")
                in_bullet_list = True
            text = item[1]
            prefix = item[2] if len(item) > 2 and item[2] else None
            b_str = "\\item "
            if prefix:
                b_str += f"\\textbf{{{tex_escape(prefix)}}} "
            b_str += tex_escape(text)
            out.append(b_str + "\n")
            
        elif itype == 'table':
            headers = item[1]
            rows = item[2]
            out.append(format_table_tex(headers, rows, caption=sec_title))
            
        elif itype == 'builtin_table':
            headers = item[2]
            rows = item[3]
            out.append(format_table_tex(headers, rows, caption=sec_title))
            
        elif itype == 'image':
            img_path = item[1]
            caption = item[2]
            base_img = os.path.basename(img_path)
            target_fig = os.path.join(FIG_DIR, base_img)
            
            if os.path.exists(target_fig) or os.path.exists(img_path):
                out.append("\\begin{figure}[H]\n\\centering\n")
                out.append(f"\\includegraphics[width=0.85\\textwidth]{{figures/{base_img}}}\n")
                out.append(f"\\caption{{{tex_escape(caption)}}}\n")
                out.append("\\end{figure}\n\n")
            else:
                out.append("\\begin{figure}[H]\n\\centering\n")
                out.append(f"% TODO: Insert verified architecture diagram/screenshot here: {base_img}\n")
                out.append(f"\\fbox{{\\parbox{{0.8\\textwidth}}{{\\centering \\vspace{{2cm}} \\textbf{{[Figure Placeholder: {tex_escape(base_img)}]}}\\\\ \\small {tex_escape(caption)} \\vspace{{2cm}}}}}}\n")
                out.append(f"\\caption{{{tex_escape(caption)}}}\n")
                out.append("\\end{figure}\n\n")
                
    if in_bullet_list:
        out.append("\\end{itemize}\n\n")
        
    return "".join(out)

# Mapping definition
CHAPTER_MAP = {
    "abstract": ["1. Abstract"],
    "introduction": [
        "2. Introduction", "2.1 Problem Scenario", "2.2 Proposed Solution", 
        "2.3 Purpose", "2.4 Scope", "3. Review-I Recommendations and Action Taken"
    ],
    "literature_review": [
        "4. Detailed Literature Survey",
        "4.1 Research Paper 1", "4.2 Research Paper 2", "4.3 Research Paper 3",
        "4.4 Research Paper 4", "4.5 Research Paper 5", "4.6 Research Paper 6",
        "4.7 Research Paper 7", "4.8 Research Paper 8", "4.9 Research Paper 9",
        "4.10 Research Paper 10"
    ],
    "background": [
        "5. Literature Review Synthesis", "5.1 Background Study", 
        "5.2 Major Approaches Identified", "5.3 Major Findings", 
        "5.4 Limitations of Existing Work", "5.5 Identified Research / Application Gap", 
        "5.6 How the Proposed Project Addresses the Gap"
    ],
    "comparative_study": [
        "6. Comparative Study of Existing Applications / Systems", 
        "7. Proposed Contribution / Distinguishing Features"
    ],
    "requirements": [
        "8. Tools and Technologies Used", "8.1 Programming Languages", "8.2 Frameworks", 
        "8.3 Libraries / Packages with Versions", "8.4 Database / Storage", 
        "8.5 Development Tools", "8.6 Deployment Environment", "8.7 Hardware Requirements",
        "9. Functional Requirements", "9.1 Users / Actors", "9.2 Modules", "9.3 Functionalities", 
        "10. Non-Functional Requirements"
    ],
    "methodology": [
        "13. Detailed Methodology", "13.1 Overall Workflow", "13.2 Algorithms / Processing Steps", "13.3 Pseudocode",
        "15. ML / DL / AI Methodology — Where Applicable", "15.1 Dataset and Source", 
        "15.2 Dataset Characteristics", "15.3 Data Preprocessing", 
        "15.4 Data Augmentation / Feature Engineering", "15.5 Train / Validation / Test Strategy", 
        "15.6 Cross Validation Strategy", "15.7 Benchmark Models", 
        "15.8 Proposed / Modified / Optimised Model", "15.9 Hyperparameter Optimisation", 
        "15.10 Evaluation Metrics"
    ],
    "system_design": [
        "11. System / Software Design", "11.1 Architecture Diagram", "11.2 Use-Case Diagram", 
        "11.3 Activity / Sequence Diagram", "11.4 Process Flow / Methodology", 
        "11.5 ML / Data Processing Pipeline", "11.6 DL Model Architecture", 
        "11.7 Network / IoT Block Diagram"
    ],
    "data_design": [
        "12. Database / Data Design", "12.1 ER Diagram", "12.2 Conceptual Schema", 
        "12.3 NoSQL / Document Structure", "12.4 Dataset / Data Schema"
    ],
    "implementation": [
        "14. Current Implementation", "14.1 Current Completion Percentage", "14.2 Completed Modules", 
        "14.3 Modules Under Development", "14.4 Pending Modules", "14.5 Implementation Screenshots", 
        "14.6 Explanation of Demonstrable Functionality",
        "17. External GenAI / API Usage Disclosure", "17.1 API / Service Used", 
        "17.2 Functionality Provided by API", "17.3 Approximate Percentage Contribution", 
        "17.4 Core Functionality Independently Implemented"
    ],
    "results": [
        "15.11 Preliminary Results", "15.12 Analysis of Results",
        "16. Testing / Evaluation", "16.1 Functional Testing", 
        "16.2 UI / UX Testing", "16.3 Model Evaluation"
    ],
    "limitations": [
        "18. Current Challenges", "19. Work Planned Before Review-III"
    ],
    "conclusion": []
}

# Special notes to inject for verified inconsistencies:
INCONSISTENCY_NOTES = {
    "methodology": """
% =========================================================================
% REVIEW NOTE / INCONSISTENCY DETECTED:
% In the offline benchmark (src/25_final_strategy_comparison.py), adaptive weights
% are computed based on pre-defined regime heuristics. Sequential batch-level feedback 
% adaptation was evaluated in src/28_sequential_feedback_eval.py.
% Review this section to ensure the textual description accurately aligns with the code.
% =========================================================================
""",
    "implementation": """
% =========================================================================
% REVIEW NOTE / INCONSISTENCY DETECTED:
% 1. Implementation Percentage: 13 of 14 functional requirements are fully implemented (92.9%);
%    FR14 (Interactive Streamlit Analytics Dashboard) is partially implemented.
% 2. Historical Error Source: src/14_historical_error_risk.py fits KNeighborsClassifier
%    on TRAINING errors (y_train != y_train_pred), whereas earlier report drafts referred to
%    validation errors. Ensure wording reflects training errors.
% =========================================================================
"""
}

for ch_name, sec_keys in CHAPTER_MAP.items():
    ch_file = os.path.join(CH_DIR, f"{ch_name}.tex")
    title_str = ch_name.replace('_', ' ').title()
    content_str = f"\\chapter{{{title_str}}}\n\n"
    
    if ch_name in INCONSISTENCY_NOTES:
        content_str += INCONSISTENCY_NOTES[ch_name] + "\n"
        
    if sec_keys:
        for k in sec_keys:
            if k in all_content:
                content_str += render_section_content(k, all_content[k])
            else:
                alt_k = [x for x in all_content.keys() if x.startswith(k) or k in x]
                if alt_k:
                    content_str += render_section_content(alt_k[0], all_content[alt_k[0]])
                else:
                    content_str += f"% Note: Section {k} had no direct items in source content.\n\n"
    else:
        if ch_name == "conclusion":
            content_str += """This capstone project (Phase-I Review-II) addresses the degradation of machine learning classifiers under temporal distribution shift within capacity-constrained operational environments. By systematically evaluating an adaptive multi-factor human-review allocation framework on a 500,000-flow chronological partition of the BigFlow-NIDS benchmark, this work demonstrates that multi-signal triage (combining uncertainty, Mahalanobis OOD distance, Population Stability Index, and historical error proximity) substantially outperforms conventional confidence-based ranking under tight review quotas (1%--2% audit budgets).

Specifically, at a 1% operational inspection quota, the adaptive multi-factor strategy captures 610 errors (17.80% error capture) compared to 463 errors (13.51%) for pure confidence ranking. At a 2% budget, it captures 1,174 errors (34.26%) compared to 916 errors (26.73%). Concurrently, empirical results reveal an honest crossover threshold: at broader review allocations (5%--10%), pure confidence triage captures a larger total volume of errors (65.45% and 84.01% respectively). 

To date, 13 of 14 functional requirements (92.9% fully implemented) have been verified across 26 sequential Python execution scripts and an interactive Streamlit exploratory analytics dashboard. Future work for Review-III and Phase-II will focus on temperature calibration of probabilities, dynamic runtime latency benchmarks, and active human-analyst review workflows.
"""
    
    with open(ch_file, "w", encoding="utf-8") as f:
        f.write(content_str)
    print(f"Wrote {ch_file} ({len(content_str)} bytes)")

print("All chapters successfully generated!")
