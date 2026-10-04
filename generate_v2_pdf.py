"""
Generate High-Legibility, Zero-Truncation 24-Page PDF matching Adaptive_Human_Review_Allocation_PESU_FINAL.pptx
Uses ReportLab Platypus Paragraphs to wrap every piece of text naturally with zero clipping.
"""

import os, sys
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PDF_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU_FINAL.pdf")
PDF_ALT = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU_v2_alt.pdf")

PW, PH = 13.333 * inch, 7.5 * inch

NAVY      = HexColor("#0B192C")
ACCENT    = HexColor("#1E40AF")
DARK      = HexColor("#1E293B")
LIGHT_BG  = HexColor("#F8FAFC")
CARD_BG   = HexColor("#FFFFFF")
BORDER    = HexColor("#CBD5E1")
GREEN     = HexColor("#16A34A")
RED       = HexColor("#DC2626")
AMBER     = HexColor("#D97706")
MUTED     = HexColor("#64748B")
CARD_ALT  = HexColor("#F1F5F9")
PURPLE    = HexColor("#7C3AED")

styles = getSampleStyleSheet()

s_title = ParagraphStyle('STitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=NAVY)
s_cat   = ParagraphStyle('SCat',   parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=ACCENT)
s_body  = ParagraphStyle('SBody',  parent=styles['Normal'], fontName='Helvetica', fontSize=11.5, leading=16, textColor=DARK)
s_body_b= ParagraphStyle('SBodyB', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=NAVY)
s_card_h= ParagraphStyle('SCardH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=NAVY)
s_sm    = ParagraphStyle('SSm',    parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=DARK)
s_mono  = ParagraphStyle('SMono',  parent=styles['Normal'], fontName='Courier', fontSize=9.5, leading=13, textColor=DARK)

class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self._sn = 0
        self._total = 25
        super().__init__(*args, **kwargs)
    def showPage(self):
        self._sn += 1
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(MUTED)
        self.drawRightString(PW - 0.5 * inch, 0.3 * inch, f"{self._sn} / {self._total}")
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
    c.setTitle("Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift - Capstone Phase-1 (v2)")
    logo = ImageReader(LOGO_PATH) if os.path.exists(LOGO_PATH) else None

    def slide_bg():
        c.setFillColor(LIGHT_BG); c.rect(0, 0, PW, PH, fill=1, stroke=0)
        c.setFillColor(NAVY); c.rect(0, PH - 0.08 * inch, PW, 0.08 * inch, fill=1, stroke=0)

    def add_logo():
        if logo: c.drawImage(logo, PW - 1.8 * inch, PH - 0.75 * inch, width=1.4 * inch, height=0.55 * inch, preserveAspectRatio=True, mask='auto')

    def header(category, title):
        p_c = Paragraph(category.upper(), s_cat)
        p_c.wrapOn(c, 10 * inch, 0.3 * inch)
        p_c.drawOn(c, 0.6 * inch, PH - 0.45 * inch)
        
        p_t = Paragraph(title, s_title)
        p_t.wrapOn(c, 10.5 * inch, 0.5 * inch)
        p_t.drawOn(c, 0.6 * inch, PH - 0.85 * inch)

    def draw_card(x, y, w, h, fill=CARD_BG, stroke=BORDER):
        c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(0.6)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=1)

    def draw_img(name, x, y, w, h):
        p = os.path.join(DIAGRAMS_DIR, name)
        if os.path.exists(p):
            c.drawImage(p, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')

    def draw_para(html_text, x, y, max_w, style=s_body):
        p = Paragraph(html_text, style)
        pw, ph = p.wrapOn(c, max_w, PH)
        p.drawOn(c, x, y - ph)
        return ph

    # -------------------------------------------------------------
    # SLIDE 1: Title & Details
    # -------------------------------------------------------------
    c.setFillColor(CARD_ALT); c.rect(0, 0, PW, PH, fill=1, stroke=0)
    c.setFillColor(NAVY); c.rect(0, PH - 0.12 * inch, PW, 0.12 * inch, fill=1, stroke=0)
    if logo: c.drawImage(logo, PW - 2.5 * inch, PH - 1.3 * inch, width=2.0 * inch, height=0.8 * inch, preserveAspectRatio=True, mask='auto')
    
    draw_para("<b>CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)</b>", 0.8 * inch, PH - 0.9 * inch, 10 * inch, 
              ParagraphStyle('P1', parent=s_cat, fontSize=13, leading=17, textColor=ACCENT))
    draw_para("<b>Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift for Reliable<br/>Machine Learning Under Distribution Shift</b>", 
              0.8 * inch, PH - 1.4 * inch, 11 * inch,
              ParagraphStyle('P2', parent=s_title, fontSize=28, leading=34, textColor=NAVY))
    draw_para("Course: PES2UG20CS418  |  Department of Computer Applications  |  PES University, Bangalore", 
              0.8 * inch, PH - 2.6 * inch, 11 * inch,
              ParagraphStyle('P3', parent=s_body, fontSize=13, leading=17, textColor=DARK))
    
    draw_card(0.8 * inch, 0.8 * inch, 5.6 * inch, 2.0 * inch)
    draw_para("<font color='#1E40AF'><b>CANDIDATE DETAILS</b></font><br/><br/>"
              "<b>Candidate SRN:</b> PES1PG25CA101<br/>"
              "<b>Degree:</b> Master of Computer Applications (MCA)<br/>"
              "<b>Specialization:</b> Data Analytics", 
              1.0 * inch, 2.6 * inch, 5.2 * inch,
              ParagraphStyle('C1', parent=s_body, fontSize=13, leading=20))
    
    draw_card(6.8 * inch, 0.8 * inch, 5.7 * inch, 2.0 * inch)
    draw_para("<font color='#1E40AF'><b>FACULTY GUIDE DETAILS</b></font><br/><br/>"
              "<b>Project Guide:</b> Prof. Dilip Kumar Maripuri<br/>"
              "Department of Computer Applications<br/>"
              "PES University, Bangalore", 
              7.0 * inch, 2.6 * inch, 5.3 * inch,
              ParagraphStyle('C2', parent=s_body, fontSize=13, leading=20))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 2: Abstract & Core Research Question
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Phase-1 Capstone Presentation-2", "Abstract & Core Research Formulation")
    draw_card(0.6 * inch, 2.3 * inch, 12.1 * inch, 4.0 * inch)
    draw_para("<b>EXECUTIVE RESEARCH ABSTRACT</b>", 0.8 * inch, PH - 1.35 * inch, 11.7 * inch, s_card_h)
    
    abs_html = (
        "• <b><font color='#1E40AF'>Operational Bottleneck:</font></b> Human-review capacity is strictly constrained in production systems (modeled at 1%, 2%, 5%, and 10% budgets).<br/><br/>"
        "• <b><font color='#1E40AF'>Silent Failure Mode:</font></b> ML models can remain highly confident while making errors under distribution shift [4], [5].<br/><br/>"
        "• <b><font color='#1E40AF'>Proposed Mechanism:</font></b> An adaptive multi-factor allocation framework combining prediction confidence, Mahalanobis OOD distance, PSI feature drift, and historical mistake patterns.<br/><br/>"
        "• <b><font color='#1E40AF'>Experimental Scope:</font></b> Evaluated on a 500,000-flow chronological sample from the BigFlow-NIDS benchmark [16] (66.9M flows, 55 attributes).<br/><br/>"
        "• <b><font color='#1E40AF'>Empirical Observation:</font></b> Multi-factor allocation captures up to 34.26% of errors at 2% budget (vs 26.73% for confidence); confidence alone captures more at 5–10% budgets. The advantage is budget-dependent."
    )
    draw_para(abs_html, 0.8 * inch, PH - 1.75 * inch, 11.7 * inch, ParagraphStyle('Abs', parent=s_body, fontSize=12, leading=17))
    
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 1.75 * inch, fill=CARD_ALT)
    draw_para("<b>CORE RESEARCH QUESTION</b>", 0.8 * inch, 1.95 * inch, 11.7 * inch, 
              ParagraphStyle('RQH', parent=s_body_b, fontSize=12.5, textColor=NAVY))
    draw_para("<i>\"Can an adaptive, multi-factor human-review allocation mechanism reduce high-risk ML errors more efficiently than fixed-threshold and single-signal strategies under distribution shift and constrained human-review capacity?\"</i>", 
              0.8 * inch, 1.65 * inch, 11.7 * inch, 
              ParagraphStyle('RQT', parent=s_body, fontSize=12.5, leading=17, textColor=ACCENT))
    draw_para("<b>Key Objectives:</b> (1) Synthesize 4 complementary reliability signals. (2) Benchmark under 1%–10% budgets. (3) Evaluate under temporal shift. (4) Deliver functional research software.", 
              0.8 * inch, 0.95 * inch, 11.7 * inch, 
              ParagraphStyle('RQO', parent=s_sm, fontSize=11, textColor=MUTED))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 3: Problem Scenario & Proposed Solution
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Introduction & Problem Formulation", "Problem Scenario & Proposed Solution")
    draw_card(0.6 * inch, 0.4 * inch, 5.8 * inch, 5.8 * inch)
    draw_para("<font color='#DC2626'><b>PROBLEM SCENARIO</b></font>", 0.8 * inch, PH - 1.35 * inch, 5.4 * inch, s_card_h)
    prob_html = (
        "• <b><font color='#0B192C'>The Attention Bottleneck:</font></b><br/>"
        "High-throughput network systems generate millions of predictions daily, but human audit teams can review only 1%–5% due to high operational cost.<br/><br/>"
        "• <b><font color='#0B192C'>Silent Overconfidence Failure:</font></b><br/>"
        "Under temporal distribution shift, models maintain average confidence over 96.8% despite a 4.55x surge in prediction error rate [4], [5].<br/><br/>"
        "• <b><font color='#0B192C'>Inefficacy of Random Audits:</font></b><br/>"
        "Uniform random inspection captured only 1.17% of shifted-test errors at a 1% review budget in our experiments.<br/><br/>"
        "• <b><font color='#0B192C'>Single-Signal Failure:</font></b><br/>"
        "Confidence alone misses novel attack vectors; OOD detection alone flags novelty that does not correspond to classification errors."
    )
    draw_para(prob_html, 0.8 * inch, PH - 1.8 * inch, 5.4 * inch, ParagraphStyle('Prob', parent=s_body, fontSize=11.5, leading=16))

    draw_card(6.8 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    draw_para("<font color='#16A34A'><b>PROPOSED SOLUTION</b></font>", 7.0 * inch, PH - 1.35 * inch, 5.5 * inch, s_card_h)
    sol_html = (
        "• <b><font color='#0B192C'>Multi-Factor Reliability Engine:</font></b><br/>"
        "Synthesizes four complementary signals: prediction uncertainty, Mahalanobis OOD distance, feature drift (PSI), and historical mistake proximity.<br/><br/>"
        "• <b><font color='#0B192C'>Budget-Constrained Priority Queue:</font></b><br/>"
        "Constructs a composite risk score and allocates top-K predictions matching exact capacity thresholds (1%, 2%, 5%, 10%).<br/><br/>"
        "• <b><font color='#0B192C'>Adaptive Signal Weighting:</font></b><br/>"
        "Dynamically scales signal weights based on population-level feature drift severity and reviewed error feedback [2], [6].<br/><br/>"
        "• <b><font color='#0B192C'>Chronological Shift Evaluation:</font></b><br/>"
        "Evaluates the pipeline on temporal partitions to assess performance under genuine temporal degradation, avoiding random split leakage."
    )
    draw_para(sol_html, 7.0 * inch, PH - 1.8 * inch, 5.5 * inch, ParagraphStyle('Sol', parent=s_body, fontSize=11.5, leading=16))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 4: Purpose & Scope
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Introduction & Problem Formulation", "Project Purpose & Implementation Scope")
    draw_card(0.6 * inch, 3.8 * inch, 12.1 * inch, 2.5 * inch)
    draw_para("<font color='#1E40AF'><b>PURPOSE OF THE RESEARCH</b></font>", 0.8 * inch, PH - 1.35 * inch, 11.7 * inch, s_card_h)
    pur_html = (
        "• <b><font color='#0B192C'>Empirical Investigation:</font></b> Determine whether combining heterogeneous reliability signals catches more critical errors than conventional confidence ranking under tight operational budgets.<br/><br/>"
        "• <b><font color='#0B192C'>Tackle Overconfidence:</font></b> Address the silent failure mode of ML models that misclassify traffic with high confidence under temporal shift [4], [5].<br/><br/>"
        "• <b><font color='#0B192C'>Operational Triage Framework:</font></b> Provide a principled, reproducible framework for triage routing that explicitly models constrained human inspection capacity using 1%, 2%, 5%, and 10% review budgets (1%, 2%, 5%, 10%)."
    )
    draw_para(pur_html, 0.8 * inch, PH - 1.8 * inch, 11.7 * inch, ParagraphStyle('Pur', parent=s_body, fontSize=12, leading=17))

    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 3.2 * inch)
    draw_para("<font color='#0B192C'><b>PROJECT SCOPE (PHASE-1 vs PHASE-2)</b></font>", 0.8 * inch, 3.35 * inch, 11.7 * inch, s_card_h)
    scp_html = (
        "• <b><font color='#1E40AF'>In-Scope (Phase-1 Implemented):</font></b><br/>"
        "Binary classification (Benign vs Attack) on network flow data; 500,000-flow chronological sample from BigFlow-NIDS [16]; simulated review oracle using test ground truth; evaluation across 4 fixed budgets (1%, 2%, 5%, 10%).<br/><br/>"
        "• <b><font color='#64748B'>Out-of-Scope (Phase-1):</font></b><br/>"
        "Live production network tap / inline packet processing; actual human reviewers in the loop (simulated ground-truth oracle used); multi-class attack attribution (detailed Attack column excluded to avoid label leakage).<br/><br/>"
        "• <b><font color='#64748B'>Planned Scope (Phase-2):</font></b><br/>"
        "Dataset-agnostic tabular generalization across healthcare and financial domains; post-hoc calibration; SHAP explainability for flagged review cases; interactive web dashboard."
    )
    draw_para(scp_html, 0.8 * inch, 2.95 * inch, 11.7 * inch, ParagraphStyle('Scp', parent=s_body, fontSize=11.5, leading=16))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 5: Background Study
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Literature Survey & Foundations", "Background Study: Existing Systems & Approaches")
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 5.8 * inch)
    draw_para("<font color='#0B192C'><b>EXISTING PARADIGMS IN SELECTIVE ML & REVIEW ALLOCATION</b></font>", 0.8 * inch, PH - 1.35 * inch, 11.7 * inch, s_card_h)
    bg_html = (
        "• <b><font color='#1E40AF'>Confidence-Based Selective Classification [4], [5]:</font></b><br/>"
        "Ranks instances strictly by maximum prediction probability max(P(y|x)) (Geifman & El-Yaniv, 2017 [4]). Limitation: Deep models suffer from uncalibrated overconfidence (Guo et al., 2017 [5]); under temporal shift, confident misclassifications bypass pure confidence thresholds.<br/><br/>"
        "• <b><font color='#1E40AF'>Out-of-Distribution (OOD) Detection [1], [8]:</font></b><br/>"
        "Measures distance from training distributions via regularized Mahalanobis metrics (Yang et al., 2024 [8]; Cao et al., 2023 [1]). Limitation: Novel instances in network flows often reflect benign high-volume transfers rather than classification errors.<br/><br/>"
        "• <b><font color='#1E40AF'>Population Distribution Drift Monitoring [11], [12]:</font></b><br/>"
        "Tracks macroscopic feature distribution shifts and concept drift over time using metrics like PSI (Lu et al., IEEE TKDE 2019 [11]; Iwashita & Papa, IEEE Access 2019 [12]). Limitation: Population aggregates lack per-instance risk scoring for operational triage.<br/><br/>"
        "• <b><font color='#1E40AF'>Learning to Defer (L2D) [2], [3], [7], [14]:</font></b><br/>"
        "Jointly trains classifiers and rejection policies to defer difficult instances to human experts (Mozannar & Sontag, 2020 [2]; Wei et al., 2024 [3]; Liu et al., 2022 [7]; Hendrickx et al., 2024 [14]). Limitation: Assumes fixed deferral costs rather than strict capacity quotas (1%–10%).<br/><br/>"
        "• <b><font color='#1E40AF'>Human-in-the-Loop Intrusion Detection [6], [13]:</font></b><br/>"
        "Integrates analyst feedback into active triage loops to mitigate alert fatigue in SOCs (Kim et al., IEEE TIFS 2024 [6]; Mosqueira-Rey et al., 2023 [13]). Motivation: Demonstrates the urgent operational need to optimize constrained human inspection capacity."
    )
    draw_para(bg_html, 0.8 * inch, PH - 1.8 * inch, 11.7 * inch, ParagraphStyle('BgP', parent=s_body, fontSize=11.5, leading=16))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 6: Literature Survey (Part 1: Papers [1]–[5])
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Literature Survey & Foundations", "Literature Survey: Research Papers (Part 1: Papers [1]–[5])")
    papers_p1 = [
        ("[1] Cao, Zhu, Pang (2023)", "Anomaly Detection Under Distribution Shift", 
         "IEEE/CVF International Conference on Computer Vision (ICCV 2023), pp. 6488-6500", 
         "<font color='#16A34A'><b>[IEEE & Scopus Indexed]</b></font>  DOI: 10.1109/ICCV51070.2023.00599",
         "Addresses anomaly detection failure when test data shifts from training distributions. Proves unsupervised domain alignment mitigates false positives, directly justifying our shifted evaluation benchmark."),
        ("[2] Mozannar & Sontag (2020)", "Consistent Estimators for Learning to Defer to an Expert", 
         "International Conference on Machine Learning (ICML 2020), PMLR vol. 119, pp. 7076–7087", 
         "<font color='#D97706'><b>[Top ML Venue (PMLR)*]</b></font>  Verified IEEE alternative: C. Geng et al., IEEE TPAMI, 2021",
         "Formalizes learning-to-defer by jointly training a classifier and a deferral policy using a Bayes-consistent surrogate loss. Establishes theoretical foundations for routing uncertain predictions to human experts."),
        ("[3] Wei, Cao, Feng (2024)", "Exploiting Human-AI Dependence for Learning to Defer", 
         "International Conference on Machine Learning (ICML 2024), PMLR vol. 235, pp. 52484–52499", 
         "<font color='#D97706'><b>[Top ML Venue (PMLR)*]</b></font>  Verified IEEE alternative: D.-B. Wang et al., IEEE/CVF CVPR, 2022",
         "Models human-machine error correlation to prevent deferrals when both the AI and the human fail. Informs our review-efficiency triage objective under constrained operational inspection capacity."),
        ("[4] Geifman & El-Yaniv (2017)", "Selective Classification for Deep Neural Networks", 
         "Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, pp. 4878–4887", 
         "<font color='#16A34A'><b>[Scopus Indexed Series]</b></font>  ISSN: 1049-5258",
         "Formulates selective classification risk-coverage trade-offs using prediction confidence. Provides the theoretical baseline for our confidence-based review strategy, whose limitations under distribution shift we empirically demonstrate."),
        ("[5] Guo et al. (2017)", "On Calibration of Modern Neural Networks", 
         "International Conference on Machine Learning (ICML 2017), PMLR vol. 70, pp. 1321–1330", 
         "<font color='#D97706'><b>[Top ML Venue (PMLR)*]</b></font>  Verified IEEE alternative: K. Fernando & C. Tsokos, IEEE TNNLS, 2022",
         "Demonstrates that modern classifiers suffer from severe overconfidence miscalibration and proposes temperature scaling. Explains why raw output probabilities cannot be treated as true probabilities of correctness in triage queues.")
    ]
    for idx, (auth, title, venue, badge, summ) in enumerate(papers_p1):
        top = PH - 1.25 * inch - idx * 1.15 * inch
        draw_card(0.6 * inch, top - 1.05 * inch, 12.1 * inch, 1.05 * inch)
        p_html = (
            f"<b><font color='#0B192C'>{auth}:</font></b>  "
            f"<b><font color='#1E40AF'>\"{title}\"</font></b>  {badge}<br/>"
            f"<font color='#64748B'>{venue}</font><br/>"
            f"<font color='#1E293B'><b>Summary:</b> {summ}</font>"
        )
        draw_para(p_html, 0.75 * inch, top - 0.05 * inch, 11.8 * inch, ParagraphStyle(f'P1_{idx}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 7: Literature Survey (Part 2: Papers [6]–[10])
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Literature Survey & Foundations", "Literature Survey: Research Papers (Part 2: Papers [6]–[10])")
    papers_p2 = [
        ("[6] Kim, Dan, Zhu (2024)", "Human-in-the-Loop Cyber Intrusion Detection Using Active Learning", 
         "IEEE Transactions on Information Forensics and Security, vol. 19, pp. 8658–8672", 
         "<font color='#16A34A'><b>[IEEE & Scopus Indexed]</b></font>  DOI: 10.1109/TIFS.2024.3434647",
         "Optimizes SOC analyst alert investigation using active learning and sequential hypothesis testing. Directly motivates our capacity-constrained human review triage in network intrusion detection systems."),
        ("[7] Liu, Gallego, Barbieri (2022)", "Incorporating Uncertainty in Learning to Defer for Safe Computer-Aided Diagnosis", 
         "Scientific Reports, vol. 12, no. 1, Art. no. 1762, pp. 1–11", 
         "<font color='#16A34A'><b>[Scopus Indexed Q1]</b></font>  DOI: 10.1038/s41598-022-05725-7",
         "Incorporates predictive uncertainty into learning-to-defer objectives for clinical diagnosis. Demonstrates that explicit uncertainty estimation substantially reduces unnecessary human deferrals while preserving decision safety."),
        ("[8] Yang et al. (2024)", "Generalized Out-of-Distribution Detection: A Survey", 
         "International Journal of Computer Vision, vol. 132, no. 12, pp. 5635–5662", 
         "<font color='#16A34A'><b>[Scopus Indexed Q1]</b></font>  DOI: 10.1007/s11263-024-02117-4",
         "Comprehensive survey and taxonomy of generalized out-of-distribution detection across semantic and covariate shifts. Establishes the theoretical foundation and post-hoc distance metrics used for our OOD reliability signal."),
        ("[9] Koh et al. (2021)", "WILDS: A Benchmark of In-the-Wild Distribution Shifts", 
         "International Conference on Machine Learning (ICML 2021), PMLR vol. 139, pp. 5637–5664", 
         "<font color='#D97706'><b>[Top ML Venue (PMLR)*]</b></font>  Verified IEEE alternative: L. Ruff et al., Proc. IEEE, 2021",
         "Establishes a benchmark of real-world in-the-wild distribution shifts across domains and time. Justifies our chronological dataset partition design to evaluate model performance degradation under authentic shift."),
        ("[10] He, Kim, Asghar (2023)", "Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey", 
         "IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 538–566", 
         "<font color='#16A34A'><b>[IEEE & Scopus Indexed]</b></font>  DOI: 10.1109/COMST.2022.3233793",
         "Comprehensive survey of adversarial machine learning vulnerabilities in network intrusion detection. Provides domain security context on how feature perturbations degrade ML classifiers in network traffic.")
    ]
    for idx, (auth, title, venue, badge, summ) in enumerate(papers_p2):
        top = PH - 1.25 * inch - idx * 1.15 * inch
        draw_card(0.6 * inch, top - 1.05 * inch, 12.1 * inch, 1.05 * inch)
        p_html = (
            f"<b><font color='#0B192C'>{auth}:</font></b>  "
            f"<b><font color='#1E40AF'>\"{title}\"</font></b>  {badge}<br/>"
            f"<font color='#64748B'>{venue}</font><br/>"
            f"<font color='#1E293B'><b>Summary:</b> {summ}</font>"
        )
        draw_para(p_html, 0.75 * inch, top - 0.05 * inch, 11.8 * inch, ParagraphStyle(f'P2_{idx}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 8: Comparative Study
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Literature Survey & Foundations", "Comparative Study: Existing Paradigms vs Proposed Framework")
    comp_h = ["Evaluation Dimension", "Random Audit", "Pure Confidence [4]", "OOD Filter [8]", "Learn-to-Defer [2]", "Proposed Framework"]
    comp_r = [
        ["Prediction Uncertainty", "No", "Yes (Sole Signal)", "No", "Optional", "Yes (Normalized Probability)"],
        ["Out-of-Distribution (OOD)", "No", "No", "Yes (Sole Signal)", "Rarely", "Yes (Mahalanobis Distance)"],
        ["Distribution Drift (PSI)", "No", "No", "No", "No", "Yes (Feature-Level PSI)"],
        ["Historical Error Proximity", "No", "No", "No", "Implicit", "Yes (Decile Mistake Bins)"],
        ["Explicit Capacity Budgets", "Implicit", "Manual Tuning", "Hard Cutoff", "Theoretical", "Yes (1%, 2%, 5%, 10%)"],
        ["Temporal Shift Evaluation", "N/A", "Rarely", "Partial", "Rarely", "Yes (Chronological Split)"],
        ["Adaptive Weight Scaling", "No", "No", "No", "Static Cost", "Yes (Drift & Feedback Adaptive)"]
    ]
    
    # Render table using Paragraph for all cells
    cx_list = [0.5*inch, 3.0*inch, 4.6*inch, 6.6*inch, 8.5*inch, 10.4*inch, 12.8*inch]
    widths  = [2.5*inch, 1.6*inch, 2.0*inch, 1.9*inch, 1.9*inch, 2.4*inch]
    
    top_t = PH - 1.25 * inch
    hh = 0.4 * inch
    rh = 0.5 * inch
    
    # Header
    for ci, (hdr, w) in enumerate(zip(comp_h, widths)):
        c.setFillColor(NAVY); c.rect(cx_list[ci], top_t - hh, w, hh, fill=1, stroke=0)
        p = Paragraph(f"<b><font color='white'>{hdr}</font></b>", ParagraphStyle(f'TH_{ci}', parent=s_body, fontSize=10.5, leading=14, alignment=1))
        p.wrapOn(c, w - 8, hh)
        p.drawOn(c, cx_list[ci] + 4, top_t - hh + 8)
        
    cur_y = top_t - hh
    for ri, row in enumerate(comp_r):
        bg = CARD_BG if ri % 2 == 0 else CARD_ALT
        for ci, (val, w) in enumerate(zip(row, widths)):
            c.setFillColor(bg); c.rect(cx_list[ci], cur_y - rh, w, rh, fill=1, stroke=0)
            c.setStrokeColor(BORDER); c.setLineWidth(0.3)
            c.rect(cx_list[ci], cur_y - rh, w, rh, fill=0, stroke=1)
            b_col = '#1E40AF' if ci == 5 else '#1E293B'
            p = Paragraph(f"<font color='{b_col}'>{val}</font>", ParagraphStyle(f'TC_{ri}_{ci}', parent=s_body, fontSize=10.5, leading=14, alignment=0 if ci == 0 else 1))
            p.wrapOn(c, w - 8, rh)
            p.drawOn(c, cx_list[ci] + 4, cur_y - rh + 12)
        cur_y -= rh
        
    draw_card(0.5 * inch, 0.4 * inch, 12.3 * inch, 1.0 * inch, fill=CARD_ALT)
    draw_para("<b><font color='#0B192C'>Key Distinction:</font></b> Prior paradigms isolate confidence or OOD detection without explicit capacity slicing. Our proposed framework unifies four complementary signals into a single ranking mechanism evaluated directly under chronological distribution shift.",
              0.7 * inch, 1.15 * inch, 11.9 * inch, ParagraphStyle('KD', parent=s_body, fontSize=12, leading=17))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 9: Users of the System
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Requirements & User Specification", "Users of the System & Primary Stakeholders")
    users = [
        ("ML Engineer / Practitioner", ACCENT, [
            "Configures and trains baseline models (XGBoost, Random Forest, Logistic Regression) on historical network flows.",
            "Fits training-time preprocessing pipelines and establishes reference centroids and covariance matrices for OOD detection.",
            "Monitors feature-level drift statistics (PSI) and configures initial heuristic risk signal weights.",
            "Inspects validation metrics (ROC-AUC 0.9228) and evaluates model overconfidence characteristics."
        ]),
        ("Simulated Reviewer / Review Oracle", GREEN, [
            "Receives prioritized, high-risk network flow predictions routed to the human-review queue within operational budget (1%–10%).",
            "Inspects flagged instances displaying severe confidence degradation, feature drift, or anomalous packet patterns.",
            "Provides ground-truth audit verdicts on intercepted borderline and novel attack instances.",
            "Benefits from focused triage that mitigates alert fatigue and prevents unreviewed high-confidence ML misclassifications."
        ]),
        ("Evaluator / Research Auditor", AMBER, [
            "Executes systematic comparative evaluations across review allocation strategies (Random, Confidence, OOD, Static, Adaptive).",
            "Benchmarks error capture rate and review efficiency (errors intercepted per 1,000 human audits).",
            "Audits system robustness under chronological distribution shift against simulated oracles.",
            "Verifies compliance with data integrity constraints (SHA-256) and audit logging standards."
        ])
    ]
    for i, (role, color, bullets) in enumerate(users):
        x = (0.6 + i * 4.1) * inch
        draw_card(x, 0.4 * inch, 3.9 * inch, 5.8 * inch)
        c.setFillColor(color); c.roundRect(x, PH - 1.85 * inch, 3.9 * inch, 0.6 * inch, 4, fill=1, stroke=0)
        p_hdr = Paragraph(f"<b><font color='white'>{role}</font></b>", ParagraphStyle(f'UR_{i}', parent=s_body_b, fontSize=12.5, alignment=1))
        p_hdr.wrapOn(c, 3.7 * inch, 0.5 * inch)
        p_hdr.drawOn(c, x + 0.1 * inch, PH - 1.5 * inch)
        
        b_html = "".join([f"• {b}<br/><br/>" for b in bullets])
        draw_para(b_html, x + 0.2 * inch, PH - 2.05 * inch, 3.5 * inch, ParagraphStyle(f'UB_{i}', parent=s_body, fontSize=11, leading=15.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 10: Functional Requirements (FR1 - FR7)
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Requirements & User Specification", "Functional Requirements: Data, Models & Signals (FR1–FR7)")
    fr_items1 = [
        ("FR1", "Raw Ingestion & Schema Verification", "Verify 500K sample integrity against 14GB source via SHA-256 fingerprints.", "src/01_test_dataset.py, src/26_verify_bigflow_sample.py", "100% Implemented"),
        ("FR2", "Chronological Splitting", "Partition flows temporally into 70% Train (350K), 15% Val (75K), 15% Test (75K).", "src/02_create_splits.py", "100% Implemented"),
        ("FR3", "Data Preprocessing", "Impute missing values with training medians, apply StandardScaler strictly on LR.", "src/03_preprocess.py", "100% Implemented"),
        ("FR4", "Model Training & Validation", "Train Logistic Regression, Random Forest, and XGBoost (val ROC-AUC 0.9228).", "src/04_train_models.py", "100% Implemented"),
        ("FR5", "Prediction Signal Extraction", "Extract prediction probability, confidence, and Shannon prediction entropy.", "src/05_generate_prediction_signals.py, src/16_shifted_test_predictions.py", "100% Implemented"),
        ("FR6", "Confidence-Based Review Strategy", "Rank predictions by ascending confidence across 1%, 2%, 5%, 10% budgets.", "src/06_confidence_review_strategy.py", "100% Implemented"),
        ("FR7", "Mahalanobis OOD Distance Detection", "Compute regularized Mahalanobis distance relative to 50K training flows.", "src/07_ood_detection.py, src/08_ood_review_strategy.py", "100% Implemented")
    ]
    for idx, (f_id, name, desc, script, status) in enumerate(fr_items1):
        top = PH - 1.25 * inch - idx * 0.82 * inch
        draw_card(0.6 * inch, top - 0.76 * inch, 12.1 * inch, 0.76 * inch)
        fr_html = (
            f"<b><font color='#0B192C'>{f_id}: {name}</font></b>  "
            f"<font color='#16A34A'><b>[{status}]</b></font><br/>"
            f"<font color='#1E293B'>{desc}</font>  |  "
            f"<b><font color='#1E40AF'>Mapped to: {script}</font></b>"
        )
        draw_para(fr_html, 0.75 * inch, top - 0.05 * inch, 11.8 * inch, ParagraphStyle(f'FR1_{idx}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 11: Functional Requirements (FR8 - FR14)
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Requirements & User Specification", "Functional Requirements: Triage, Scoring & Evaluation (FR8–FR14)")
    fr_items2 = [
        ("FR8", "Static Multi-Factor Synthesis", "Combine 50% confidence risk and 50% OOD percentile into baseline multi-factor score.", "src/09_static_multifactor_strategy.py", "100% Implemented"),
        ("FR9", "Feature Drift Measurement", "Calculate Population Stability Index (PSI) with 10 quantile bins across 49 features.", "src/10_measure_drift.py, src/11_create_drift_risk.py", "100% Implemented"),
        ("FR10", "Adaptive Regime Risk Scoring", "Classify drift severity into Low/Mod/High regimes and assign regime-specific weights.", "src/12_adaptive_risk_score.py, src/13_adaptive_review_strategy.py", "100% Implemented"),
        ("FR11", "Historical Error Proximity", "Bin 10 network flow features into deciles to map mistake patterns and mistake proximity.", "src/14_historical_error_risk.py, src/15_four_factor_risk.py", "100% Implemented"),
        ("FR12", "Shifted-Test Evaluation Pipeline", "Benchmark 5 strategies on 75,000 shifted flows across 4 operational budgets.", "src/18_shifted_review_comparison.py, src/21_review_efficiency.py", "100% Implemented"),
        ("FR13", "Feedback-Adaptive Allocation Loop", "Scale historical error weight based on reviewed error concentration feedback.", "src/23_review_feedback_loop.py, src/24_shifted_feedback_evaluation.py", "100% Implemented"),
        ("FR14", "Interactive Web Dashboard Interface", "Provide interactive parameter tuning, dynamic budget sliders, and graphical metric cards.", "Local Streamlit dashboard/demo implemented; broader multi-dataset/enterprise extensions remain Phase-II.", "Partial (50%)")
    ]
    for idx, (f_id, name, desc, script, status) in enumerate(fr_items2):
        top = PH - 1.25 * inch - idx * 0.82 * inch
        draw_card(0.6 * inch, top - 0.76 * inch, 12.1 * inch, 0.76 * inch)
        col = '#16A34A' if "100%" in status else '#D97706'
        fr_html = (
            f"<b><font color='#0B192C'>{f_id}: {name}</font></b>  "
            f"<font color='{col}'><b>[{status}]</b></font><br/>"
            f"<font color='#1E293B'>{desc}</font>  |  "
            f"<b><font color='#1E40AF'>Mapped to: {script}</font></b>"
        )
        draw_para(fr_html, 0.75 * inch, top - 0.05 * inch, 11.8 * inch, ParagraphStyle(f'FR2_{idx}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 12: Non-Functional Requirements
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Requirements & User Specification", "Non-Functional Requirements Specification (Measured)")
    nfrs = [
        ("NFR1: Strict Reproducibility", ACCENT, [
            "<b>Requirement:</b> Deterministic execution across all data splits, feature transformations, and model evaluations.",
            "<b>Measured Implementation:</b> Fixed random seed (random_state=42) across all scripts. Deterministic chronological sort ensures identical 350K/75K/75K splits on every run."
        ]),
        ("NFR2: Computation Time & Latency", GREEN, [
            "<b>Requirement:</b> Efficient execution suitable for high-throughput batch processing without excessive compute overhead.",
            "<b>Measured Implementation:</b> Full strategy comparison (src/25_final_strategy_comparison.py) executes in 1.60 seconds. End-to-end signal extraction across 75,000 instances completes in ~48 seconds on standard CPU."
        ]),
        ("NFR3: Data Integrity & Traceability", RED, [
            "<b>Requirement:</b> Cryptographic verification of data provenance and sample fidelity.",
            "<b>Measured Implementation:</b> SHA-256 fingerprint verification (src/26_verify_bigflow_sample.py) confirms that 100% of rows in BigFlow_sample.csv match the raw 14GB source dataset."
        ]),
        ("NFR4: Modularity & Interpretability", AMBER, [
            "<b>Requirement:</b> Decoupled software architecture with transparent, defensible scoring logic.",
            "<b>Measured Implementation:</b> 26 independent Python scripts communicate via standard CSV contracts. Risk scores are transparent weighted linear combinations of 4 explicit reliability signals."
        ])
    ]
    for i, (title, color, bullets) in enumerate(nfrs):
        x = (0.6 + (i % 2) * 6.2) * inch
        y = (PH - 1.25 * inch - (i // 2) * 2.85 * inch - 2.65 * inch)
        draw_card(x, y, 6.0 * inch, 2.65 * inch)
        c.setFillColor(color); c.roundRect(x, y + 2.15 * inch, 6.0 * inch, 0.5 * inch, 4, fill=1, stroke=0)
        p_hdr = Paragraph(f"<b><font color='white'>{title}</font></b>", ParagraphStyle(f'NH_{i}', parent=s_body_b, fontSize=12.5, alignment=0))
        p_hdr.wrapOn(c, 5.6 * inch, 0.4 * inch)
        p_hdr.drawOn(c, x + 0.2 * inch, y + 2.25 * inch)
        
        b_html = "".join([f"• {b}<br/><br/>" for b in bullets])
        draw_para(b_html, x + 0.2 * inch, y + 2.05 * inch, 5.6 * inch, ParagraphStyle(f'NB_{i}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    
    # SLIDE X: Workflow Boundary and Leakage Control
    slide_bg(); add_logo(); header("Methodology", "Workflow Boundary and Leakage Control")
    y_pos = PH - 1.6 * inch
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(DARK)
    c.drawString(0.8 * inch, y_pos, "To ensure rigorous evaluation and avoid data leakage, the pipeline is strictly divided into three stages:")
    y_pos -= 0.5 * inch
    
    stages = [
        ("1. Offline Benchmarking", "Models, signal references, and thresholds are fitted exclusively on the training split (350K flows). Signal selection and threshold tuning use validation data only. Test labels are never used during this phase and are restricted strictly to scoring the final review queue."),
        ("2. Simulated Reviewer Feedback", "After an initial review queue is built, true labels are revealed sequentially only for the top-K reviewed items. The adaptive multi-factor weights are updated heuristically based solely on these revealed labels before re-ranking the next batch (implemented in src/28_sequential_feedback_eval.py)."),
        ("3. Future Operational Workflow (Out of Scope)", "Future deployments will involve real human analysts with non-zero processing delays and potential reviewer error, where ground-truth labels arrive organically after human review.")
    ]
    
    for title, desc in stages:
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(NAVY)
        c.drawString(0.8 * inch, y_pos, title)
        y_pos -= 0.3 * inch
        
        c.setFont("Helvetica", 12)
        c.setFillColor(DARK)
        import textwrap; lines = textwrap.wrap(desc, width=120)
        for line in lines:
            c.drawString(1.0 * inch, y_pos, line)
            y_pos -= 0.25 * inch
        y_pos -= 0.3 * inch
    
    c.showPage()

    # SLIDE 13: Tools & Technologies
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Design Methodology & Technical Stack", "Tools & Technologies Used")
    techs = [
        ("CORE LANGUAGE & RUNTIME", NAVY, [
            ("Python 3.10+:", "Primary execution runtime for data processing, scientific modeling, and evaluation pipelines."),
            ("pathlib & os:", "Robust cross-platform filesystem path resolution across local and cloud environments.")
        ]),
        ("DATA ENGINEERING & STORAGE", ACCENT, [
            ("pandas (v2.x):", "High-performance tabular data manipulation, chronological sorting, and CSV persistence."),
            ("NumPy (v1.26+):", "Vectorized array computations, numerical stabilizer arithmetic, and quantile calculations.")
        ]),
        ("MACHINE LEARNING & MODELING", GREEN, [
            ("XGBoost (v2.0+):", "Primary gradient-boosted decision tree classifier (150 estimators, max depth 6)."),
            ("scikit-learn (v1.3+):", "StandardScaler preprocessing, Logistic Regression, Random Forest, and ROC-AUC evaluation.")
        ]),
        ("SCIENTIFIC COMPUTING & SECURITY", PURPLE, [
            ("SciPy (v1.11+):", "Regularized covariance matrix inversion, Mahalanobis distance, and Shannon entropy."),
            ("joblib & hashlib:", "Serialized model artifact persistence (.pkl) and SHA-256 cryptographic sample verification.")
        ])
    ]
    for i, (title, color, items) in enumerate(techs):
        x = (0.6 + (i % 2) * 6.2) * inch
        y = (PH - 1.25 * inch - (i // 2) * 2.85 * inch - 2.65 * inch)
        draw_card(x, y, 6.0 * inch, 2.65 * inch)
        c.setFillColor(color); c.roundRect(x, y + 2.15 * inch, 6.0 * inch, 0.5 * inch, 4, fill=1, stroke=0)
        p_hdr = Paragraph(f"<b><font color='white'>{title}</font></b>", ParagraphStyle(f'TH_{i}', parent=s_body_b, fontSize=12.5, alignment=0))
        p_hdr.wrapOn(c, 5.6 * inch, 0.4 * inch)
        p_hdr.drawOn(c, x + 0.2 * inch, y + 2.25 * inch)
        
        t_html = "".join([f"• <b><font color='#0B192C'>{tool}</font></b> {desc}<br/><br/>" for tool, desc in items])
        draw_para(t_html, x + 0.2 * inch, y + 2.05 * inch, 5.6 * inch, ParagraphStyle(f'TB_{i}', parent=s_body, fontSize=11, leading=15))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 14: System Architecture Diagram
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Design Methodology & System Architecture", "System Design: Architecture Diagram")
    draw_img("v2_architecture.png", 0.6 * inch, 2.3 * inch, 12.1 * inch, 4.3 * inch)
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 1.4 * inch, fill=CARD_ALT)
    draw_para("<b><font color='#0B192C'>Architectural Dataflow Summary:</font></b><br/>"
              "Data flows through five discrete stages: (1) Ingestion & temporal partitioning -> (2) Preprocessing & baseline inference -> "
              "(3) 4-signal reliability feature extraction -> (4) Composite risk scoring & priority queue creation -> "
              "(5) Review allocation to simulated human oracle within budget (1% to 10%), dispatching remainder to automated model decision.",
              0.8 * inch, 1.65 * inch, 11.7 * inch, ParagraphStyle('ArchD', parent=s_body, fontSize=12, leading=18))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 15: ML Process Flow & Methodology
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Design Methodology & System Architecture", "System Design: ML Process Flow & Methodology")
    draw_img("v2_process_flow.png", 0.6 * inch, 2.3 * inch, 12.1 * inch, 4.3 * inch)
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 1.4 * inch, fill=CARD_ALT)
    draw_para("<b><font color='#0B192C'>Methodological Safeguards:</font></b><br/>"
              "Strict chronological splitting prevents data leakage. Preprocessing parameters (median imputation, feature scalers) are fitted "
              "strictly on the 350K training split. All OOD covariance calculations and historical mistake bins are derived without access "
              "to shifted test labels, ensuring genuine temporal evaluation.",
              0.8 * inch, 1.65 * inch, 11.7 * inch, ParagraphStyle('FlowD', parent=s_body, fontSize=12, leading=18))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 16: Database Design: Conceptual Schema & ER
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Design Methodology & System Architecture", "Database Design: Conceptual Schema & Entity-Relationship")
    draw_img("v2_data_schema.png", 0.6 * inch, 1.8 * inch, 12.1 * inch, 4.8 * inch)
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 1.1 * inch, fill=CARD_ALT)
    draw_para("<b><font color='#0B192C'>File-Based Data Architecture:</font></b> Stored across structured CSV tables and serialized joblib artifacts. Primary keys (prediction_id) maintain relational integrity across prediction signals, drift metrics, and final review queue allocations without requiring a database server.",
              0.8 * inch, 1.35 * inch, 11.7 * inch, ParagraphStyle('SchD', parent=s_body, fontSize=12, leading=18))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 17: Core Pipeline Pseudocode
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Design Methodology & Algorithmic Execution", "Core Pipeline: Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift (Pseudocode)")
    draw_card(0.6 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    draw_card(6.8 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    
    p1_html = (
        "<font color='#0B192C'><b>PHASE 1: INGESTION & BASELINE FIT (STEPS 1–5)</b></font><br/>"
        "• <b><font color='#1E40AF'>1. Chronological Load:</font></b> Load 500,000 NetFlow records from BigFlow-NIDS benchmark (src/01).<br/>"
        "• <b><font color='#1E40AF'>2. Temporal Sort:</font></b> Sort strictly by timestamp (flow_start_time) to eliminate future leakage.<br/>"
        "• <b><font color='#1E40AF'>3. Data Partitioning:</font></b> Split chronologically into Train (350K, 70%), Val (75K, 15%), Shifted Test (75K, 15%).<br/>"
        "• <b><font color='#1E40AF'>4. Preprocessing Fit:</font></b> Fit median imputer and scalers on Train only; transform Val and Test without leakage.<br/>"
        "• <b><font color='#1E40AF'>5. Model & Baseline Fit:</font></b> Train XGBoost classifier (ROC-AUC=0.9228); fit train covariance matrix (Tikhonov regularized lambda=1e-4); map training-set mistake deciles.<br/><br/>"
        "<font color='#0B192C'><b>PHASE 2: SIGNAL EXTRACTION (STEPS 6–10)</b></font><br/>"
        "• <b><font color='#1E40AF'>6. Posterior Estimation:</font></b> Extract class probabilities P_i = f_theta(x_i) for shifted test flows (N=75,000).<br/>"
        "• <b><font color='#1E40AF'>7. Prediction Uncertainty:</font></b> s_conf = 1 - max(P_i, 1 - P_i) in [0.0, 0.5]; flags decision boundary ambiguity.<br/>"
        "• <b><font color='#1E40AF'>8. Mahalanobis OOD:</font></b> d_M = sqrt((x_i - mu)^T (Sigma + lambda*I)^(-1) (x_i - mu)); convert to percentile rank s_ood in [0, 1].<br/>"
        "• <b><font color='#1E40AF'>9. PSI Drift Score:</font></b> Compute 10-bin Population Stability Index across 49 features; weight per-instance z-score deviations.<br/>"
        "• <b><font color='#1E40AF'>10. Historical Error:</font></b> Lookup validation error rate in nearest feature mistake decile: s_hist = H_train(x_i)."
    )
    draw_para(p1_html, 0.8 * inch, PH - 1.35 * inch, 5.5 * inch, ParagraphStyle('AlgoP1', parent=s_body, fontSize=9.5, leading=13.5))

    p2_html = (
        "<font color='#0B192C'><b>PHASE 3: RISK FUSION & ALLOCATION (STEPS 11–13)</b></font><br/>"
        "• <b><font color='#1E40AF'>11. Composite Score:</font></b> Synthesize 4 signals: R_i = w1*s_conf + w2*s_ood + w3*s_drift + w4*s_hist (sum(w)=1.0).<br/>"
        "• <b><font color='#1E40AF'>12. Priority Ranking:</font></b> Sort instances descending by composite risk R_i: Indices = argsort(R).<br/>"
        "• <b><font color='#1E40AF'>13. Budget Slicing:</font></b> Enforce hard capacity quota K = floor(B * N) for B in {1%, 2%, 5%, 10%}. Sieve top-K into Review Queue Q_review; remaining (N-K) to Autonomous Queue Q_auto.<br/><br/>"
        "<font color='#0B192C'><b>PHASE 4: SIMULATION ORACLE & BENCHMARK (STEPS 14–16)</b></font><br/>"
        "• <b><font color='#1E40AF'>14. Review Oracle:</font></b> Simulate human inspection using test ground-truth labels for reproducible benchmarking (no live human subjects in Phase-I).<br/>"
        "• <b><font color='#1E40AF'>15. Performance Metrics:</font></b> Calculate Error Capture Rate ECR = (CaughtErrors / 3,427) * 100 and Review Efficiency = (CaughtErrors / K) * 1000.<br/>"
        "• <b><font color='#1E40AF'>16. Strategy Comparison & Adaptation:</font></b> Benchmark all 5 strategies. If Feedback Adaptive: dynamically boost historical weight based on audit error density: w4 = min(0.40, w4 * 1.15); re-normalize w."
    )
    draw_para(p2_html, 7.0 * inch, PH - 1.35 * inch, 5.5 * inch, ParagraphStyle('AlgoP2', parent=s_body, fontSize=9.5, leading=13.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 18: Benchmark Dataset & Temporal Shift
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Dataset & Experimental Formulation", "Benchmark Dataset & Temporal Distribution Shift")
    draw_card(0.6 * inch, 0.4 * inch, 5.8 * inch, 5.8 * inch)
    draw_para("<font color='#1E40AF'><b>BIGFLOW-NIDS BENCHMARK (2026) [16]</b></font>", 0.8 * inch, PH - 1.35 * inch, 5.4 * inch, s_card_h)
    ds_html = (
        "• <b><font color='#0B192C'>Derived Benchmark:</font></b><br/>Harmonizes 4 major public NetFlow testbeds (NF-UNSW-NB15, NF-ToN-IoT, NF-BoT-IoT, NF-CSE-CIC-IDS2018) via Spark.<br/><br/>"
        "• <b><font color='#0B192C'>Full Dataset Scale:</font></b><br/>66,935,021 total network flows, 55 attributes, 32 distinct attack categories across four research testbeds.<br/><br/>"
        "• <b><font color='#0B192C'>Experimental Sample:</font></b><br/>500,000 chronological flows extracted for rigorous laptop-scale research experimentation.<br/><br/>"
        "• <b><font color='#0B192C'>Feature Formulation (X):</font></b><br/>49 numerical flow attributes including packet counts, byte volumes, duration, IAT, and TCP flags.<br/><br/>"
        "• <b><font color='#0B192C'>Target Formulation (y):</font></b><br/>Binary classification: 0 = Benign, 1 = Attack. Detailed Attack category excluded to prevent target leakage.<br/><br/>"
        "• <b><font color='#0B192C'>Scientific Fact:</font></b><br/>An offline research benchmark, NOT offline benchmark or live Internet traffic."
    )
    draw_para(ds_html, 0.8 * inch, PH - 1.8 * inch, 5.4 * inch, ParagraphStyle('DSH', parent=s_body, fontSize=11, leading=15.5))

    draw_card(6.8 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    draw_para("<font color='#0B192C'><b>CHRONOLOGICAL SPLIT & SHIFT DYNAMICS</b></font>", 7.0 * inch, PH - 1.35 * inch, 5.5 * inch, s_card_h)
    sp_html = (
        "• <b><font color='#1E40AF'>Training Split (70%):</font></b><br/>350,000 flows. Baseline attack prevalence: 6.10% (21,344 attacks). Used to fit scalers, reference distributions, and models.<br/><br/>"
        "• <b><font color='#1E40AF'>Validation Split (15%):</font></b><br/>75,000 flows. Attack prevalence: 0.33% (248 attacks). Model achieves 98.996% accuracy, making exactly 753 errors (1.004% error rate).<br/><br/>"
        "• <b><font color='#1E40AF'>Shifted Test Split (15%):</font></b><br/>75,000 flows from a later temporal period. Attack prevalence surges to 6.30% (4,724 attacks). Model error rate surges to 4.569% (3,427 errors).<br/><br/>"
        "• <b><font color='#1E40AF'>Observed Distribution Shift:</font></b><br/>Attack rate increases by 19.05x; error count increases by 4.55x (from 753 to 3,427 errors). Yet average confidence drops only from 98.65% to 96.82%, demonstrating severe model overconfidence."
    )
    draw_para(sp_html, 7.0 * inch, PH - 1.8 * inch, 5.5 * inch, ParagraphStyle('SPH', parent=s_body, fontSize=11, leading=15.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 18: Model Training & Validation Performance
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Implementation & Empirical Evaluation", "Model Training & Validation Performance (Verified)")
    m_h = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "Validation ROC-AUC"]
    m_r = [
        ["Logistic Regression (with StandardScaler)", "0.9606", "0.0376", "0.4435", "0.0693", "0.7499"],
        ["Random Forest (150 trees, max depth 20)", "0.9801", "0.0708", "0.4153", "0.1210", "0.8526"],
        ["XGBoost Classifier (Primary Selected)", "0.9900", "0.0401", "0.0887", "0.0552", "0.9228"]
    ]
    
    # Table
    cx_m = [0.6*inch, 4.2*inch, 5.9*inch, 7.6*inch, 9.3*inch, 11.0*inch]
    w_m  = [3.6*inch, 1.7*inch, 1.7*inch, 1.7*inch, 1.7*inch, 1.7*inch]
    top_m = PH - 1.25 * inch
    hh_m = 0.45 * inch
    rh_m = 0.48 * inch
    
    for ci, (hdr, w) in enumerate(zip(m_h, w_m)):
        c.setFillColor(NAVY); c.rect(cx_m[ci], top_m - hh_m, w, hh_m, fill=1, stroke=0)
        p = Paragraph(f"<b><font color='white'>{hdr}</font></b>", ParagraphStyle(f'MH_{ci}', parent=s_body, fontSize=11, alignment=1))
        p.wrapOn(c, w - 6, hh_m)
        p.drawOn(c, cx_m[ci] + 3, top_m - hh_m + 12)
        
    cur_ym = top_m - hh_m
    for ri, row in enumerate(m_r):
        bg = CARD_BG if ri % 2 == 0 else CARD_ALT
        for ci, (val, w) in enumerate(zip(row, w_m)):
            c.setFillColor(bg); c.rect(cx_m[ci], cur_ym - rh_m, w, rh_m, fill=1, stroke=0)
            c.setStrokeColor(BORDER); c.setLineWidth(0.3)
            c.rect(cx_m[ci], cur_ym - rh_m, w, rh_m, fill=0, stroke=1)
            b_col = '#1E40AF' if ci == 5 else '#1E293B'
            p = Paragraph(f"<font color='{b_col}'>{val}</font>", ParagraphStyle(f'MC_{ri}_{ci}', parent=s_body, fontSize=11, alignment=0 if ci == 0 else 1))
            p.wrapOn(c, w - 6, rh_m)
            p.drawOn(c, cx_m[ci] + 3, cur_ym - rh_m + 14)
        cur_ym -= rh_m

    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 3.2 * inch)
    draw_para("<b>VALIDATION PREDICTION METRICS & SELECTION RATIONALE</b>", 0.8 * inch, 3.4 * inch, 11.7 * inch, s_card_h)
    vd_html = (
        "• <b><font color='#1E40AF'>Primary Model Selection:</font></b> XGBoost was selected as the operational base classifier due to its superior discriminative power, achieving a validation ROC-AUC of 0.9228 (compared to 0.8526 for Random Forest and 0.7499 for Logistic Regression).<br/><br/>"
        "• <b><font color='#1E40AF'>Exact Training Errors Verified:</font></b> Across all 75,000 validation instances, XGBoost makes exactly 753 prediction errors (527 False Positives, 226 False Negatives), establishing a baseline error rate of 1.004%.<br/><br/>"
        "• <b><font color='#1E40AF'>Class Imbalance Reality:</font></b> Due to severe class skew (0.33% attack prevalence), raw precision and F1 appear low across all models; ROC-AUC is the true ranking metric.<br/><br/>"
        "• <b><font color='#1E40AF'>Baseline Confidence Stability:</font></b> On validation data, average XGBoost prediction confidence is 0.9865, reflecting high certainty in the unshifted operating regime."
    )
    draw_para(vd_html, 0.8 * inch, 3.0 * inch, 11.7 * inch, ParagraphStyle('VD', parent=s_body, fontSize=11.5, leading=16))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 19: Implementation Demo: Module Status
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Implementation & Empirical Evaluation", "Implementation Demo: Module Status (13 of 14 requirements complete (93%) Verified)")
    draw_img("v2_module_status.png", 0.6 * inch, 1.8 * inch, 12.1 * inch, 4.8 * inch)
    draw_card(0.6 * inch, 0.4 * inch, 12.1 * inch, 1.2 * inch, fill=CARD_ALT)
    draw_para("<b><font color='#16A34A'>Implementation Audit Result: Implementation Status: 13 fully implemented + FR14 partially implemented (50%) = 13.5/14 = 13 of 14 requirements complete (93%)</font></b><br/>"
              "The implementation consists of 26 sequentially executable Python scripts covering end-to-end data ingestion, model training, "
              "4-factor signal extraction, and review allocation. FR14 is implemented as a local Streamlit dashboard (Phase-1), with broader extensions reserved for Phase-2.",
              0.8 * inch, 1.45 * inch, 11.7 * inch, ParagraphStyle('ModD', parent=s_body, fontSize=12, leading=18))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 20: Implementation Demo: Signals & Shift Evidence
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Implementation & Empirical Evaluation", "Implementation Demo: Signal Extraction & Shift Evidence")
    draw_card(0.6 * inch, 0.4 * inch, 5.8 * inch, 5.8 * inch)
    draw_para("<font color='#1E40AF'><b>4 EXTRACTED RELIABILITY SIGNALS</b></font>", 0.8 * inch, PH - 1.35 * inch, 5.4 * inch, s_card_h)
    sig_html = (
        "• <b><font color='#0B192C'>1. Prediction Uncertainty (s_conf):</font></b><br/>"
        "Derived directly from XGBoost predict_proba output as (1 - max(P(y|x))). Ranks predictions near the decision boundary.<br/><br/>"
        "• <b><font color='#0B192C'>2. Mahalanobis OOD Distance (s_ood):</font></b><br/>"
        "Computed using regularized pseudo-inverse covariance (eps=1e-6) relative to 50K training flows, converted to percentile ranks.<br/><br/>"
        "• <b><font color='#0B192C'>3. Feature Drift Score (s_drift):</font></b><br/>"
        "Identifies features with PSI >= 0.10. Scores instances by absolute z-score deviation weighted by feature PSI.<br/><br/>"
        "• <b><font color='#0B192C'>4. Historical Error Proximity (s_hist):</font></b><br/>"
        "Projects validation instances into 10-decile error risk bins across 10 network flow attributes based on training-set mistake patterns."
    )
    draw_para(sig_html, 0.8 * inch, PH - 1.8 * inch, 5.4 * inch, ParagraphStyle('SigH', parent=s_body, fontSize=11, leading=15.5))

    draw_card(6.8 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    draw_para("<font color='#DC2626'><b>MEASURED DISTRIBUTION SHIFT EVIDENCE</b></font>", 7.0 * inch, PH - 1.35 * inch, 5.5 * inch, s_card_h)
    ev_html = (
        "• <b><font color='#1E40AF'>Error Surge (4.55x):</font></b><br/>"
        "Validation errors: exactly 753 (1.004%). Shifted test errors: exactly 3,427 (4.569%). Error count increases by exactly 4.551x.<br/><br/>"
        "• <b><font color='#1E40AF'>Attack Prevalence Surge (19.05x):</font></b><br/>"
        "True attacks increase from 248 (0.33%) in validation to 4,724 (6.30%) in the shifted test period.<br/><br/>"
        "• <b><font color='#1E40AF'>Feature Drift (PSI Measurement):</font></b><br/>"
        "Population Stability Index reveals severe drift across key flow metrics: SHORTEST_FLOW_PKT (PSI=0.766), MAX_IP_PKT_LEN (PSI=0.757), and IN_BYTES (PSI=0.604).<br/><br/>"
        "• <b><font color='#1E40AF'>Model Overconfidence:</font></b><br/>"
        "Average model confidence drops by only 1.83% (from 98.65% to 96.82%), indicating high-confidence errors under the shifted test distribution."
    )
    draw_para(ev_html, 7.0 * inch, PH - 1.8 * inch, 5.5 * inch, ParagraphStyle('EvH', parent=s_body, fontSize=11, leading=15.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 21: Empirical Results & Strategy Benchmark
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Implementation & Empirical Evaluation", "Empirical Results: Shifted-Test Strategy Benchmark")
    res_h = ["Budget", "Random Audit", "Pure Confidence", "OOD-Only Filter", "Static Multi-Factor", "Feedback Adaptive"]
    res_r = [
        [("1.0%", "(750)"), ("1.17%", "40 errs | 53.3/k"), ("13.51%", "463 errs | 617.3/k"), ("0.03%", "1 err | 1.3/k"), ("17.51%", "600 errs | 800.0/k"), ("17.80%", "610 errs | 813.3/k", True)],
        [("2.0%", "(1,500)"), ("2.13%", "73 errs | 48.7/k"), ("26.73%", "916 errs | 610.7/k"), ("0.26%", "9 errs | 6.0/k"), ("34.00%", "1,165 errs | 776.7/k"), ("34.26%", "1,174 errs | 782.7/k", True)],
        [("5.0%", "(3,750)"), ("5.52%", "189 errs | 50.4/k"), ("65.45%", "2,243 errs | 598.1/k", True), ("6.10%", "12 errs | 3.2/k"), ("54.57%", "1,870 errs | 498.7/k"), ("45.90%", "1,573 errs | 419.5/k")],
        [("10.0%", "(7,500)"), ("9.92%", "340 errs | 45.3/k"), ("84.01%", "2,879 errs | 383.9/k", True), ("6.10%", "12 errs | 1.6/k"), ("65.42%", "2,242 errs | 298.9/k"), ("52.35%", "1,794 errs | 239.2/k")]
    ]
    
    cx_r = [0.5*inch, 1.55*inch, 2.75*inch, 4.05*inch, 5.25*inch, 6.55*inch]
    w_r  = [1.05*inch, 1.20*inch, 1.30*inch, 1.20*inch, 1.30*inch, 1.30*inch]
    top_r = PH - 1.20 * inch
    hh_r = 0.44 * inch
    rh_r = 0.45 * inch
    
    for ci, (hdr, w) in enumerate(zip(res_h, w_r)):
        c.setFillColor(NAVY); c.rect(cx_r[ci], top_r - hh_r, w, hh_r, fill=1, stroke=0)
        p = Paragraph(f"<b><font color='white'>{hdr}</font></b>", ParagraphStyle(f'RH_{ci}', parent=s_body, fontSize=9.5, leading=12, alignment=1))
        p.wrapOn(c, w - 4, hh_r)
        p.drawOn(c, cx_r[ci] + 2, top_r - hh_r + 10)
        
    cur_yr = top_r - hh_r
    for ri, row in enumerate(res_r):
        bg = CARD_BG if ri % 2 == 0 else CARD_ALT
        for ci, (item, w) in enumerate(zip(row, w_r)):
            c.setFillColor(bg); c.rect(cx_r[ci], cur_yr - rh_r, w, rh_r, fill=1, stroke=0)
            c.setStrokeColor(BORDER); c.setLineWidth(0.3)
            c.rect(cx_r[ci], cur_yr - rh_r, w, rh_r, fill=0, stroke=1)
            
            is_win = len(item) == 3 and item[2]
            pct_col = '#1E40AF' if is_win else '#0B192C'
            sub_col = '#1E40AF' if is_win else '#64748B'
            
            val_html = f"<b><font color='{pct_col}' size=9.5>{item[0]}</font></b><br/><font color='{sub_col}' size=7.5>{item[1]}</font>"
            p = Paragraph(val_html, ParagraphStyle(f'RC_{ri}_{ci}', parent=s_body, leading=10, alignment=1))
            p.wrapOn(c, w - 4, rh_r)
            p.drawOn(c, cx_r[ci] + 2, cur_yr - rh_r + 8)
        cur_yr -= rh_r

    draw_img("v2_results_chart.png", 8.0 * inch, 4.05 * inch, 4.8 * inch, 2.25 * inch)
    
    draw_card(0.5 * inch, 0.35 * inch, 12.3 * inch, 3.45 * inch)
    draw_para("<b>CRITICAL SCIENTIFIC INSIGHTS & HONEST INTERPRETATION</b>", 0.7 * inch, 3.65 * inch, 11.9 * inch, s_card_h)
    ins_html = (
        "• <b><font color='#1E40AF'>Tight Budget Advantage (1%–2%):</font></b> Feedback Adaptive and Static Multi-Factor capture more errors than confidence alone (17.80% vs 13.51% at 1%; 34.26% vs 26.73% at 2%). Multi-factor triage is most beneficial under tight human review constraints.<br/><br/>"
        "• <b><font color='#1E40AF'>Broad Budget Crossover (5%–10%):</font></b> At higher review budgets, pure Confidence ranking catches up and captures more total errors (65.45% at 5%, 84.01% at 10%). Confidence targets broad decision-boundary ambiguity across the general distribution.<br/><br/>"
        "• <b><font color='#1E40AF'>OOD Standalone Failure (Honest Negative Result):</font></b> Mahalanobis OOD distance alone underperformed random audit across all budgets (0.03% vs 1.17% at 1%), indicating that OOD-only ranking was ineffective for error capture in this experiment.<br/><br/>"
        "• <b><font color='#1E40AF'>Core Defensible Finding:</font></b> Strategy effectiveness is budget-dependent. No single strategy dominates across all budgets, establishing that human-review allocation mechanisms must be selected to match operational review capacity."
    )
    draw_para(ins_html, 0.7 * inch, 3.30 * inch, 11.9 * inch, ParagraphStyle('InsH', parent=s_body, fontSize=11.5, leading=16))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 22: Limitations & Phase-2 Roadmap
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("Project Roadmap & Conclusion", "Limitations & Phase-2 Research Roadmap")
    draw_card(0.6 * inch, 0.4 * inch, 5.8 * inch, 5.8 * inch)
    draw_para("<font color='#DC2626'><b>IDENTIFIED RESEARCH LIMITATIONS</b></font>", 0.8 * inch, PH - 1.35 * inch, 5.4 * inch, s_card_h)
    lim_html = (
        "• <b><font color='#0B192C'>Simulated Review Oracle:</font></b><br/>"
        "Review evaluation uses test ground-truth labels rather than human subjects; real-world reviewer fatigue, latency, and human error are unmodeled.<br/><br/>"
        "• <b><font color='#0B192C'>Heuristic Signal Weighting:</font></b><br/>"
        "Weights are experimentally defined rather than formally learned through bilevel optimization or reinforcement learning.<br/><br/>"
        "• <b><font color='#0B192C'>Single-Dataset Benchmark:</font></b><br/>"
        "Current findings are evaluated exclusively on BigFlow-NIDS; cross-domain validity on healthcare and financial tabular data remains to be tested.<br/><br/>"
        "• <b><font color='#0B192C'>Historical Error Leakage Consideration:</font></b><br/>"
        "Historical error proximity currently uses training-set mistakes and would benefit from out-of-fold cross-validation estimates.<br/><br/>"
        "• <b><font color='#0B192C'>No Universal Dominance:</font></b><br/>"
        "Multi-factor allocation does not dominate confidence at large budgets (5%–10%)."
    )
    draw_para(lim_html, 0.8 * inch, PH - 1.8 * inch, 5.4 * inch, ParagraphStyle('LimH', parent=s_body, fontSize=11, leading=15.5))

    draw_card(6.8 * inch, 0.4 * inch, 5.9 * inch, 5.8 * inch)
    draw_para("<font color='#16A34A'><b>PHASE-2 RESEARCH ROADMAP</b></font>", 7.0 * inch, PH - 1.35 * inch, 5.5 * inch, s_card_h)
    p2_html = (
        "• <b><font color='#1E40AF'>Dataset-Agnostic Ingestion:</font></b><br/>"
        "Extend framework to automatically profile and process arbitrary tabular datasets across credit risk, fraud, and medical diagnosis.<br/><br/>"
        "• <b><font color='#1E40AF'>Post-Hoc Probability Calibration:</font></b><br/>"
        "Integrate temperature scaling and conformal prediction [4], [5] to provide distribution-free confidence guarantees.<br/><br/>"
        "• <b><font color='#1E40AF'>Instance-Level Explainability (SHAP):</font></b><br/>"
        "Generate feature attribution explanations for each routed prediction so human reviewers understand why an alert was escalated.<br/><br/>"
        "• <b><font color='#1E40AF'>Cost-Sensitive Optimization:</font></b><br/>"
        "Replace heuristic linear weights with learned optimal routing policies incorporating asymmetric financial penalty matrices.<br/><br/>"
        "• <b><font color='#1E40AF'>Interactive Demonstration UI (FR14):</font></b><br/>"
        "Extend the local Streamlit dashboard with broader budget controls, review-queue visualization, and multi-dataset support."
    )
    draw_para(p2_html, 7.0 * inch, PH - 1.8 * inch, 5.5 * inch, ParagraphStyle('P2H', parent=s_body, fontSize=11, leading=15.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 23: References: Primary Research Papers (2 Columns)
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("References & Documentation", "References: Primary Research Papers (IEEE Format)")
    draw_card(0.5 * inch, 0.4 * inch, 6.0 * inch, 5.8 * inch)
    draw_para("<b><font color='#0B192C'>PAPERS [1] – [5]</font></b>", 0.7 * inch, PH - 1.35 * inch, 5.6 * inch, s_card_h)
    
    r1_html = (
        "<b>[1]</b> T. Cao, J. Zhu, and G. Pang, \"Anomaly detection under distribution shift,\" in Proceedings of the IEEE/CVF International Conference on Computer Vision, 2023, pp. 6511-6523. DOI: 10.1109/ICCV51070.2023.00599.<br/><br/>"
        "<b>[2]</b> H. Mozannar and D. Sontag, \"Consistent estimators for learning to defer to an expert,\" in International Conference on Machine Learning, 2020, pp. 7076-7087. DOI: [TO CONFIRM].<br/><br/>"
        "<b>[3]</b> Z. Wei, T. Cao, and J. Feng, \"Exploiting human-AI dependence for learning to defer,\" in International Conference on Machine Learning, 2024. DOI: [TO CONFIRM].<br/><br/>"
        "<b>[4]</b> Y. Geifman and R. El-Yaniv, \"Selective classification for deep neural networks,\" in Advances in Neural Information Processing Systems, 2017. DOI: [TO CONFIRM].<br/><br/>"
        "<b>[5]</b> C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, \"On calibration of modern neural networks,\" in International Conference on Machine Learning, 2017, pp. 1321-1330. DOI: [TO CONFIRM]."
    )
    draw_para(r1_html, 0.7 * inch, PH - 1.8 * inch, 5.6 * inch, ParagraphStyle('R1H', parent=s_sm, fontSize=10, leading=14.5))

    draw_card(6.8 * inch, 0.4 * inch, 6.0 * inch, 5.8 * inch)
    draw_para("<b><font color='#0B192C'>PAPERS [6] – [10]</font></b>", 7.0 * inch, PH - 1.35 * inch, 5.6 * inch, s_card_h)
    
    r2_html = (
        "<b>[6]</b> Y. Kim, G. Dan, and J. Zhu, \"Human-in-the-loop cyber intrusion detection using active learning,\" IEEE Transactions on Information Forensics and Security, vol. 19, 2024. DOI: 10.1109/TIFS.2024.3361234.<br/><br/>"
        "<b>[7]</b> J. Liu, O. Gallego, and M. Barbieri, \"Incorporating uncertainty in learning to defer algorithms for safe computer-aided diagnosis,\" Scientific Reports, vol. 12, 2022. DOI: 10.1038/s41598-022-04873-1.<br/><br/>"
        "<b>[8]</b> J. Yang et al., \"Generalized out-of-distribution detection: A survey,\" International Journal of Computer Vision, 2024. DOI: 10.1007/s11263-024-02058-6.<br/><br/>"
        "<b>[9]</b> P. W. Koh et al., \"WILDS: A benchmark of in-the-wild distribution shifts,\" in International Conference on Machine Learning, 2021, pp. 5637-5664. DOI: [TO CONFIRM].<br/><br/>"
        "<b>[10]</b> K. He, Y. Kim, and S. Asghar, \"Adversarial machine learning for network intrusion detection systems: A comprehensive survey,\" IEEE Communications Surveys & Tutorials, vol. 25, no. 1, 2023. DOI: 10.1109/COMST.2022.3233793."
    )
    draw_para(r2_html, 7.0 * inch, PH - 1.8 * inch, 5.6 * inch, ParagraphStyle('R2H', parent=s_sm, fontSize=10, leading=14.5))
    c.showPage()

    # -------------------------------------------------------------
    # SLIDE 24: References: Textbooks, Datasets & Software
    # -------------------------------------------------------------
    slide_bg(); add_logo(); header("References & Documentation", "References: Textbooks, Datasets & Software Documentation")
    draw_card(0.5 * inch, 0.4 * inch, 12.3 * inch, 5.8 * inch)
    draw_para("<b>BENCHMARK DATASETS, REFERENCE TEXTBOOKS & SOFTWARE CITATIONS</b>", 0.7 * inch, PH - 1.35 * inch, 11.9 * inch, s_card_h)
    
    r_other_html = (
        "<b>[11]</b> M. Uddin and M. Arefin, \"BigFlow-NIDS: Large-Scale Benchmark Dataset,\" Data in Brief, 2026. DOI: 10.1016/j.dib.2026.112530."
    )
    draw_para(r_other_html, 0.7 * inch, PH - 1.8 * inch, 11.9 * inch, ParagraphStyle('ROther', parent=s_body, fontSize=11, leading=16))
    c.showPage()

    c.save()
    print(f"\n[OK] Saved 24-page PDF to: {target}")
    print(f"     File size: {os.path.getsize(target):,} bytes")

if __name__ == "__main__":
    build_pdf()
