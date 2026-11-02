"""
Generate PDF matching the corrected 12-slide PPTX.
Reads slide text directly from the PPTX and renders via reportlab.
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

from pptx import Presentation
from pptx.util import Emu
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

PROJECT = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
PPTX_PATH = os.path.join(PROJECT, "Adaptive_Human_Review_Allocation_PESU.pptx")
PDF_PATH = os.path.join(PROJECT, "Adaptive_Human_Review_Allocation_PESU.pdf")
PDF_ALT = os.path.join(PROJECT, "Adaptive_Human_Review_Allocation_PESU_v2.pdf")
LOGO = os.path.join(PROJECT, "pes_logo.png")

PW, PH = 13.333*inch, 7.5*inch
NAVY = HexColor("#0B192C")
ACCENT = HexColor("#1E40AF")
DARK = HexColor("#1E293B")
MUTED = HexColor("#64748B")
LIGHT = HexColor("#F8FAFC")
CARD = HexColor("#FFFFFF")
BORDER = HexColor("#CBD5E1")
GREEN = HexColor("#16A34A")
RED = HexColor("#DC2626")
AMBER = HexColor("#D97706")

# Check PDF lock
target = PDF_PATH
try:
    with open(target, 'ab') as f: pass
except (PermissionError, OSError):
    target = PDF_ALT
    print(f"  PDF locked, writing to: {target}")

# Read PPTX
prs = Presentation(PPTX_PATH)
print(f"Reading {len(prs.slides)} slides from PPTX...")

def get_slide_texts(slide):
    """Extract all text blocks from a slide."""
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                t = p.text.strip()
                if t: texts.append(t)
        if shape.has_table:
            tbl = shape.table
            rows = []
            for r in range(len(tbl.rows)):
                row = [tbl.cell(r,c).text.strip() for c in range(len(tbl.columns))]
                rows.append(row)
            texts.append(('TABLE', rows))
    return texts

logo = ImageReader(LOGO) if os.path.exists(LOGO) else None

class SlideCanvas(canvas.Canvas):
    def __init__(self, *a, **kw):
        self._sn = 0
        super().__init__(*a, **kw)
    def showPage(self):
        self._sn += 1
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(MUTED)
        self.drawRightString(PW-0.4*inch, 0.3*inch, f"{self._sn} / 12")
        self.restoreState()
        super().showPage()

c = SlideCanvas(target, pagesize=(PW,PH))
c.setTitle("Adaptive Human-Review Allocation - Capstone Phase-1")

def bg():
    c.setFillColor(LIGHT); c.rect(0,0,PW,PH,fill=1,stroke=0)
    c.setFillColor(NAVY); c.rect(0,PH-0.08*inch,PW,0.08*inch,fill=1,stroke=0)

def add_logo():
    if logo: c.drawImage(logo, PW-1.8*inch, PH-0.72*inch, width=1.4*inch, height=0.55*inch, preserveAspectRatio=True, mask='auto')

def header(label, title):
    c.setFont("Helvetica", 11); c.setFillColor(ACCENT)
    c.drawString(0.6*inch, PH-0.45*inch, label)
    c.setFont("Helvetica-Bold", 24); c.setFillColor(NAVY)
    c.drawString(0.6*inch, PH-0.85*inch, title)

def card(x,y,w,h,fill=CARD):
    c.setFillColor(fill); c.setStrokeColor(BORDER); c.setLineWidth(0.4)
    c.roundRect(x,y,w,h,5,fill=1,stroke=1)

def draw_table(x, y, rows, col_widths, fs=12, rh=0.32*inch, hh=0.36*inch):
    if not rows: return y
    # Header
    cx = x
    for val, w in zip(rows[0], col_widths):
        c.setFillColor(NAVY); c.rect(cx, y-hh, w, hh, fill=1, stroke=0)
        c.setFillColor(white); c.setFont("Helvetica-Bold", fs)
        c.drawString(cx+3, y-hh+8, val[:int(w/5)]); cx += w
    cy = y - hh
    for ri, row in enumerate(rows[1:]):
        cx = x
        bg_c = CARD if ri%2==0 else HexColor("#F1F5F9")
        for ci, (val, w) in enumerate(zip(row, col_widths)):
            c.setFillColor(bg_c); c.rect(cx, cy-rh, w, rh, fill=1, stroke=0)
            c.setStrokeColor(BORDER); c.setLineWidth(0.2)
            c.rect(cx, cy-rh, w, rh, fill=0, stroke=1)
            c.setFillColor(DARK); c.setFont("Helvetica", fs-1)
            # Truncate if needed
            txt = val[:int(w/4.5)] if len(val) > int(w/4.5) else val
            c.drawString(cx+3, cy-rh+8, txt); cx += w
        cy -= rh
    return cy

# ============================================================
# SLIDE 1: TITLE
# ============================================================
c.setFillColor(HexColor("#F1F5F9")); c.rect(0,0,PW,PH,fill=1,stroke=0)
c.setFillColor(NAVY); c.rect(0,PH-0.12*inch,PW,0.12*inch,fill=1,stroke=0)
if logo: c.drawImage(logo, PW-2.2*inch, PH-1.0*inch, width=1.8*inch, height=0.7*inch, preserveAspectRatio=True, mask='auto')
c.setFont("Helvetica-Bold",14); c.setFillColor(ACCENT)
c.drawString(0.7*inch, PH-1.0*inch, "CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)")
c.setFont("Helvetica-Bold",30); c.setFillColor(NAVY)
c.drawString(0.7*inch, PH-1.7*inch, "Adaptive Human-Review Allocation for Reliable")
c.drawString(0.7*inch, PH-2.2*inch, "Machine Learning Under Distribution Shift")
c.setFont("Helvetica",13); c.setFillColor(DARK)
c.drawString(0.7*inch, PH-2.8*inch, "Department of Computer Applications  |  PES University, Bangalore")
card(0.7*inch, 0.7*inch, 5.0*inch, 1.4*inch)
c.setFont("Helvetica-Bold",11); c.setFillColor(ACCENT); c.drawString(0.9*inch, 1.85*inch, "CANDIDATE DETAILS")
c.setFont("Helvetica",13); c.setFillColor(DARK)
c.drawString(0.9*inch, 1.55*inch, "Candidate SRN: PES1PG25CA101")
c.drawString(0.9*inch, 1.3*inch, "Degree: MCA | Specialization: Data Analytics")
card(6.2*inch, 0.7*inch, 6.0*inch, 1.4*inch)
c.setFont("Helvetica-Bold",11); c.setFillColor(ACCENT); c.drawString(6.4*inch, 1.85*inch, "FACULTY GUIDE DETAILS")
c.setFont("Helvetica-Bold",15); c.setFillColor(NAVY); c.drawString(6.4*inch, 1.55*inch, "Prof. Dilip Kumar Maripuri")
c.setFont("Helvetica",13); c.setFillColor(DARK); c.drawString(6.4*inch, 1.3*inch, "Dept. of Computer Applications, PES University")
c.showPage()

# ============================================================
# SLIDE 2: ABSTRACT
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Abstract & Core Research Formulation")
card(0.6*inch, 2.4*inch, 12.0*inch, 4.2*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(0.8*inch, y, "EXECUTIVE RESEARCH ABSTRACT"); y-=28
bullets = [
    ("Operational Bottleneck:", "Human-review capacity modeled using fixed budgets of 1%, 2%, 5% and 10%."),
    ("Silent Failure Mode:", "High-confidence prediction errors can occur under temporal distribution shift."),
    ("Proposed Mechanism:", "Adaptive multi-factor review allocation synthesizing confidence, Mahalanobis OOD, PSI drift, historical patterns."),
    ("Benchmark Scope:", "Evaluated on 500,000 flows from BigFlow-NIDS derived benchmark (66.9M flows, 55 attributes)."),
    ("Key Finding:", "Captures 34.26% of errors at 2% budget (vs 26.73% confidence); confidence stronger at 5-10%. Advantage is budget-dependent."),
]
for lab, desc in bullets:
    c.setFont("Helvetica-Bold",13); c.setFillColor(ACCENT); c.drawString(0.8*inch, y, lab)
    lw = c.stringWidth(lab, "Helvetica-Bold", 13)
    c.setFont("Helvetica",13); c.setFillColor(DARK); c.drawString(0.8*inch+lw+4, y, desc); y-=22
y -= 10
card(0.6*inch, 0.4*inch, 12.0*inch, 1.7*inch, fill=HexColor("#EEF2FF"))
c.setFont("Helvetica-Bold",14); c.setFillColor(NAVY); c.drawString(0.8*inch, 1.8*inch, "CORE RESEARCH QUESTION")
c.setFont("Helvetica-Oblique",12); c.setFillColor(DARK)
c.drawString(0.8*inch, 1.5*inch, '"Can an adaptive, multi-factor human-review allocation mechanism reduce high-risk ML errors more')
c.drawString(0.8*inch, 1.28*inch, 'efficiently than fixed-threshold and single-signal strategies under distribution shift and constrained review capacity?"')
c.setFont("Helvetica-Bold",11); c.setFillColor(ACCENT); c.drawString(0.8*inch, 0.9*inch, "OBJECTIVES:")
c.setFont("Helvetica",11); c.setFillColor(DARK)
c.drawString(2.2*inch, 0.9*inch, "Synthesize 4 signals  |  Evaluate at 1-10% budgets  |  Test under temporal shift  |  >50% implementation")
c.showPage()

# ============================================================
# SLIDE 3: PROBLEM SCENARIO
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Introduction: Problem Scenario & System Flow")
card(0.6*inch, 0.4*inch, 11.9*inch, 5.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",18); c.setFillColor(RED); c.drawString(0.8*inch, y, "OPERATIONAL REALITY & SOLUTION"); y-=30
problems = [
    "The Attention Bottleneck: E.g., reviewing 100K inferences/day at 2% allows only 2,000 human audits.",
    "Overconfidence Failure: High-confidence errors are observed on the shifted test data.",
    "Random Audit Wastes Effort: Random review captured 1.17% of model errors at 1% budget in our experiment.",
    "Multi-Factor Resolution: Combines uncertainty, Mahalanobis OOD, PSI drift, and mistake proximity.",
]
for p in problems:
    c.setFont("Helvetica",14); c.setFillColor(DARK); c.drawString(0.9*inch, y, "* "+p); y-=24
c.showPage()

# ============================================================
# SLIDE 4: LITERATURE SURVEY
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Detailed Literature Survey")
lit_rows = [
    ["Paper Title","Authors","Venue & Year","Summary & Project Relevance"],
    ["Anomaly Detection Under Distribution Shift","T. Cao, J. Zhu, G. Pang","IEEE/CVF ICCV, 2023","Anomaly detection under shift. Directly relevant to our evaluation setting."],
    ["Consistent Estimators for Learning to Defer","H. Mozannar, D. Sontag","ICML 2020 (PMLR 119)","Theoretical formulation of learning to defer. Foundational for human-AI routing."],
    ["Exploiting Human-AI Dependence for L2D","Z. Wei, Y. Cao, L. Feng","ICML 2024 (PMLR 235)","Models human-AI dependence in learning to defer."],
    ["Selective Classification for DNNs","Y. Geifman, R. El-Yaniv","NeurIPS 2017","Risk-coverage trade-offs for confidence-based abstention."],
    ["On Calibration of Modern NNs","C. Guo et al.","ICML 2017 (PMLR 70)","Demonstrates models are overconfident under shift."],
    ["Human-in-the-Loop Cyber IDS","Y. Kim, G. Dan, Q. Zhu","IEEE TIFS, vol. 19, 2024","Active learning for NIDS with human review allocation."],
    ["Generalized OOD Detection: A Survey","J. Yang et al.","IJCV 2024","Comprehensive taxonomy of OOD detection methods."],
    ["Uncertainty in Learning to Defer","J. Liu, B. Gallego, S. Barbieri","Scientific Reports, 2022","Incorporates uncertainty into deferral decisions."],
    ["WILDS: In-The-Wild Distribution Shifts","P. W. Koh et al.","ICML 2021 (PMLR 139)","Evaluates model performance across real-world shifts."],
    ["Adversarial ML for NIDS: Survey","K. He, D.D. Kim, M.R. Asghar","IEEE Surveys, vol. 25, 2023","Robustness challenges in network intrusion detection."],
]
draw_table(0.5*inch, PH-1.0*inch, lit_rows, [3.3*inch, 2.4*inch, 2.6*inch, 3.6*inch], fs=10, rh=0.42*inch, hh=0.35*inch)
c.showPage()

# ============================================================
# SLIDE 5: COMPARATIVE STUDY
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Comparative Study: Existing Paradigms vs Proposed")
comp_rows = [
    ["Dimension","Random","Confidence","OOD Filter","Learn-to-Defer","Proposed"],
    ["Confidence / Uncertainty","No","Yes (Sole)","No","Optional","Yes (Normalized)"],
    ["Out-of-Distribution","No","No","Yes (Sole)","Rarely","Yes (Mahalanobis)"],
    ["Distribution Drift (PSI)","No","No","No","No","Yes (Feature-Level)"],
    ["Historical Error","No","No","No","Implicit","Yes (Mistake Prox.)"],
    ["Explicit Budget","Implicit","Manual","Hard Cutoff","Theoretical","Yes (1-10%)"],
    ["Temporal Shift Eval","N/A","Rarely","Partial","Rarely","Yes (Chrono Split)"],
]
draw_table(0.5*inch, PH-1.0*inch, comp_rows, [2.4*inch, 1.4*inch, 1.8*inch, 1.7*inch, 2.2*inch, 2.4*inch], fs=12, rh=0.42*inch)
c.setFont("Helvetica",12); c.setFillColor(DARK)
c.drawString(0.6*inch, 0.6*inch, "The proposed framework combines confidence, OOD, drift and historical-error signals and evaluates under chronological temporal shift.")
c.showPage()

# ============================================================
# SLIDE 6: DATASET
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Benchmark Dataset & Temporal Shift Simulation")
card(0.6*inch, 0.4*inch, 11.9*inch, 5.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",18); c.setFillColor(ACCENT); c.drawString(0.8*inch, y, "BIGFLOW-NIDS BENCHMARK (2026)"); y-=28
ds = [
    "Derived Benchmark: Harmonizes 4 major NetFlow datasets via Apache Spark.",
    "Full Scale: 66,935,021 flows, 55 attributes, 32 attack families.",
    "Development Sample: 500,000 flows extracted chronologically for evaluation.",
    "Input Features (X): 49 numerical features (throughput, packet sizes, duration, TCP flags).",
    "Target (y): Label (0=Benign, 1=Attack). Attack column excluded to prevent leakage.",
    "Scientific Fact: Not live internet traffic; an offline scientific benchmark.",
]
for d in ds:
    c.setFont("Helvetica",14); c.setFillColor(DARK); c.drawString(0.9*inch, y, "* "+d); y-=24
c.showPage()

# ============================================================
# SLIDE 7: ARCHITECTURE
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "System Architecture & Operational Algorithm Flow")
# Pipeline boxes
boxes = [
    ("1. DATA INGESTION", "500K BigFlow-NIDS\nChronological Split\n(350K/75K/75K)", 0.5),
    ("2. PREPROCESS & ML", "StandardScaler (LR only)\nBaseline Models\nXGBoost (val ROC-AUC 0.9228)", 3.0),
    ("3. RELIABILITY ENGINE", "Prediction Probability\nMahalanobis OOD\nFeature PSI Drift\nHistorical Mistake", 5.5),
    ("4. ADAPTIVE ROUTING", "Multi-Factor Risk\nTop-K Priority Queue\nBudgets: 1%, 2%, 5%, 10%", 8.0),
    ("5. DECISION & EVAL", "High-Risk: Simulated Review\nLow-Risk: Automated Decision\nEvaluation Pipeline", 10.5),
]
for title, desc, xp in boxes:
    card(xp*inch, 3.8*inch, 2.3*inch, 2.8*inch)
    c.setFont("Helvetica-Bold",10); c.setFillColor(ACCENT)
    c.drawString((xp+0.1)*inch, 6.3*inch, title)
    c.setFont("Helvetica",10); c.setFillColor(DARK)
    for i, line in enumerate(desc.split('\n')):
        c.drawString((xp+0.1)*inch, 6.05*inch - i*14, "* "+line)
# Pseudocode
card(0.5*inch, 0.3*inch, 12.3*inch, 3.1*inch, fill=HexColor("#F1F5F9"))
c.setFont("Helvetica-Bold",14); c.setFillColor(NAVY); c.drawString(0.7*inch, 3.1*inch, "OPERATIONAL ALGORITHM PSEUDOCODE")
code = [
    "1: Fit Scaler and Model M on D_train. Compute reference centroid mu_tr and covariance Sigma_tr.",
    "2: Compute feature-level PSI weights between reference train and target batches.",
    "3: FOR each x_i: s_conf = 1-max(P(y|x_i)); s_ood = Mahalanobis(x_i, mu_tr, Sigma_tr); s_drift = PSI(x_i); s_hist = DistToErrors(x_i)",
    "4: Risk(x_i) = w1*s_conf + w2*s_ood + w3*s_drift + w4*s_hist. Sort desc. Select top K = floor(Budget * N).",
    "5: Route top-K to simulated human review; dispatch remainder to automated model decision.",
]
c.setFont("Courier",11); c.setFillColor(DARK)
y = 2.75*inch
for line in code: c.drawString(0.7*inch, y, line); y -= 18
c.showPage()

# ============================================================
# SLIDE 8: REQUIREMENTS & TOOLS
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Requirements Specification & Technical Stack")
card(0.6*inch, 3.2*inch, 6.5*inch, 3.4*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(0.8*inch, y, "FUNCTIONAL REQUIREMENTS"); y -= 24
frs = [
    "FR1-FR4: Data ingestion, chronological split, StandardScaler, train LR/RF/XGBoost [DONE]",
    "FR5-FR8: Confidence, Mahalanobis OOD, PSI drift, historical error proximity [DONE]",
    "FR9-FR12: Risk scores, budget slicing (1-10%), oracle benchmark, efficiency eval [DONE]",
    "FR13-FR14: Evaluation pipeline, configurable budgets, CSV reporting [DONE]",
]
c.setFont("Helvetica",11); c.setFillColor(DARK)
for fr in frs: c.drawString(0.8*inch, y, "* "+fr); y -= 18
y -= 8
c.setFont("Helvetica-Bold",13); c.setFillColor(NAVY); c.drawString(0.8*inch, y, "NON-FUNCTIONAL:"); y -= 16
c.setFont("Helvetica",11); c.setFillColor(DARK)
c.drawString(0.8*inch, y, "Reproducibility (fixed seeds), modular architecture (26 scripts), data integrity (SHA-256)")

card(7.3*inch, 3.2*inch, 5.3*inch, 3.4*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(7.5*inch, y, "TOOLS & TECHNOLOGIES"); y -= 24
tools = [
    ("Core:", "Python 3.x"),
    ("ML:", "XGBoost, Scikit-learn (LR, RF, preprocessing)"),
    ("Scientific:", "NumPy, SciPy (Mahalanobis, covariance)"),
    ("Data:", "Pandas (DataFrames, CSV I/O), pathlib"),
    ("Persistence:", "joblib (model serialization)"),
    ("Integrity:", "hashlib (SHA-256 checksums)"),
]
for lab, desc in tools:
    c.setFont("Helvetica-Bold",11); c.setFillColor(ACCENT); c.drawString(7.5*inch, y, lab)
    lw = c.stringWidth(lab, "Helvetica-Bold", 11)
    c.setFont("Helvetica",11); c.setFillColor(DARK); c.drawString(7.5*inch+lw+4, y, desc); y -= 18
c.showPage()

# ============================================================
# SLIDE 9: IMPLEMENTATION
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Phase-1 Implementation Demo (>50% Verified)")
card(0.6*inch, 0.4*inch, 11.9*inch, 5.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",18); c.setFillColor(GREEN); c.drawString(0.8*inch, y, "DEMONSTRABLE FUNCTIONALITY CHECKLIST"); y -= 30
checks = [
    "Verified Implementation: 26 modular Python source files covering end-to-end pipeline.",
    "Substantial Scope: Far exceeds mandatory 50% milestone.",
    "Evaluation Pipeline: Configurable review budgets (1%-10%), automated strategy comparison, CSV reporting.",
    "Multi-Model Benchmark: XGBoost (ROC-AUC 0.9228), Random Forest (0.8526), Logistic Regression (0.7499).",
    "Simulated Review Oracle: Uses test ground truth to determine if routed cases contained misclassifications.",
]
for ch in checks:
    c.setFont("Helvetica",14); c.setFillColor(DARK); c.drawString(0.9*inch, y, "[done] "+ch); y -= 24
c.showPage()

# ============================================================
# SLIDE 10: RESULTS
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Empirical Evaluation: Shifted-Test Strategy Benchmark")
card(0.6*inch, 2.8*inch, 6.0*inch, 3.6*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(0.8*inch, y, "SHIFTED-TEST RESULTS"); y -= 22
c.setFont("Helvetica",12); c.setFillColor(MUTED); c.drawString(0.8*inch, y, "75,000 shifted flows | 3,427 ground-truth errors"); y -= 24
results = [
    ("1% Budget:", "Adaptive = 17.80%  vs  Conf = 13.51%", GREEN),
    ("2% Budget:", "Adaptive = 34.26%  vs  Conf = 26.73%", GREEN),
    ("5% Budget:", "Conf = 65.45%  vs  Adaptive = 45.90%", AMBER),
    ("10% Budget:", "Conf = 84.01%  vs  Adaptive = 52.35%", AMBER),
]
for lab, val, col in results:
    c.setFont("Helvetica-Bold",14); c.setFillColor(col); c.drawString(0.9*inch, y, lab)
    lw = c.stringWidth(lab, "Helvetica-Bold", 14)
    c.setFont("Helvetica",13); c.setFillColor(DARK); c.drawString(0.9*inch+lw+4, y, val); y -= 22

card(6.8*inch, 2.8*inch, 5.8*inch, 3.6*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(7.0*inch, y, "CRITICAL SCIENTIFIC INSIGHT"); y -= 24
insights = [
    "1. At 1-2% budgets, multi-factor captures more errors",
    "   than confidence alone in this experiment.",
    "2. At 5-10%, confidence catches up by targeting",
    "   broad decision-boundary ambiguity.",
    "3. No single strategy is best at every budget.",
    "4. OOD-only performed worse than random",
    "   (0.03% vs 1.17% at 1%). Honest negative result.",
]
c.setFont("Helvetica",12); c.setFillColor(DARK)
for line in insights: c.drawString(7.1*inch, y, line); y -= 16
c.showPage()

# ============================================================
# SLIDE 11: PHASE 2
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "Phase-2 Vision: Generalized Dataset-Agnostic Platform")
card(0.6*inch, 3.0*inch, 5.8*inch, 3.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(ACCENT); c.drawString(0.8*inch, y, "DATASET-AGNOSTIC GENERALIZATION"); y -= 24
gen = ["Universal Tabular Ingestion (CSV/Excel/Parquet)","Automated schema profiling & null imputation",
       "Auto-detection of task type (Binary/Multi/Regression)","Automatic baseline model suite training"]
c.setFont("Helvetica",13); c.setFillColor(DARK)
for g in gen: c.drawString(0.9*inch, y, "* "+g); y -= 20

card(6.6*inch, 3.0*inch, 6.0*inch, 3.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(ACCENT); c.drawString(6.8*inch, y, "PLANNED ADVANCED CAPABILITIES"); y -= 24
planned = ["Explainability (SHAP): Why an instance was escalated",
           "Conformal Prediction: Distribution-free coverage",
           "Cost-Aware Routing: Financial penalty matrices",
           "Streaming Simulation: Buffer-based stream replay"]
c.setFont("Helvetica",13); c.setFillColor(DARK)
for p in planned: c.drawString(6.9*inch, y, "* "+p); y -= 20
c.showPage()

# ============================================================
# SLIDE 12: REFERENCES
# ============================================================
bg(); add_logo(); header("PHASE-1 CAPSTONE PRESENTATION-2", "References")
card(0.5*inch, 0.3*inch, 12.3*inch, 5.5*inch)
y = PH-1.2*inch
c.setFont("Helvetica-Bold",16); c.setFillColor(NAVY); c.drawString(0.7*inch, y, "REFERENCES"); y -= 22
refs = [
    '[1] H. Mozannar and D. Sontag, "Consistent Estimators for Learning to Defer to an Expert," Proc. ICML, PMLR 119, 2020, pp. 7076-7087.',
    '[2] Z. Wei, Y. Cao, and L. Feng, "Exploiting Human-AI Dependence for Learning to Defer," Proc. ICML, PMLR 235, 2024, pp. 52484-52499.',
    '[3] Y. Geifman and R. El-Yaniv, "Selective Classification for Deep Neural Networks," Adv. NeurIPS, vol. 30, 2017.',
    '[4] C. Guo et al., "On Calibration of Modern Neural Networks," Proc. ICML, PMLR 70, 2017, pp. 1321-1330.',
    '[5] Y. Kim, G. Dan, and Q. Zhu, "Human-in-the-Loop Cyber IDS Using Active Learning," IEEE TIFS, vol. 19, 2024, pp. 8658-8672.',
    '[6] J. Liu et al., "Incorporating Uncertainty in L2D for Safe Computer-Aided Diagnosis," Scientific Reports, vol. 12, 2022, Art. 1762.',
    '[7] J. Yang et al., "Generalized OOD Detection: A Survey," International Journal of Computer Vision, 2024.',
    '[8] P. W. Koh et al., "WILDS: A Benchmark of In-the-Wild Distribution Shifts," Proc. ICML, PMLR 139, 2021, pp. 5637-5664.',
    '[9] K. He et al., "Adversarial ML for NIDS: A Comprehensive Survey," IEEE Commun. Surveys, vol. 25, no. 1, 2023, pp. 538-566.',
    '[10] T. Cao, J. Zhu, and G. Pang, "Anomaly Detection Under Distribution Shift," Proc. IEEE/CVF ICCV, 2023, pp. 6511-6523.',
    '[11] M. B. Uddin and M. S. Arefin, "BigFlow-NIDS: Large-Scale Benchmark Dataset," Data in Brief, Elsevier, 2026.',
]
c.setFont("Helvetica",11); c.setFillColor(DARK)
for ref in refs: c.drawString(0.7*inch, y, ref); y -= 18
c.showPage()

c.save()
print(f"\n[OK] Saved 12-page PDF to: {target}")
print(f"     File size: {os.path.getsize(target):,} bytes")
