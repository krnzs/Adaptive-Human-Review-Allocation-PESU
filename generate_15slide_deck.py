"""
Generate 15-Slide Capstone Presentation (Phase-1, Presentation-2)
=================================================================
Adaptive Human-Review Allocation for Reliable ML Under Distribution Shift

Projector-readable fonts:
  - Headings: 32-38 pt
  - Body text: 24-26 pt
  - Table text: 18-20 pt
  - Important numbers: 28-36 pt

HARD LIMIT: 15 SLIDES. Student/guide details on Slide 1 only.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PPTX_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pptx")

# ── Colour palette ──────────────────────────────────────────────
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

# ── Slide dimensions (16:9 widescreen) ──────────────────────────
SW = Inches(13.333)
SH = Inches(7.5)


def build_deck():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH
    blank = prs.slide_layouts[6]

    # ── Helper: add background + accent bar + logo (NO footer) ──
    def base(slide, heading, notes=""):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
        bg.fill.solid(); bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()

        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.10))
        bar.fill.solid(); bar.fill.fore_color.rgb = NAVY
        bar.line.fill.background()

        # Heading
        hbox = slide.shapes.add_textbox(Inches(0.7), Inches(0.22), Inches(10.5), Inches(0.7))
        tf = hbox.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = heading
        p.font.size = Pt(34); p.font.bold = True; p.font.color.rgb = NAVY

        # Logo top-right
        if os.path.exists(LOGO_PATH):
            slide.shapes.add_picture(LOGO_PATH, Inches(11.3), Inches(0.18), width=Inches(1.6))

        # Speaker notes
        if notes:
            slide.notes_slide.notes_text_frame.text = notes

    # ── Helper: add a rounded card ──────────────────────────────
    def card(slide, left, top, w, h, fill=WHITE):
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                   Inches(left), Inches(top), Inches(w), Inches(h))
        s.fill.solid(); s.fill.fore_color.rgb = fill
        s.line.color.rgb = BORDER
        return s

    # ── Helper: styled text frame with bullets ──────────────────
    def add_bullets(tf, items, size=Pt(24), color=DARK_GRAY, bold_prefix=False):
        """items can be str or (bold_part, rest)"""
        for item in items:
            p = tf.add_paragraph()
            p.space_before = Pt(4); p.space_after = Pt(4)
            if isinstance(item, tuple):
                r1 = p.add_run(); r1.text = "• " + item[0]
                r1.font.bold = True; r1.font.size = size; r1.font.color.rgb = NAVY
                r2 = p.add_run(); r2.text = " " + item[1]
                r2.font.size = size; r2.font.color.rgb = color
            else:
                r = p.add_run(); r.text = "• " + item
                r.font.size = size; r.font.color.rgb = color

    # ══════════════════════════════════════════════════════════════
    # SLIDE 1: TITLE (Only slide with student/guide details)
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor(241, 245, 249)
    bg.line.fill.background()

    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.14))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()

    if os.path.exists(LOGO_PATH):
        s.shapes.add_picture(LOGO_PATH, Inches(10.5), Inches(0.4), width=Inches(2.3))

    tb = s.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.5), Inches(3.5))
    tf = tb.text_frame; tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CAPSTONE PROJECT PHASE-1  •  PRESENTATION-2"
    p.font.size = Pt(18); p.font.bold = True; p.font.color.rgb = ACCENT

    p = tf.add_paragraph()
    p.text = "Adaptive Human-Review Allocation\nfor Reliable Machine Learning\nUnder Distribution Shift"
    p.font.size = Pt(36); p.font.bold = True; p.font.color.rgb = NAVY
    p.space_before = Pt(12)

    p = tf.add_paragraph()
    p.text = "Course: UQ25CA741A  |  Dept. of Computer Applications  |  PES University, Bangalore"
    p.font.size = Pt(16); p.font.color.rgb = DARK_GRAY
    p.space_before = Pt(14)

    # Student card
    sc = card(s, 0.8, 5.0, 5.5, 1.8)
    stf = sc.text_frame; stf.word_wrap = True
    p = stf.paragraphs[0]; p.text = "STUDENT"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT
    p = stf.add_paragraph(); p.text = "SRN: PES1PG25CA101"
    p.font.size = Pt(20); p.font.color.rgb = NAVY; p.font.bold = True
    p = stf.add_paragraph(); p.text = "MCA – Data Analytics"
    p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY

    # Guide card
    gc = card(s, 6.8, 5.0, 5.5, 1.8)
    gtf = gc.text_frame; gtf.word_wrap = True
    p = gtf.paragraphs[0]; p.text = "PROJECT GUIDE"
    p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT
    p = gtf.add_paragraph(); p.text = "Prof. Dilip Kumar Maripuri"
    p.font.size = Pt(20); p.font.color.rgb = NAVY; p.font.bold = True
    p = gtf.add_paragraph(); p.text = "Dept. of Computer Applications"
    p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY

    s.notes_slide.notes_text_frame.text = (
        "Good morning panel members and Prof. Dilip Kumar Maripuri. "
        "I am presenting my Phase-1 Capstone Presentation-2 on Adaptive Human-Review "
        "Allocation for Reliable Machine Learning Under Distribution Shift. "
        "This presentation covers our research motivation, implemented prototype, "
        "empirical findings on the BigFlow-NIDS benchmark, and Phase-2 plans."
    )

    # ══════════════════════════════════════════════════════════════
    # SLIDE 2: ABSTRACT
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Abstract", notes=(
        "This slide summarizes the project in a structured flow: problem, approach, "
        "experiment, observation, and limitations. Human auditing capacity is limited "
        "to roughly 1-5% of predictions. We implemented four complementary reliability "
        "signals and evaluated them on 500K benchmark flows. Multi-factor allocation "
        "showed improved error capture at tight budgets, but strategy effectiveness "
        "varies with budget size. This is an empirical foundation, not a complete solution."
    ))

    c = card(s, 0.7, 1.05, 11.9, 5.9)
    tf = c.text_frame; tf.word_wrap = True

    abstract_parts = [
        ("Problem:", "ML systems produce high prediction volumes, but manual "
         "verification capacity is strictly limited (typically 1–5%). Models can "
         "make confident errors when the data distribution changes."),
        ("Approach:", "We investigate an experimental framework combining four "
         "complementary reliability signals — prediction uncertainty, OOD distance, "
         "feature-level drift, and historical error proximity — to prioritize "
         "predictions for human review."),
        ("Experiment:", "We evaluate the pipeline on a 500K-flow sample from the "
         "BigFlow-NIDS benchmark using a chronological train/validation/shifted-test "
         "partition."),
        ("Observation:", "Multi-factor prioritization captures more errors at tight "
         "budgets (1–2%), while confidence-only captures more at larger budgets "
         "(5–10%). Effectiveness varies with budget."),
        ("Future:", "Phase 2 will investigate generalization across diverse "
         "tabular datasets and add explainability features."),
    ]
    first = True
    for label, body in abstract_parts:
        if first:
            p = tf.paragraphs[0]; first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(6); p.space_after = Pt(6)
        r1 = p.add_run(); r1.text = label + " "
        r1.font.bold = True; r1.font.size = Pt(22)
        r1.font.color.rgb = ACCENT if label != "Future:" else AMBER
        r2 = p.add_run(); r2.text = body
        r2.font.size = Pt(21); r2.font.color.rgb = DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 3: PROBLEM + PROPOSED SOLUTION (with pipeline diagram)
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Problem & Proposed Solution", notes=(
        "ML systems can generate thousands of predictions daily, but humans can only "
        "inspect a small fraction. The challenge is that prediction confidence alone "
        "can fail when the environment drifts — models remain confident while making "
        "mistakes. Our approach combines multiple complementary signals to score and "
        "prioritize predictions for review under explicit budget constraints. "
        "The pipeline diagram shows the flow from data input through the reliability engine."
    ))

    # Left side: Problem + Solution text
    c_left = card(s, 0.7, 1.05, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True

    p = tf.paragraphs[0]; p.text = "THE PROBLEM"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = RED

    add_bullets(tf, [
        "ML models produce high-volume predictions",
        "Humans can inspect only 1–5% of outputs",
        "Confidence alone fails under distribution shift",
    ], size=Pt(22))

    p = tf.add_paragraph(); p.space_before = Pt(16)
    p.text = "OUR APPROACH"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = GREEN

    add_bullets(tf, [
        "Combine 4 complementary reliability signals",
        "Score & rank predictions by composite risk",
        "Review highest-risk cases within fixed budget",
    ], size=Pt(22))

    # Right side: Pipeline diagram
    arch_img = os.path.join(DIAGRAMS_DIR, "diagram_system_architecture.png")
    if os.path.exists(arch_img):
        s.shapes.add_picture(arch_img, Inches(6.7), Inches(1.05),
                             width=Inches(6.1))

    # ══════════════════════════════════════════════════════════════
    # SLIDE 4: RESEARCH QUESTION + OBJECTIVES
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Research Question & Objectives", notes=(
        "Our primary research question asks whether combining multiple reliability "
        "signals can identify model errors more effectively than confidence alone "
        "when the data distribution shifts. The four objectives structure our Phase-1 "
        "work: build the prototype, implement the four signals, evaluate under "
        "controlled shift, and compare strategies at various review budgets."
    ))

    # Research question box
    qbox = card(s, 0.7, 1.05, 11.9, 1.8, fill=RGBColor(238, 242, 255))
    tf = qbox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = ("RQ: Can combining multiple complementary reliability signals "
              "identify model errors more effectively than prediction confidence "
              "alone, under distribution shift and constrained review budgets?")
    p.font.size = Pt(24); p.font.italic = True; p.font.color.rgb = NAVY

    # Objectives
    obox = card(s, 0.7, 3.15, 11.9, 4.0)
    tf = obox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "PHASE-1 OBJECTIVES"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ACCENT

    objs = [
        ("O1:", "Build a prototype pipeline for budget-constrained review allocation"),
        ("O2:", "Implement four complementary reliability signals (confidence, OOD, drift, historical error)"),
        ("O3:", "Evaluate under controlled temporal shift using chronological data splitting"),
        ("O4:", "Compare review strategies at 1%, 2%, 5%, and 10% budgets"),
    ]
    for label, text in objs:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        r1 = p.add_run(); r1.text = label + " "
        r1.font.bold = True; r1.font.size = Pt(24); r1.font.color.rgb = ACCENT
        r2 = p.add_run(); r2.text = text
        r2.font.size = Pt(24); r2.font.color.rgb = DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 5: BACKGROUND + LITERATURE GAP
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Background & Literature Gap", notes=(
        "This slide covers the four foundational research areas. Selective classification "
        "allows models to abstain but relies on confidence alone. Calibration research "
        "shows models are often overconfident. OOD detection finds unfamiliar inputs "
        "using feature distances. Learning-to-defer models human-AI routing. "
        "The gap is that no existing work combines all four signal types under "
        "explicit operational review budgets with temporal shift evaluation."
    ))

    # 4 compact background cards (2x2 grid)
    bg_items = [
        ("Selective Classification", "Abstention when uncertain\n(Geifman & El-Yaniv, 2017)", ACCENT),
        ("Model Calibration", "Overconfidence under shift\n(Guo et al., 2017)", RED),
        ("OOD Detection", "Feature-space novelty scoring\n(Lee et al., 2018; Yang et al., 2024)", GREEN),
        ("Learning to Defer", "Human-AI deferral under cost\n(Mozannar & Sontag, 2020)", AMBER),
    ]
    positions = [(0.7, 1.05, 5.8, 2.3), (6.7, 1.05, 5.9, 2.3),
                 (0.7, 3.55, 5.8, 2.3), (6.7, 3.55, 5.9, 2.3)]
    for (title, desc, col), (l, t, w, h) in zip(bg_items, positions):
        c = card(s, l, t, w, h)
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title
        p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = col
        p = tf.add_paragraph(); p.text = desc
        p.font.size = Pt(22); p.font.color.rgb = DARK_GRAY; p.space_before = Pt(8)

    # Gap banner at bottom
    gbox = card(s, 0.7, 6.05, 11.9, 1.0, fill=RGBColor(254, 243, 199))
    tf = gbox.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = ("GAP: No existing work combines all four signal types under explicit "
              "operational review budgets with temporal shift evaluation.")
    p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = NAVY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 6: LITERATURE SURVEY — Papers 1-5
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Literature Survey (1/2)", notes=(
        "Papers 1 through 5. BigFlow-NIDS is our primary benchmark dataset. "
        "Mozannar and Sontag formalize learning to defer. Wei et al. extend it "
        "to multiple experts. Geifman and El-Yaniv formulate selective classification. "
        "Guo et al. demonstrate model miscalibration and motivate supplementing "
        "confidence with additional signals."
    ))

    papers1 = [
        ("1. BigFlow-NIDS: Large-Scale Benchmark",
         "Mendeley / Data in Brief, Elsevier 2026",
         "66.9M-flow benchmark. Our primary evaluation dataset."),
        ("2. Consistent Estimators for Learning to Defer",
         "Mozannar & Sontag, ICML 2020 (PMLR 119)",
         "Theoretical formulation of human-AI deferral under cost."),
        ("3. Deep Learning to Defer with Multiple Experts",
         "Wei et al., ICML 2024 (PMLR 235)",
         "Extends deferral to multi-expert pools."),
        ("4. Selective Classification for Deep Neural Networks",
         "Geifman & El-Yaniv, NeurIPS 2017",
         "Risk-coverage trade-offs for confidence-based abstention."),
        ("5. On Calibration of Modern Neural Networks",
         "Guo et al., ICML 2017 (PMLR 70)",
         "Demonstrates model overconfidence under distribution shift."),
    ]

    t = s.shapes.add_table(6, 3, Inches(0.7), Inches(1.05), Inches(11.9), Inches(5.5))
    tbl = t.table
    tbl.columns[0].width = Inches(4.5)
    tbl.columns[1].width = Inches(3.7)
    tbl.columns[2].width = Inches(3.7)

    hdrs = ["Paper", "Venue / Year", "Relevance"]
    for i, h in enumerate(hdrs):
        cell = tbl.cell(0, i); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = WHITE

    for r, (title, venue, rel) in enumerate(papers1, 1):
        for c, val in enumerate([title, venue, rel]):
            cell = tbl.cell(r, c); cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 == 0 else CARD_ALT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 7: LITERATURE SURVEY — Papers 6-10
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Literature Survey (2/2)", notes=(
        "Papers 6 through 10. Angelopoulos and Bates cover conformal prediction "
        "for distribution-free uncertainty. Yang et al. provide a comprehensive "
        "OOD detection survey. Lee et al. use Mahalanobis distance for OOD. "
        "Koh et al. benchmark in-the-wild distribution shifts with WILDS. "
        "Charusaie et al. formulate budget-constrained expert query allocation."
    ))

    papers2 = [
        ("6. Conformal Prediction & Distribution-Free UQ",
         "Angelopoulos & Bates, arXiv 2021",
         "Finite-sample distribution-free uncertainty intervals."),
        ("7. Generalized OOD Detection: A Survey",
         "Yang et al., IEEE TPAMI 2024",
         "Comprehensive taxonomy of OOD detection methods."),
        ("8. Simple Unified Framework for OOD Detection",
         "Lee et al., NeurIPS 2018",
         "Mahalanobis distance in feature space for OOD."),
        ("9. WILDS: In-The-Wild Distribution Shifts",
         "Koh et al., ICML 2021 (PMLR 139)",
         "Real-world shift benchmarks. Motivates temporal evaluation."),
        ("10. Sample Efficient Learning to Defer",
         "Charusaie et al., NeurIPS 2022",
         "Budget-constrained expert query allocation under cost."),
    ]

    t = s.shapes.add_table(6, 3, Inches(0.7), Inches(1.05), Inches(11.9), Inches(5.5))
    tbl = t.table
    tbl.columns[0].width = Inches(4.5)
    tbl.columns[1].width = Inches(3.7)
    tbl.columns[2].width = Inches(3.7)

    for i, h in enumerate(hdrs):
        cell = tbl.cell(0, i); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = WHITE

    for r, (title, venue, rel) in enumerate(papers2, 1):
        for c, val in enumerate([title, venue, rel]):
            cell = tbl.cell(r, c); cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 == 0 else CARD_ALT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(18); p.font.color.rgb = DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 8: COMPARATIVE STUDY
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Comparative Study", notes=(
        "This table compares existing reliability paradigms on six dimensions. "
        "Random review has no signal. Confidence threshold relies on softmax scores. "
        "OOD filters detect feature novelties. Learning to defer optimizes surrogate "
        "losses. Our framework investigates combining all four signals under budget "
        "constraints evaluated with chronological shift. We do not claim superiority; "
        "we present this as a comparative investigation."
    ))

    t = s.shapes.add_table(7, 5, Inches(0.7), Inches(1.05), Inches(11.9), Inches(5.5))
    tbl = t.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(2.0)
    tbl.columns[3].width = Inches(2.3)
    tbl.columns[4].width = Inches(3.0)

    comp_hdrs = ["Dimension", "Random", "Confidence", "L2D / OOD", "This Work"]
    for i, h in enumerate(comp_hdrs):
        cell = tbl.cell(0, i); cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if i < 4 else ACCENT
        for p in cell.text_frame.paragraphs:
            p.font.bold = True; p.font.size = Pt(19); p.font.color.rgb = WHITE

    comp_rows = [
        ("Confidence signal",       "No",  "Yes (primary)", "Optional",  "Yes (normalized)"),
        ("OOD / Novelty",           "No",  "No",            "Yes",       "Yes (Mahalanobis)"),
        ("Drift measurement",       "No",  "No",            "No",        "Yes (PSI)"),
        ("Historical error",        "No",  "No",            "Implicit",  "Yes (error proximity)"),
        ("Budget-aware eval.",      "—",   "Manual tuning",  "Hard cutoff","1%, 2%, 5%, 10%"),
        ("Temporal shift eval.",    "Yes",  "Rarely",        "Partial",   "Yes (chronological)"),
    ]
    for r, row_data in enumerate(comp_rows, 1):
        for c, val in enumerate(row_data):
            cell = tbl.cell(r, c); cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 == 0 else CARD_ALT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(18)
                p.font.bold = (c == 0 or c == 4)
                p.font.color.rgb = ACCENT if c == 4 else DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 9: DATASET + DATA REPRESENTATION
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Dataset & Data Representation", notes=(
        "We use BigFlow-NIDS, published in 2026. It is an offline scientific benchmark "
        "built from four NetFlow datasets using Apache Spark. Full scale is 66.9M flows "
        "with 55 attributes. We use a 500K-flow development sample. X is 49 numerical "
        "features covering ports, packets, bytes, throughput, and timing. Y is binary: "
        "0=Benign, 1=Attack. The Attack category column was excluded from training to "
        "prevent leakage."
    ))

    # Left: Dataset
    c_left = card(s, 0.7, 1.05, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "BigFlow-NIDS Benchmark"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ACCENT

    add_bullets(tf, [
        ("Full scale:", "66.9M flows, 55 attributes, 32 attack types"),
        ("Dev sample:", "500,000 flows (current experiments)"),
        ("Source:", "Elsevier/Mendeley 2026 — offline benchmark"),
        ("Format:", "CSV/Parquet, chronological order preserved"),
    ], size=Pt(22))

    # Right: X and Y
    c_right = card(s, 6.7, 1.05, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Features (X) & Target (Y)"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = NAVY

    p = tf.add_paragraph(); p.space_before = Pt(8)
    p.text = "X: 49 numerical network-flow features"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = ACCENT

    add_bullets(tf, [
        "Ports, protocol, packet counts, byte volumes",
        "Throughput, flow duration, IAT statistics",
        "TCP flags, window sizes, packet lengths",
    ], size=Pt(20))

    p = tf.add_paragraph(); p.space_before = Pt(12)
    p.text = "Y: Binary — Benign (0) vs Attack (1)"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = ACCENT

    p = tf.add_paragraph(); p.space_before = Pt(4)
    r = p.add_run(); r.text = "• Attack category excluded from training (leakage prevention)"
    r.font.size = Pt(20); r.font.color.rgb = DARK_GRAY

    # ══════════════════════════════════════════════════════════════
    # SLIDE 10: EXPERIMENT DESIGN + MODEL RESULTS
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Experiment Design & Model Results", notes=(
        "We split the 500K sample chronologically: 350K train, 75K validation, "
        "75K shifted test. This simulates temporal non-stationarity. "
        "Three models were compared on validation: XGBoost achieved the highest "
        "ROC-AUC at 0.9228 and was selected as the primary classifier. "
        "Validation attack rate is about 0.33%, so accuracy alone is insufficient "
        "for model selection."
    ))

    # Left: Chronological split + diagram
    c_left = card(s, 0.7, 1.05, 6.2, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Chronological Split"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ACCENT

    splits = [
        ("Train:", "350,000 flows"),
        ("Validation:", "75,000 flows (attack rate ≈ 0.33%)"),
        ("Shifted Test:", "75,000 flows (attack rate ≈ 6.30%)"),
    ]
    for label, val in splits:
        p = tf.add_paragraph(); p.space_before = Pt(6)
        r1 = p.add_run(); r1.text = label + " "
        r1.font.bold = True; r1.font.size = Pt(24); r1.font.color.rgb = NAVY
        r2 = p.add_run(); r2.text = val
        r2.font.size = Pt(24); r2.font.color.rgb = DARK_GRAY

    # embed timeline diagram
    time_img = os.path.join(DIAGRAMS_DIR, "diagram_temporal_shift_timeline.png")
    if os.path.exists(time_img):
        s.shapes.add_picture(time_img, Inches(0.8), Inches(4.0),
                             width=Inches(5.9))

    # Right: Model comparison table
    c_right = card(s, 7.1, 1.05, 5.5, 3.4)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Model Comparison (Validation)"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY

    models = [
        ("Logistic Regression", "0.7499"),
        ("Random Forest", "0.8526"),
        ("XGBoost ✓", "0.9228"),
    ]
    for name, auc in models:
        p = tf.add_paragraph(); p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = name + "  →  "
        r1.font.size = Pt(24); r1.font.color.rgb = DARK_GRAY
        r1.font.bold = ("XGBoost" in name)
        r2 = p.add_run(); r2.text = "AUC " + auc
        r2.font.size = Pt(26); r2.font.bold = True
        r2.font.color.rgb = ACCENT if "XGBoost" in name else DARK_GRAY

    # Shift stats box
    c_shift = card(s, 7.1, 4.65, 5.5, 2.3, fill=RGBColor(254, 243, 199))
    tf = c_shift.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Shift Impact (Shifted Test)"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    shift_stats = [
        ("Error rate:", "4.57%  (vs 1.00% validation)"),
        ("Avg confidence:", "96.82%  (vs 98.65% val)"),
        ("Total errors:", "3,427  in 75,000 flows"),
    ]
    for label, val in shift_stats:
        p = tf.add_paragraph(); p.space_before = Pt(4)
        r1 = p.add_run(); r1.text = label + " "
        r1.font.bold = True; r1.font.size = Pt(20); r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run(); r2.text = val
        r2.font.size = Pt(20); r2.font.color.rgb = RED

    # ══════════════════════════════════════════════════════════════
    # SLIDE 11: RELIABILITY ENGINE + REVIEW ALLOCATION
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Reliability Engine & Review Allocation", notes=(
        "We implemented four complementary reliability signals. Confidence measures "
        "prediction uncertainty as 1 minus max probability. OOD uses Mahalanobis-like "
        "distance to the training centroid. Drift uses Population Stability Index "
        "across features. Historical error measures proximity to training-time mistakes "
        "(currently uses training-time performance and would benefit from an out-of-fold "
        "estimate). These signals are combined into a composite risk score, and the "
        "highest-risk predictions are selected for simulated human review."
    ))

    # Four signal cards
    sig_items = [
        ("① Confidence", "1 – max P(y|x)\nCloseness to decision boundary", ACCENT),
        ("② OOD Distance", "Mahalanobis-like distance\nto training centroid", GREEN),
        ("③ Drift (PSI)", "Population Stability Index\nacross features", AMBER),
        ("④ Historical Error", "Proximity to training-time\nmistake patterns*", RED),
    ]
    sig_positions = [(0.7, 1.05, 2.85, 2.7), (3.7, 1.05, 2.85, 2.7),
                     (6.7, 1.05, 2.85, 2.7), (9.7, 1.05, 2.85, 2.7)]
    for (title, desc, col), (l, t, w, h) in zip(sig_items, sig_positions):
        c = card(s, l, t, w, h)
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title
        p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = col
        p = tf.add_paragraph(); p.text = desc
        p.font.size = Pt(20); p.font.color.rgb = DARK_GRAY; p.space_before = Pt(8)

    # Combination arrow + review mechanism
    c_combo = card(s, 0.7, 4.0, 11.9, 3.0)
    tf = c_combo.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Signals  →  Normalize  →  Weighted Composite Score  →  Rank  →  Review Top-k"
    p.font.size = Pt(24); p.font.bold = True; p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph(); p.space_before = Pt(10)
    p.text = "Review is simulated using ground-truth labels as evaluation oracle (no actual human reviewers)"
    p.font.size = Pt(22); p.font.color.rgb = DARK_GRAY; p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph(); p.space_before = Pt(8)
    p.text = "*Historical error signal currently uses training-time performance; would benefit from out-of-fold estimation"
    p.font.size = Pt(18); p.font.italic = True; p.font.color.rgb = MUTED
    p.alignment = PP_ALIGN.CENTER

    # ══════════════════════════════════════════════════════════════
    # SLIDE 12: IMPLEMENTED MODULES + SHIFTED-TEST RESULTS
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Implemented Modules & Shift Results", notes=(
        "This slide lists the implemented modules. We have data preprocessing, "
        "chronological splitting, three baseline models, all four reliability signals, "
        "three review strategies (confidence-only, static multi-factor, and feedback "
        "adaptive), and an evaluation pipeline with budget-based error-capture metrics. "
        "Under temporal shift, the error rate jumped from 1% to 4.57%, while average "
        "confidence only dropped from 98.65% to 96.82%, confirming that confidence "
        "alone is not sufficient to detect all errors."
    ))

    # Left: modules
    c_left = card(s, 0.7, 1.05, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Implemented Modules"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ACCENT

    add_bullets(tf, [
        "Data preprocessing + chronological split",
        "XGBoost, Random Forest, Logistic Regression",
        "Four reliability signal extractors",
        "Three review strategies implemented",
        "Budget-based evaluation pipeline",
    ], size=Pt(22))

    # Right: shift comparison
    c_right = card(s, 6.7, 1.05, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Validation → Shifted Test"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = NAVY

    comparisons = [
        ("Attack rate:", "0.33%  →  6.30%", "19× increase"),
        ("Error rate:", "1.00%  →  4.57%", "4.6× increase"),
        ("Avg confidence:", "98.65%  →  96.82%", "Only slight drop"),
        ("Total errors:", "747  →  3,427", "4.6× more errors"),
    ]
    for label, vals, note in comparisons:
        p = tf.add_paragraph(); p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = label + "\n"
        r1.font.bold = True; r1.font.size = Pt(22); r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run(); r2.text = vals + "  "
        r2.font.size = Pt(24); r2.font.bold = True; r2.font.color.rgb = RED
        r3 = p.add_run(); r3.text = "(" + note + ")"
        r3.font.size = Pt(18); r3.font.italic = True; r3.font.color.rgb = MUTED

    # ══════════════════════════════════════════════════════════════
    # SLIDE 13: REVIEW STRATEGY RESULTS (table + chart)
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Review Strategy Results", notes=(
        "This table shows the percentage of total errors captured at each review "
        "budget. At 1% budget, Feedback Adaptive captures 17.80% of errors versus "
        "13.51% for confidence-only. At 2%, it captures 34.26% vs 26.73%. "
        "However, at 5% and 10%, confidence-only outperforms multi-factor strategies. "
        "This is an honest finding — the multi-factor approach shows its advantage "
        "specifically at tight budgets where review capacity is most constrained."
    ))

    # Results table
    t = s.shapes.add_table(5, 4, Inches(0.7), Inches(1.05), Inches(11.9), Inches(3.2))
    tbl = t.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(3.1)
    tbl.columns[2].width = Inches(3.1)
    tbl.columns[3].width = Inches(3.2)

    res_hdrs = ["Budget", "Confidence-Only", "Static Multi-Factor", "Feedback Adaptive"]
    for i, h in enumerate(res_hdrs):
        cell = tbl.cell(0, i); cell.text = h
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True; p.font.size = Pt(20); p.font.color.rgb = WHITE

    res_rows = [
        ("1%",  "13.51%", "17.51%", "17.80%"),
        ("2%",  "26.73%", "33.99%", "34.26%"),
        ("5%",  "65.45%", "54.57%", "45.90%"),
        ("10%", "84.01%", "65.42%", "52.35%"),
    ]
    for r, row_data in enumerate(res_rows, 1):
        for c, val in enumerate(row_data):
            cell = tbl.cell(r, c); cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 == 0 else CARD_ALT
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(22)
                p.font.bold = (c == 3 and r <= 2) or c == 0
                if c == 3 and r <= 2:
                    p.font.color.rgb = GREEN
                elif c == 1 and r >= 3:
                    p.font.color.rgb = ACCENT
                else:
                    p.font.color.rgb = DARK_GRAY

    # Key observation box
    obs_box = card(s, 0.7, 4.5, 11.9, 2.5)
    tf = obs_box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "KEY OBSERVATIONS"
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY

    add_bullets(tf, [
        ("At tight budgets (1–2%):", "multi-factor strategies capture more errors than confidence alone"),
        ("At larger budgets (5–10%):", "confidence-only outperforms — multi-factor advantage diminishes"),
        ("Interpretation:", "strategy effectiveness is budget-dependent, not universally superior"),
    ], size=Pt(22))

    # Embed results chart if available
    chart_img = os.path.join(DIAGRAMS_DIR, "diagram_results_line_chart.png")
    # Skip chart embed to keep slide clean — table is sufficient

    # ══════════════════════════════════════════════════════════════
    # SLIDE 14: LIMITATIONS + FUTURE WORK
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Limitations & Phase-2 Plan", notes=(
        "Current limitations: single binary classification dataset, simulated review "
        "rather than actual human reviewers, no model recalibration applied, historical "
        "error signal uses training-time data rather than out-of-fold estimates, and "
        "subgroup fairness analysis is not applicable to network-flow data — planned "
        "for a future dataset with demographic attributes. Phase 2 will generalize "
        "the framework to diverse tabular datasets, add online drift monitoring, "
        "and build an explainability interface."
    ))

    # Left: Limitations
    c_left = card(s, 0.7, 1.05, 5.8, 5.9)
    tf = c_left.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Current Limitations"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = RED

    add_bullets(tf, [
        "Single dataset (binary classification only)",
        "Simulated review, not actual human reviewers",
        "No model recalibration applied",
        "Historical error uses training-time data\n(would benefit from out-of-fold estimate)",
        "Subgroup/fairness: not applicable to network\ndata — planned for future demographic dataset",
    ], size=Pt(20))

    # Right: Phase 2 plan
    c_right = card(s, 6.7, 1.05, 5.9, 5.9)
    tf = c_right.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Phase-2 Plan"
    p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = GREEN

    add_bullets(tf, [
        "Generalize to diverse tabular datasets",
        "Online drift monitoring & live recalibration",
        "Explainability interface for flagged cases",
        "Compare with learned deferral baselines",
        "Evaluate on datasets with demographic\nattributes for fairness analysis",
    ], size=Pt(20))

    # Phase 2 flow diagram if available
    p2_img = os.path.join(DIAGRAMS_DIR, "diagram_phase2_platform.png")
    # Embedding in the bottom would make slide too dense at readable fonts

    # ══════════════════════════════════════════════════════════════
    # SLIDE 15: CONCLUSION
    # ══════════════════════════════════════════════════════════════
    s = prs.slides.add_slide(blank)
    base(s, "Conclusion", notes=(
        "To summarize: we built and evaluated a working research prototype for "
        "budget-constrained human-review allocation under distribution shift. "
        "The multi-factor approach shows promise at tight review budgets but is "
        "not universally superior. This is a preliminary empirical investigation, "
        "not a solved problem. Phase 2 will focus on generalization and explainability. "
        "Thank you for your time and feedback."
    ))

    c = card(s, 0.7, 1.05, 11.9, 5.4)
    tf = c.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "Summary of Contributions"
    p.font.size = Pt(30); p.font.bold = True; p.font.color.rgb = NAVY

    conclusions = [
        ("Built:", "A working prototype combining four complementary reliability "
         "signals for human-review allocation under temporal shift"),
        ("Evaluated:", "On 500K flows from BigFlow-NIDS with chronological "
         "splitting, comparing three review strategies at four budget levels"),
        ("Found:", "Multi-factor prioritization captures more errors at tight "
         "budgets (1–2%); confidence-only is more effective at larger budgets"),
        ("Acknowledged:", "Strategy effectiveness is budget-dependent — this is "
         "a preliminary empirical finding, not a universal solution"),
        ("Next:", "Phase 2 → diverse datasets, online drift, explainability"),
    ]
    for label, text in conclusions:
        p = tf.add_paragraph(); p.space_before = Pt(8)
        r1 = p.add_run(); r1.text = label + " "
        r1.font.bold = True; r1.font.size = Pt(24); r1.font.color.rgb = ACCENT
        r2 = p.add_run(); r2.text = text
        r2.font.size = Pt(24); r2.font.color.rgb = DARK_GRAY

    # Thank you line
    p = tf.add_paragraph(); p.space_before = Pt(20)
    p.text = "Thank you for your time and feedback."
    p.font.size = Pt(26); p.font.italic = True
    p.font.color.rgb = NAVY; p.alignment = PP_ALIGN.CENTER

    # ── SAVE ────────────────────────────────────────────────────
    prs.save(PPTX_PATH)
    print(f"\n[OK] Saved {len(prs.slides)} slides to:\n   {PPTX_PATH}")
    print(f"   File size: {os.path.getsize(PPTX_PATH):,} bytes")


if __name__ == "__main__":
    build_deck()
