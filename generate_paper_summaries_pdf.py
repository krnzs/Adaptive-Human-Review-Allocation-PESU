"""
Generate a Publication-Grade Paper_Summaries.pdf using ReportLab.
Converts Paper_Summaries.md into a beautifully formatted, structured PDF document.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
PDF_PATH = os.path.join(PROJECT_DIR, "Paper_Summaries.pdf")

# Palette
NAVY      = HexColor("#0B192C")
ACCENT    = HexColor("#1E40AF")
DARK      = HexColor("#1E293B")
LIGHT_BG  = HexColor("#F8FAFC")
BORDER    = HexColor("#CBD5E1")
GREEN     = HexColor("#16A34A")
RED       = HexColor("#DC2626")
AMBER     = HexColor("#D97706")
MUTED     = HexColor("#64748B")
CARD_ALT  = HexColor("#F1F5F9")
CALLOUT_BG= HexColor("#EFF6FF")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFillColor(NAVY)
        self.rect(54, 11 * 72 - 36, 8.5 * 72 - 108, 3, fill=1, stroke=0)
        
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(ACCENT)
            self.drawString(54, 11 * 72 - 48, "PES UNIVERSITY  |  CAPSTONE LITERATURE SURVEY & DEFENSE GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED)
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 48, "SRN: PES1PG25CA101")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 52, 8.5 * 72 - 54, 11 * 72 - 52)

        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * 72 - 54, 45)
        self.setFont("Helvetica", 8.5)
        self.setFillColor(MUTED)
        self.drawString(54, 32, "Project Guide: Prof. Dilip Kumar Maripuri  |  Course: UQ25CA741A  |  Department of Computer Applications")
        self.drawRightString(8.5 * 72 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=NAVY, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=ACCENT, spaceAfter=8
    )
    meta_style = ParagraphStyle(
        'DocMeta', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=MUTED
    )
    h1 = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=NAVY,
        spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h2 = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=ACCENT,
        spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    paper_title = ParagraphStyle(
        'PaperTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=NAVY,
        spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5, textColor=DARK, spaceAfter=4
    )
    bullet = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=DARK,
        leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )
    callout_text = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12, textColor=DARK
    )
    q_style = ParagraphStyle(
        'QStyle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=RED, spaceAfter=2, keepWithNext=True
    )
    a_style = ParagraphStyle(
        'AStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=DARK, spaceAfter=5
    )

    # Table styles
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=white, alignment=1)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=DARK, alignment=1)
    tc_left  = ParagraphStyle('TCL', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=DARK, alignment=0)
    tc_left_b= ParagraphStyle('TCLB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=NAVY, alignment=0)

    story = []

    # Title block
    story.append(Paragraph("CAPSTONE LITERATURE SURVEY & VIVA DEFENSE GUIDE", subtitle_style))
    story.append(Paragraph("Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift", title_style))
    story.append(Paragraph("<b>Student:</b> MCA Candidate (Data Analytics)  |  <b>SRN:</b> PES1PG25CA101  |  <b>Guide:</b> Prof. Dilip Kumar Maripuri<br/>"
                           "<b>Department:</b> Department of Computer Applications, PES University, Bangalore  |  <b>Course:</b> UQ25CA741A", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=2, spaceAfter=8))

    # Read and parse Paper_Summaries.md into flowables
    md_file = os.path.join(PROJECT_DIR, "Paper_Summaries.md")
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Split into sections
    sections = md_text.split("### ")
    
    # Process papers
    story.append(Paragraph("Detailed Literature Summaries (16 Verified Papers)", h1))
    
    for sec in sections[1:]:
        lines = sec.strip().split("\n")
        title_line = lines[0].strip()
        
        # Check if it's a section header or a paper
        if title_line.startswith("["):
            story.append(Paragraph(f"<b>{title_line}</b>", paper_title))
            content_lines = lines[1:]
            
            for line in content_lines:
                line_str = line.strip()
                if not line_str:
                    continue
                if line_str.startswith("- **Citation"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Indexing:"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Problem:"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Core Idea"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Data & Experiments:"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Main Results:"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("  1.") or line_str.startswith("  2.") or line_str.startswith("  3."):
                    story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{line_str.strip()}", bullet))
                elif line_str.startswith("- **Limitations"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **Relevance to My Project:"):
                    story.append(Paragraph(line_str.replace("- ", "• "), bullet))
                elif line_str.startswith("- **2-Line Slide Summary:"):
                    story.append(Paragraph(f"<b>Slide Summary:</b> <i>{line_str.replace('- **2-Line Slide Summary:**', '').strip()}</i>", bullet))
                elif line_str.startswith("- **20-Second Spoken Version:"):
                    spk = line_str.replace("- **20-Second Spoken Version:**", "").strip()
                    story.append(Paragraph(f"<b>Spoken Version:</b> <font color='#1E40AF'>{spk}</font>", bullet))
                elif line_str.startswith("- **Panel Question"):
                    pass # Will handle Q&A
                elif line_str.startswith("  - *Panel Question:*"):
                    pq = line_str.replace("  - *Panel Question:*", "").strip()
                    story.append(Paragraph(f"<b>Panel Q:</b> <font color='#DC2626'>{pq}</font>", q_style))
                elif line_str.startswith("  - *Answer:*"):
                    pa = line_str.replace("  - *Answer:*", "").strip()
                    story.append(Paragraph(f"<b>Defense Answer:</b> {pa}", a_style))
                elif line_str.startswith("$$"):
                    pass
                else:
                    if not line_str.startswith("---"):
                        story.append(Paragraph(line_str, body))
            story.append(Spacer(1, 4))
            story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceBefore=2, spaceAfter=4))

    # Add Section A: Related-Work Map
    story.append(Spacer(1, 8))
    story.append(Paragraph("Section A: Related-Work Mapping Table & Research Gap", h1))
    
    # Mapping table data
    table_headers = ["Paper", "Indexing", "Conf", "OOD", "PSI", "Hist", "Budg", "Shift", "NIDS"]
    map_rows = [
        ["[1] Cao (ICCV 23)", "IEEE/Scopus", "", "✓", "", "", "", "✓", ""],
        ["[2] Mozannar (ICML 20)", "PMLR*", "✓", "", "", "", "", "", ""],
        ["[3] Wei (ICML 24)", "PMLR*", "", "", "", "", "✓", "", ""],
        ["[4] Geifman (NeurIPS 17)", "Scopus", "✓", "", "", "", "", "", ""],
        ["[5] Guo (ICML 17)", "PMLR*", "✓", "", "", "", "", "", ""],
        ["[6] Kim (TIFS 24)", "IEEE/Scopus", "", "", "", "", "✓", "", "✓"],
        ["[7] Liu (Sci. Rep. 22)", "Scopus", "✓", "", "", "", "", "", ""],
        ["[8] Yang (IJCV 24)", "Scopus", "", "✓", "", "", "", "✓", ""],
        ["[9] Koh (ICML 21)", "PMLR*", "", "", "", "", "", "✓", ""],
        ["[10] He (COMST 23)", "IEEE/Scopus", "", "", "", "", "", "", "✓"],
        ["[11] Lu (TKDE 19)", "IEEE/Scopus", "", "", "✓", "✓", "", "✓", ""],
        ["[12] Iwashita (Access 19)", "IEEE/Scopus", "", "", "✓", "", "", "✓", ""],
        ["[13] Mosqueira (AIR 23)", "Scopus", "", "", "", "", "✓", "", ""],
        ["[14] Hendrickx (ML 24)", "Scopus", "✓", "✓", "", "", "✓", "", ""],
        ["[15] Sarhan (MNA 22)", "Scopus", "", "", "", "", "", "", "✓"],
        ["[16] Uddin (DiB 26)", "Scopus", "", "", "", "", "", "✓", "✓"],
        ["OUR FRAMEWORK", "Capstone", "✓", "✓", "✓", "✓", "✓", "✓", "✓"]
    ]
    t_map_data = [[Paragraph(f"<b>{h}</b>", th_style) for h in table_headers]]
    for r in map_rows:
        is_ours = r[0] == "OUR FRAMEWORK"
        bg_col = ACCENT if is_ours else NAVY
        row_c = []
        for ci, val in enumerate(r):
            if ci == 0:
                row_c.append(Paragraph(f"<b>{val}</b>", tc_left_b if not is_ours else ParagraphStyle('TO', parent=tc_left_b, textColor=ACCENT)))
            elif ci == 1:
                row_c.append(Paragraph(val, tc_left))
            else:
                txt = f"<b><font color='{ACCENT.hexval()}'>{val}</font></b>" if is_ours else val
                row_c.append(Paragraph(txt, tc_style))
        t_map_data.append(row_c)

    t_map = Table(t_map_data, colWidths=[1.5*inch, 1.1*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch, 0.55*inch])
    t_map.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, CARD_ALT]),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor("#DBEAFE")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_map)
    story.append(Spacer(1, 6))

    # 5-Sentence Gap
    gap_html = (
        "<b>The Five-Sentence Research Gap:</b><br/>"
        "1. Existing selective classification frameworks [4], [5] rely strictly on prediction confidence, which fails silently under temporal distribution shift because modern classifiers remain overconfident even when error rates surge.<br/>"
        "2. Out-of-distribution detection techniques [1], [8] successfully identify statistical feature novelty, but novelty in high-throughput network environments frequently corresponds to benign high-volume transfers rather than true classification errors.<br/>"
        "3. While literature on concept drift [11], [12] and adversarial vulnerabilities [10] highlights macroscopic model degradation, these approaches track population aggregates without providing per-instance risk scoring for operational triage.<br/>"
        "4. Furthermore, learning-to-defer formulations [2], [3], [7], [14] theoretically model expert handoffs under abstract cost penalties but fail to model strict top-K operational review quotas (e.g., exactly 1% or 2% human capacity) under genuine temporal shift.<br/>"
        "5. <b>Our project fills this exact gap:</b> we build a unified, post-hoc triage framework synthesizing prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake proximity to optimize error interception under explicit operational capacity constraints."
    )
    story.append(Paragraph(gap_html, body))
    story.append(Spacer(1, 8))

    # Section B: The Story
    story.append(Paragraph("Section B: How the Papers Connect (150-Word Viva Narrative)", h1))
    story.append(Paragraph(
        "<i>\"Modern deep classifiers are severely miscalibrated and overconfident, as proven by Guo et al. Consequently, when Geifman's confidence-based selective prediction is deployed in non-stationary environments, it fails silently because models make confident mistakes under temporal shift. While Yang and Cao propose Out-of-Distribution detection to catch shifts, our experiments confirm that feature novelty alone does not correlate with classification errors in network security. Meanwhile, Lu and Iwashita demonstrate that tracking macroscopic feature drift and error feedback is necessary to detect emerging degradation. Hendrickx's premier survey proves that effective rejection must combine ambiguity and novelty, while Mozannar, Wei, and Liu formalize learning-to-defer to human experts. Finally, Kim and Mosqueira-Rey show that human attention in cybersecurity operations is strictly constrained by alert fatigue. Our project unifies these separate threads: we combine uncertainty, OOD distance, PSI drift, and historical mistake patterns into an adaptive triage mechanism that maximizes error interception under strict 1% to 2% operational human review budgets.\"</i>",
        body
    ))
    story.append(Spacer(1, 8))

    # Section C: Glossary
    story.append(Paragraph("Section C: Technical Glossary (15 Essential Terms)", h1))
    glossary_items = [
        ("Distribution Shift", "Change in joint probability distribution P(X, Y) between training and test environments."),
        ("Covariate Shift", "Change in input feature distribution P(X) while class posterior P(Y|X) remains unchanged."),
        ("Concept Drift", "Change in class posterior P(Y|X), meaning identical inputs produce different labels over time."),
        ("Population Stability Index (PSI)", "Statistical metric measuring population drift across feature bins; PSI >= 0.10 indicates moderate drift."),
        ("Mahalanobis Distance", "Multivariate distance metric incorporating feature covariance: D_M(x) = sqrt((x - u)^T Sigma^-1 (x - u))."),
        ("Model Calibration", "Degree to which predicted confidence matches empirical correctness probability."),
        ("Selective Classification", "Classification paradigm allowing a model to abstain on low-confidence instances."),
        ("Learning to Defer (L2D)", "Framework where model jointly learns when to predict autonomously and when to defer to an expert."),
        ("Active Learning", "ML paradigm where algorithm actively selects informative instances to query human annotators."),
        ("Validation ROC-AUC", "Area Under ROC Curve on validation data measuring threshold-independent discriminative ranking."),
        ("Error Capture Rate", "Percentage of total model errors intercepted by the human review queue."),
        ("Review Efficiency", "Density of errors intercepted per unit of human effort (standardized per 1,000 reviews)."),
        ("Ambiguity Rejection", "Abstaining because an instance lies close to the classification decision boundary."),
        ("Novelty Rejection", "Abstaining because an instance falls into low-density, unexplored feature space (OOD)."),
        ("NetFlow", "Aggregated flow representation summarizing IP traffic into statistical sessions without payload inspection.")
    ]
    for term, defn in glossary_items:
        story.append(Paragraph(f"• <b><font color='#0B192C'>{term}:</font></b> {defn}", bullet))
    story.append(Spacer(1, 8))

    # Section D: 10 Viva Questions
    story.append(Paragraph("Section D: Top 10 Tough Viva Questions & Bulletproof Answers", h1))
    viva_qa = [
        ("Q1: Why not just retrain the model when drift occurs?",
         "Retraining requires newly labeled ground truth that takes weeks to collect; our triage operates in real time at inference time to intercept dangerous errors today before retraining is feasible."),
        ("Q2: Why does Confidence beat Adaptive at 5% and 10% budgets?",
         "This is an honest empirical finding: Adaptive triage is specialized for tight budgets (1%-2%) where it beats confidence by 4.3%-7.5%; at 5%-10%, the budget is large enough to audit the broad decision boundary where confidence excels."),
        ("Q3: Why did OOD capture only 0.03% of errors (worse than random)?",
         "In network traffic, extreme Mahalanobis outliers are benign high-bandwidth file transfers that XGBoost classifies correctly (Decile 9 had only 0.16% error rate); feature novelty does not equal classification error."),
        ("Q4: Why didn't you just use temperature scaling to fix overconfidence?",
         "Temperature scaling only rescales probabilities monotonically on in-distribution data without changing instance ranking; it cannot detect shifted high-confidence errors without external drift signals."),
        ("Q5: Are your signal weights learned or heuristic?",
         "In Phase 1 they are experimentally defined heuristics; Phase 2 explicitly introduces bilevel optimization to learn optimal routing policies from asymmetric cost matrices."),
        ("Q6: Why is validation Precision only 0.04?",
         "Validation attack prevalence is extremely low (0.33%, 248 attacks in 75K flows); ROC-AUC is 0.9228, proving strong ranking, and our triage engine exists specifically to intercept the false alarms."),
        ("Q7: How did you prevent data leakage?",
         "Strict chronological split (350K train / 75K val / 75K test); all scalers, OOD covariance matrices, and mistake bins were fitted exclusively on training data."),
        ("Q8: How does this differ from Mozannar's Learning to Defer?",
         "Mozannar modifies the training loss under fixed deferral cost for stationary data; we provide a post-hoc triage layer operating over an existing model under temporal shift with explicit capacity budgets (1%-10%)."),
        ("Q9: Is this tested on live campus traffic?",
         "No, it uses the peer-reviewed 2026 BigFlow-NIDS benchmark so that all 3,427 shifted errors and 753 validation errors are 100% reproducible and verifiable."),
        ("Q10: What is your concrete Phase-2 plan?",
         "Conformal prediction coverage guarantees, SHAP explainability on routed alerts, cross-domain evaluation on medical/financial tabular data, and an interactive Streamlit UI.")
    ]
    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", a_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Successfully built Paper Summaries PDF: {PDF_PATH}")
    print(f"     File size: {os.path.getsize(PDF_PATH):,} bytes")

if __name__ == "__main__":
    build_pdf()
