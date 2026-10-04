"""
Generate a Comprehensive, Professional Mentor Discussion Guide & Project Walkthrough PDF.
Explains the entire Capstone Phase-1 in simple, defensible plain English.
Uses ReportLab Platypus Paragraphs in all table cells to eliminate any clipping or text overlap.
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
PDF_PATH = os.path.join(PROJECT_DIR, "Capstone_Phase1_Mentor_Walkthrough_Guide.pdf")

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
        # Top banner line
        self.setFillColor(NAVY)
        self.rect(54, 11 * 72 - 36, 8.5 * 72 - 108, 3, fill=1, stroke=0)
        
        # Running header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(ACCENT)
            self.drawString(54, 11 * 72 - 48, "PES UNIVERSITY  |  CAPSTONE PHASE-1 MENTOR WALKTHROUGH GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED)
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 48, "SRN: PES1PG25CA101")
            self.setStrokeColor(BORDER)
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 52, 8.5 * 72 - 54, 11 * 72 - 52)

        # Footer
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.5)
        self.line(54, 45, 8.5 * 72 - 54, 45)
        self.setFont("Helvetica", 8.5)
        self.setFillColor(MUTED)
        self.drawString(54, 32, "Project Guide: Prof. Dilip Kumar Maripuri  |  Course: UQ25CA741A  |  Department of Computer Applications")
        self.drawRightString(8.5 * 72 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_guide_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Typography styles
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
    body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5, textColor=DARK, spaceAfter=5
    )
    bullet = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=DARK,
        leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )
    callout_text = ParagraphStyle(
        'Callout', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=DARK
    )
    q_style = ParagraphStyle(
        'QStyle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13.5, textColor=RED, spaceAfter=2, keepWithNext=True
    )
    a_style = ParagraphStyle(
        'AStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=DARK, spaceAfter=6
    )

    # Table styles
    th_style = ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=white, alignment=1)
    tc_style = ParagraphStyle('TC', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=DARK, alignment=1)
    tc_bold  = ParagraphStyle('TCB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=NAVY, alignment=1)
    tc_win   = ParagraphStyle('TCW', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=ACCENT, alignment=1)
    tc_left  = ParagraphStyle('TCL', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=DARK, alignment=0)
    tc_left_b= ParagraphStyle('TCLB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=NAVY, alignment=0)

    story = []

    def make_callout(title, text, bg=CALLOUT_BG, border_c=ACCENT):
        p_t = Paragraph(f"<b><font color='{border_c.hexval()}'>{title}</font></b>", h2)
        p_b = Paragraph(text, callout_text)
        t = Table([[p_t], [p_b]], colWidths=[7.0 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg),
            ('BOX', (0,0), (-1,-1), 1, border_c),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    # -------------------------------------------------------------
    # HEADER SECTION
    # -------------------------------------------------------------
    story.append(Paragraph("CAPSTONE PHASE-1: MENTOR DISCUSSION & WALKTHROUGH GUIDE", subtitle_style))
    story.append(Paragraph("Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift", title_style))
    story.append(Paragraph("<b>Student:</b> MCA Candidate (Data Analytics)  |  <b>SRN:</b> PES1PG25CA101  |  <b>Guide:</b> Prof. Dilip Kumar Maripuri<br/>"
                           "<b>Department:</b> Department of Computer Applications, PES University, Bangalore  |  <b>Course:</b> UQ25CA741A", meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceBefore=2, spaceAfter=8))

    # -------------------------------------------------------------
    # SECTION 1: THE 60-SECOND ELEVATOR PITCH
    # -------------------------------------------------------------
    story.append(Paragraph("1. The 60-Second Elevator Pitch (How to Explain It Informally)", h1))
    pitch_html = (
        "<i>\"Professor, in high-speed applications like network security, machine learning models process millions of events "
        "every day, but human security analysts can only afford to manually inspect a tiny fraction—typically just 1% to 2% "
        "due to operational costs and alert fatigue.<br/><br/>"
        "The dangerous problem is that when real-world traffic patterns change over time (distribution shift), the model starts "
        "making 4 to 5 times more mistakes, but it remains 97% confident in its wrong decisions! So if you only review the predictions "
        "where the model looks uncertain, you miss the vast majority of silent, high-confidence errors.<br/><br/>"
        "My project builds an adaptive triage engine that combines <b>four signals</b>—prediction uncertainty, how strange the packet is "
        "(OOD distance), macroscopic feature drift (PSI), and historical mistake patterns. Under strict human inspection limits (1% to 2%), "
        "our multi-factor strategy captures <b>34.26% of errors</b> compared to only <b>26.73%</b> for confidence alone and just <b>2.13%</b> for random checks. "
        "I have completely built 13 out of 14 modules across 26 verified Python scripts on 500,000 real flows from the 2026 BigFlow-NIDS benchmark.\"</i>"
    )
    story.append(make_callout("How to Start Your Informal Conversation", pitch_html, bg=CALLOUT_BG, border_c=ACCENT))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 2: THE REAL PROBLEM (WHAT ACTUALLY BREAKS?)
    # -------------------------------------------------------------
    story.append(Paragraph("2. The Problem We Are Solving: Why Does ML Fail in Production?", h1))
    story.append(Paragraph("In textbooks, machine learning models are evaluated by taking a dataset, shuffling it randomly, and splitting it 80/20. "
                           "In the real world, this is a dangerous illusion because time moves forward. An intrusion detection system trained on Monday "
                           "faces entirely new attacker behavior and shifted network volumes on Friday.", body))
    
    story.append(Paragraph("Three critical realities create the operational bottleneck:", h2))
    story.append(Paragraph("• <b>The Attention Bottleneck:</b> Human analysts cannot review 100,000 alerts a day. Reviewing costs real time and money. Real SOC teams operate at 1% to 5% review budgets.", bullet))
    story.append(Paragraph("• <b>Silent Overconfidence Failure (Guo et al., ICML 2017 [5]):</b> When a model encounters shifted data, its accuracy drops, but its probability outputs remain artificially high. In our experiment, errors surged by <b>4.55x</b>, but average confidence only dropped from <b>98.65% to 96.82%</b>.", bullet))
    story.append(Paragraph("• <b>Random Audit Fails:</b> Picking alerts randomly captures almost nothing (only 1.17% of errors at a 1% budget in our tests).", bullet))
    story.append(Paragraph("• <b>Single Signal Blindspots:</b> If you only look at low confidence, you miss confident mistakes. If you only look at Out-of-Distribution (OOD) distance, you flag benign high-speed traffic spikes that aren't actually classification errors.", bullet))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 3: THE EXPERIMENTAL DATASET & CHRONOLOGICAL SHIFT
    # -------------------------------------------------------------
    story.append(Paragraph("3. The Dataset & How We Modeled Real Distribution Shift", h1))
    story.append(Paragraph("To make our results rock-solid and impossible to dismiss as synthetic, we used a brand-new 2026 research benchmark:", body))
    story.append(Paragraph("• <b>Dataset:</b> <b>BigFlow-NIDS (Data in Brief, Feb 2026) [11]</b>. It harmonizes four major NetFlow datasets (UNSW-NB15, ToN-IoT, BoT-IoT, CIC-IDS2018) totaling 66.9 million flows with 55 attributes.", bullet))
    story.append(Paragraph("• <b>Our Experimental Sample:</b> Exactly <b>500,000 chronological network flows</b>. We verified that 100% of rows match the raw 14GB source using SHA-256 cryptographic hashes.", bullet))
    story.append(Paragraph("• <b>Chronological Split (Strictly No Future Leakage):</b> We did NOT use random train-test splitting. We sorted by time:", bullet))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <b>Training Split (70% = 350,000 flows):</b> Baseline attack rate of 6.10% (21,344 attacks). Used to fit models, scalers, and reference covariance matrices.", bullet))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <b>Validation Split (15% = 75,000 flows):</b> Next time window. Attack rate dropped to 0.33% (248 attacks). XGBoost made exactly <b>753 errors (1.004% error rate)</b>.", bullet))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3. <b>Shifted Test Split (15% = 75,000 flows):</b> Future time window. Attack rate surged to 6.30% (4,724 attacks). XGBoost made exactly <b>3,427 errors (4.569% error rate)</b>.", bullet))
    
    # Table of Split Dynamics
    split_headers = ["Split Partition", "Flow Count", "Attack Prevalence", "XGBoost Error Count", "Error Rate", "Avg Confidence"]
    split_rows = [
        ["Training (70%)", "350,000", "6.10% (21,344)", "Reference Fit", "N/A", "0.9882"],
        ["Validation (15%)", "75,000", "0.33% (248)", "753 errors", "1.004%", "0.9865"],
        ["Shifted Test (15%)", "75,000", "6.30% (4,724)", "3,427 errors", "4.569%", "0.9682"]
    ]
    t_split_data = [[Paragraph(f"<b>{h}</b>", th_style) for h in split_headers]]
    for row in split_rows:
        t_split_data.append([
            Paragraph(f"<b>{row[0]}</b>", tc_left_b),
            Paragraph(row[1], tc_style),
            Paragraph(row[2], tc_style),
            Paragraph(row[3], tc_style),
            Paragraph(row[4], tc_style),
            Paragraph(row[5], tc_style)
        ])

    t_split = Table(t_split_data, colWidths=[1.4*inch, 1.0*inch, 1.3*inch, 1.2*inch, 0.9*inch, 1.2*inch])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, CARD_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_split)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 4: THE FOUR SIGNALS IN SIMPLE WORDS
    # -------------------------------------------------------------
    story.append(Paragraph("4. The Four Reliability Signals: How We Detect Risky Decisions", h1))
    story.append(Paragraph("Instead of relying only on model confidence, our framework extracts <b>four distinct signals</b> for every single prediction:", body))

    signals_desc = [
        ("Signal 1: Prediction Uncertainty (s_conf)", "1 - max(P(y|x))", 
         "How hesitant is the model? Extracted directly from XGBoost predict_proba. If the model says 51% Benign / 49% Attack, uncertainty is 0.49 (very high). If it says 99.9% Benign, uncertainty is 0.001."),
        ("Signal 2: Mahalanobis OOD Distance (s_ood)", "Regularized (x-u)^T S^-1 (x-u)", 
         "How unusual is this packet compared to normal training data? It measures multivariate distance taking feature correlations into account, regularized with eps=1e-6 so the covariance matrix is invertible."),
        ("Signal 3: Feature Drift Score (s_drift)", "Weighted Z-Score x PSI", 
         "Is this packet deviating in features that we know have macroscopically shifted? We calculate Population Stability Index (PSI) across all 49 features. Features with PSI >= 0.10 are flagged, and we score how far each flow deviates along those drifted features."),
        ("Signal 4: Historical Mistake Proximity (s_hist)", "Decile Error Frequency", 
         "Does this packet resemble past mistakes the model made during training? We discretize 10 key features into 10 deciles and map the empirical error rate of each bin. If a packet falls into bins where the model historically blundered, its risk score increases.")
    ]
    for s_name, s_form, s_exp in signals_desc:
        story.append(Paragraph(f"<b><font color='#1E40AF'>{s_name}</font></b>  <font color='#64748B'>[{s_form}]</font>", h2))
        story.append(Paragraph(s_exp, body))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 5: THE STRATEGIES & EMPIRICAL RESULTS
    # -------------------------------------------------------------
    story.append(Paragraph("5. What Are the Results? (The Core Slide You Must Defend)", h1))
    story.append(Paragraph("We evaluated 5 strategies across 4 operational human-review budgets (1%, 2%, 5%, 10%) on the 75,000 shifted test flows (where total errors = 3,427):", body))

    res_headers = ["Review Budget", "Uniform Random", "Pure Confidence", "OOD-Only Filter", "Static Multi-Factor", "Feedback Adaptive"]
    res_raw = [
        [("1.0%", "750 reviews"), ("1.17%", "40 errs"), ("13.51%", "463 errs"), ("0.03%", "1 err"), ("17.51%", "600 errs"), ("17.80%", "610 errs", True)],
        [("2.0%", "1,500 reviews"), ("2.13%", "73 errs"), ("26.73%", "916 errs"), ("0.26%", "9 errs"), ("33.99%", "1,165 errs"), ("34.26%", "1,174 errs", True)],
        [("5.0%", "3,750 reviews"), ("5.52%", "189 errs"), ("65.45%", "2,243 errs", True), ("0.35%", "12 errs"), ("54.57%", "1,870 errs"), ("45.90%", "1,573 errs")],
        [("10.0%", "7,500 reviews"), ("9.92%", "340 errs"), ("84.01%", "2,879 errs", True), ("0.35%", "12 errs"), ("65.42%", "2,242 errs"), ("52.35%", "1,794 errs")]
    ]
    t_res_data = [[Paragraph(f"<b>{h}</b>", th_style) for h in res_headers]]
    for row in res_raw:
        row_cells = []
        for ci, item in enumerate(row):
            is_win = len(item) == 3 and item[2]
            col = '#1E40AF' if is_win else ('#0B192C' if ci == 0 else '#1E293B')
            sub_col = '#1E40AF' if is_win else '#64748B'
            star = " <b>[WIN]</b>" if is_win else ""
            txt = f"<b><font color='{col}'>{item[0]}</font></b>{star}<br/><font color='{sub_col}' size=7>{item[1]}</font>"
            align_style = tc_left if ci == 0 else tc_style
            row_cells.append(Paragraph(txt, align_style))
        t_res_data.append(row_cells)

    t_res = Table(t_res_data, colWidths=[1.3*inch, 1.1*inch, 1.2*inch, 1.1*inch, 1.15*inch, 1.15*inch])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, CARD_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>The Three Critical Insights to Tell Your Mentor:</b>", h2))
    story.append(Paragraph("1. <b>Why Multi-Factor wins at tight budgets (1% and 2%):</b> When you can only review 750 or 1,500 items, multi-factor triage catches up to <b>147 more errors at 1%</b> and <b>258 more errors at 2%</b> than confidence alone! It intercepts high-risk drifted packets that confidence completely ignores.", bullet))
    story.append(Paragraph("2. <b>Why Confidence overtakes at broad budgets (5% and 10%):</b> At larger review budgets, you have enough quota to review the broad decision boundary. Pure confidence is optimal when human resources are abundant.", bullet))
    story.append(Paragraph("3. <b>The OOD Negative Result (Honest Science):</b> OOD alone caught only 1 error at 1% budget (worse than random!). Why? In network traffic, extreme outliers in feature space are benign high-volume transfers (e.g. large file backups), NOT attacker packets or model errors! Pointing this out proves you didn't fake your results.", bullet))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 6: WHAT IS ACTUALLY IMPLEMENTED (THE CODEBASE)
    # -------------------------------------------------------------
    story.append(Paragraph("6. What Is Actually Implemented? (13 of 14 Modules = 92.9%)", h1))
    story.append(Paragraph("Your mentor may ask: <i>\"Did you just make slides, or is there real code running?\"</i><br/>"
                           "Here is the exact proof: We wrote and executed <b>26 discrete Python scripts</b> in <code>src/</code>:", body))
    
    code_summary = [
        ["Phase / Category", "Scripts", "Exact Functionality Delivered", "Status"],
        ["1. Ingestion & Split", "src/01, 02, 03, 26", "Ingests 500K sample, verifies SHA-256 hash against 14GB source, chronological 70/15/15 split, missing value median imputation.", "100% Implemented"],
        ["2. Model Training", "src/04", "Trains Logistic Regression, Random Forest, and XGBoost. Evaluates validation ROC-AUC (0.9228 for XGBoost). Saves .pkl artifacts.", "100% Implemented"],
        ["3. Signal Extraction", "src/05, 07, 10, 14", "Extracts uncertainty, regularized Mahalanobis OOD distance, 49-feature PSI drift, and 10-feature decile mistake risk.", "100% Implemented"],
        ["4. Strategy Benchmark", "src/06, 08, 09, 13, 20, 24, 25", "Implements 5 triage strategies, executes 1%, 2%, 5%, 10% budget allocations on 75,000 shifted flows, outputs comparison CSVs.", "100% Implemented"],
        ["5. Interactive Web UI", "Phase 2", "Lightweight Streamlit/Dash dashboard for live slider control and triage queue inspection.", "Planned (0%)"]
    ]
    t_code_data = [[Paragraph(f"<b>{h}</b>", th_style) for h in code_summary[0]]]
    for row in code_summary[1:]:
        col_st = GREEN if "100%" in row[3] else RED
        t_code_data.append([
            Paragraph(f"<b>{row[0]}</b>", tc_left_b),
            Paragraph(row[1], tc_style),
            Paragraph(row[2], tc_left),
            Paragraph(f"<b><font color='{col_st.hexval()}'>{row[3]}</font></b>", tc_style)
        ])

    t_code = Table(t_code_data, colWidths=[1.3*inch, 1.2*inch, 3.4*inch, 1.1*inch])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, CARD_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_code)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 7: SLIDE-BY-SLIDE INFORMAL TALKING POINTS
    # -------------------------------------------------------------
    story.append(Paragraph("7. Slide-by-Slide Informal Guide: What to Say on Each Slide", h1))
    story.append(Paragraph("When presenting the 24-slide deck to your mentor or committee, use this exact informal mental roadmap:", body))

    slide_talks = [
        ("Slide 1 (Title)", "State your name, SRN, Guide (Prof. Dilip Kumar Maripuri), and the title clearly."),
        ("Slide 2 (Abstract & RQ)", "State the core question: 'Can an adaptive multi-factor mechanism catch more errors than confidence alone under tight human budgets?'"),
        ("Slide 3 (Problem Scenario)", "Explain the 1% human review bottleneck and the silent overconfidence failure."),
        ("Slide 4 (Purpose & Scope)", "Clarify Phase-1 scope: binary NetFlow classification on 500K sample; Phase-2 scope: cross-domain tabular generalization."),
        ("Slide 5 (Background Study)", "Briefly mention the 5 existing paradigms: Selective classification, OOD detection, PSI drift, Learning-to-defer, and Human-in-the-loop NIDS."),
        ("Slide 6 & 7 (Literature Survey)", "Highlight IEEE/Scopus indexing. Mention Cao et al. (ICCV 2023 [1]) and Kim et al. (IEEE TIFS 2024 [6]). Note that PMLR papers have verified IEEE equivalents."),
        ("Slide 8 (Comparative Study)", "Point to the comparison table showing how our proposed system is the only one combining all 4 signals with explicit budget slicing."),
        ("Slide 9 (Users of the System)", "Describe the three roles: ML Engineer (builds & monitors), SOC Analyst (reviews queued alerts), Evaluator (audits strategies)."),
        ("Slide 10 & 11 (Functional Reqs)", "Walk through FR1 to FR13 as 100% completed across our 26 scripts; explain FR14 (dashboard) is the Phase-2 target."),
        ("Slide 12 (Non-Functional Reqs)", "Mention strict reproducibility (seed=42), 1.6-second execution speed, SHA-256 integrity, and modular architecture."),
        ("Slide 13 (Tools & Tech)", "Highlight Python 3.10, XGBoost, scikit-learn, SciPy, pandas, and ReportLab."),
        ("Slide 14 & 15 (Architecture & Flow)", "Trace the dataflow: Ingestion -> Preprocess -> XGBoost Inference -> 4-Signal Extraction -> Risk Scoring -> Queue Allocation."),
        ("Slide 16 (Database Schema)", "Explain the file-based schema: structured CSV tables linked by prediction_id and serialized .pkl models with SHA-256 checks."),
        ("Slide 17 (Dataset & Shift)", "Explain the BigFlow-NIDS benchmark, chronological splits, and the 4.55x error surge from validation to shifted test."),
        ("Slide 18 (Model Performance)", "Show XGBoost validation ROC-AUC of 0.9228 and explain the 753 baseline validation errors."),
        ("Slide 19 (Module Status)", "Demonstrate that 13 out of 14 modules (92.9%) are fully implemented and verified in code."),
        ("Slide 20 (Signal & Shift Evidence)", "Show the PSI drift measurements (PSI=0.766 for packet length) and explain that the model fails silently with 96.8% confidence."),
        ("Slide 21 (Empirical Results)", "The climax slide: Show that Multi-Factor wins at 1% and 2% budgets (34.26% vs 26.73%), confidence wins at 5%-10%, and OOD alone fails."),
        ("Slide 22 (Limitations & Phase-2)", "Be honest: review oracle is simulated, signal weights are heuristic. State Phase-2 plans (SHAP, calibration, UI)."),
        ("Slide 23 & 24 (References)", "Conclude with 10 peer-reviewed papers in IEEE format, plus textbook and software citations.")
    ]

    t_slide_data = [[Paragraph("<b>Slide</b>", th_style), Paragraph("<b>What to Say Informally in 1-2 Sentences</b>", th_style)]]
    for s_title, s_talk in slide_talks:
        t_slide_data.append([
            Paragraph(f"<b>{s_title}</b>", tc_left_b),
            Paragraph(s_talk, tc_left)
        ])
    t_slides = Table(t_slide_data, colWidths=[1.8*inch, 5.2*inch])
    t_slides.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, CARD_ALT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_slides)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 8: MENTOR Q&A DEFENSE CHEAT-SHEET
    # -------------------------------------------------------------
    story.append(Paragraph("8. Anticipated Mentor Questions & Bulletproof Answers", h1))
    
    qa_list = [
        ("Mentor Q1: \"Why didn't you just retrain the machine learning model on new data?\"",
         "<b>Your Answer:</b> In production, retraining requires newly labeled ground-truth data, which takes days or weeks to curate and audit. "
         "Our framework operates <i>in real time at inference time</i>. It decides which incoming predictions are too dangerous to trust right now, "
         "routing them to human analysts today before any retraining cycle can take place."),

        ("Mentor Q2: \"Why did OOD detection perform so terribly (0.03% capture)? Did your code have a bug?\"",
         "<b>Your Answer:</b> No, sir. We thoroughly debugged this: in high-throughput network data, the highest Mahalanobis distances correspond to "
         "extreme feature outliers—like high-bandwidth file downloads or large MTU transfers. These flows are statistically rare, but they are completely "
         "benign and correctly classified by XGBoost! In fact, Decile 9 of OOD distance had only 12 errors (0.16% error rate), whereas Decile 7 had 1,799 errors. "
         "This proves an important scientific finding: novelty in feature space does not equal classification error in network security."),

        ("Mentor Q3: \"How did you pick the signal weights for the Multi-Factor strategy? Are they learned?\"",
         "<b>Your Answer:</b> In Phase 1, the weights are experimentally defined heuristics (e.g., 50% uncertainty + 50% OOD percentile rank, and regime-based "
         "scaling where drift and feedback increase the historical mistake weight). We do NOT claim they are globally optimal. In Phase 2, one of our key "
         "objectives is to replace heuristic weights with bilevel optimization or learned routing policies incorporating cost matrices."),

        ("Mentor Q4: \"Why are precision and F1 low on validation (Precision = 0.04, F1 = 0.05)? Is the model broken?\"",
         "<b>Your Answer:</b> The validation split has severe class imbalance: only 248 attacks out of 75,000 flows (0.33% prevalence). When prevalence is that low, "
         "any standard threshold produces false alarms that depress raw precision. However, the model's <b>ROC-AUC is 0.9228</b>, which confirms high ranking ability. "
         "More importantly, our project's goal is not to produce a flawless stand-alone classifier, but to build an efficient <i>review allocation mechanism</i> "
         "that intercepts the errors the classifier does make."),

        ("Mentor Q5: \"Are you testing this on live Internet traffic?\"",
         "<b>Your Answer:</b> No, sir. This is evaluated on an offline research benchmark—the 2026 BigFlow-NIDS dataset. Evaluating on a reproducible benchmark "
         "allows exact ground-truth comparison against all 3,427 errors across 4 fixed budgets. Live network taps are explicitly out-of-scope for Phase 1.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, q_style))
        story.append(Paragraph(a, a_style))

    story.append(Spacer(1, 8))

    # -------------------------------------------------------------
    # SECTION 9: PHASE-2 ROADMAP
    # -------------------------------------------------------------
    story.append(Paragraph("9. Phase-2 Roadmap: What Will You Do Next?", h1))
    story.append(Paragraph("When concluding your conversation with your mentor, clearly present these four Phase-2 objectives:", body))
    story.append(Paragraph("• <b>1. Multi-Domain Tabular Generalization:</b> Expand from network intrusion to medical diagnosis (e.g., MIMIC-IV) and financial fraud (Credit Card Fraud) to show that the multi-factor triage engine is dataset-agnostic.", bullet))
    story.append(Paragraph("• <b>2. Post-Hoc Probability Calibration:</b> Implement temperature scaling and conformal prediction (Guo et al. [5], Geifman & El-Yaniv [4]) to bound error rates with formal statistical coverage guarantees.", bullet))
    story.append(Paragraph("• <b>3. Instance-Level Explainability (SHAP):</b> Attach SHAP feature attributions to routed alerts so the human reviewer can see <i>why</i> a packet was escalated in under 10 seconds.", bullet))
    story.append(Paragraph("• <b>4. Interactive Web Dashboard (FR14):</b> Deliver a lightweight Streamlit interface allowing administrators to slide human budget quotas (1% to 10%) and observe triage queues in real time.", bullet))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Successfully built Mentor Guide PDF: {PDF_PATH}")
    print(f"     File size: {os.path.getsize(PDF_PATH):,} bytes")

if __name__ == "__main__":
    build_guide_pdf()
