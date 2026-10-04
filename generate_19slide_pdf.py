"""
19-Page PDF matching the 19-slide PPTX capstone presentation.
Uses reportlab. Handles locked-file fallback.
"""
import os
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PDF_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pdf")
PDF_ALT = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU_v2.pdf")

PW, PH = 13.333 * inch, 7.5 * inch

NAVY      = HexColor("#0B192C")
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
PURPLE    = HexColor("#7C3AED")
GAP_BG    = HexColor("#FEF3C7")
RQ_BG     = HexColor("#EEF2FF")


class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._sn = 0; self._total = 19
        super().__init__(*args, **kwargs)
    def showPage(self):
        self._sn += 1
        self.saveState()
        self.setFont("Helvetica", 10); self.setFillColor(MUTED)
        self.drawRightString(PW - 0.5*inch, 0.35*inch, f"{self._sn} / {self._total}")
        self.restoreState()
        super().showPage()


def build_pdf():
    target = PDF_PATH
    try:
        with open(target, "ab") as f: pass
    except (PermissionError, OSError):
        target = PDF_ALT
        print(f"  Primary PDF locked, writing to: {target}")

    c = SlideCanvas(target, pagesize=(PW, PH))
    c.setTitle("Adaptive Human-Review Allocation - Capstone Phase-1")

    logo = ImageReader(LOGO_PATH) if os.path.exists(LOGO_PATH) else None

    def slide_bg():
        c.setFillColor(LIGHT_BG); c.rect(0,0,PW,PH,fill=1,stroke=0)
        c.setFillColor(NAVY); c.rect(0,PH-0.10*inch,PW,0.10*inch,fill=1,stroke=0)

    def add_logo():
        if logo: c.drawImage(logo, PW-1.9*inch, PH-0.82*inch, width=1.5*inch, height=0.6*inch, preserveAspectRatio=True, mask='auto')

    def heading(text, y=None):
        if y is None: y = PH - 0.75*inch
        c.setFont("Helvetica-Bold", 28); c.setFillColor(NAVY); c.drawString(0.7*inch, y, text)

    def draw_card(x, y, w, h, fill=CARD_BG):
        c.setFillColor(fill); c.setStrokeColor(BORDER); c.setLineWidth(0.5)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    def draw_img(name, x, y, w):
        p = os.path.join(DIAGRAMS_DIR, name)
        if os.path.exists(p):
            c.drawImage(p, x, y, width=w, height=w*0.45, preserveAspectRatio=True, mask='auto')

    def draw_table(x, y, headers, rows, col_widths, fs=14, rh=0.38*inch, hh=0.42*inch):
        cy = y; cx = x
        for i, (hdr, w) in enumerate(zip(headers, col_widths)):
            c.setFillColor(NAVY); c.rect(cx, cy-hh, w, hh, fill=1, stroke=0)
            c.setFillColor(white); c.setFont("Helvetica-Bold", fs)
            c.drawString(cx+4, cy-hh+8, hdr); cx += w
        cy -= hh
        for ri, row in enumerate(rows):
            cx = x
            bg = CARD_BG if ri%2==0 else CARD_ALT
            for ci, (val, w) in enumerate(zip(row, col_widths)):
                c.setFillColor(bg); c.rect(cx, cy-rh, w, rh, fill=1, stroke=0)
                c.setStrokeColor(BORDER); c.setLineWidth(0.3)
                c.rect(cx, cy-rh, w, rh, fill=0, stroke=1)
                c.setFillColor(DARK_GRAY); c.setFont("Helvetica", fs-1)
                # Handle multi-line
                lines = val.split('\n')
                for li, line in enumerate(lines):
                    c.drawString(cx+4, cy-rh+8+li*(-12 if li>0 else 0)+(len(lines)-1)*6, line if li==0 else line)
                cx += w
            cy -= rh
        return cy

    # ═══════════════════════════════════════════════════════════
    # SLIDE 1: TITLE
    # ═══════════════════════════════════════════════════════════
    c.setFillColor(CARD_ALT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    c.setFillColor(NAVY); c.rect(0,PH-0.14*inch,PW,0.14*inch,fill=1,stroke=0)
    if logo: c.drawImage(logo, PW-2.5*inch, PH-1.1*inch, width=2.0*inch, height=0.8*inch, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold",16); c.setFillColor(ACCENT)
    c.drawString(0.8*inch, PH-1.2*inch, "CAPSTONE PROJECT PHASE-1  |  PRESENTATION-2")
    c.setFont("Helvetica-Bold",32); c.setFillColor(NAVY)
    c.drawString(0.8*inch, PH-1.9*inch, "Adaptive Human-Review Allocation")
    c.drawString(0.8*inch, PH-2.45*inch, "for Reliable Machine Learning")
    c.drawString(0.8*inch, PH-3.0*inch, "Under Distribution Shift")
    c.setFont("Helvetica",14); c.setFillColor(DARK_GRAY)
    c.drawString(0.8*inch, PH-3.6*inch, "Course: UQ25CA741A  |  Dept. of Computer Applications  |  PES University, Bangalore")
    draw_card(0.8*inch, 0.8*inch, 5.2*inch, 1.5*inch)
    c.setFont("Helvetica-Bold",12); c.setFillColor(ACCENT); c.drawString(1.0*inch, 2.0*inch, "STUDENT")
    c.setFont("Helvetica-Bold",17); c.setFillColor(NAVY); c.drawString(1.0*inch, 1.65*inch, "SRN: PES1PG25CA101")
    c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY); c.drawString(1.0*inch, 1.3*inch, "MCA - Data Analytics")
    draw_card(6.5*inch, 0.8*inch, 5.5*inch, 1.5*inch)
    c.setFont("Helvetica-Bold",12); c.setFillColor(ACCENT); c.drawString(6.7*inch, 2.0*inch, "PROJECT GUIDE")
    c.setFont("Helvetica-Bold",17); c.setFillColor(NAVY); c.drawString(6.7*inch, 1.65*inch, "Prof. Dilip Kumar Maripuri")
    c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY); c.drawString(6.7*inch, 1.3*inch, "Dept. of Computer Applications")
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 2: ABSTRACT
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Abstract")
    draw_card(0.7*inch, 0.5*inch, 11.9*inch, 5.9*inch)
    abstract = [
        ("Problem:", "ML systems produce high prediction volumes, but manual verification", "capacity is limited (1-5%). Models make confident errors when distributions change."),
        ("Approach:", "We investigate combining four complementary reliability signals --", "uncertainty, OOD distance, drift, and historical error proximity."),
        ("Experiment:", "We evaluate on a 500K-flow sample from BigFlow-NIDS with a", "chronological train/validation/shifted-test partition."),
        ("Observation:", "Multi-factor captures more errors at tight budgets (1-2%);", "confidence-only captures more at larger budgets (5-10%)."),
        ("Future:", "Phase 2: generalize across diverse tabular datasets,", "add explainability features."),
    ]
    y = PH-1.35*inch
    for label, l1, l2 in abstract:
        c.setFont("Helvetica-Bold",17); c.setFillColor(ACCENT)
        c.drawString(1.0*inch, y, label)
        lw = c.stringWidth(label, "Helvetica-Bold", 17)
        c.setFont("Helvetica",16); c.setFillColor(DARK_GRAY)
        c.drawString(1.0*inch+lw+4, y, l1)
        c.drawString(1.0*inch, y-20, l2)
        y -= 56
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 3: PROBLEM SCENARIO + PURPOSE
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Introduction: Problem Scenario & Purpose")
    draw_card(0.7*inch, 0.5*inch, 5.6*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",22); c.setFillColor(RED); c.drawString(0.9*inch, y, "PROBLEM SCENARIO"); y-=32
    for t in ["ML systems produce high-volume predictions","Humans can inspect only 1-5% of outputs",
              "Confidence can be misleading under shift","Models make high-confidence errors on drifted data",
              "Current approaches mostly use a single signal"]:
        c.setFont("Helvetica",17); c.setFillColor(DARK_GRAY); c.drawString(1.0*inch, y, "* "+t); y-=26
    draw_card(6.5*inch, 0.5*inch, 6.1*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",22); c.setFillColor(GREEN); c.drawString(6.7*inch, y, "PURPOSE"); y-=32
    for t in ["Investigate multi-signal review allocation","Combine complementary reliability indicators",
              "Evaluate under explicit budget constraints","Study behavior under temporal distribution shift",
              "Build a working research prototype"]:
        c.setFont("Helvetica",17); c.setFillColor(DARK_GRAY); c.drawString(6.8*inch, y, "* "+t); y-=26
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 4: PROPOSED SOLUTION + SCOPE
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Proposed Solution & Scope")
    draw_img('diagram_system_architecture.png', 0.7*inch, 2.5*inch, 12.0*inch)
    draw_card(0.7*inch, 0.5*inch, 11.9*inch, 1.6*inch, fill=GAP_BG)
    c.setFont("Helvetica-Bold",20); c.setFillColor(NAVY); c.drawString(0.9*inch, 1.75*inch, "SCOPE (Phase 1)")
    c.setFont("Helvetica",16); c.setFillColor(DARK_GRAY)
    c.drawString(0.9*inch, 1.35*inch, "* Binary classification on network-flow data (BigFlow-NIDS benchmark)")
    c.drawString(0.9*inch, 1.0*inch, "* Evaluated under simulated review budget; not a live production deployment")
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 5: BACKGROUND STUDY
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Background Study")
    bg_items = [
        ("Confidence-Based Review", "Uses softmax scores; limited by overconfidence (Guo et al., 2017)", ACCENT),
        ("OOD Detection", "Feature-space distances for novelty (Lee et al., 2018; Yang et al., 2024)", GREEN),
        ("Distribution Shift Detection", "Population-level feature changes via PSI", AMBER),
        ("Selective Prediction / L2D", "Abstention & routing under cost (Geifman 2017; Mozannar 2020)", PURPLE),
        ("Human-in-the-Loop ML", "Integrating human expertise efficiently (Charusaie et al., 2022)", RED),
    ]
    positions = [(0.7, 5.7), (6.7, 5.7), (0.7, 3.6), (6.7, 3.6), (0.7, 1.5)]
    for (title, desc, col), (xp, yp) in zip(bg_items, positions):
        draw_card(xp*inch, yp*inch-0.5*inch, 5.6*inch if xp<5 else 5.9*inch, 1.6*inch)
        c.setFont("Helvetica-Bold",18); c.setFillColor(col)
        c.drawString((xp+0.15)*inch, yp*inch+0.7*inch, title)
        c.setFont("Helvetica",14); c.setFillColor(DARK_GRAY)
        c.drawString((xp+0.15)*inch, yp*inch+0.3*inch, desc)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 6: LITERATURE SURVEY 1-5
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Literature Survey (1/2)")
    papers1 = [
        ("1. BigFlow-NIDS Benchmark", "Mendeley/Elsevier 2026", "66.9M-flow benchmark, our primary dataset"),
        ("2. Learning to Defer to Expert", "Mozannar, ICML 2020", "Formalizes human-AI deferral under cost"),
        ("3. L2D with Multiple Experts", "Wei et al., ICML 2024", "Multi-expert routing for deferral"),
        ("4. Selective Classification", "Geifman, NeurIPS 2017", "Risk-coverage for abstention baselines"),
        ("5. Calibration of Neural Nets", "Guo et al., ICML 2017", "Model overconfidence under shift"),
    ]
    draw_table(0.7*inch, PH-1.1*inch, ["Paper","Venue/Year","Relevance"],
               papers1, [4.0*inch, 3.5*inch, 4.4*inch], fs=14, rh=0.65*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 7: LITERATURE SURVEY 6-10
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Literature Survey (2/2)")
    papers2 = [
        ("6. Conformal Prediction & UQ", "Angelopoulos, arXiv 2021", "Distribution-free uncertainty intervals"),
        ("7. Generalized OOD Survey", "Yang et al., TPAMI 2024", "Comprehensive OOD detection taxonomy"),
        ("8. Unified OOD Framework", "Lee et al., NeurIPS 2018", "Mahalanobis distance for OOD"),
        ("9. WILDS Benchmark", "Koh et al., ICML 2021", "Real-world distribution shift evaluation"),
        ("10. Sample Efficient L2D", "Charusaie, NeurIPS 2022", "Budget-constrained expert allocation"),
    ]
    draw_table(0.7*inch, PH-1.1*inch, ["Paper","Venue/Year","Relevance"],
               papers2, [4.0*inch, 3.5*inch, 4.4*inch], fs=14, rh=0.65*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 8: COMPARATIVE STUDY
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Comparative Study")
    comp_rows = [
        ("Confidence signal","No","Yes (primary)","Optional","Yes (normalized)"),
        ("OOD / Novelty","No","No","Yes","Yes (Mahalanobis)"),
        ("Drift measurement","No","No","No","Yes (PSI)"),
        ("Historical error","No","No","Implicit","Yes (error proximity)"),
        ("Budget-aware eval.","--","Manual tuning","Hard cutoff","1%, 2%, 5%, 10%"),
        ("Temporal shift eval.","Yes","Rarely","Partial","Yes (chronological)"),
    ]
    draw_table(0.7*inch, PH-1.1*inch, ["Dimension","Random","Confidence","L2D/OOD","This Work"],
               comp_rows, [2.6*inch, 1.7*inch, 2.0*inch, 2.1*inch, 3.5*inch], fs=13, rh=0.52*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 9: TOOLS & TECHNOLOGIES
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Tools & Technologies Used")
    cats = [
        ("DATA HANDLING", ACCENT, ["Python 3.x - Primary language","pandas - DataFrame ops, CSV/Parquet I/O","numpy - Numerical computations"]),
        ("ML MODELING", GREEN, ["scikit-learn - Preprocessing, LR, RF, metrics","XGBoost - Primary classifier","joblib - Model serialization"]),
        ("STATISTICAL ANALYSIS", AMBER, ["scipy - Mahalanobis, covariance, PSI","hashlib - Data integrity (SHA-256)","pathlib - Cross-platform file paths"]),
        ("INFRASTRUCTURE", PURPLE, ["Platform: Local Windows machine","Data format: CSV / Parquet","Pipeline: 26 sequential Python scripts"]),
    ]
    positions = [(0.7, PH-3.3*inch), (6.7, PH-3.3*inch), (0.7, PH-5.5*inch), (6.7, PH-5.5*inch)]
    for (title, col, items), (xp, yp) in zip(cats, positions):
        draw_card(xp*inch, yp, 5.6*inch if xp<5 else 5.9*inch, 1.9*inch)
        c.setFont("Helvetica-Bold",18); c.setFillColor(col)
        c.drawString((xp+0.15)*inch, yp+1.55*inch, title)
        c.setFont("Helvetica",14); c.setFillColor(DARK_GRAY)
        for i, item in enumerate(items):
            c.drawString((xp+0.2)*inch, yp+1.2*inch - i*22, "* "+item)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 10: FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Functional & Non-Functional Requirements")
    draw_card(0.7*inch, 0.5*inch, 6.0*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",20); c.setFillColor(ACCENT); c.drawString(0.9*inch, y, "FUNCTIONAL REQUIREMENTS"); y-=22
    c.setFont("Helvetica-Oblique",12); c.setFillColor(MUTED); c.drawString(0.9*inch, y, "Users: ML Practitioner, Reviewer, Evaluator"); y-=22
    frs = [("FR1:","Ingest & preprocess network-flow data"),("FR2:","Train & evaluate classification models"),
           ("FR3:","Compute confidence score per prediction"),("FR4:","Compute OOD distance per input"),
           ("FR5:","Measure feature-level drift (PSI)"),("FR6:","Compute historical error proximity"),
           ("FR7:","Generate composite risk score"),("FR8:","Allocate predictions to review queue"),
           ("FR9:","Report error-capture metrics per strategy")]
    for lab, desc in frs:
        c.setFont("Helvetica-Bold",13); c.setFillColor(NAVY); c.drawString(0.9*inch, y, lab)
        c.setFont("Helvetica",13); c.setFillColor(DARK_GRAY); c.drawString(1.5*inch, y, desc); y-=20

    draw_card(6.9*inch, 0.5*inch, 5.7*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",20); c.setFillColor(GREEN); c.drawString(7.1*inch, y, "NON-FUNCTIONAL"); y-=28
    nfrs = [("NFR1: Reproducibility","Deterministic splits, seeded models"),
            ("NFR2: Computation Time","Full pipeline in minutes on laptop"),
            ("NFR3: Interpretability","Clear signal definitions, weighted sum"),
            ("NFR4: Scalability","Design supports larger samples"),
            ("NFR5: Data Integrity","SHA-256 hash verification")]
    for lab, desc in nfrs:
        c.setFont("Helvetica-Bold",14); c.setFillColor(NAVY); c.drawString(7.1*inch, y, lab); y-=18
        c.setFont("Helvetica",13); c.setFillColor(DARK_GRAY); c.drawString(7.2*inch, y, desc); y-=24
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 11: ARCHITECTURE + PROCESS FLOW
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Architecture & ML Process Flow")
    draw_img('diagram_system_architecture.png', 0.7*inch, 3.2*inch, 12.0*inch)
    draw_img('diagram_process_flow.png', 0.7*inch, 0.5*inch, 12.0*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 12: DATABASE DESIGN
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Database Design (Conceptual Schema)")
    draw_img('diagram_er_schema.png', 0.7*inch, 0.5*inch, 12.0*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 13: DATASET + DATA REPRESENTATION
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Dataset & Data Representation")
    draw_card(0.7*inch, 0.5*inch, 5.6*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(ACCENT); c.drawString(0.9*inch, y, "BigFlow-NIDS Benchmark"); y-=32
    for lab, val in [("Full scale:","66.9M flows, 55 attrs, 32 attack types"),
                     ("Dev sample:","500,000 flows (current experiments)"),
                     ("Source:","Elsevier / Mendeley Data, 2026"),
                     ("Construction:","Four NetFlow datasets via Spark"),
                     ("Note:","Offline benchmark, NOT live traffic")]:
        c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(0.9*inch, y, "* "+lab)
        lw = c.stringWidth("* "+lab, "Helvetica-Bold", 16)
        c.setFont("Helvetica",16); c.setFillColor(DARK_GRAY); c.drawString(0.9*inch+lw+4, y, val); y-=26
    draw_card(6.5*inch, 0.5*inch, 6.1*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(NAVY); c.drawString(6.7*inch, y, "Features (X) & Target (Y)"); y-=30
    c.setFont("Helvetica-Bold",17); c.setFillColor(ACCENT); c.drawString(6.7*inch, y, "X: 49 numerical network-flow features"); y-=26
    for item in ["Ports, protocol, packet counts, bytes","Throughput, flow duration, IAT stats","TCP flags, window sizes, packet lengths"]:
        c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY); c.drawString(6.8*inch, y, "* "+item); y-=22
    y-=10
    c.setFont("Helvetica-Bold",17); c.setFillColor(ACCENT); c.drawString(6.7*inch, y, "Y: Binary - Benign (0) vs Attack (1)"); y-=24
    c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY)
    c.drawString(6.8*inch, y, "* Attack category excluded (leakage prevention)")
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 14: EXPERIMENT DESIGN + MODEL RESULTS
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Experiment Design & Model Results")
    draw_card(0.7*inch, 3.5*inch, 6.0*inch, 2.8*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",20); c.setFillColor(ACCENT); c.drawString(0.9*inch, y, "Chronological Split (500K)"); y-=30
    for lab, val in [("Train:","350,000 flows"),("Validation:","75,000 (attack ~0.33%)"),("Shifted Test:","75,000 (attack ~6.30%)")]:
        c.setFont("Helvetica-Bold",17); c.setFillColor(NAVY); c.drawString(0.9*inch, y, lab)
        lw = c.stringWidth(lab, "Helvetica-Bold", 17)
        c.setFont("Helvetica",17); c.setFillColor(DARK_GRAY); c.drawString(0.9*inch+lw+4, y, val); y-=26
    model_rows = [("Logistic Regression","0.9606","0.0693","0.7499"),("Random Forest","0.9801","0.1210","0.8526"),("XGBoost (selected)","0.9900","0.0552","0.9228")]
    draw_table(7.0*inch, PH-1.1*inch, ["Model","Acc","F1","AUC"], model_rows, [2.8*inch, 1.0*inch, 0.9*inch, 1.0*inch], fs=14, rh=0.4*inch)
    draw_card(0.7*inch, 0.5*inch, 11.9*inch, 2.6*inch, fill=CARD_ALT)
    c.setFont("Helvetica-Bold",18); c.setFillColor(NAVY); c.drawString(0.9*inch, 2.7*inch, "PSEUDOCODE: Training & Prediction")
    code = ["model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1)",
            "model.fit(X_train, y_train)",
            "probabilities = model.predict_proba(X_validation)",
            "confidence = max(probabilities, axis=1)",
            "roc_auc = roc_auc_score(y_validation, probabilities[:, 1])"]
    y = 2.3*inch
    c.setFont("Courier",13); c.setFillColor(DARK_GRAY)
    for line in code: c.drawString(1.0*inch, y, line); y-=18
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 15: RELIABILITY ENGINE + REVIEW ALLOCATION
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Reliability Engine & Review Allocation")
    draw_img('diagram_signals_allocation.png', 0.7*inch, 3.0*inch, 12.0*inch)
    draw_card(0.7*inch, 0.4*inch, 11.9*inch, 2.3*inch, fill=CARD_ALT)
    c.setFont("Helvetica-Bold",18); c.setFillColor(NAVY); c.drawString(0.9*inch, 2.3*inch, "PSEUDOCODE: Risk Scoring")
    code2 = ["risk_score = w1*confidence + w2*ood + w3*drift + w4*historical_error",
             "review_queue = top_k(risk_score, k = budget * total_predictions)",
             "errors_found = count(review_queue where true != predicted)"]
    y = 1.9*inch
    c.setFont("Courier",13); c.setFillColor(DARK_GRAY)
    for line in code2: c.drawString(1.0*inch, y, line); y-=18
    c.setFont("Helvetica-Oblique",11); c.setFillColor(MUTED)
    c.drawString(1.0*inch, y-4, "Historical error uses training-time data; would benefit from out-of-fold. Fairness: planned for future dataset.")
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 16: IMPLEMENTED MODULES + SHIFT RESULTS
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Implemented Modules & Shift Results")
    draw_card(0.7*inch, 0.5*inch, 5.6*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(GREEN); c.drawString(0.9*inch, y, "IMPLEMENTED (Phase 1)"); y-=28
    impl = ["Data preprocessing & chronological split","XGBoost + RF + Logistic Regression",
            "Confidence signal extractor","OOD distance signal extractor",
            "Drift (PSI) signal extractor","Historical error proximity extractor",
            "Three review strategies (Conf/Multi/Adaptive)","Budget-based evaluation pipeline",
            "Strategy comparison & reporting"]
    c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY)
    for item in impl: c.drawString(1.0*inch, y, "[done] "+item); y-=22
    draw_card(6.5*inch, 0.5*inch, 6.1*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(NAVY); c.drawString(6.7*inch, y, "Validation vs. Shifted Test"); y-=36
    for lab, vv, vs, note in [("Attack rate:","0.33%","6.30%","(19x)"),("Error rate:","1.00%","4.57%","(4.6x)"),
                               ("Avg confidence:","98.65%","96.82%","(slight drop)"),("Total errors:","747","3,427","(4.6x)")]:
        c.setFont("Helvetica-Bold",16); c.setFillColor(DARK_GRAY); c.drawString(6.8*inch, y, lab); y-=22
        c.setFont("Helvetica-Bold",17); c.setFillColor(RED)
        c.drawString(6.8*inch, y, vv+"  -->  "+vs+"  "+note); y-=30
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 17: REVIEW STRATEGY RESULTS
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Review Strategy Results")
    res_rows = [("1%","1.17%","13.51%","0.03%","17.51%","17.80%"),
                ("2%","2.13%","26.73%","0.26%","33.99%","34.26%"),
                ("5%","5.52%","65.45%","0.35%","54.57%","45.90%"),
                ("10%","9.92%","84.01%","0.35%","65.42%","52.35%")]
    draw_table(0.7*inch, PH-1.1*inch, ["Budget","Random","Confidence","OOD-Only","Static Multi-F","Feedback Adpt"],
               res_rows, [1.2*inch, 1.3*inch, 1.8*inch, 1.5*inch, 2.5*inch, 2.5*inch], fs=14, rh=0.45*inch, hh=0.45*inch)
    draw_card(0.7*inch, 0.5*inch, 5.5*inch, 2.2*inch)
    c.setFont("Helvetica-Bold",18); c.setFillColor(NAVY); c.drawString(0.9*inch, 2.35*inch, "KEY OBSERVATIONS")
    obs = ["* Multi-factor captures more errors at 1-2%","* Confidence-only outperforms at 5-10%",
           "* OOD-only underperformed random at all budgets","* No strategy is universally superior"]
    y = 2.0*inch
    c.setFont("Helvetica",14); c.setFillColor(DARK_GRAY)
    for o in obs: c.drawString(1.0*inch, y, o); y-=22
    draw_img('diagram_results_chart.png', 6.4*inch, 0.3*inch, 6.2*inch)
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 18: LIMITATIONS + CONCLUSION
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("Limitations & Conclusion")
    draw_card(0.7*inch, 0.5*inch, 5.6*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(RED); c.drawString(0.9*inch, y, "LIMITATIONS"); y-=28
    lims = ["Uses 500K sample, not full 66.9M","Simulated review, not actual reviewers",
            "Strategy weights are heuristic, not learned","Binary classification only (single dataset)",
            "Temporal shift only, not cross-dataset","Historical error needs out-of-fold estimate",
            "No universal superiority established"]
    c.setFont("Helvetica",15); c.setFillColor(DARK_GRAY)
    for lim in lims: c.drawString(1.0*inch, y, "* "+lim); y-=22
    draw_card(6.5*inch, 0.5*inch, 6.1*inch, 5.6*inch)
    y = PH-1.3*inch
    c.setFont("Helvetica-Bold",21); c.setFillColor(GREEN); c.drawString(6.7*inch, y, "CONCLUSION"); y-=32
    concs = [("Built:","Working prototype with 4 reliability signals"),
             ("Evaluated:","3 strategies at 4 budgets on shifted test"),
             ("Observed:","Multi-factor better at tight budgets (1-2%)"),
             ("Found:","Effectiveness depends on budget & signals"),
             ("Next:","Phase 2: diverse datasets + explainability")]
    for lab, desc in concs:
        c.setFont("Helvetica-Bold",16); c.setFillColor(ACCENT); c.drawString(6.8*inch, y, lab)
        lw = c.stringWidth(lab, "Helvetica-Bold", 16)
        c.setFont("Helvetica",16); c.setFillColor(DARK_GRAY); c.drawString(6.8*inch+lw+4, y, desc); y-=28
    c.showPage()

    # ═══════════════════════════════════════════════════════════
    # SLIDE 19: REFERENCES
    # ═══════════════════════════════════════════════════════════
    slide_bg(); add_logo(); heading("References")
    draw_card(0.7*inch, 0.4*inch, 11.9*inch, 5.8*inch)
    refs = [
        '[1] "BigFlow-NIDS," Mendeley Data / Data in Brief, Elsevier, 2026.',
        '[2] H. Mozannar and D. Sontag, "Consistent Estimators for Learning to Defer," ICML, PMLR 119, 2020.',
        '[3] D. Wei et al., "Deep Learning to Defer with Multiple Experts," ICML, PMLR 235, 2024.',
        '[4] Y. Geifman and R. El-Yaniv, "Selective Classification for DNNs," NeurIPS, 2017.',
        '[5] C. Guo et al., "On Calibration of Modern Neural Networks," ICML, PMLR 70, 2017.',
        '[6] A. Angelopoulos and S. Bates, "Conformal Prediction & Distribution-Free UQ," arXiv, 2021.',
        '[7] J. Yang et al., "Generalized OOD Detection: A Survey," IEEE TPAMI, 2024.',
        '[8] K. Lee et al., "Simple Unified Framework for OOD Detection," NeurIPS, 2018.',
        '[9] P. W. Koh et al., "WILDS: In-the-Wild Distribution Shifts," ICML, PMLR 139, 2021.',
        '[10] M. Charusaie et al., "Sample Efficient Learning to Defer," NeurIPS, 2022.',
        '[11] T. Chen and C. Guestrin, "XGBoost," KDD, 2016.',
        '[12] F. Pedregosa et al., "Scikit-learn," JMLR, vol. 12, 2011.',
    ]
    y = PH-1.3*inch
    c.setFont("Helvetica",12); c.setFillColor(DARK_GRAY)
    for ref in refs: c.drawString(0.9*inch, y, ref); y-=20
    c.showPage()

    c.save()
    print(f"\n[OK] Saved 19-page PDF to:\n   {target}")
    print(f"   File size: {os.path.getsize(target):,} bytes")

if __name__ == "__main__":
    build_pdf()
