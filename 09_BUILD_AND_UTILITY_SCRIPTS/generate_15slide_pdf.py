"""
Generate 15-Slide PDF matching the PPTX capstone presentation.
Uses reportlab for direct PDF rendering (no PowerPoint COM needed).
"""

import os
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PDF_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pdf")
PDF_ALT = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU_v2.pdf")

# 16:9 page  (13.333 x 7.5 inches)
PW, PH = 13.333 * inch, 7.5 * inch

# Colours
NAVY      = HexColor("#0B1924")
ACCENT    = HexColor("#0066CC")
DARK_GRAY = HexColor("#334155")
LIGHT_BG  = HexColor("#F8FAFC")
CARD_BG   = HexColor("#FFFFFF")
BORDER    = HexColor("#CBD5E1")
GREEN     = HexColor("#16A34A")
RED       = HexColor("#DC2626")
AMBER     = HexColor("#D97706")
MUTED     = HexColor("#64748B")
CARD_ALT  = HexColor("#F1F5F9")
GAP_BG    = HexColor("#FEF3C7")
RQ_BG     = HexColor("#EEF2FF")


class SlideCanvas(canvas.Canvas):
    """Custom canvas that adds slide numbers."""
    def __init__(self, *args, **kwargs):
        self._slide_num = 0
        self._total = 15
        super().__init__(*args, **kwargs)

    def showPage(self):
        self._slide_num += 1
        # slide number bottom-right
        self.saveState()
        self.setFont("Helvetica", 10)
        self.setFillColor(MUTED)
        self.drawRightString(PW - 0.5 * inch, 0.35 * inch,
                             f"{self._slide_num} / {self._total}")
        self.restoreState()
        super().showPage()


def build_pdf():
    # Check if primary path is locked
    target = PDF_PATH
    try:
        with open(target, "ab") as f:
            pass
    except (PermissionError, OSError):
        target = PDF_ALT
        print(f"  Primary PDF locked, writing to: {target}")

    c = SlideCanvas(target, pagesize=(PW, PH))
    c.setTitle("Adaptive Human-Review Allocation - Capstone Phase-1")
    c.setAuthor("PES1PG25CA101")

    logo = None
    if os.path.exists(LOGO_PATH):
        logo = ImageReader(LOGO_PATH)

    # ── Helpers ──────────────────────────────────────────────────
    def slide_bg():
        c.setFillColor(LIGHT_BG)
        c.rect(0, 0, PW, PH, fill=1, stroke=0)
        # top accent bar
        c.setFillColor(NAVY)
        c.rect(0, PH - 0.10 * inch, PW, 0.10 * inch, fill=1, stroke=0)

    def add_logo():
        if logo:
            c.drawImage(logo, PW - 1.9 * inch, PH - 0.82 * inch,
                        width=1.5 * inch, height=0.6 * inch,
                        preserveAspectRatio=True, mask='auto')

    def heading(text, y=None):
        if y is None:
            y = PH - 0.75 * inch
        c.setFont("Helvetica-Bold", 28)
        c.setFillColor(NAVY)
        c.drawString(0.7 * inch, y, text)

    def draw_card(x, y, w, h, fill=CARD_BG):
        c.setFillColor(fill)
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    def text_block(x, y, lines, font="Helvetica", size=18, color=DARK_GRAY,
                   leading=24, max_width=None):
        """Draw multi-line text, returns final y position."""
        to = c.beginText(x, y)
        to.setFont(font, size)
        to.setFillColor(color)
        to.setLeading(leading)
        for line in lines:
            to.textLine(line)
        c.drawText(to)
        return y - len(lines) * leading

    def draw_table(x, y, headers, rows, col_widths, header_bg=NAVY,
                   font_size=14, row_height=0.38 * inch, header_height=0.42 * inch):
        """Draw a simple table."""
        cy = y
        # Header row
        cx = x
        for i, (hdr, w) in enumerate(zip(headers, col_widths)):
            c.setFillColor(header_bg if i < len(headers) - 1 or header_bg == NAVY else ACCENT)
            c.rect(cx, cy - header_height, w, header_height, fill=1, stroke=0)
            c.setFillColor(white)
            c.setFont("Helvetica-Bold", font_size)
            c.drawString(cx + 6, cy - header_height + 10, hdr)
            cx += w
        cy -= header_height

        # Data rows
        for r_idx, row in enumerate(rows):
            cx = x
            bg = CARD_BG if r_idx % 2 == 0 else CARD_ALT
            for c_idx, (val, w) in enumerate(zip(row, col_widths)):
                c.setFillColor(bg)
                c.rect(cx, cy - row_height, w, row_height, fill=1, stroke=0)
                c.setStrokeColor(BORDER)
                c.setLineWidth(0.3)
                c.rect(cx, cy - row_height, w, row_height, fill=0, stroke=1)
                c.setFillColor(DARK_GRAY)
                c.setFont("Helvetica", font_size - 1)
                # Truncate if needed
                display = val
                c.drawString(cx + 6, cy - row_height + 10, display)
                cx += w
            cy -= row_height
        return cy

    # ══════════════════════════════════════════════════════════════
    # SLIDE 1: TITLE
    # ══════════════════════════════════════════════════════════════
    c.setFillColor(CARD_ALT)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PH - 0.14 * inch, PW, 0.14 * inch, fill=1, stroke=0)

    if logo:
        c.drawImage(logo, PW - 2.5 * inch, PH - 1.1 * inch,
                    width=2.0 * inch, height=0.8 * inch,
                    preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(ACCENT)
    c.drawString(0.8 * inch, PH - 1.2 * inch,
                 "CAPSTONE PROJECT PHASE-1  |  PRESENTATION-2")

    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(NAVY)
    c.drawString(0.8 * inch, PH - 1.9 * inch,
                 "Adaptive Human-Review Allocation")
    c.drawString(0.8 * inch, PH - 2.45 * inch,
                 "for Reliable Machine Learning")
    c.drawString(0.8 * inch, PH - 3.0 * inch,
                 "Under Distribution Shift")

    c.setFont("Helvetica", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(0.8 * inch, PH - 3.6 * inch,
                 "Course: UQ25CA741A  |  Dept. of Computer Applications  |  PES University, Bangalore")

    # Student card
    draw_card(0.8 * inch, 0.8 * inch, 5.2 * inch, 1.5 * inch)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(ACCENT)
    c.drawString(1.0 * inch, 2.0 * inch, "STUDENT")
    c.setFont("Helvetica-Bold", 17); c.setFillColor(NAVY)
    c.drawString(1.0 * inch, 1.65 * inch, "SRN: PES1PG25CA101")
    c.setFont("Helvetica", 15); c.setFillColor(DARK_GRAY)
    c.drawString(1.0 * inch, 1.3 * inch, "MCA - Data Analytics")

    # Guide card
    draw_card(6.5 * inch, 0.8 * inch, 5.5 * inch, 1.5 * inch)
    c.setFont("Helvetica-Bold", 12); c.setFillColor(ACCENT)
    c.drawString(6.7 * inch, 2.0 * inch, "PROJECT GUIDE")
    c.setFont("Helvetica-Bold", 17); c.setFillColor(NAVY)
    c.drawString(6.7 * inch, 1.65 * inch, "Prof. Dilip Kumar Maripuri")
    c.setFont("Helvetica", 15); c.setFillColor(DARK_GRAY)
    c.drawString(6.7 * inch, 1.3 * inch, "Dept. of Computer Applications")

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 2: ABSTRACT
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Abstract")

    draw_card(0.7 * inch, 0.5 * inch, 11.9 * inch, 5.9 * inch)

    abstract = [
        ("Problem:", "ML systems produce high prediction volumes, but manual verification capacity is",
         "limited (typically 1-5%). Models can make confident errors when distributions change."),
        ("Approach:", "We investigate combining four complementary reliability signals - prediction",
         "uncertainty, OOD distance, feature-level drift, and historical error proximity."),
        ("Experiment:", "We evaluate on a 500K-flow sample from BigFlow-NIDS using a chronological",
         "train/validation/shifted-test partition."),
        ("Observation:", "Multi-factor prioritization captures more errors at tight budgets (1-2%),",
         "while confidence-only captures more at larger budgets (5-10%)."),
        ("Future:", "Phase 2 will investigate generalization across diverse tabular datasets and",
         "add explainability features."),
    ]
    y = PH - 1.35 * inch
    for label, line1, line2 in abstract:
        c.setFont("Helvetica-Bold", 18); c.setFillColor(ACCENT)
        c.drawString(1.0 * inch, y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 18)
        c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
        c.drawString(1.0 * inch + lw + 6, y, line1)
        c.drawString(1.0 * inch, y - 22, line2)
        y -= 62

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 3: PROBLEM & PROPOSED SOLUTION
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Problem & Proposed Solution")

    # Left card
    draw_card(0.7 * inch, 0.5 * inch, 5.6 * inch, 5.9 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(RED)
    c.drawString(0.9 * inch, y, "THE PROBLEM"); y -= 32

    problems = [
        "ML models produce high-volume predictions",
        "Humans can inspect only 1-5% of outputs",
        "Confidence alone fails under distribution shift",
    ]
    c.setFont("Helvetica", 18); c.setFillColor(DARK_GRAY)
    for p in problems:
        c.drawString(1.0 * inch, y, "* " + p); y -= 28

    y -= 16
    c.setFont("Helvetica-Bold", 22); c.setFillColor(GREEN)
    c.drawString(0.9 * inch, y, "OUR APPROACH"); y -= 32

    approach = [
        "Combine 4 complementary reliability signals",
        "Score & rank predictions by composite risk",
        "Review highest-risk cases within fixed budget",
    ]
    c.setFont("Helvetica", 18); c.setFillColor(DARK_GRAY)
    for p in approach:
        c.drawString(1.0 * inch, y, "* " + p); y -= 28

    # Right: pipeline diagram
    arch_img = os.path.join(DIAGRAMS_DIR, "diagram_system_architecture.png")
    if os.path.exists(arch_img):
        c.drawImage(arch_img, 6.5 * inch, 0.6 * inch,
                    width=6.0 * inch, height=5.5 * inch,
                    preserveAspectRatio=True, mask='auto')

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 4: RESEARCH QUESTION & OBJECTIVES
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Research Question & Objectives")

    # RQ box
    draw_card(0.7 * inch, PH - 2.6 * inch, 11.9 * inch, 1.5 * inch, fill=RQ_BG)
    c.setFont("Helvetica-Oblique", 18); c.setFillColor(NAVY)
    c.drawString(0.9 * inch, PH - 1.55 * inch,
                 "RQ: Can combining multiple complementary reliability signals identify model")
    c.drawString(0.9 * inch, PH - 1.85 * inch,
                 "errors more effectively than prediction confidence alone, under distribution")
    c.drawString(0.9 * inch, PH - 2.15 * inch,
                 "shift and constrained review budgets?")

    # Objectives box
    draw_card(0.7 * inch, 0.5 * inch, 11.9 * inch, 3.8 * inch)
    c.setFont("Helvetica-Bold", 24); c.setFillColor(ACCENT)
    c.drawString(0.9 * inch, 3.9 * inch, "PHASE-1 OBJECTIVES")

    objs = [
        ("O1:", "Build a prototype pipeline for budget-constrained review allocation"),
        ("O2:", "Implement four complementary reliability signals"),
        ("O3:", "Evaluate under controlled temporal shift using chronological splitting"),
        ("O4:", "Compare review strategies at 1%, 2%, 5%, and 10% budgets"),
    ]
    y = 3.4 * inch
    for label, text in objs:
        c.setFont("Helvetica-Bold", 20); c.setFillColor(ACCENT)
        c.drawString(1.0 * inch, y, label)
        c.setFont("Helvetica", 20); c.setFillColor(DARK_GRAY)
        c.drawString(1.5 * inch, y, text)
        y -= 36

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 5: BACKGROUND & LITERATURE GAP
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Background & Literature Gap")

    bg_items = [
        ("Selective Classification", "Abstention when uncertain (Geifman & El-Yaniv, 2017)", ACCENT),
        ("Model Calibration", "Overconfidence under shift (Guo et al., 2017)", RED),
        ("OOD Detection", "Feature-space novelty (Lee et al., 2018; Yang et al., 2024)", GREEN),
        ("Learning to Defer", "Human-AI deferral under cost (Mozannar & Sontag, 2020)", AMBER),
    ]
    positions = [
        (0.7 * inch, PH - 3.3 * inch, 5.6 * inch, 1.9 * inch),
        (6.7 * inch, PH - 3.3 * inch, 5.9 * inch, 1.9 * inch),
        (0.7 * inch, PH - 5.5 * inch, 5.6 * inch, 1.9 * inch),
        (6.7 * inch, PH - 5.5 * inch, 5.9 * inch, 1.9 * inch),
    ]
    for (title, desc, col), (bx, by, bw, bh) in zip(bg_items, positions):
        draw_card(bx, by, bw, bh)
        c.setFont("Helvetica-Bold", 21); c.setFillColor(col)
        c.drawString(bx + 10, by + bh - 30, title)
        c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
        c.drawString(bx + 10, by + bh - 56, desc)

    # Gap banner
    draw_card(0.7 * inch, 0.4 * inch, 11.9 * inch, 0.75 * inch, fill=GAP_BG)
    c.setFont("Helvetica-Bold", 17); c.setFillColor(NAVY)
    c.drawString(0.9 * inch, 0.72 * inch,
                 "GAP: No existing work combines all four signal types under explicit operational")
    c.drawString(0.9 * inch, 0.48 * inch,
                 "review budgets with temporal shift evaluation.")

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 6: LITERATURE SURVEY (Papers 1-5)
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Literature Survey (1/2)")

    headers_lit = ["Paper", "Venue / Year", "Relevance"]
    col_w = [4.3 * inch, 3.5 * inch, 4.1 * inch]
    papers1 = [
        ("BigFlow-NIDS: Large-Scale Benchmark", "Mendeley / Elsevier 2026", "Primary evaluation dataset (66.9M flows)"),
        ("Consistent Estimators for L2D", "Mozannar & Sontag, ICML 2020", "Theoretical human-AI deferral formulation"),
        ("Deep Learning to Defer (Multi-Expert)", "Wei et al., ICML 2024", "Extends deferral to multi-expert pools"),
        ("Selective Classification for DNNs", "Geifman & El-Yaniv, NeurIPS 2017", "Risk-coverage trade-offs / abstention"),
        ("Calibration of Modern Neural Networks", "Guo et al., ICML 2017", "Model overconfidence under shift"),
    ]
    draw_table(0.7 * inch, PH - 1.1 * inch, headers_lit, papers1, col_w,
               font_size=15, row_height=0.7 * inch)

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 7: LITERATURE SURVEY (Papers 6-10)
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Literature Survey (2/2)")

    papers2 = [
        ("Conformal Prediction & Dist-Free UQ", "Angelopoulos & Bates, arXiv 2021", "Distribution-free uncertainty intervals"),
        ("Generalized OOD Detection Survey", "Yang et al., IEEE TPAMI 2024", "Comprehensive OOD detection taxonomy"),
        ("Unified Framework for OOD Detection", "Lee et al., NeurIPS 2018", "Mahalanobis distance for OOD"),
        ("WILDS: In-The-Wild Distribution Shifts", "Koh et al., ICML 2021", "Real-world shift benchmarks"),
        ("Sample Efficient Learning to Defer", "Charusaie et al., NeurIPS 2022", "Budget-constrained expert allocation"),
    ]
    draw_table(0.7 * inch, PH - 1.1 * inch, headers_lit, papers2, col_w,
               font_size=15, row_height=0.7 * inch)

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 8: COMPARATIVE STUDY
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Comparative Study")

    comp_hdrs = ["Dimension", "Random", "Confidence", "L2D / OOD", "This Work"]
    comp_w = [2.6 * inch, 1.7 * inch, 1.9 * inch, 2.2 * inch, 3.5 * inch]
    comp_rows = [
        ("Confidence signal",   "No", "Yes (primary)", "Optional", "Yes (normalized)"),
        ("OOD / Novelty",       "No", "No",            "Yes",      "Yes (Mahalanobis)"),
        ("Drift measurement",   "No", "No",            "No",       "Yes (PSI)"),
        ("Historical error",    "No", "No",            "Implicit", "Yes (error proximity)"),
        ("Budget-aware eval.",  "--", "Manual tuning",  "Hard cutoff", "1%, 2%, 5%, 10%"),
        ("Temporal shift eval.","Yes","Rarely",         "Partial",  "Yes (chronological)"),
    ]
    draw_table(0.7 * inch, PH - 1.1 * inch, comp_hdrs, comp_rows, comp_w,
               font_size=14, row_height=0.55 * inch)

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 9: DATASET & DATA REPRESENTATION
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Dataset & Data Representation")

    # Left card
    draw_card(0.7 * inch, 0.5 * inch, 5.6 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(ACCENT)
    c.drawString(0.9 * inch, y, "BigFlow-NIDS Benchmark"); y -= 36

    ds_items = [
        ("Full scale:", "66.9M flows, 55 attributes"),
        ("Dev sample:", "500,000 flows (current expts)"),
        ("Source:", "Elsevier/Mendeley 2026"),
        ("Format:", "CSV/Parquet, chronological order"),
    ]
    for label, val in ds_items:
        c.setFont("Helvetica-Bold", 18); c.setFillColor(NAVY)
        c.drawString(0.9 * inch, y, "* " + label)
        lw = c.stringWidth("* " + label, "Helvetica-Bold", 18)
        c.setFont("Helvetica", 18); c.setFillColor(DARK_GRAY)
        c.drawString(0.9 * inch + lw + 4, y, val)
        y -= 30

    # Right card
    draw_card(6.5 * inch, 0.5 * inch, 6.1 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(NAVY)
    c.drawString(6.7 * inch, y, "Features (X) & Target (Y)"); y -= 36

    c.setFont("Helvetica-Bold", 19); c.setFillColor(ACCENT)
    c.drawString(6.7 * inch, y, "X: 49 numerical network-flow features"); y -= 30

    x_items = ["Ports, protocol, packet counts, bytes",
               "Throughput, flow duration, IAT stats",
               "TCP flags, window sizes, packet lengths"]
    c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
    for item in x_items:
        c.drawString(6.8 * inch, y, "* " + item); y -= 26

    y -= 12
    c.setFont("Helvetica-Bold", 19); c.setFillColor(ACCENT)
    c.drawString(6.7 * inch, y, "Y: Binary - Benign (0) vs Attack (1)"); y -= 30
    c.setFont("Helvetica", 16); c.setFillColor(DARK_GRAY)
    c.drawString(6.8 * inch, y, "* Attack category excluded (leakage prevention)")

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 10: EXPERIMENT DESIGN & MODEL RESULTS
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Experiment Design & Model Results")

    # Left: Chronological split
    draw_card(0.7 * inch, 0.5 * inch, 6.0 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(ACCENT)
    c.drawString(0.9 * inch, y, "Chronological Split"); y -= 36

    splits = [
        ("Train:", "350,000 flows"),
        ("Validation:", "75,000 flows (attack ~0.33%)"),
        ("Shifted Test:", "75,000 flows (attack ~6.30%)"),
    ]
    for label, val in splits:
        c.setFont("Helvetica-Bold", 20); c.setFillColor(NAVY)
        c.drawString(0.9 * inch, y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 20)
        c.setFont("Helvetica", 20); c.setFillColor(DARK_GRAY)
        c.drawString(0.9 * inch + lw + 6, y, val)
        y -= 34

    # Timeline diagram
    time_img = os.path.join(DIAGRAMS_DIR, "diagram_temporal_shift_timeline.png")
    if os.path.exists(time_img):
        c.drawImage(time_img, 0.8 * inch, 0.6 * inch,
                    width=5.6 * inch, height=2.5 * inch,
                    preserveAspectRatio=True, mask='auto')

    # Right: Model comparison + shift stats
    draw_card(6.9 * inch, 3.0 * inch, 5.7 * inch, 3.1 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 21); c.setFillColor(NAVY)
    c.drawString(7.1 * inch, y, "Model Comparison (Validation)"); y -= 36

    models = [
        ("Logistic Regression", "AUC 0.7499", DARK_GRAY),
        ("Random Forest", "AUC 0.8526", DARK_GRAY),
        ("XGBoost (selected)", "AUC 0.9228", ACCENT),
    ]
    for name, auc, col in models:
        c.setFont("Helvetica", 19); c.setFillColor(DARK_GRAY)
        c.drawString(7.2 * inch, y, name + "  ->  ")
        lw = c.stringWidth(name + "  ->  ", "Helvetica", 19)
        c.setFont("Helvetica-Bold", 20); c.setFillColor(col)
        c.drawString(7.2 * inch + lw, y, auc)
        y -= 32

    # Shift impact box
    draw_card(6.9 * inch, 0.5 * inch, 5.7 * inch, 2.2 * inch, fill=GAP_BG)
    y = 2.35 * inch
    c.setFont("Helvetica-Bold", 20); c.setFillColor(NAVY)
    c.drawString(7.1 * inch, y, "Shift Impact (Shifted Test)"); y -= 32

    shift_stats = [
        ("Error rate:", "4.57% (vs 1.00% val)"),
        ("Avg confidence:", "96.82% (vs 98.65% val)"),
        ("Total errors:", "3,427 in 75,000 flows"),
    ]
    for label, val in shift_stats:
        c.setFont("Helvetica-Bold", 17); c.setFillColor(DARK_GRAY)
        c.drawString(7.2 * inch, y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 17)
        c.setFont("Helvetica", 17); c.setFillColor(RED)
        c.drawString(7.2 * inch + lw + 4, y, val)
        y -= 26

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 11: RELIABILITY ENGINE & REVIEW ALLOCATION
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Reliability Engine & Review Allocation")

    sig_items = [
        ("(1) Confidence", "1 - max P(y|x)", "Decision boundary", ACCENT),
        ("(2) OOD Distance", "Mahalanobis-like", "Training centroid", GREEN),
        ("(3) Drift (PSI)", "Population Stability", "Feature-level shift", AMBER),
        ("(4) Historical Error", "Error proximity", "Training mistakes*", RED),
    ]
    x_positions = [0.7, 3.65, 6.6, 9.55]
    for (title, line1, line2, col), xp in zip(sig_items, x_positions):
        draw_card(xp * inch, PH - 3.6 * inch, 2.75 * inch, 2.3 * inch)
        c.setFont("Helvetica-Bold", 17); c.setFillColor(col)
        c.drawString((xp + 0.12) * inch, PH - 1.65 * inch, title)
        c.setFont("Helvetica", 16); c.setFillColor(DARK_GRAY)
        c.drawString((xp + 0.12) * inch, PH - 2.0 * inch, line1)
        c.drawString((xp + 0.12) * inch, PH - 2.3 * inch, line2)

    # Combination flow
    draw_card(0.7 * inch, 0.5 * inch, 11.9 * inch, 2.6 * inch)
    c.setFont("Helvetica-Bold", 20); c.setFillColor(NAVY)
    c.drawString(1.5 * inch, 2.7 * inch,
                 "Signals  ->  Normalize  ->  Weighted Composite  ->  Rank  ->  Review Top-k")
    c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
    c.drawString(1.8 * inch, 2.2 * inch,
                 "Review is simulated using ground-truth labels as evaluation oracle")
    c.setFont("Helvetica-Oblique", 14); c.setFillColor(MUTED)
    c.drawString(1.2 * inch, 1.7 * inch,
                 "*Historical error signal uses training-time performance; would benefit from out-of-fold estimation")

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 12: IMPLEMENTED MODULES & SHIFT RESULTS
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Implemented Modules & Shift Results")

    # Left: modules
    draw_card(0.7 * inch, 0.5 * inch, 5.6 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(ACCENT)
    c.drawString(0.9 * inch, y, "Implemented Modules"); y -= 36

    modules = [
        "Data preprocessing + chronological split",
        "XGBoost, Random Forest, Logistic Reg.",
        "Four reliability signal extractors",
        "Three review strategies implemented",
        "Budget-based evaluation pipeline",
    ]
    c.setFont("Helvetica", 18); c.setFillColor(DARK_GRAY)
    for m in modules:
        c.drawString(1.0 * inch, y, "* " + m); y -= 30

    # Right: shift comparison
    draw_card(6.5 * inch, 0.5 * inch, 6.1 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(NAVY)
    c.drawString(6.7 * inch, y, "Validation -> Shifted Test"); y -= 40

    comparisons = [
        ("Attack rate:", "0.33% -> 6.30%", "(19x increase)"),
        ("Error rate:", "1.00% -> 4.57%", "(4.6x increase)"),
        ("Avg confidence:", "98.65% -> 96.82%", "(slight drop only)"),
        ("Total errors:", "747 -> 3,427", "(4.6x more errors)"),
    ]
    for label, vals, note in comparisons:
        c.setFont("Helvetica-Bold", 19); c.setFillColor(DARK_GRAY)
        c.drawString(6.8 * inch, y, label); y -= 26
        c.setFont("Helvetica-Bold", 20); c.setFillColor(RED)
        c.drawString(6.8 * inch, y, vals)
        lw = c.stringWidth(vals, "Helvetica-Bold", 20)
        c.setFont("Helvetica-Oblique", 15); c.setFillColor(MUTED)
        c.drawString(6.8 * inch + lw + 8, y, note)
        y -= 36

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 13: REVIEW STRATEGY RESULTS
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Review Strategy Results")

    res_hdrs = ["Budget", "Confidence-Only", "Static Multi-Factor", "Feedback Adaptive"]
    res_w = [2.0 * inch, 3.3 * inch, 3.3 * inch, 3.3 * inch]
    res_rows = [
        ("1%",  "13.51%", "17.51%", "17.80%"),
        ("2%",  "26.73%", "33.99%", "34.26%"),
        ("5%",  "65.45%", "54.57%", "45.90%"),
        ("10%", "84.01%", "65.42%", "52.35%"),
    ]
    draw_table(0.7 * inch, PH - 1.1 * inch, res_hdrs, res_rows, res_w,
               font_size=18, row_height=0.55 * inch, header_height=0.5 * inch)

    # Key observations
    draw_card(0.7 * inch, 0.5 * inch, 11.9 * inch, 2.2 * inch)
    c.setFont("Helvetica-Bold", 22); c.setFillColor(NAVY)
    c.drawString(0.9 * inch, 2.35 * inch, "KEY OBSERVATIONS")

    obs = [
        "* At tight budgets (1-2%): multi-factor captures more errors than confidence alone",
        "* At larger budgets (5-10%): confidence-only outperforms multi-factor",
        "* Strategy effectiveness is budget-dependent, not universally superior",
    ]
    y = 1.95 * inch
    c.setFont("Helvetica", 18); c.setFillColor(DARK_GRAY)
    for o in obs:
        c.drawString(1.0 * inch, y, o); y -= 28

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 14: LIMITATIONS & PHASE-2 PLAN
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Limitations & Phase-2 Plan")

    # Left: Limitations
    draw_card(0.7 * inch, 0.5 * inch, 5.6 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(RED)
    c.drawString(0.9 * inch, y, "Current Limitations"); y -= 34

    limitations = [
        "Single dataset (binary classification)",
        "Simulated review, not actual humans",
        "No model recalibration applied",
        "Historical error uses training-time data",
        "  (needs out-of-fold estimate)",
        "Subgroup/fairness: not applicable to",
        "  network data - planned for future",
    ]
    c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
    for lim in limitations:
        c.drawString(1.0 * inch, y, "* " + lim if not lim.startswith("  ") else lim); y -= 26

    # Right: Phase 2
    draw_card(6.5 * inch, 0.5 * inch, 6.1 * inch, 5.6 * inch)
    y = PH - 1.3 * inch
    c.setFont("Helvetica-Bold", 22); c.setFillColor(GREEN)
    c.drawString(6.7 * inch, y, "Phase-2 Plan"); y -= 34

    phase2 = [
        "Generalize to diverse tabular datasets",
        "Online drift monitoring & recalibration",
        "Explainability interface for flagged cases",
        "Compare with learned deferral baselines",
        "Evaluate on datasets with demographic",
        "  attributes for fairness analysis",
    ]
    c.setFont("Helvetica", 17); c.setFillColor(DARK_GRAY)
    for p2 in phase2:
        c.drawString(6.8 * inch, y, "* " + p2 if not p2.startswith("  ") else p2); y -= 26

    c.showPage()

    # ══════════════════════════════════════════════════════════════
    # SLIDE 15: CONCLUSION
    # ══════════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Conclusion")

    draw_card(0.7 * inch, 0.5 * inch, 11.9 * inch, 5.3 * inch)

    c.setFont("Helvetica-Bold", 24); c.setFillColor(NAVY)
    c.drawString(0.9 * inch, 5.4 * inch, "Summary of Contributions")

    conclusions = [
        ("Built:", "Working prototype combining four complementary reliability signals"),
        ("Evaluated:", "500K flows from BigFlow-NIDS with chronological splitting"),
        ("Found:", "Multi-factor captures more errors at tight budgets (1-2%)"),
        ("", "Confidence-only is more effective at larger budgets (5-10%)"),
        ("Acknowledged:", "Strategy effectiveness is budget-dependent (preliminary finding)"),
        ("Next:", "Phase 2 -> diverse datasets, online drift, explainability"),
    ]
    y = 4.9 * inch
    for label, text in conclusions:
        if label:
            c.setFont("Helvetica-Bold", 20); c.setFillColor(ACCENT)
            c.drawString(1.0 * inch, y, label)
            lw = c.stringWidth(label, "Helvetica-Bold", 20)
            c.setFont("Helvetica", 20); c.setFillColor(DARK_GRAY)
            c.drawString(1.0 * inch + lw + 6, y, text)
        else:
            c.setFont("Helvetica", 20); c.setFillColor(DARK_GRAY)
            c.drawString(1.7 * inch, y, text)
        y -= 34

    y -= 16
    c.setFont("Helvetica-Oblique", 22); c.setFillColor(NAVY)
    c.drawCentredString(PW / 2, y, "Thank you for your time and feedback.")

    c.showPage()

    # ── SAVE ──
    c.save()
    print(f"\n[OK] Saved 15-page PDF to:\n   {target}")
    print(f"   File size: {os.path.getsize(target):,} bytes")


if __name__ == "__main__":
    build_pdf()
