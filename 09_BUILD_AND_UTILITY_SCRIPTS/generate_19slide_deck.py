"""
19-Slide Capstone Presentation: Phase-1, Presentation-2
========================================================
Adaptive Human-Review Allocation for Reliable ML Under Distribution Shift

University checklist compliance:
  1. Title slide                    -> Slide 1
  2. Abstract                       -> Slide 2
  3. Introduction (Problem+Purpose) -> Slide 3
  4. Introduction (Solution+Scope)  -> Slide 4
  5. Background Study               -> Slide 5
  6. Literature Survey 1-5          -> Slide 6
  7. Literature Survey 6-10         -> Slide 7
  8. Comparative Study              -> Slide 8
  9. Tools & Technologies           -> Slide 9
 10. Functional + Non-Functional    -> Slide 10
 11. Architecture + Process Flow    -> Slide 11
 12. Database Design                -> Slide 12
 13. Dataset + Data Representation  -> Slide 13
 14. Experiment Design + Models     -> Slide 14
 15. Reliability Engine + Review    -> Slide 15
 16. Implemented Modules + Shift    -> Slide 16
 17. Review Strategy Results        -> Slide 17
 18. Limitations + Conclusion       -> Slide 18
 19. References                     -> Slide 19

Font rules:
  Headings: 32-38pt | Body: 24-26pt | Tables: 18-22pt | Key numbers: 28-36pt
  Student/guide details on Slide 1 ONLY. No footers.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PPTX_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pptx")

# Colours
NAVY      = RGBColor(11, 25, 44)
ACCENT    = RGBColor(0, 102, 204)
DARK_GRAY = RGBColor(51, 65, 85)
LIGHT_BG  = RGBColor(248, 250, 252)
WHITE     = RGBColor(255, 255, 255)
BORDER    = RGBColor(203, 213, 225)
GREEN     = RGBColor(22, 163, 74)
RED       = RGBColor(220, 38, 38)
AMBER     = RGBColor(217, 119, 6)
MUTED     = RGBColor(100, 116, 139)
CARD_ALT  = RGBColor(241, 245, 249)
PURPLE    = RGBColor(124, 58, 237)

SW = Inches(13.333)
SH = Inches(7.5)


def build():
    prs = Presentation()
    prs.slide_width = SW; prs.slide_height = SH
    blank = prs.slide_layouts[6]

    def base(slide, heading, notes=""):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
        bg.fill.solid(); bg.fill.fore_color.rgb = LIGHT_BG; bg.line.fill.background()
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.10))
        bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
        hbox = slide.shapes.add_textbox(Inches(0.7), Inches(0.20), Inches(10.5), Inches(0.7))
        tf = hbox.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = heading
        p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY
        if os.path.exists(LOGO_PATH):
            slide.shapes.add_picture(LOGO_PATH, Inches(11.3), Inches(0.15), width=Inches(1.6))
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    def card(slide, left, top, w, h, fill=WHITE):
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Inches(left), Inches(top), Inches(w), Inches(h))
        s.fill.solid(); s.fill.fore_color.rgb = fill
        s.line.color.rgb = BORDER
        return s

    def bullets(tf, items, size=Pt(22), color=DARK_GRAY):
        for item in items:
            p = tf.add_paragraph(); p.space_before = Pt(3); p.space_after = Pt(3)
            if isinstance(item, tuple):
                r1 = p.add_run(); r1.text = "  " + item[0]
                r1.font.bold = True; r1.font.size = size; r1.font.color.rgb = NAVY
                r2 = p.add_run(); r2.text = " " + item[1]
                r2.font.size = size; r2.font.color.rgb = color
            else:
                r = p.add_run(); r.text = "  " + item
                r.font.size = size; r.font.color.rgb = color

    def img(slide, name, left, top, width):
        path = os.path.join(DIAGRAMS_DIR, name)
        if os.path.exists(path):
            slide.shapes.add_picture(path, Inches(left), Inches(top), width=Inches(width))

    def make_table(slide, rows_data, col_widths, left, top, headers, hdr_bg=NAVY,
                   font_size=Pt(18)):
        n_rows = len(rows_data) + 1
        n_cols = len(headers)
        t = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top),
                                   sum(Inches(w) for w in col_widths),
                                   Inches(0.42 * n_rows))
        tbl = t.table
        for i, w in enumerate(col_widths):
            tbl.columns[i].width = Inches(w)
        for i, h in enumerate(headers):
            cell = tbl.cell(0, i); cell.text = h
            cell.fill.solid(); cell.fill.fore_color.rgb = hdr_bg
            for p in cell.text_frame.paragraphs:
                p.font.bold = True; p.font.size = font_size; p.font.color.rgb = WHITE
        for r, row in enumerate(rows_data, 1):
            for c, val in enumerate(row):
                cell = tbl.cell(r, c); cell.text = val
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r % 2 == 0 else CARD_ALT
                for p in cell.text_frame.paragraphs:
                    p.font.size = font_size; p.font.color.rgb = DARK_GRAY
        return t

    # =====================================================================
    # SLIDE 1: TITLE
    # =====================================================================
    s = prs.slides.add_slide(blank)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid(); bg.fill.fore_color.rgb = CARD_ALT; bg.line.fill.background()
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.14))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    if os.path.exists(LOGO_PATH):
        s.shapes.add_picture(LOGO_PATH, Inches(10.5), Inches(0.4), width=Inches(2.3))
    tb = s.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(11.5), Inches(3.5))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "CAPSTONE PROJECT PHASE-1  |  PRESENTATION-2"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = ACCENT
    p = tf.add_paragraph()
    p.text = "Adaptive Human-Review Allocation\nfor Reliable Machine Learning\nUnder Distribution Shift"
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = NAVY; p.space_before = Pt(12)
    p = tf.add_paragraph()
    p.text = "Course: UQ25CA741A  |  Dept. of Computer Applications  |  PES University, Bangalore"
    p.font.size = Pt(16); p.font.color.rgb = DARK_GRAY; p.space_before = Pt(14)
    sc = card(s, 0.8, 5.0, 5.5, 1.8)
    stf = sc.text_frame; stf.word_wrap = True
    p = stf.paragraphs[0]; p.text = "STUDENT"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT
    p = stf.add_paragraph(); p.text = "SRN: PES1PG25CA101"; p.font.size = Pt(20); p.font.color.rgb = NAVY; p.font.bold = True
    p = stf.add_paragraph(); p.text = "MCA - Data Analytics"; p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY
    gc = card(s, 6.8, 5.0, 5.5, 1.8)
    gtf = gc.text_frame; gtf.word_wrap = True
    p = gtf.paragraphs[0]; p.text = "PROJECT GUIDE"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT
    p = gtf.add_paragraph(); p.text = "Prof. Dilip Kumar Maripuri"; p.font.size = Pt(20); p.font.color.rgb = NAVY; p.font.bold = True
    p = gtf.add_paragraph(); p.text = "Dept. of Computer Applications"; p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY
    s.notes_slide.notes_text_frame.text = (
        "Good morning panel members and Prof. Dilip Kumar Maripuri. I am presenting my "
        "Phase-1 Capstone Presentation-2 on Adaptive Human-Review Allocation for Reliable "
        "Machine Learning Under Distribution Shift. I will walk you through the research "
        "motivation, implemented prototype, empirical findings, and Phase-2 plans.")

    # =====================================================================
    # SLIDE 2: ABSTRACT
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Abstract", notes=(
        "This slide gives the abstract in a structured flow. ML systems produce lots of "
        "predictions but humans can only check a small fraction. We built a pipeline that "
        "combines four reliability signals to prioritize which predictions get reviewed. "
        "We tested it on 500K network flows with a chronological split. Multi-factor "
        "allocation captured more errors at tight budgets like 1-2 percent, but confidence-only "
        "did better at larger budgets. Phase 2 will test on more datasets."))
    c = card(s, 0.7, 1.0, 11.9, 5.9)
    tf = c.text_frame; tf.word_wrap = True
    parts = [
        ("Problem:", "ML systems produce high prediction volumes, but manual verification "
         "capacity is strictly limited (typically 1-5%). Models can make confident errors "
         "when the data distribution changes."),
        ("Approach:", "We investigate combining four complementary reliability signals -- "
         "prediction uncertainty, OOD distance, feature-level drift, and historical error "
         "proximity -- to prioritize predictions for human review."),
        ("Experiment:", "We evaluate on a 500K-flow sample from the BigFlow-NIDS benchmark "
         "using a chronological train/validation/shifted-test partition."),
        ("Observation:", "Multi-factor prioritization captures more errors at tight budgets "
         "(1-2%), while confidence-only captures more at larger budgets (5-10%)."),
        ("Future:", "Phase 2 will investigate generalization across diverse tabular datasets "
         "and add explainability features."),
    ]
    first = True
    for label, body in parts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_before = Pt(5); p.space_after = Pt(5)
        r1 = p.add_run(); r1.text = label + " "; r1.font.bold = True; r1.font.size = Pt(21)
        r1.font.color.rgb = ACCENT if label != "Future:" else AMBER
        r2 = p.add_run(); r2.text = body; r2.font.size = Pt(20); r2.font.color.rgb = DARK_GRAY

    # =====================================================================
    # SLIDE 3: INTRODUCTION - PROBLEM SCENARIO + PURPOSE
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Introduction: Problem Scenario & Purpose", notes=(
        "So the core problem is this: ML models can generate thousands of predictions, but "
        "humans can only manually check a small fraction, maybe 1 to 5 percent. And here is "
        "the tricky part -- when the data distribution changes over time, model confidence "
        "alone does not reliably indicate which predictions are wrong. The model can be very "
        "confident and still be wrong. Our purpose is to investigate whether combining multiple "
        "reliability signals can help allocate that limited review capacity more effectively."))
    c_left = card(s, 0.7, 1.0, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PROBLEM SCENARIO"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = RED
    bullets(tf, [
        "ML systems produce high-volume predictions daily",
        "Human reviewers can inspect only 1-5% of outputs",
        "Prediction confidence can be misleading under shift",
        "Models make high-confidence errors on drifted data",
        "Current approaches mostly rely on a single signal",
    ], size=Pt(21))
    c_right = card(s, 6.7, 1.0, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PURPOSE"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = GREEN
    bullets(tf, [
        "Investigate multi-signal review allocation",
        "Combine complementary reliability indicators",
        "Evaluate under explicit budget constraints",
        "Study behavior under temporal distribution shift",
        "Build a working research prototype for evaluation",
    ], size=Pt(21))

    # =====================================================================
    # SLIDE 4: INTRODUCTION - PROPOSED SOLUTION + SCOPE (with diagram)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Proposed Solution & Scope", notes=(
        "Here is how our solution works. Data goes into the ML model, which produces "
        "predictions with probabilities. Then the reliability engine computes four signals: "
        "confidence, OOD distance, drift, and historical error. These get combined into a "
        "composite risk score. The highest-risk predictions are sent for review within a "
        "fixed budget. The scope for Phase 1 is binary classification on network-flow data, "
        "evaluated offline with simulated review. This is not a live production deployment."))
    # Pipeline diagram
    img(s, 'diagram_system_architecture.png', 0.7, 1.0, 12.0)
    # Scope box at bottom
    c_scope = card(s, 0.7, 5.2, 11.9, 1.8, fill=RGBColor(254, 243, 199))
    tf = c_scope.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "SCOPE (Phase 1)"; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    bullets(tf, [
        "Binary classification on network-flow data (BigFlow-NIDS benchmark)",
        "Evaluated under simulated review budget; not a live production deployment",
    ], size=Pt(20))

    # =====================================================================
    # SLIDE 5: BACKGROUND STUDY
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Background Study", notes=(
        "This slide covers existing approaches in the literature. Confidence-based review "
        "uses softmax scores to flag uncertain predictions, but calibration research shows "
        "models can be overconfident. OOD detection identifies inputs far from training data "
        "using feature distances. Distribution shift detection measures population-level "
        "changes. Selective prediction and learning-to-defer formalize the abstention and "
        "routing decisions. Human-in-the-loop ML studies how to integrate human expertise."))
    bg_items = [
        ("Confidence-Based Review", "Uses softmax scores to flag uncertain predictions. "
         "Limited by model overconfidence under shift (Guo et al., 2017).", ACCENT),
        ("OOD Detection", "Identifies inputs far from training distribution using feature "
         "distances (Lee et al., 2018; Yang et al., 2024).", GREEN),
        ("Distribution Shift Detection", "Measures population-level changes in feature "
         "distributions over time using metrics like PSI.", AMBER),
        ("Selective Prediction / Learning-to-Defer", "Formalizes abstention and human "
         "routing under cost constraints (Geifman & El-Yaniv, 2017; Mozannar & Sontag, 2020).", PURPLE),
        ("Human-in-the-Loop ML", "Studies how to integrate human expertise into ML "
         "pipelines efficiently (Charusaie et al., 2022).", RED),
    ]
    positions = [(0.7, 1.0, 5.8, 1.7), (6.7, 1.0, 5.9, 1.7),
                 (0.7, 2.9, 5.8, 1.7), (6.7, 2.9, 5.9, 1.7),
                 (0.7, 4.8, 5.8, 1.7)]
    for (title, desc, col), (l, t, w, h) in zip(bg_items, positions):
        c = card(s, l, t, w, h)
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title
        p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = col
        p = tf.add_paragraph(); p.text = desc
        p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY; p.space_before = Pt(4)

    # =====================================================================
    # SLIDE 6: LITERATURE SURVEY - Papers 1-5
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Literature Survey (1/2)", notes=(
        "Papers 1 through 5. BigFlow-NIDS is our primary benchmark with 66.9 million flows. "
        "Mozannar and Sontag formalized learning to defer as a cost-sensitive classification "
        "problem. Wei et al. extended that to multiple experts. Geifman and El-Yaniv proposed "
        "selective classification where models can abstain. Guo et al. showed that modern "
        "neural networks are poorly calibrated and tend to be overconfident."))
    papers1 = [
        ("1. BigFlow-NIDS: A Large-Scale\n    Network Intrusion Dataset",
         "Mendeley/Data in Brief\nElsevier, 2026",
         "66.9M-flow benchmark built from four\npublic NetFlow datasets using Spark.\nOur primary evaluation dataset."),
        ("2. Consistent Estimators for\n    Learning to Defer to an Expert",
         "H. Mozannar, D. Sontag\nICML 2020 (PMLR 119)",
         "Formalizes human-AI deferral as\ncost-sensitive classification. Foundation\nfor our review-allocation concept."),
        ("3. Deep Learning to Defer\n    with Multiple Experts",
         "D. Wei et al.\nICML 2024 (PMLR 235)",
         "Extends deferral to multi-expert pools\nwith learned routing. Informs multi-\ntiered review strategy design."),
        ("4. Selective Classification for\n    Deep Neural Networks",
         "Y. Geifman, R. El-Yaniv\nNeurIPS 2017",
         "Formulates risk-coverage trade-offs\nfor confidence-based abstention.\nOur confidence-only baseline."),
        ("5. On Calibration of Modern\n    Neural Networks",
         "C. Guo et al.\nICML 2017 (PMLR 70)",
         "Shows modern classifiers produce\noverconfident probabilities. Motivates\nsupplementing confidence with other signals."),
    ]
    make_table(s, papers1, [4.0, 3.2, 4.7], 0.7, 1.0,
               ["Paper Title", "Authors / Venue", "Summary & Relevance"],
               font_size=Pt(16))

    # =====================================================================
    # SLIDE 7: LITERATURE SURVEY - Papers 6-10
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Literature Survey (2/2)", notes=(
        "Papers 6 through 10. Angelopoulos and Bates survey conformal prediction for "
        "distribution-free uncertainty quantification. Yang et al. give a comprehensive "
        "taxonomy of OOD detection methods. Lee et al. use Mahalanobis distance in feature "
        "space for OOD detection, which inspired our OOD signal. Koh et al. created the "
        "WILDS benchmark for real-world distribution shifts. Charusaie et al. address "
        "budget-constrained expert allocation, directly relevant to our setup."))
    papers2 = [
        ("6. Conformal Prediction &\n    Distribution-Free UQ",
         "A. Angelopoulos, S. Bates\narXiv Survey, 2021",
         "Establishes finite-sample distribution-\nfree uncertainty intervals. Relevant\nto our uncertainty quantification."),
        ("7. Generalized Out-of-Distribution\n    Detection: A Survey",
         "J. Yang et al.\nIEEE TPAMI, 2024",
         "Comprehensive taxonomy of OOD\ndetection across feature/logit spaces.\nFrames our OOD signal design."),
        ("8. Simple Unified Framework\n    for OOD Detection",
         "K. Lee et al.\nNeurIPS 2018",
         "Uses Mahalanobis distance in feature\nspace for OOD identification. Directly\ninspired our OOD distance signal."),
        ("9. WILDS: A Benchmark of\n    In-The-Wild Distribution Shifts",
         "P. W. Koh et al.\nICML 2021 (PMLR 139)",
         "Evaluates model robustness across\nreal-world shifts. Motivates our\ntemporal shift evaluation design."),
        ("10. Sample Efficient Learning\n     to Defer",
         "M. Charusaie et al.\nNeurIPS 2022",
         "Formulates budget-constrained expert\nquery allocation under cost limits.\nDirectly motivates our budget setup."),
    ]
    make_table(s, papers2, [4.0, 3.2, 4.7], 0.7, 1.0,
               ["Paper Title", "Authors / Venue", "Summary & Relevance"],
               font_size=Pt(16))

    # =====================================================================
    # SLIDE 8: COMPARATIVE STUDY
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Comparative Study", notes=(
        "This table compares existing approaches against our framework on six dimensions. "
        "The key difference is that most existing methods focus on one signal type. Our "
        "project investigates combining all four under explicit budget constraints with "
        "temporal shift evaluation. We do not claim universal superiority -- this is a "
        "comparative investigation of complementary approaches."))
    comp_rows = [
        ("Confidence signal",    "No",  "Yes (primary)", "Optional",   "Yes (normalized)"),
        ("OOD / Novelty",        "No",  "No",            "Yes",        "Yes (Mahalanobis)"),
        ("Drift measurement",    "No",  "No",            "No",         "Yes (PSI)"),
        ("Historical error",     "No",  "No",            "Implicit",   "Yes (error proximity)"),
        ("Budget-aware eval.",   "--",  "Manual tuning",  "Hard cutoff","1%, 2%, 5%, 10%"),
        ("Temporal shift eval.", "Yes", "Rarely",         "Partial",    "Yes (chronological)"),
    ]
    make_table(s, comp_rows, [2.8, 1.8, 2.2, 2.1, 3.0], 0.7, 1.0,
               ["Dimension", "Random", "Confidence", "L2D / OOD", "This Work"],
               font_size=Pt(18))
    # Synthesis note
    c_note = card(s, 0.7, 5.5, 11.9, 1.2, fill=RGBColor(238, 242, 255))
    tf = c_note.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = ("Note: Existing approaches emphasize different aspects of prediction reliability. "
              "This project investigates combining complementary signals within a budget-aware "
              "review-allocation framework evaluated under temporal shift.")
    p.font.size = Pt(20); p.font.color.rgb = NAVY

    # =====================================================================
    # SLIDE 9: TOOLS & TECHNOLOGIES USED
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Tools & Technologies Used", notes=(
        "These are the actual tools and libraries used in the project. Python is our primary "
        "language. For data handling we use pandas and numpy. For ML modeling we use "
        "scikit-learn and XGBoost. Scipy is used for statistical computations like "
        "Mahalanobis distance and PSI. Joblib handles model serialization. Hashlib is "
        "used for data integrity verification. Everything runs on a local machine."))
    # Data Handling
    c1 = card(s, 0.7, 1.0, 5.8, 2.5)
    tf = c1.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "DATA HANDLING"; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = ACCENT
    bullets(tf, [
        ("Python 3.x:", "Primary programming language"),
        ("pandas:", "DataFrame operations, CSV/Parquet I/O"),
        ("numpy:", "Numerical computations, array operations"),
    ], size=Pt(20))
    # ML Modeling
    c2 = card(s, 6.7, 1.0, 5.9, 2.5)
    tf = c2.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "ML MODELING"; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = GREEN
    bullets(tf, [
        ("scikit-learn:", "Preprocessing, Logistic Regression, Random Forest, metrics"),
        ("XGBoost:", "Primary classifier (gradient boosting)"),
        ("joblib:", "Model serialization and persistence"),
    ], size=Pt(20))
    # Statistical & Evaluation
    c3 = card(s, 0.7, 3.7, 5.8, 2.5)
    tf = c3.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "STATISTICAL ANALYSIS"; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = AMBER
    bullets(tf, [
        ("scipy:", "Mahalanobis distance, covariance, PSI computation"),
        ("hashlib:", "Data integrity verification (SHA-256)"),
        ("pathlib:", "Cross-platform file path handling"),
    ], size=Pt(20))
    # Infrastructure
    c4 = card(s, 6.7, 3.7, 5.9, 2.5)
    tf = c4.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "INFRASTRUCTURE"; p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = PURPLE
    bullets(tf, [
        ("Platform:", "Local development machine (Windows)"),
        ("Data format:", "CSV and compressed Parquet files"),
        ("Pipeline:", "26 sequential Python scripts (src/)"),
    ], size=Pt(20))

    # =====================================================================
    # SLIDE 10: FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Functional & Non-Functional Requirements", notes=(
        "The primary users are ML practitioners who train models and data reviewers who "
        "examine flagged predictions. Functional requirements cover the full pipeline from "
        "data ingestion to results reporting. Non-functional requirements focus on "
        "reproducibility, reasonable computation time on the development sample, and "
        "interpretability of the risk scores."))
    # Functional (left)
    c_left = card(s, 0.7, 1.0, 6.1, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "FUNCTIONAL REQUIREMENTS"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = ACCENT
    p = tf.add_paragraph(); p.text = "Users: ML Practitioner, Data Reviewer, Evaluator"
    p.font.size = Pt(18); p.font.italic = True; p.font.color.rgb = MUTED; p.space_after = Pt(4)
    frs = [
        ("FR1:", "Ingest and preprocess network-flow data"),
        ("FR2:", "Train and evaluate classification models"),
        ("FR3:", "Compute confidence score for every prediction"),
        ("FR4:", "Compute OOD distance for each input"),
        ("FR5:", "Measure feature-level distribution drift (PSI)"),
        ("FR6:", "Compute historical error proximity score"),
        ("FR7:", "Generate composite risk score from all signals"),
        ("FR8:", "Allocate predictions to review queue by budget"),
        ("FR9:", "Report error-capture metrics per strategy"),
    ]
    for label, desc in frs:
        p = tf.add_paragraph(); p.space_before = Pt(2); p.space_after = Pt(1)
        r1 = p.add_run(); r1.text = "  " + label + " "; r1.font.bold = True
        r1.font.size = Pt(17); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = desc; r2.font.size = Pt(17); r2.font.color.rgb = DARK_GRAY
    # Non-Functional (right)
    c_right = card(s, 7.0, 1.0, 5.6, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "NON-FUNCTIONAL REQUIREMENTS"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = GREEN
    nfrs = [
        ("NFR1: Reproducibility", "Deterministic splits and seeded models "
         "ensure identical results across runs"),
        ("NFR2: Computation Time", "Full pipeline completes within minutes "
         "on a standard laptop for the 500K sample"),
        ("NFR3: Interpretability", "Each reliability signal has a clear, "
         "explainable definition; composite score is a weighted sum"),
        ("NFR4: Scalability", "Pipeline design supports scaling to "
         "larger samples; current bottleneck is I/O, not compute"),
        ("NFR5: Data Integrity", "SHA-256 hash verification ensures "
         "dataset consistency across experiments"),
    ]
    for label, desc in nfrs:
        p = tf.add_paragraph(); p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = "  " + label; r1.font.bold = True
        r1.font.size = Pt(18); r1.font.color.rgb = NAVY
        p = tf.add_paragraph()
        r2 = p.add_run(); r2.text = "    " + desc
        r2.font.size = Pt(16); r2.font.color.rgb = DARK_GRAY

    # =====================================================================
    # SLIDE 11: ARCHITECTURE DIAGRAM + ML PROCESS FLOW
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Architecture & ML Process Flow", notes=(
        "The architecture diagram shows the six layers of our system: data layer, model "
        "layer, signal computation layer, risk scoring layer, review allocation layer, and "
        "results reporting. The process flow below shows the actual ML pipeline sequence "
        "we followed: chronological split, then preprocessing, model training, signal "
        "generation, risk scoring, review allocation, and finally strategy evaluation."))
    img(s, 'diagram_system_architecture.png', 0.7, 0.95, 12.0)
    img(s, 'diagram_process_flow.png', 0.7, 4.2, 12.0)

    # =====================================================================
    # SLIDE 12: DATABASE DESIGN (Conceptual Schema)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Database Design (Conceptual Schema)", notes=(
        "Since this is a research pipeline rather than a live database application, we show "
        "a conceptual schema for how results are structured. The Predictions entity holds "
        "model outputs and true labels. The Signals entity stores the four reliability scores. "
        "The Review Queue tracks which predictions were selected for review at each budget. "
        "The Experiments entity records strategy-level summary metrics. Physical storage "
        "uses CSV files in the results directory and pickle files for trained models."))
    img(s, 'diagram_er_schema.png', 0.7, 0.95, 12.0)

    # =====================================================================
    # SLIDE 13: DATASET + DATA REPRESENTATION
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Dataset & Data Representation", notes=(
        "We use BigFlow-NIDS, published in 2026 by Elsevier. It is an offline scientific "
        "benchmark built from four publicly available NetFlow datasets using Apache Spark. "
        "The full dataset has 66.9 million flows with 55 attributes. We use a 500K-flow "
        "development sample. X is 49 numerical features like ports, packet counts, bytes, "
        "and timing. Y is binary: 0 for Benign, 1 for Attack. The detailed Attack category "
        "column was excluded from training to prevent label leakage."))
    c_left = card(s, 0.7, 1.0, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "BigFlow-NIDS Benchmark"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = ACCENT
    bullets(tf, [
        ("Full scale:", "66.9M flows, 55 attributes, 32 attack types"),
        ("Dev sample:", "500,000 flows (current experiments)"),
        ("Source:", "Elsevier / Mendeley Data, 2026"),
        ("Construction:", "Four public NetFlow datasets merged via Spark"),
        ("Important:", "Offline benchmark from research testbeds,\n    NOT live production/Internet traffic"),
    ], size=Pt(20))
    c_right = card(s, 6.7, 1.0, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Features (X) & Target (Y)"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY
    p = tf.add_paragraph(); p.space_before = Pt(6)
    p.text = "X: 49 numerical network-flow features"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = ACCENT
    bullets(tf, [
        "Ports, protocol, packet counts, byte volumes",
        "Throughput, flow duration, IAT statistics",
        "TCP flags, window sizes, packet lengths",
    ], size=Pt(19))
    p = tf.add_paragraph(); p.space_before = Pt(10)
    p.text = "Y: Binary -- Benign (0) vs Attack (1)"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = ACCENT
    bullets(tf, [
        "Attack category column excluded from\n    classifier to prevent label leakage",
        "Used only for post-prediction error analysis",
    ], size=Pt(19))

    # =====================================================================
    # SLIDE 14: EXPERIMENT DESIGN + MODEL RESULTS (with pseudocode)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Experiment Design & Model Results", notes=(
        "We split the 500K flows chronologically: 350K for training, 75K for validation, "
        "75K for shifted test. The shifted test represents a later temporal period. Three "
        "models were compared: Logistic Regression, Random Forest, and XGBoost. XGBoost "
        "achieved the highest validation ROC-AUC at 0.9228 and was selected as the primary "
        "classifier. Validation attack rate is about 0.33 percent, so accuracy alone is "
        "not sufficient for model selection."))
    # Left: split + timeline
    c_left = card(s, 0.7, 1.0, 6.0, 3.0)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Chronological Split (500K flows)"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = ACCENT
    splits = [("Train:", "350,000 flows"), ("Validation:", "75,000 flows (attack ~0.33%)"),
              ("Shifted Test:", "75,000 flows (attack ~6.30%)")]
    for label, val in splits:
        p = tf.add_paragraph(); p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = "  " + label + " "; r1.font.bold = True
        r1.font.size = Pt(22); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = val; r2.font.size = Pt(22); r2.font.color.rgb = DARK_GRAY
    p = tf.add_paragraph(); p.space_before = Pt(6)
    p.text = "  Shifted test = later temporal period, used to study\n  performance under changed data conditions."
    p.font.size = Pt(18); p.font.italic = True; p.font.color.rgb = MUTED
    # Right: model table
    model_rows = [
        ("Logistic Regression", "0.9606", "0.0693", "0.7499"),
        ("Random Forest",       "0.9801", "0.1210", "0.8526"),
        ("XGBoost (selected)",  "0.9900", "0.0552", "0.9228"),
    ]
    make_table(s, model_rows, [3.2, 1.2, 1.0, 1.2], 7.0, 1.0,
               ["Model", "Accuracy", "F1", "ROC-AUC"], font_size=Pt(18))
    # Pseudocode box
    c_code = card(s, 0.7, 4.3, 11.9, 2.5, fill=RGBColor(241, 245, 249))
    tf = c_code.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PSEUDOCODE: Model Training & Prediction"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    code_lines = [
        "  model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1)",
        "  model.fit(X_train, y_train)",
        "  probabilities = model.predict_proba(X_validation)",
        "  confidence = max(probabilities, axis=1)     # per-sample confidence",
        "  roc_auc = roc_auc_score(y_validation, probabilities[:, 1])",
    ]
    for line in code_lines:
        p = tf.add_paragraph(); p.space_before = Pt(1)
        r = p.add_run(); r.text = line; r.font.size = Pt(16)
        r.font.color.rgb = DARK_GRAY; r.font.name = "Consolas"

    # =====================================================================
    # SLIDE 15: RELIABILITY ENGINE + REVIEW ALLOCATION (with pseudocode)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Reliability Engine & Review Allocation", notes=(
        "We implemented four complementary reliability signals. Confidence is 1 minus "
        "max probability. OOD uses Mahalanobis-like distance to the training centroid. "
        "Drift uses Population Stability Index across features. Historical error measures "
        "proximity to training-time mistakes -- though this currently uses training-time "
        "performance and would benefit from an out-of-fold estimate. These are combined "
        "into a weighted composite risk score. Human review is simulated using ground-truth "
        "labels. Subgroup fairness is not applicable to network-flow data."))
    # Signal diagram
    img(s, 'diagram_signals_allocation.png', 0.7, 0.95, 12.0)
    # Pseudocode box
    c_code = card(s, 0.7, 4.3, 11.9, 2.8, fill=CARD_ALT)
    tf = c_code.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PSEUDOCODE: Risk Scoring & Review Allocation"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    code = [
        "  risk_score = w1*confidence_risk + w2*ood_risk + w3*drift_risk + w4*historical_risk",
        "  review_queue = top_k(risk_score, k = budget_percent * total_predictions)",
        "  # Review is simulated using ground-truth labels as evaluation oracle",
        "  errors_found = sum(review_queue.true_label != review_queue.predicted_label)",
    ]
    for line in code:
        p = tf.add_paragraph(); p.space_before = Pt(1)
        r = p.add_run(); r.text = line; r.font.size = Pt(16)
        r.font.color.rgb = DARK_GRAY; r.font.name = "Consolas"
    p = tf.add_paragraph(); p.space_before = Pt(6)
    r = p.add_run()
    r.text = ("  Note: Historical error signal uses training-time performance; would benefit "
              "from out-of-fold estimation.\n  Subgroup/fairness: not applicable to network-flow "
              "data -- planned for a future dataset with demographic attributes.")
    r.font.size = Pt(15); r.font.italic = True; r.font.color.rgb = MUTED

    # =====================================================================
    # SLIDE 16: IMPLEMENTED MODULES + SHIFTED-TEST RESULTS
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Implemented Modules & Shift Results", notes=(
        "On the left, here is what is actually built and working: data preprocessing, "
        "chronological splitting, three model trainers, all four signal extractors, three "
        "review strategies, the evaluation pipeline, and a comparison dashboard. On the "
        "right, the before-after comparison shows the shifted test was significantly more "
        "challenging: attack rate went from 0.33 to 6.3 percent, error rate from 1 to "
        "4.57 percent, but average confidence only dropped slightly from 98.65 to 96.82 "
        "percent. This motivates reliability-aware evaluation."))
    # Left: checklist
    c_left = card(s, 0.7, 1.0, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "IMPLEMENTED (Phase 1)"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = GREEN
    impl = [
        "Data preprocessing & chronological split",
        "XGBoost + Random Forest + Logistic Reg.",
        "Confidence signal extractor",
        "OOD distance signal extractor",
        "Distribution drift (PSI) signal extractor",
        "Historical error proximity extractor",
        "Three review strategies (Conf / Multi / Adaptive)",
        "Budget-based evaluation pipeline",
        "Strategy comparison & reporting",
    ]
    for item in impl:
        p = tf.add_paragraph(); p.space_before = Pt(2)
        r = p.add_run(); r.text = "  [done] " + item
        r.font.size = Pt(18); r.font.color.rgb = DARK_GRAY
    # Right: shift comparison
    c_right = card(s, 6.7, 1.0, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Validation vs. Shifted Test"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY
    comparisons = [
        ("Attack rate:", "0.33%", "6.30%", "(19x increase)"),
        ("Error rate:", "1.00%", "4.57%", "(4.6x increase)"),
        ("Avg confidence:", "98.65%", "96.82%", "(slight drop)"),
        ("Total errors:", "747", "3,427", "(4.6x more)"),
    ]
    for label, val_v, val_s, note in comparisons:
        p = tf.add_paragraph(); p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = "  " + label; r1.font.bold = True
        r1.font.size = Pt(21); r1.font.color.rgb = DARK_GRAY
        p = tf.add_paragraph()
        r2 = p.add_run(); r2.text = "    " + val_v + "  -->  " + val_s + "  " + note
        r2.font.size = Pt(20); r2.font.bold = True; r2.font.color.rgb = RED
    p = tf.add_paragraph(); p.space_before = Pt(10)
    p.text = ("  The later test period was more challenging for\n"
              "  the model, motivating reliability-aware evaluation.")
    p.font.size = Pt(17); p.font.italic = True; p.font.color.rgb = MUTED

    # =====================================================================
    # SLIDE 17: REVIEW STRATEGY RESULTS (table + chart)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Review Strategy Results", notes=(
        "This table shows percentage of total errors captured at each budget. At 1 percent, "
        "Feedback Adaptive captures 17.80 percent versus 13.51 for confidence-only. At 2 "
        "percent, it captures 34.26 versus 26.73. But at 5 and 10 percent, confidence-only "
        "outperforms multi-factor. The OOD-only strategy performed worse than random at all "
        "budgets, capturing almost no errors, probably because the OOD signal alone does not "
        "correlate well with model errors in this particular dataset. Different strategies "
        "work better at different budgets -- there is no universal winner."))
    # Results table -- including OOD-only for honesty
    res_rows = [
        ("1%",  "1.17%",  "13.51%", "0.03%",  "17.51%", "17.80%"),
        ("2%",  "2.13%",  "26.73%", "0.26%",  "33.99%", "34.26%"),
        ("5%",  "5.52%",  "65.45%", "0.35%",  "54.57%", "45.90%"),
        ("10%", "9.92%",  "84.01%", "0.35%",  "65.42%", "52.35%"),
    ]
    make_table(s, res_rows, [1.4, 1.5, 1.9, 1.6, 2.5, 2.5], 0.7, 1.0,
               ["Budget", "Random", "Confidence", "OOD-Only", "Static Multi-\nFactor (Weighted)", "Feedback\nAdaptive"],
               font_size=Pt(16))
    # Note below table
    c_note = card(s, 0.7, 3.8, 5.5, 2.0)
    tf = c_note.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "KEY OBSERVATIONS"
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY
    bullets(tf, [
        "Multi-factor captures more errors at 1-2%",
        "Confidence-only outperforms at 5-10%",
        "OOD-only underperformed random at all budgets",
        "No strategy is universally superior",
    ], size=Pt(18))
    # Chart
    img(s, 'diagram_results_chart.png', 6.4, 3.5, 6.2)

    # =====================================================================
    # SLIDE 18: LIMITATIONS + CONCLUSION
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "Limitations & Conclusion", notes=(
        "Limitations: we used a 500K sample not the full 66.9M, human review is simulated, "
        "strategy weights are heuristic not learned, only binary classification, temporal "
        "shift only not cross-dataset, historical error signal needs out-of-fold estimation, "
        "and results do not establish universal superiority. Conclusion: we built and evaluated "
        "a working prototype, found that strategy effectiveness depends on budget and signals "
        "used, and Phase 2 will extend to other datasets and mechanisms."))
    # Limitations
    c_left = card(s, 0.7, 1.0, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "LIMITATIONS"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = RED
    bullets(tf, [
        "Uses 500K sample, not full 66.9M dataset",
        "Human review is simulated, not actual reviewers",
        "Strategy weights are heuristic, not learned",
        "Binary classification only (single dataset)",
        "Temporal shift only, not cross-dataset",
        "Historical error needs out-of-fold estimation",
        "No universal superiority established",
    ], size=Pt(18))
    # Conclusion
    c_right = card(s, 6.7, 1.0, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "CONCLUSION"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = GREEN
    conclusions = [
        ("Built:", "Working prototype with 4 complementary reliability signals"),
        ("Evaluated:", "3 strategies at 4 budget levels on shifted test data"),
        ("Observed:", "Multi-factor captures more errors at tight budgets (1-2%)"),
        ("Found:", "Strategy effectiveness depends on budget and signals used"),
        ("Next:", "Phase 2 extends to diverse datasets and explainability"),
    ]
    for label, text in conclusions:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        r1 = p.add_run(); r1.text = "  " + label + " "
        r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = ACCENT
        r2 = p.add_run(); r2.text = text
        r2.font.size = Pt(20); r2.font.color.rgb = DARK_GRAY

    # =====================================================================
    # SLIDE 19: REFERENCES (IEEE Format)
    # =====================================================================
    s = prs.slides.add_slide(blank)
    base(s, "References", notes=(
        "This slide lists all references in IEEE format for the record. It includes all "
        "10 research papers, the BigFlow-NIDS dataset source, and the key libraries used. "
        "This slide is for reference rather than reading aloud in detail."))
    c = card(s, 0.7, 1.0, 11.9, 6.0)
    tf = c.text_frame; tf.word_wrap = True
    refs = [
        '[1] "BigFlow-NIDS: A Large-Scale Network Intrusion Detection Benchmark," '
        'Mendeley Data / Data in Brief, Elsevier, 2026. DOI: 10.1016/j.dib.2026.112530.',
        '[2] H. Mozannar and D. Sontag, "Consistent Estimators for Learning to Defer to an Expert," '
        'in Proc. ICML, PMLR 119, 2020, pp. 7076-7087.',
        '[3] D. Wei et al., "Deep Learning to Defer with Multiple Experts," '
        'in Proc. ICML, PMLR 235, 2024.',
        '[4] Y. Geifman and R. El-Yaniv, "Selective Classification for Deep Neural Networks," '
        'in Proc. NeurIPS, 2017, pp. 4878-4887.',
        '[5] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," '
        'in Proc. ICML, PMLR 70, 2017, pp. 1321-1330.',
        '[6] A. N. Angelopoulos and S. Bates, "A Gentle Introduction to Conformal Prediction '
        'and Distribution-Free Uncertainty Quantification," arXiv:2107.07511, 2021.',
        '[7] J. Yang et al., "Generalized Out-of-Distribution Detection: A Survey," '
        'IEEE Trans. PAMI, vol. 46, no. 3, pp. 1-20, 2024.',
        '[8] K. Lee, K. Lee, H. Lee, and J. Shin, "A Simple Unified Framework for Detecting '
        'Out-of-Distribution Samples and Adversarial Attacks," in Proc. NeurIPS, 2018.',
        '[9] P. W. Koh et al., "WILDS: A Benchmark of In-the-Wild Distribution Shifts," '
        'in Proc. ICML, PMLR 139, 2021, pp. 5637-5664.',
        '[10] M. Charusaie et al., "Sample Efficient Learning to Defer," '
        'in Proc. NeurIPS, 2022.',
        '[11] XGBoost: T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," '
        'in Proc. KDD, 2016, pp. 785-794.',
        '[12] scikit-learn: F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," '
        'JMLR, vol. 12, pp. 2825-2830, 2011.',
    ]
    first = True
    for ref in refs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = ref; p.font.size = Pt(13); p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(3); p.space_after = Pt(2)

    # ── SAVE ──
    prs.save(PPTX_PATH)
    print(f"\n[OK] Saved {len(prs.slides)} slides to:\n   {PPTX_PATH}")
    print(f"   File size: {os.path.getsize(PPTX_PATH):,} bytes")


if __name__ == "__main__":
    build()
