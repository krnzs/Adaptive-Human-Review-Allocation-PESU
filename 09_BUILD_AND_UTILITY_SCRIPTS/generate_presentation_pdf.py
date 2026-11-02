import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PDF_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pdf")
PDF_CREATIVE_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU_Creative.pdf")

PAGE_WIDTH = 13.333 * 72 # 960 pt
PAGE_HEIGHT = 7.5 * 72   # 540 pt

NAVY = colors.HexColor("#0B192C")
ACCENT_BLUE = colors.HexColor("#0066CC")
DARK_GRAY = colors.HexColor("#334155")
LIGHT_BG = colors.HexColor("#F8FAFC")
WHITE = colors.HexColor("#FFFFFF")
BORDER_GRAY = colors.HexColor("#CBD5E1")
GREEN = colors.HexColor("#16A34A")
RED = colors.HexColor("#DC2626")
ROW_ALT = colors.HexColor("#F1F5F9")
BG_CODE = colors.HexColor("#F1F5F9")

class SlideNumberedCanvas(canvas.Canvas):
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, num_pages):
        self.saveState()
        # Top banner
        self.setFillColor(NAVY)
        self.rect(0, PAGE_HEIGHT - 8, PAGE_WIDTH, 8, stroke=0, fill=1)

        # PES Logo on top right of EVERY slide
        if os.path.exists(LOGO_PATH):
            try:
                self.drawImage(LOGO_PATH, PAGE_WIDTH - 160, PAGE_HEIGHT - 52, width=130, height=42, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass

        # Footer
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(DARK_GRAY)
        self.drawString(50, 20, "PES UNIVERSITY  |  MCA DATA ANALYTICS  |  SRN: PES1PG25CA101  |  GUIDE: PROF. DILIP KUMAR MARIPURI")
        
        page_str = f"Slide {self._pageNumber} of {num_pages}"
        self.drawRightString(PAGE_WIDTH - 50, 20, page_str)

        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.5)
        self.line(50, 32, PAGE_WIDTH - 50, 32)
        self.restoreState()

def build_pdf():
    target_path = PDF_PATH
    try:
        with open(PDF_PATH, "ab"):
            pass
    except Exception:
        target_path = PDF_CREATIVE_PATH
        print(f"Original PDF is currently locked in reader. Writing to: {target_path}")

    doc = SimpleDocTemplate(
        target_path,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=50,
        rightMargin=50,
        topMargin=55,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'SlideCategory',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=ACCENT_BLUE,
        spaceAfter=3
    )

    card_title_style = ParagraphStyle(
        'CardTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_GRAY
    )

    body_bold = ParagraphStyle(
        'SlideBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'SlideCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=DARK_GRAY
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=DARK_GRAY
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=WHITE
    )

    story = []

    def make_header(title, category="PHASE-1 CAPSTONE PRESENTATION-2"):
        return [
            Paragraph(category.upper(), subtitle_style),
            Paragraph(title, title_style)
        ]

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)", subtitle_style))
    story.append(Paragraph("Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift", ParagraphStyle(
        'MainTitle',
        parent=title_style,
        fontSize=24,
        leading=30,
        spaceAfter=10
    )))
    story.append(Paragraph("Course Code: UQ25CA741A  |  Department of Computer Applications  |  PES University, Bangalore", body_bold))
    story.append(Spacer(1, 25))

    student_info = [
        Paragraph("<b>STUDENT RESEARCHER</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>Program:</b> Master of Computer Applications (MCA)<br/>"
                  "<b>Specialization:</b> Data Analytics<br/>"
                  "<b>Candidate SRN:</b> PES1PG25CA101<br/>"
                  "<b>Institution:</b> PES University, Bangalore", body_style)
    ]
    guide_info = [
        Paragraph("<b>FACULTY PROJECT GUIDE</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>Faculty Guide:</b><br/>"
                  "<b>Prof. Dilip Kumar Maripuri</b><br/>"
                  "Department of Computer Applications<br/>"
                  "PES University, Bangalore", body_style)
    ]

    meta_table = Table([[student_info, guide_info]], colWidths=[420, 420])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 2: ABSTRACT
    # ==========================================
    story.extend(make_header("Abstract: Research Context & Scope"))

    abs_content = [
        Paragraph("<b>PROBLEM:</b> Machine-learning systems can produce high prediction volumes, but manual verification capacity is strictly limited (typically 1% to 5% of traffic). Furthermore, models can make confident errors when the data distribution changes over time.<br/><br/>"
                  "<b>APPROACH:</b> This work investigates an experimental framework for adaptive human-review allocation. Instead of relying solely on prediction confidence, the system combines four complementary reliability signals: prediction uncertainty, out-of-distribution distance, feature-level drift, and historical mistake pattern proximity.<br/><br/>"
                  "<b>EXPERIMENT:</b> We implement the pipeline and evaluate it on a 500,000-flow development sample extracted from the BigFlow-NIDS derived benchmark using a chronological train/validation/shifted-test partition.<br/><br/>"
                  "<b>OBSERVATION:</b> The experiments indicate that multi-factor prioritization captures more errors at tight review budgets (1%–2%), while confidence-based prioritization captures more errors at larger budgets (5%–10%). Under the tested conditions, review effectiveness varies with the available budget.<br/><br/>"
                  "<b>LIMITATION / FUTURE WORK:</b> Current experiments evaluate a binary classification prototype with simulated review feedback on one benchmark. Phase 2 will investigate generalization across diverse tabular datasets and explainability.", body_style)
    ]
    t2 = Table([[abs_content]], colWidths=[850])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    story.extend(make_header("Introduction: Problem Scenario & Purpose"))

    i_p1 = [
        Paragraph("<b>PROBLEM SCENARIO</b>", ParagraphStyle('H', parent=card_title_style, textColor=NAVY)),
        Paragraph("<b>High-Volume ML Inferences:</b><br/>"
                  "• Machine learning systems produce large volumes of predictions daily.<br/>"
                  "• Manual verification of every output is impractical due to constrained human capacity.<br/>"
                  "• In practice, organizations can inspect only a tiny fraction (e.g., 1%–5%) of predictions.", body_style)
    ]
    i_p2 = [
        Paragraph("<b>THE CHALLENGE</b>", ParagraphStyle('H', parent=card_title_style, textColor=RED)),
        Paragraph("<b>Overconfidence Under Shift:</b><br/>"
                  "• When input data distributions change, model accuracy often drops.<br/>"
                  "• Crucially, prediction confidence alone may not reflect true reliability under shift.<br/>"
                  "• Models can make high-confidence mistakes on drifted or unfamiliar inputs.", body_style)
    ]
    i_p3 = [
        Paragraph("<b>PROPOSED IDEA</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>Multi-Signal Review Allocation:</b><br/>"
                  "• Combine multiple complementary reliability signals rather than relying on one.<br/>"
                  "• Consider prediction confidence, OOD novelty, feature drift, and historical mistakes.<br/>"
                  "• Score and rank predictions to prioritize the most uncertain cases for review.", body_style)
    ]
    i_p4 = [
        Paragraph("<b>PURPOSE & SCOPE</b>", ParagraphStyle('H', parent=card_title_style, textColor=GREEN)),
        Paragraph("<b>Investigating Capacity Trade-Offs:</b><br/>"
                  "• Study whether adaptive review allocation concentrates human attention on errors.<br/>"
                  "• Evaluate trade-offs under explicit, constrained operational review budgets.<br/>"
                  "• Scope of Phase 1: Prototype validation using an offline chronological benchmark.", body_style)
    ]

    t3 = Table([[i_p1, i_p2], [i_p3, i_p4]], colWidths=[420, 420])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('BOX', (0,1), (0,1), 1, BORDER_GRAY),
        ('BOX', (1,1), (1,1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t3)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 4: CORE CONCEPTUAL PIPELINE
    # ==========================================
    story.extend(make_header("Core Concept: Human-Review Allocation Pipeline"))

    c4_banner = [
        Paragraph("<b>CORE PROJECT EXPLANATION</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<i>\"Machine-learning systems can generate very large numbers of predictions, but humans cannot manually verify all of them. This project investigates whether multiple reliability signals can be used to prioritize predictions for human review when review capacity is limited, particularly when the data distribution changes.\"</i>", body_style)
    ]
    t4_b = Table([[c4_banner]], colWidths=[850])
    t4_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 1, ACCENT_BLUE),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t4_b)
    story.append(Spacer(1, 10))

    arch_img = os.path.join(DIAGRAMS_DIR, "diagram_system_architecture.png")
    if os.path.exists(arch_img):
        story.append(RLImage(arch_img, width=850, height=290))
    story.append(PageBreak())

    # ==========================================
    # SLIDE 5: BACKGROUND STUDY
    # ==========================================
    story.extend(make_header("Background Study & Theoretical Foundations"))

    bg_c1 = [
        Paragraph("<b>1. SELECTIVE PREDICTION</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>Risk-Coverage Trade-Offs:</b><br/>"
                  "• Formulated by Geifman & El-Yaniv (2017) to allow models to abstain when uncertain.<br/>"
                  "• Evaluates accuracy on accepted predictions as a function of coverage.<br/>"
                  "• Limitation: Primarily relies on prediction confidence, which can degrade under shift.", body_style)
    ]
    bg_c2 = [
        Paragraph("<b>2. MODEL MISCALIBRATION</b>", ParagraphStyle('H', parent=card_title_style, textColor=RED)),
        Paragraph("<b>Overconfidence Under Shift:</b><br/>"
                  "• Guo et al. (2017) demonstrated modern classifiers produce overconfident probabilities.<br/>"
                  "• Softmax scores often remain high even on incorrect predictions.<br/>"
                  "• Motivates supplementing confidence with data-centric reliability signals.", body_style)
    ]
    bg_c3 = [
        Paragraph("<b>3. OUT-OF-DISTRIBUTION DETECTION</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>Distance-Based Novelty:</b><br/>"
                  "• Lee et al. (2018) and Yang et al. (2024) use feature-space distances for OOD detection.<br/>"
                  "• Identifies inputs that deviate from the training manifold regardless of softmax score.<br/>"
                  "• Helps detect unfamiliar instances that confidence alone might overlook.", body_style)
    ]
    bg_c4 = [
        Paragraph("<b>4. LEARNING TO DEFER</b>", ParagraphStyle('H', parent=card_title_style, textColor=GREEN)),
        Paragraph("<b>Human-AI Decision Systems:</b><br/>"
                  "• Mozannar & Sontag (2020) and Charusaie et al. (2022) model algorithmic deferral.<br/>"
                  "• Balances machine predictions against expert review under operational costs.<br/>"
                  "• Directly motivates our budget-constrained review allocation setup.", body_style)
    ]

    t5 = Table([[bg_c1, bg_c2], [bg_c3, bg_c4]], colWidths=[420, 420])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('BOX', (0,1), (0,1), 1, BORDER_GRAY),
        ('BOX', (1,1), (1,1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t5)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 6: LITERATURE SURVEY (10 Verified Papers)
    # ==========================================
    story.extend(make_header("Literature Survey: 10 Verified Research Papers"))

    papers_data = [
        [Paragraph("<b>Paper Title</b>", table_header), Paragraph("<b>Authors</b>", table_header), Paragraph("<b>Venue & Year</b>", table_header), Paragraph("<b>Summary & Project Relevance</b>", table_header)],
        [Paragraph("BigFlow-NIDS: Large-Scale Benchmark Dataset", table_cell), Paragraph("Mendeley / Data in Brief", table_cell), Paragraph("Elsevier 2026", table_cell), Paragraph("66.9M flow derived benchmark. Used as our primary offline evaluation benchmark.", table_cell)],
        [Paragraph("Consistent Estimators for Learning to Defer to an Expert", table_cell), Paragraph("H. Mozannar, D. Sontag", table_cell), Paragraph("ICML 2020", table_cell), Paragraph("Theoretical formulation of learning to defer. Foundational basis for human-AI routing.", table_cell)],
        [Paragraph("Deep Learning to Defer with Multiple Experts", table_cell), Paragraph("D. Wei et al.", table_cell), Paragraph("ICML 2024", table_cell), Paragraph("Extends deferral to multi-expert pools. Informs multi-tiered review routing.", table_cell)],
        [Paragraph("Selective Classification for Deep Neural Networks", table_cell), Paragraph("Y. Geifman, R. El-Yaniv", table_cell), Paragraph("NeurIPS 2017", table_cell), Paragraph("Formulates risk-coverage trade-offs for confidence-based abstention baselines.", table_cell)],
        [Paragraph("On Calibration of Modern Neural Networks", table_cell), Paragraph("C. Guo et al.", table_cell), Paragraph("ICML 2017", table_cell), Paragraph("Demonstrates model miscalibration and overconfidence under distribution shift.", table_cell)],
        [Paragraph("Conformal Prediction & Distribution-Free UQ", table_cell), Paragraph("A. Angelopoulos, S. Bates", table_cell), Paragraph("arXiv / Survey 2021", table_cell), Paragraph("Establishes finite-sample distribution-free uncertainty intervals.", table_cell)],
        [Paragraph("Generalized Out-of-Distribution Detection: A Survey", table_cell), Paragraph("J. Yang et al.", table_cell), Paragraph("IEEE TPAMI 2024", table_cell), Paragraph("Comprehensive taxonomy of OOD detection across feature and logit spaces.", table_cell)],
        [Paragraph("Simple Unified Framework for OOD Detection", table_cell), Paragraph("K. Lee et al.", table_cell), Paragraph("NeurIPS 2018", table_cell), Paragraph("Utilizes Mahalanobis distance in feature space for robust OOD identification.", table_cell)],
        [Paragraph("WILDS: Benchmark of In-The-Wild Distribution Shifts", table_cell), Paragraph("P. W. Koh et al.", table_cell), Paragraph("ICML 2021", table_cell), Paragraph("Evaluates model collapse across real-world shifts. Motivates temporal evaluation.", table_cell)],
        [Paragraph("Sample Efficient Learning to Defer", table_cell), Paragraph("M. Charusaie et al.", table_cell), Paragraph("NeurIPS 2022", table_cell), Paragraph("Formulates budget-constrained expert query allocation under cost limits.", table_cell)]
    ]

    t6 = Table(papers_data, colWidths=[240, 160, 110, 340])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t6)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 7: COMPARATIVE STUDY
    # ==========================================
    story.extend(make_header("Comparative Study of Reliability Paradigms"))

    matrix_data = [
        [Paragraph("<b>Evaluation Dimension</b>", table_header), Paragraph("<b>Random Review</b>", table_header), Paragraph("<b>Confidence Threshold</b>", table_header), Paragraph("<b>OOD Filter</b>", table_header), Paragraph("<b>Learning to Defer</b>", table_header), Paragraph("<b>Proposed Framework</b>", table_header)],
        [Paragraph("Confidence-based reliability", table_cell), Paragraph("No", table_cell), Paragraph("Yes (Primary)", table_cell), Paragraph("No", table_cell), Paragraph("Optional", table_cell), Paragraph("<b>Yes (Normalized)</b>", table_cell)],
        [Paragraph("OOD / Novelty detection", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("Yes (Primary)", table_cell), Paragraph("Rarely", table_cell), Paragraph("<b>Yes (Mahalanobis)</b>", table_cell)],
        [Paragraph("Distribution drift measurement", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("<b>Yes (Feature PSI)</b>", table_cell)],
        [Paragraph("Historical error tracking", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("Implicit", table_cell), Paragraph("<b>Yes (Mistake Proximity)</b>", table_cell)],
        [Paragraph("Budget-aware evaluation", table_cell), Paragraph("Implicit", table_cell), Paragraph("Manual tuning", table_cell), Paragraph("Hard cutoff", table_cell), Paragraph("Theoretical", table_cell), Paragraph("<b>Yes (1%, 2%, 5%, 10%)</b>", table_cell)],
        [Paragraph("Evaluated under temporal shift", table_cell), Paragraph("Yes", table_cell), Paragraph("Rarely", table_cell), Paragraph("Partial", table_cell), Paragraph("Rarely", table_cell), Paragraph("<b>Yes (Chronological)</b>", table_cell)]
    ]

    t7 = Table(matrix_data, colWidths=[200, 110, 130, 130, 130, 150])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-2,0), NAVY),
        ('BACKGROUND', (-1,0), (-1,0), ACCENT_BLUE),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t7)
    story.append(Spacer(1, 15))

    c7_note = Paragraph("<b>Comparative Synthesis:</b> Existing approaches emphasize different aspects of prediction reliability. This project investigates combining several complementary signals within an adaptive review-allocation framework evaluated under constrained human-review budgets.", body_style)
    t7_n = Table([[c7_note]], colWidths=[850])
    t7_n.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(t7_n)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 8: PRIMARY DATASET
    # ==========================================
    story.extend(make_header("Primary Research Dataset: BigFlow-NIDS Benchmark"))

    ds_c1 = [
        Paragraph("<b>BENCHMARK SPECIFICATIONS</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("• <b>Derived Benchmark:</b> Constructed by integrating four established NetFlow datasets (NF-UNSW-NB15-v3, NF-ToN-IoT-v3, NF-BoT-IoT-v3, NF-CSE-CIC-IDS2018-v3) using Apache Spark.<br/>"
                  "• <b>Full Benchmark Scale:</b> 66,935,021 network flow records, 55 attributes, and 32 attack categories.<br/>"
                  "• <b>Current Development Data:</b> A 500,000-flow development sample extracted from the benchmark for offline model development and experimentation.<br/>"
                  "• <b>Publication Details:</b> Published in Data in Brief / Mendeley Data (2026), DOI: 10.1016/j.dib.2026.112530.<br/>"
                  "• <b>Important Clarification:</b> BigFlow-NIDS is an offline scientific benchmark used for controlled evaluation, not live uncurated Internet traffic.", body_style)
    ]
    ds_c2 = [
        Paragraph("<b>DATASET STRUCTURE IN CURRENT EXPERIMENTS</b>", ParagraphStyle('H', parent=card_title_style, textColor=NAVY)),
        Paragraph("• <b>Development Volume:</b> 500,000 network flows in CSV and compressed Parquet format.<br/>"
                  "• <b>Observation Ordering:</b> Preserves chronological flow sequence to study temporal shifts.<br/>"
                  "• <b>Task Formulation:</b> Binary classification: Benign vs. Attack.<br/>"
                  "• <b>Ground-Truth Oracles:</b> The Label column serves as the evaluation oracle to assess model accuracy and simulated review efficiency.<br/>"
                  "• <b>Offline Rigor:</b> Evaluated locally without external network dependencies, ensuring fully reproducible experimental runs.", body_style)
    ]

    t8 = Table([[ds_c1, ds_c2]], colWidths=[420, 420])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t8)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 9: DATA / X / Y FORMULATION
    # ==========================================
    story.extend(make_header("Feature Space (X) and Target Formulation (Y)"))

    x_col = [
        Paragraph("<b>INPUT FEATURE SPACE (X)</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<b>49 Numerical Network-Flow Features:</b><br/>"
                  "• <b>Connection Identifiers:</b> Source Port, Destination Port, Protocol.<br/>"
                  "• <b>Volume Statistics:</b> Inward Bytes, Outward Bytes, Packet Counts.<br/>"
                  "• <b>Throughput & Rate Metrics:</b> Source-to-Destination Average Throughput, Flow Duration.<br/>"
                  "• <b>Timing Characteristics:</b> Packet Inter-Arrival Time (IAT) statistics (Min, Max, Mean, Std).<br/>"
                  "• <b>TCP Flags & Packet Lengths:</b> TCP Flags, Window Max In, Shortest Flow Packet, Max IP Packet Length.", body_style)
    ]
    y_col = [
        Paragraph("<b>TARGET FORMULATION (Y)</b>", ParagraphStyle('H', parent=card_title_style, textColor=NAVY)),
        Paragraph("<b>Binary Classification Target: Label</b><br/>"
                  "• <b>Class 0 (Benign):</b> Normal legitimate network traffic.<br/>"
                  "• <b>Class 1 (Attack):</b> Malicious activity / security events.<br/><br/>"
                  "<b>Attack Column Handling:</b><br/>"
                  "• The dataset includes a detailed multi-class Attack column (e.g., DDoS, Exploits, Fuzzers, Reconnaissance).<br/>"
                  "• The detailed Attack category was excluded from the binary prediction model to prevent label leakage.<br/>"
                  "• Used post-prediction for error analysis and diagnostic inspection.", body_style)
    ]

    t9 = Table([[x_col, y_col]], colWidths=[420, 420])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t9)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 10: EXPERIMENTAL DESIGN
    # ==========================================
    story.extend(make_header("Experimental Design: Chronological Partitioning"))

    time_img = os.path.join(DIAGRAMS_DIR, "diagram_temporal_shift_timeline.png")
    if os.path.exists(time_img):
        story.append(RLImage(time_img, width=850, height=270))
        story.append(Spacer(1, 10))

    c10_rat = [
        Paragraph("<b>RATIONALE FOR CHRONOLOGICAL SPLITTING</b>", card_title_style),
        Paragraph("• Standard random splitting shuffles past and future events together, which can artificially mask temporal distribution drift.<br/>"
                  "• Chronological splitting evaluates model behavior on later observations, reflecting how models operate after initial deployment.<br/>"
                  "• Note: This setup simulates temporal non-stationarity within the benchmark; it does not claim to represent every possible real-world shift.", body_style)
    ]
    t10_r = Table([[c10_rat]], colWidths=[850])
    t10_r.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(t10_r)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 11: MODEL DEVELOPMENT
    # ==========================================
    story.extend(make_header("Model Development & Validation Comparison"))

    model_data = [
        [Paragraph("<b>Model Architecture</b>", table_header), Paragraph("<b>Accuracy</b>", table_header), Paragraph("<b>Precision</b>", table_header), Paragraph("<b>Recall</b>", table_header), Paragraph("<b>F1-Score</b>", table_header), Paragraph("<b>ROC-AUC</b>", table_header)],
        [Paragraph("Logistic Regression", table_cell), Paragraph("0.9606", table_cell), Paragraph("0.0376", table_cell), Paragraph("0.4435", table_cell), Paragraph("0.0693", table_cell), Paragraph("0.7499", table_cell)],
        [Paragraph("Random Forest", table_cell), Paragraph("0.9801", table_cell), Paragraph("0.0708", table_cell), Paragraph("0.4153", table_cell), Paragraph("0.1210", table_cell), Paragraph("0.8526", table_cell)],
        [Paragraph("<b>XGBoost (Selected Primary)</b>", table_cell), Paragraph("0.9899", table_cell), Paragraph("0.0401", table_cell), Paragraph("0.0887", table_cell), Paragraph("0.0552", table_cell), Paragraph("<b>0.9228</b>", table_cell)]
    ]
    t11 = Table(model_data, colWidths=[230, 120, 120, 120, 120, 140])
    t11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t11)
    story.append(Spacer(1, 15))

    c11_note = [
        Paragraph("<b>MODEL SELECTION & EVALUATION NOTES</b>", card_title_style),
        Paragraph("• <b>Validation Class Imbalance:</b> Attack prevalence in the validation split is approximately 0.33% (248 attacks in 75,000 flows). Because of this severe class imbalance, accuracy alone is insufficient for model selection.<br/>"
                  "• <b>Selection Rationale:</b> XGBoost was selected as the primary classifier for subsequent reliability experiments based on its validation ROC-AUC of 0.9228, indicating stronger probability ranking across thresholds.<br/>"
                  "• <b>Downstream Pipeline Role:</b> The reliability analysis pipeline operates downstream of XGBoost probability outputs, evaluating predicted instances under fixed human-review budgets.", body_style)
    ]
    t11_n = Table([[c11_note]], colWidths=[850])
    t11_n.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t11_n)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 12: FOUR RELIABILITY SIGNALS
    # ==========================================
    story.extend(make_header("Four Complementary Reliability Signals"))

    s12_c1 = [
        Paragraph("<b>1. PREDICTION CONFIDENCE</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<i>\"How certain is the model about its prediction?\"</i><br/><br/>"
                  "• Computed from class probabilities: 1.0 - max P(y|x).<br/>"
                  "• Reflects proximity to the model decision boundary.<br/>"
                  "• Captures traditional classification ambiguity under stationary distributions.", body_style)
    ]
    s12_c2 = [
        Paragraph("<b>2. OUT-OF-DISTRIBUTION (OOD)</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<i>\"Does the input look unusual compared with the training reference?\"</i><br/><br/>"
                  "• Mahalanobis-like distance relative to the training centroid and covariance.<br/>"
                  "• Measures distance to the reference training manifold in feature space.<br/>"
                  "• Flags novel patterns that may yield overconfident misclassifications.", body_style)
    ]
    s12_c3 = [
        Paragraph("<b>3. DISTRIBUTION DRIFT</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<i>\"Has the feature distribution changed relative to the reference data?\"</i><br/><br/>"
                  "• Evaluated using Population Stability Index (PSI) across features.<br/>"
                  "• Quantifies aggregate shift between reference and batch distributions.<br/>"
                  "• Weights inputs higher if heavily drifted features are prominent.", body_style)
    ]
    s12_c4 = [
        Paragraph("<b>4. HISTORICAL ERROR RISK</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("<i>\"Has the model historically made errors on similar patterns?\"</i><br/><br/>"
                  "• Measures distance to patterns where the model made errors during training.<br/>"
                  "• Assigns higher risk to inputs resembling known historical mistake clusters.<br/>"
                  "• Combines with other signals into an adaptive review risk score.", body_style)
    ]

    t12 = Table([[s12_c1, s12_c2], [s12_c3, s12_c4]], colWidths=[420, 420])
    t12.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('BOX', (0,1), (0,1), 1, BORDER_GRAY),
        ('BOX', (1,1), (1,1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t12)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 13: SIMULATED HUMAN REVIEW
    # ==========================================
    story.extend(make_header("Simulated Human Review & Allocation Strategies"))

    hr_left = [
        Paragraph("<b>CRITICAL EXPERIMENTAL CLARIFICATION</b>", ParagraphStyle('H', parent=card_title_style, textColor=RED)),
        Paragraph("• <b>Simulated Review Setup:</b> Human review is simulated using ground-truth labels for experimental evaluation. Actual human participants were not recruited.<br/>"
                  "• <b>Oracle Evaluation:</b> Ground-truth labels serve as an evaluation oracle to assess whether prioritized predictions contained genuine model errors.<br/>"
                  "• <b>Capacity-Constrained Budgets:</b> Review capacity is evaluated at fixed enterprise percentages of total test records (75,000 flows):<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;• <i>1% Review Budget:</i> Review top 750 predictions.<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;• <i>2% Review Budget:</i> Review top 1,500 predictions.<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;• <i>5% Review Budget:</i> Review top 3,750 predictions.<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;• <i>10% Review Budget:</i> Review top 7,500 predictions.", body_style)
    ]
    hr_right = [
        Paragraph("<b>FIVE REVIEW STRATEGIES COMPARED</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("1. <b>Random Review:</b> Selects predictions uniformly at random as a naive baseline.<br/>"
                  "2. <b>Confidence-Based Review:</b> Prioritizes predictions with the lowest model confidence (highest output uncertainty).<br/>"
                  "3. <b>OOD-Based Review:</b> Prioritizes predictions with the highest Mahalanobis distance from training references.<br/>"
                  "4. <b>Static Multi-Factor Review:</b> Ranks predictions by a static weighted combination of all four reliability signals.<br/>"
                  "5. <b>Feedback-Informed Adaptive Review:</b> Dynamically adjusts signal weights based on feedback from earlier reviews.<br/><br/>"
                  "<b>Research Objective:</b> The purpose is to study strategy behavior across budgets, not to declare a universally superior strategy.", body_style)
    ]

    t13 = Table([[hr_left, hr_right]], colWidths=[420, 420])
    t13.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t13)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 14: SHIFTED TEST OBSERVATIONS
    # ==========================================
    story.extend(make_header("Shifted-Test Observations & Model Challenge"))

    shift_data = [
        [Paragraph("<b>Metric / Dimension</b>", table_header), Paragraph("<b>Validation Split (75K)</b>", table_header), Paragraph("<b>Shifted Test Split (75K)</b>", table_header), Paragraph("<b>Empirical Observation</b>", table_header)],
        [Paragraph("Attack Prevalence", table_cell), Paragraph("≈ 0.33% (248 attacks)", table_cell), Paragraph("<b>≈ 6.30% (4,725 attacks)</b>", table_cell), Paragraph("Substantial surge in malicious flow volume", table_cell)],
        [Paragraph("Model Prediction Errors", table_cell), Paragraph("753 errors", table_cell), Paragraph("<b>3,427 errors</b>", table_cell), Paragraph("4.55× increase in classification mistakes", table_cell)],
        [Paragraph("Model Error Rate", table_cell), Paragraph("≈ 1.00%", table_cell), Paragraph("<b>≈ 4.57%</b>", table_cell), Paragraph("Higher operational error rate in later period", table_cell)],
        [Paragraph("Average Model Confidence", table_cell), Paragraph("≈ 98.65%", table_cell), Paragraph("<b>≈ 96.82%</b>", table_cell), Paragraph("Model remains overconfident despite error surge", table_cell)]
    ]
    t14 = Table(shift_data, colWidths=[200, 180, 190, 280])
    t14.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t14)
    story.append(Spacer(1, 15))

    c14_note = [
        Paragraph("<b>RESEARCH TAKEAWAY</b>", card_title_style),
        Paragraph("• The chronological evaluation reveals a substantial change in prediction behavior between the validation and later shifted-test periods.<br/>"
                  "• The later test period was more challenging for the trained model, motivating the evaluation of reliability-aware review strategies.<br/>"
                  "• Note: We state that the later period was more challenging; we do not claim that temporal shift alone mathematically caused every performance change.", body_style)
    ]
    t14_n = Table([[c14_note]], colWidths=[850])
    t14_n.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t14_n)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 15: SHIFTED TEST EXPERIMENTAL RESULTS
    # ==========================================
    story.extend(make_header("Shifted-Test Experimental Results"))

    res_table_data = [
        [Paragraph("<b>Review Budget</b>", table_header), Paragraph("<b>Reviews Sliced</b>", table_header), Paragraph("<b>Confidence-Based</b>", table_header), Paragraph("<b>Static Multi-Factor</b>", table_header), Paragraph("<b>Feedback Adaptive</b>", table_header)],
        [Paragraph("1% Review Budget", table_cell), Paragraph("750 predictions", table_cell), Paragraph("13.51%", table_cell), Paragraph("17.51%", table_cell), Paragraph("<b>17.80%</b>", table_cell)],
        [Paragraph("2% Review Budget", table_cell), Paragraph("1,500 predictions", table_cell), Paragraph("26.73%", table_cell), Paragraph("33.99%", table_cell), Paragraph("<b>34.26%</b>", table_cell)],
        [Paragraph("5% Review Budget", table_cell), Paragraph("3,750 predictions", table_cell), Paragraph("<b>65.45%</b>", table_cell), Paragraph("54.57%", table_cell), Paragraph("45.90%", table_cell)],
        [Paragraph("10% Review Budget", table_cell), Paragraph("7,500 predictions", table_cell), Paragraph("<b>84.01%</b>", table_cell), Paragraph("65.42%", table_cell), Paragraph("52.35%", table_cell)]
    ]
    t15 = Table(res_table_data, colWidths=[170, 170, 170, 170, 170])
    t15.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t15)
    story.append(Spacer(1, 15))

    c15_note = [
        Paragraph("<b>EMPIRICAL FINDINGS & SCIENTIFIC OBSERVATIONS</b>", ParagraphStyle('H', parent=card_title_style, textColor=RED)),
        Paragraph("• <b>The relative effectiveness of the strategies changes with the available review budget.</b><br/>"
                  "• At lower review budgets (1%–2%), the multi-factor strategies captured more errors in this experiment.<br/>"
                  "• At larger review budgets (5%–10%), confidence-based prioritization captured more errors.<br/>"
                  "• This is an important scientific observation: review allocation strategy should be budget-aware rather than assumed to be universally optimal.", body_style)
    ]
    t15_n = Table([[c15_note]], colWidths=[850])
    t15_n.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t15_n)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 16: RESULTS VISUALIZATION
    # ==========================================
    story.extend(make_header("Results Visualization: Error Capture Curves"))

    chart_img = os.path.join(DIAGRAMS_DIR, "diagram_results_line_chart.png")
    c16_left = [RLImage(chart_img, width=520, height=310)] if os.path.exists(chart_img) else [Paragraph("Line chart generated in diagrams.", body_style)]

    c16_right = [
        Paragraph("<b>INTERPRETATION</b>", card_title_style),
        Paragraph("<i>\"Review strategy effectiveness is budget-dependent.\"</i><br/><br/>"
                  "• <b>Budget-Dependent Crossover:</b> At tight budgets (1%–2%), incorporating OOD and drift signals prioritizes high-risk anomalies that confidence alone misses.<br/><br/>"
                  "• <b>Decision Boundary Saturation:</b> At larger budgets (5%–10%), confidence thresholding aggregates instances near the decision boundary, capturing broader classification ambiguity.<br/><br/>"
                  "• <b>No Universal Winner:</b> The experiment shows that no single strategy remains superior across all budgets, supporting the hypothesis that review allocation mechanisms must be budget-aware.", body_style)
    ]

    t16 = Table([[c16_left, c16_right]], colWidths=[530, 320])
    t16.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t16)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 17: IMPLEMENTED PROTOTYPE
    # ==========================================
    story.extend(make_header("Implemented Research Prototype (>50% Verification)"))

    c17_body = [
        Paragraph("<b>CORE IMPLEMENTED COMPONENTS (PHASE 1)</b>", ParagraphStyle('H', parent=card_title_style, textColor=GREEN)),
        Paragraph("<i>Subtitle: Core prediction, reliability analysis, and review-allocation pipeline implemented and experimentally evaluated.</i><br/>", body_style),
        Paragraph("✓ Dataset preprocessing and feature extraction on BigFlow-NIDS<br/>"
                  "✓ Chronological data splitting (350K Train / 75K Val / 75K Shifted Test)<br/>"
                  "✓ Machine learning baseline training (Logistic Regression, Random Forest, XGBoost)<br/>"
                  "✓ Prediction generation and calibrated class probability scoring<br/>"
                  "✓ Reliability signal generation: Prediction uncertainty (1 - max P)<br/>"
                  "✓ Out-of-distribution (OOD) detection using Mahalanobis reference distances<br/>"
                  "✓ Distribution drift analysis using Population Stability Index (PSI)<br/>"
                  "✓ Historical training error proximity and mistake pattern matching<br/>"
                  "✓ Multi-factor adaptive risk scoring and prediction ranking<br/>"
                  "✓ Fixed-budget review allocation (1%, 2%, 5%, 10% slices)<br/>"
                  "✓ Shifted-test evaluation and review efficiency analysis<br/>"
                  "✓ Feedback simulation and interactive experiment dashboard", body_style)
    ]
    t17 = Table([[c17_body]], colWidths=[850])
    t17.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t17)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 18: DASHBOARD
    # ==========================================
    story.extend(make_header("Interactive Experiment & Monitoring Dashboard"))

    dash_left = [
        Paragraph("<b>STREAMLIT INTERACTION MODULES</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("• <b>Interface Characterization:</b> Built as an interactive experiment and monitoring interface for research inspection (not a production monitoring platform).<br/>"
                  "• <b>Review Budget Tuning:</b> Dynamic slider allowing evaluation across 1%, 2%, 5%, and 10% review allocations.<br/>"
                  "• <b>Errors Captured Display:</b> Real-time metric cards and curves showing captured errors across strategies.<br/>"
                  "• <b>Review Efficiency Tracking:</b> Errors captured per 1,000 reviews evaluated across budgets.<br/>"
                  "• <b>Distribution Drift Viewer:</b> Ranks and visualizes features by Population Stability Index (PSI).<br/>"
                  "• <b>Model Comparison View:</b> Confusion matrices, ROC curves, and classification metrics for LR, RF, and XGBoost.", body_style)
    ]

    drift_img = os.path.join(RESULTS_DIR, "top10_drift_features.png")
    dash_right = [RLImage(drift_img, width=440, height=310)] if os.path.exists(drift_img) else [Paragraph("Drift visualization in results.", body_style)]

    t18 = Table([[dash_left, dash_right]], colWidths=[400, 450])
    t18.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t18)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 19: REQUIREMENTS
    # ==========================================
    story.extend(make_header("Functional & Non-Functional Requirements"))

    fr_data = [
        [Paragraph("<b>ID</b>", table_header), Paragraph("<b>Functional Requirement Description</b>", table_header), Paragraph("<b>Status</b>", table_header)],
        [Paragraph("FR1", table_cell), Paragraph("Load and preprocess network-flow benchmark data", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR2", table_cell), Paragraph("Train ML classification models (LR, RF, XGBoost)", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR3", table_cell), Paragraph("Generate predictions and class probabilities", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR4", table_cell), Paragraph("Calculate 4 complementary reliability signals", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR5", table_cell), Paragraph("Calculate adaptive risk score from signals", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR6", table_cell), Paragraph("Rank predictions for human-review prioritization", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR7", table_cell), Paragraph("Apply fixed review budgets (1%, 2%, 5%, 10%)", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR8", table_cell), Paragraph("Compare review strategies against ground truth", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR9", table_cell), Paragraph("Evaluate performance under shifted temporal data", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)],
        [Paragraph("FR10", table_cell), Paragraph("Visualize experimental results on dashboard", table_cell), Paragraph("<b>IMPLEMENTED</b>", table_cell)]
    ]
    t19_fr = Table(fr_data, colWidths=[40, 340, 100])
    t19_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, ROW_ALT]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    nfr_card = [
        Paragraph("<b>NON-FUNCTIONAL REQUIREMENTS</b>", card_title_style),
        Paragraph("• <b>Reproducibility:</b> Deterministic seed setting across model training and chronological splitting.<br/>"
                  "• <b>Scalability for Dev Data:</b> Efficient processing of the 500,000-flow sample on local workstations.<br/>"
                  "• <b>Interpretability:</b> Transparent decomposition of risk scores into confidence, OOD, drift, and historical factors.<br/>"
                  "• <b>Modular Architecture:</b> Decoupled modules for preprocessing, modeling, reliability, and evaluation.<br/>"
                  "• <b>Data Privacy Awareness:</b> Offline processing preventing sensitive network header transmission.<br/>"
                  "• <b>Maintainability & Usability:</b> Clean script modularity with clear parameter configuration in dashboard.", body_style)
    ]

    t19 = Table([[t19_fr, nfr_card]], colWidths=[490, 360])
    t19.setStyle(TableStyle([
        ('BACKGROUND', (1,0), (1,0), WHITE),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (1,0), (1,0), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t19)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 20: ARCHITECTURE & PSEUDOCODE
    # ==========================================
    story.extend(make_header("High-Level Architecture & Conceptual Pseudocode"))

    arch_txt = [
        Paragraph("<b>HIGH-LEVEL ARCHITECTURE</b>", card_title_style),
        Paragraph("BIGFLOW DATA (500K Sample)<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "PREPROCESSING (Scaling & Splitting)<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "ML MODEL (XGBoost)<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "PREDICTIONS & PROBABILITIES<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "RELIABILITY ENGINE<br/>"
                  "├── Prediction Confidence<br/>"
                  "├── Mahalanobis OOD<br/>"
                  "├── Feature Drift (PSI)<br/>"
                  "└── Historical Error Proximity<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "ADAPTIVE RISK SCORE<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "REVIEW BUDGET (1%, 2%, 5%, 10%)<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "TOP-K REVIEW PRIORITIZATION<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;↓<br/>"
                  "EVALUATION & DASHBOARD", code_style)
    ]

    pc_txt = [
        Paragraph("<b>CONCEPTUAL IMPLEMENTATION PSEUDOCODE</b>", card_title_style),
        Paragraph("FOR each prediction x_i:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;calculate prediction confidence: s_conf<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;calculate OOD signal: s_ood<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;calculate drift signal: s_drift<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;calculate historical error risk: s_hist<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;combine reliability signals<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;calculate risk score: Risk(x_i)<br/><br/>"
                  "SORT predictions descending by risk score<br/><br/>"
                  "SELECT top K predictions based on available<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;review budget B: K = floor(B * N)<br/><br/>"
                  "COMPARE reviewed cases with ground truth<br/><br/>"
                  "CALCULATE:<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;errors captured<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;coverage rate<br/>"
                  "&nbsp;&nbsp;&nbsp;&nbsp;review efficiency (errors/1000 reviews)", code_style)
    ]

    t20 = Table([[arch_txt, pc_txt]], colWidths=[420, 420])
    t20.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t20)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 21: LIMITATIONS
    # ==========================================
    story.extend(make_header("Experimental & Methodological Limitations"))

    limits_txt = [
        Paragraph("<b>RESEARCH LIMITATIONS IDENTIFIED IN CURRENT PROTOTYPE</b>", ParagraphStyle('H', parent=card_title_style, textColor=RED)),
        Paragraph("1. <b>Development Sample Size:</b> Current experiments evaluate a 500,000-flow development sample rather than the full 66.9M BigFlow benchmark.<br/>"
                  "2. <b>Simulated Review Oracle:</b> Human review is simulated using ground-truth labels rather than recruiting actual human analysts.<br/>"
                  "3. <b>Heuristic Signal Weights:</b> Current review-allocation weights are heuristic rather than learned through an optimal loss formulation.<br/>"
                  "4. <b>Binary Task Formulation:</b> Current classification evaluates binary Benign vs. Attack; multi-class attack classification remains future work.<br/>"
                  "5. <b>Temporal Sample Shift:</b> Shifted evaluation represents a chronological test within the benchmark sample, not cross-dataset validation.<br/>"
                  "6. <b>Streaming Simulation:</b> Real-time streaming is currently simulated from benchmark buffers rather than live production traffic.<br/>"
                  "7. <b>Tabular Generalization:</b> Generalization to arbitrary tabular domains requires additional dataset testing and automated validation.<br/>"
                  "8. <b>Strategy Trade-Offs:</b> Current experiments do not establish universal superiority of one strategy, highlighting budget dependency.", body_style)
    ]
    t21 = Table([[limits_txt]], colWidths=[850])
    t21.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t21)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 22: PHASE 2 (PLANNED)
    # ==========================================
    story.extend(make_header("Phase 2: Planned Dataset-Agnostic Platform"))

    p2_img = os.path.join(DIAGRAMS_DIR, "diagram_phase2_platform.png")
    if os.path.exists(p2_img):
        story.append(RLImage(p2_img, width=850, height=210))
        story.append(Spacer(1, 10))

    p2_box = [
        Paragraph("<b>PLANNED FUNCTIONALITY ROADMAP (PHASE 2)</b>", card_title_style),
        Paragraph("• <b>Data Formats & Tasks [PLANNED]:</b> Support CSV, Excel, and Parquet; auto-detect binary, multi-class, and regression tasks.<br/>"
                  "• <b>Model Comparison [PLANNED]:</b> Train baseline suites and compare performance across models.<br/>"
                  "• <b>Explainability (SHAP) [PLANNED]:</b> Provide feature attributions explaining why specific cases were prioritized for human review.<br/>"
                  "• <b>Conformal Prediction [PLANNED]:</b> Implement distribution-free uncertainty intervals with statistical coverage guarantees.<br/>"
                  "• <b>Cost-Aware Review Queues [PLANNED]:</b> Optimize review queues factoring inspection costs versus penalty of undetected errors.", body_style)
    ]
    t22 = Table([[p2_box]], colWidths=[850])
    t22.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 10)
    ]))
    story.append(t22)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 23: RESEARCH SUMMARY
    # ==========================================
    story.extend(make_header("Research Summary & Current Contributions"))

    sum_left = [
        Paragraph("<b>CURRENT RESEARCH CONTRIBUTIONS</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("1. Implemented a reliability-aware ML prediction pipeline on benchmark data.<br/>"
                  "2. Combined multiple complementary reliability signals for review prioritization.<br/>"
                  "3. Evaluated review strategies under a later chronological temporal test period.<br/>"
                  "4. Studied experimentally how review effectiveness changes with review budget.<br/>"
                  "5. Built an interactive dashboard for experimental analysis and monitoring.<br/><br/>"
                  "<b>CURRENT RESEARCH FINDING:</b><br/>"
                  "<i>\"The experiments indicate that the effectiveness of review allocation depends on both the reliability signals used and the available review budget.\"</i>", body_style)
    ]
    sum_right = [
        Paragraph("<b>TRANSITION TO PHASE 2</b>", ParagraphStyle('H', parent=card_title_style, textColor=NAVY)),
        Paragraph("<b>From Research Prototype to Dataset-Agnostic Platform:</b><br/>"
                  "• <b>Current State:</b> Core reliability and human-review allocation pipeline implemented and validated on benchmark data.<br/>"
                  "• <b>Next Step:</b> Generalize, test across diverse tabular datasets, and evaluate additional human-AI reliability mechanisms.<br/>"
                  "• <b>Concluding Statement:</b> <i>\"The current work provides an experimental foundation for further investigation of adaptive human-review allocation under distribution shift.\"</i><br/><br/>"
                  "<b>Thank you. Open to questions and guidance from the committee.</b>", body_style)
    ]

    t23 = Table([[sum_left, sum_right]], colWidths=[420, 420])
    t23.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (0,0), 1, BORDER_GRAY),
        ('BOX', (1,0), (1,0), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t23)
    story.append(PageBreak())

    # ==========================================
    # SLIDE 24: REFERENCES
    # ==========================================
    story.extend(make_header("References (IEEE Standard Format)"))

    refs_content = [
        Paragraph("<b>PEER-REVIEWED ACADEMIC REFERENCES</b>", ParagraphStyle('H', parent=card_title_style, textColor=ACCENT_BLUE)),
        Paragraph("[1] Mendeley Data, 'BigFlow-NIDS: A large-scale derived benchmark for network intrusion detection,' <i>Data in Brief</i>, V2, 2026. DOI: 10.1016/j.dib.2026.112530.<br/>"
                  "[2] H. Mozannar and D. Sontag, 'Consistent estimators for learning to defer to an expert,' in <i>Proc. 37th Int. Conf. Mach. Learn. (ICML)</i>, PMLR, vol. 119, 2020, pp. 7076–7087.<br/>"
                  "[3] D. Wei et al., 'Deep learning to defer with multiple experts,' in <i>Proc. 41st Int. Conf. Mach. Learn. (ICML)</i>, PMLR, vol. 235, 2024.<br/>"
                  "[4] Y. Geifman and R. El-Yaniv, 'Selective classification for deep neural networks,' in <i>Adv. Neural Inf. Process. Syst. 30 (NeurIPS)</i>, 2017.<br/>"
                  "[5] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, 'On calibration of modern neural networks,' in <i>Proc. 34th Int. Conf. Mach. Learn. (ICML)</i>, PMLR, vol. 70, 2017, pp. 1321–1330.<br/>"
                  "[6] A. N. Angelopoulos and S. Bates, 'A gentle introduction to conformal prediction and distribution-free uncertainty quantification,' <i>arXiv preprint arXiv:2107.07511</i>, 2021.<br/>"
                  "[7] J. Yang et al., 'Generalized out-of-distribution detection: A survey,' <i>IEEE Trans. Pattern Anal. Mach. Intell. (TPAMI)</i>, 2024.<br/>"
                  "[8] P. W. Koh et al., 'WILDS: A benchmark of in-the-wild distribution shifts,' in <i>Proc. 38th Int. Conf. Mach. Learn. (ICML)</i>, PMLR, vol. 139, 2021, pp. 5637–5664.<br/>"
                  "[9] K. Lee, K. Lee, H. Lee, and J. Shin, 'A simple unified framework for detecting out-of-distribution samples and adversarial attacks,' in <i>Adv. Neural Inf. Process. Syst. 31 (NeurIPS)</i>, 2018.<br/>"
                  "[10] M. Charusaie et al., 'Sample efficient learning to defer for auction-based crowdsourcing,' in <i>Adv. Neural Inf. Process. Syst. 35 (NeurIPS)</i>, 2022.", table_cell)
    ]
    t24 = Table([[refs_content]], colWidths=[850])
    t24.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, BORDER_GRAY),
        ('PADDING', (0,0), (-1,-1), 12)
    ]))
    story.append(t24)

    doc.build(story, canvasmaker=SlideNumberedCanvas)
    print(f"Successfully generated PDF presentation at: {target_path}")

if __name__ == "__main__":
    build_pdf()
