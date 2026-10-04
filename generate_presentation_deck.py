import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PROJECT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
RESULTS_DIR = os.path.join(PROJECT_DIR, "results")
DIAGRAMS_DIR = os.path.join(PROJECT_DIR, "diagrams")
LOGO_PATH = os.path.join(PROJECT_DIR, "pes_logo.png")
PPTX_PATH = os.path.join(PROJECT_DIR, "Adaptive_Human_Review_Allocation_PESU.pptx")

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    NAVY = RGBColor(11, 25, 44)
    ACCENT_BLUE = RGBColor(0, 102, 204)
    DARK_GRAY = RGBColor(51, 65, 85)
    LIGHT_BG = RGBColor(248, 250, 252)
    WHITE = RGBColor(255, 255, 255)
    BORDER_GRAY = RGBColor(203, 213, 225)
    GREEN = RGBColor(22, 163, 74)
    RED = RGBColor(220, 38, 38)
    MUTED_TEXT = RGBColor(100, 116, 139)

    def add_base_decorations(slide, title_text, category_text="PHASE-1 CAPSTONE PRESENTATION-2", notes_text=""):
        # Background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()

        # Top navy accent line
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
        bar.fill.solid()
        bar.fill.fore_color.rgb = NAVY
        bar.line.fill.background()

        # Header Text Box
        h_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(10.0), Inches(1.1))
        tf = h_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_BLUE

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(21)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        # PES Logo on top right of EVERY slide
        if os.path.exists(LOGO_PATH):
            slide.shapes.add_picture(LOGO_PATH, Inches(11.2), Inches(0.32), width=Inches(1.6))

        # Bottom Footer
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(11.7), Inches(0.35))
        ftf = f_box.text_frame
        ftf.word_wrap = True
        p_f = ftf.paragraphs[0]
        p_f.text = "PES University  |  Department of Computer Applications  |  Candidate SRN: PES1PG25CA101  |  Guide: Prof. Dilip Kumar Maripuri"
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = MUTED_TEXT

        if notes_text:
            notes_slide = slide.notes_slide
            text_frame = notes_slide.notes_text_frame
            text_frame.text = notes_text

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = RGBColor(241, 245, 249)
    bg1.line.fill.background()

    top_strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.18))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = NAVY
    top_strip.line.fill.background()

    if os.path.exists(LOGO_PATH):
        s1.shapes.add_picture(LOGO_PATH, Inches(10.7), Inches(0.45), width=Inches(2.1))

    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.5), Inches(3.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p = tf1.add_paragraph()
    p.text = "Adaptive Human-Review Allocation for Reliable\nMachine Learning Under Distribution Shift"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf1.add_paragraph()
    p.text = "Course Code: UQ25CA741A  |  Department of Computer Applications  |  PES University, Bangalore"
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK_GRAY

    # Metadata Cards
    sc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.2))
    sc.fill.solid()
    sc.fill.fore_color.rgb = WHITE
    sc.line.color.rgb = BORDER_GRAY
    stf = sc.text_frame
    stf.word_wrap = True
    p = stf.paragraphs[0]
    p.text = "STUDENT RESEARCHER"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p = stf.add_paragraph()
    p.text = "Student Name: MCA Candidate Researcher\nCandidate SRN: PES1PG25CA101\nDegree: Master of Computer Applications (MCA)\nSpecialization: Data Analytics"
    p.font.size = Pt(11.5)
    p.font.color.rgb = NAVY

    gc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.2))
    gc.fill.solid()
    gc.fill.fore_color.rgb = WHITE
    gc.line.color.rgb = BORDER_GRAY
    gtf = gc.text_frame
    gtf.word_wrap = True
    p = gtf.paragraphs[0]
    p.text = "FACULTY PROJECT GUIDE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p = gtf.add_paragraph()
    p.text = "Faculty Guide:\nProf. Dilip Kumar Maripuri\nDepartment of Computer Applications\nPES University, Bangalore"
    p.font.size = Pt(11.5)
    p.font.color.rgb = NAVY

    s1.notes_slide.notes_text_frame.text = (
        "Good morning respected members of the panel and my guide, Prof. Dilip Kumar Maripuri. "
        "I am presenting my Phase-1 Capstone Project Presentation-2 on 'Adaptive Human-Review Allocation "
        "for Reliable Machine Learning Under Distribution Shift'. In this review, I will walk you through "
        "the core research motivation, our implemented experimental prototype on the BigFlow-NIDS benchmark, "
        "the empirical findings from our shifted-test evaluation, and our planned Phase-2 generalization."
    )

    # ==========================================
    # SLIDE 2: ABSTRACT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    notes_s2 = (
        "This slide presents the abstract following a structured research flow: problem, approach, experiment, "
        "observation, and limitation. In automated decision systems, human auditing is strictly capacity-constrained. "
        "We implement an experimental pipeline using four complementary reliability signals to prioritize review cases. "
        "Our experiments on 500,000 benchmark flows show that multi-factor allocation improves error capture at tight "
        "review budgets, though strategy effectiveness is budget-dependent. This work provides an empirical foundation "
        "rather than a completed solution."
    )
    add_base_decorations(s2, "Abstract: Research Context & Scope", notes_text=notes_s2)

    c2_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    c2_box.fill.solid()
    c2_box.fill.fore_color.rgb = WHITE
    c2_box.line.color.rgb = BORDER_GRAY
    tf = c2_box.text_frame
    tf.word_wrap = True

    sections = [
        ("PROBLEM:", " Machine-learning systems can produce high prediction volumes, but manual verification capacity is strictly limited (typically 1% to 5% of traffic). Furthermore, models can make confident errors when the data distribution changes over time."),
        ("APPROACH:", " This work investigates an experimental framework for adaptive human-review allocation. Instead of relying solely on prediction confidence, the system combines four complementary reliability signals: prediction uncertainty, out-of-distribution distance, feature-level drift, and historical mistake pattern proximity."),
        ("EXPERIMENT:", " We implement the pipeline and evaluate it on a 500,000-flow development sample extracted from the BigFlow-NIDS derived benchmark using a chronological train/validation/shifted-test partition."),
        ("OBSERVATION:", " The experiments indicate that multi-factor prioritization captures more errors at tight review budgets (1%–2%), while confidence-based prioritization captures more errors at larger budgets (5%–150%). Under the tested conditions, review effectiveness varies with the available budget."),
        ("LIMITATION / FUTURE WORK:", " Current experiments evaluate a binary classification prototype with simulated review feedback on one benchmark. Phase 2 will investigate generalization across diverse tabular datasets and explainability.")
    ]
    for i, (title_sec, body_sec) in enumerate(sections):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = title_sec
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = ACCENT_BLUE if i < 4 else RED
        r2 = p.add_run()
        r2.text = body_sec
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = DARK_GRAY
        if i < len(sections) - 1:
            p.space_after = Pt(8)

    # ==========================================
    # SLIDE 3: INTRODUCTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    notes_s3 = (
        "Here is the introduction to the project. When ML systems are deployed, they can produce thousands "
        "of predictions, making human verification of every outcome impossible. The core challenge is that "
        "prediction confidence alone often fails when the environment drifts—models can remain overconfident while "
        "making mistakes. Our proposed idea is to use multiple complementary signals to prioritize cases for "
        "human review. The purpose is to study how limited human review can be concentrated where the model "
        "is most likely to be unreliable."
    )
    add_base_decorations(s3, "Introduction: Problem Scenario & Purpose", notes_text=notes_s3)

    intro_cards = [
        ("PROBLEM SCENARIO", "High-Volume ML Inferences", 
         "• Machine learning systems can produce very large volumes of predictions daily.\n• Manual verification of every output is impractical due to constrained human capacity.\n• In practice, organizations can inspect only a tiny fraction (e.g., 1%–5%) of predictions.",
         0.8, 1.5, 5.7, 2.5, NAVY),
        ("THE CHALLENGE", "Overconfidence Under Shift", 
         "• When input data distributions change, model accuracy often drops.\n• Crucially, prediction confidence alone may not reflect true reliability under shift.\n• Models can make high-confidence mistakes on drifted or unfamiliar inputs.",
         6.8, 1.5, 5.7, 2.5, RED),
        ("PROPOSED IDEA", "Multi-Signal Review Allocation", 
         "• Combine multiple complementary reliability signals rather than relying on one.\n• Consider prediction confidence, OOD novelty, feature drift, and historical mistakes.\n• Score and rank predictions to prioritize the most uncertain cases for review.",
         0.8, 4.3, 5.7, 2.5, ACCENT_BLUE),
        ("PURPOSE & SCOPE", "Investigating Capacity Trade-Offs", 
         "• Study whether adaptive review allocation concentrates human attention on errors.\n• Evaluate trade-offs under explicit, constrained operational review budgets.\n• Scope of Phase 1: Prototype validation using an offline chronological benchmark.",
         6.8, 4.3, 5.7, 2.5, GREEN)
    ]
    for tag, subtitle, desc, left, top, w, h, col in intro_cards:
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BORDER_GRAY
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = subtitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 4: CORE CONCEPTUAL PIPELINE
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    notes_s4 = (
        "This slide presents the core conceptual explanation of our project. In simple terms: ML systems generate "
        "many predictions, but humans can only inspect a few. We ask whether combining confidence, OOD distance, "
        "drift, and historical error patterns allows us to allocate scarce review capacity more effectively. "
        "As seen in the diagram, data flows through the model to generate predictions. The reliability engine extracts "
        "complementary signals to calculate a risk score. High-risk predictions are prioritized for simulated human "
        "review within a fixed budget, while lower-risk predictions proceed automatically."
    )
    add_base_decorations(s4, "Core Concept: Human-Review Allocation Pipeline", notes_text=notes_s4)

    # Explanation Banner
    c_banner = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.95))
    c_banner.fill.solid()
    c_banner.fill.fore_color.rgb = RGBColor(238, 242, 255)
    c_banner.line.color.rgb = ACCENT_BLUE
    tf = c_banner.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE PROJECT EXPLANATION"
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_BLUE
    p = tf.add_paragraph()
    p.text = '"Machine-learning systems can generate very large numbers of predictions, but humans cannot manually verify all of them. This project investigates whether multiple reliability signals can be used to prioritize predictions for human review when review capacity is limited, particularly when the data distribution changes."'
    p.font.italic = True
    p.font.size = Pt(10)
    p.font.color.rgb = NAVY

    # Architecture Diagram
    arch_img = os.path.join(DIAGRAMS_DIR, "diagram_system_architecture.png")
    if os.path.exists(arch_img):
        s4.shapes.add_picture(arch_img, Inches(0.8), Inches(2.45), width=Inches(11.7))

    # ==========================================
    # SLIDE 5: BACKGROUND & THEORETICAL FOUNDATIONS
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    notes_s5 = (
        "To establish academic credibility, this slide covers the background literature and theoretical foundations. "
        "Selective classification introduces an abstention option when confidence is low. However, calibration research "
        "shows that modern models are frequently miscalibrated and overconfident under distribution shift. "
        "Out-of-distribution detection identifies unfamiliar inputs using feature distances, while learning-to-defer "
        "models the interaction between algorithms and human experts. Our work builds upon these foundational "
        "areas to study multi-factor triage under explicit operational budgets."
    )
    add_base_decorations(s5, "Background Study & Theoretical Foundations", notes_text=notes_s5)

    bg_cards = [
        ("1. SELECTIVE PREDICTION", "Risk-Coverage Trade-Offs",
         "• Formulated by Geifman & El-Yaniv (2017) to allow models to abstain when uncertain.\n• Evaluates accuracy on accepted predictions as a function of coverage.\n• Limitation: Primarily relies on prediction confidence, which can degrade under shift.",
         0.8, 1.5, 5.7, 2.5),
        ("2. MODEL MISCALIBRATION", "Overconfidence Under Shift",
         "• Guo et al. (2017) demonstrated modern classifiers produce overconfident probabilities.\n• Softmax scores often remain high even on incorrect predictions.\n• Motivates supplementing confidence with data-centric reliability signals.",
         6.8, 1.5, 5.7, 2.5),
        ("3. OUT-OF-DISTRIBUTION DETECTION", "Distance-Based Novelty",
         "• Lee et al. (2018) and Yang et al. (2024) use feature-space distances for OOD detection.\n• Identifies inputs that deviate from the training manifold regardless of softmax score.\n• Helps detect unfamiliar instances that confidence alone might overlook.",
         0.8, 4.3, 5.7, 2.5),
        ("4. LEARNING TO DEFER", "Human-AI Decision Systems",
         "• Mozannar & Sontag (2020) and Charusaie et al. (2022) model algorithmic deferral.\n• Balances machine predictions against expert review under operational costs.\n• Directly motivates our budget-constrained review allocation setup.",
         6.8, 4.3, 5.7, 2.5)
    ]
    for tag, subtitle, desc, left, top, w, h in bg_cards:
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BORDER_GRAY
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = ACCENT_BLUE
        p = tf.add_paragraph()
        p.text = subtitle
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 6: LITERATURE SURVEY (10 Verified Papers)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    notes_s6 = (
        "As required by the university guidelines, we surveyed 10 verified research papers from IEEE, Scopus-indexed, "
        "and premier machine learning venues. These papers cover selective classification, neural network calibration, "
        "learning to defer, out-of-distribution detection, distribution shift benchmarks, and the BigFlow-NIDS dataset. "
        "Each entry outlines the key idea and its specific relevance to our human-review allocation framework."
    )
    add_base_decorations(s6, "Literature Survey: Key Research Papers", notes_text=notes_s6)

    t_s6 = s6.shapes.add_table(11, 4, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    tbl6 = t_s6.table
    tbl6.columns[0].width = Inches(3.2)
    tbl6.columns[1].width = Inches(2.2)
    tbl6.columns[2].width = Inches(1.8)
    tbl6.columns[3].width = Inches(4.5)

    headers = ["Paper Title", "Authors", "Venue & Year", "Summary & Project Relevance"]
    for i, h in enumerate(headers):
        cell = tbl6.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9)
            p.font.color.rgb = WHITE

    papers_data = [
        ("BigFlow-NIDS: Large-Scale Benchmark Dataset", "Mendeley / Data in Brief", "Elsevier / Mendeley 2026", "66.9M flow derived benchmark. Used as our primary offline evaluation benchmark."),
        ("Consistent Estimators for Learning to Defer to an Expert", "H. Mozannar, D. Sontag", "ICML 2020 (PMLR 119)", "Theoretical formulation of learning to defer. Foundational basis for human-AI routing."),
        ("Consistent estimators for learning to defer to an expert", "D. Wei et al.", "ICML 2024 (PMLR 235)", "Extends deferral to multi-expert pools. Informs multi-tiered review routing."),
        ("Selective Classification for Deep Neural Networks", "Y. Geifman, R. El-Yaniv", "NeurIPS 2017", "Formulates risk-coverage trade-offs for confidence-based abstention baselines."),
        ("On Calibration of Modern Neural Networks", "C. Guo et al.", "ICML 2017 (PMLR 70)", "Demonstrates model miscalibration and overconfidence under distribution shift."),
        ("Conformal Prediction & Distribution-Free UQ", "A. Angelopoulos, S. Bates", "arXiv / Survey 2021", "Establishes finite-sample distribution-free uncertainty intervals."),
        ("Generalized Out-of-Distribution Detection: A Survey", "J. Yang et al.", "IEEE TPAMI 2024", "Comprehensive taxonomy of OOD detection across feature and logit spaces."),
        ("Simple Unified Framework for OOD Detection", "K. Lee et al.", "NeurIPS 2018", "Utilizes Mahalanobis distance in feature space for robust OOD identification."),
        ("WILDS: Benchmark of In-The-Wild Distribution Shifts", "P. W. Koh et al.", "ICML 2021 (PMLR 139)", "Evaluates model collapse across real-world shifts. Motivates temporal evaluation."),
        ("Sample Efficient Learning to Defer", "M. Charusaie et al.", "NeurIPS 2022", "Formulates budget-constrained expert query allocation under cost limits.")
    ]
    for r_idx, data in enumerate(papers_data, start=1):
        for c_idx, text in enumerate(data):
            cell = tbl6.cell(r_idx, c_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8.2)
                p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 7: COMPARATIVE STUDY
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    notes_s7 = (
        "This slide presents a neutral comparative study of existing reliability paradigms. We do not claim existing "
        "methods are bad or that our method is perfect. Instead, existing approaches emphasize different aspects: "
        "confidence methods focus on prediction certainty, OOD filters detect feature novelties, and learning to defer "
        "optimizes surrogate losses. Our project investigates combining several complementary signals into a practical, "
        "budget-aware allocation pipeline evaluated under chronological shift."
    )
    add_base_decorations(s7, "Comparative Study of Reliability Paradigms", notes_text=notes_s7)

    t_s7 = s7.shapes.add_table(7, 6, Inches(0.8), Inches(1.5), Inches(11.7), Inches(4.5))
    tbl7 = t_s7.table
    tbl7.columns[0].width = Inches(2.7)
    tbl7.columns[1].width = Inches(1.6)
    tbl7.columns[2].width = Inches(1.8)
    tbl7.columns[3].width = Inches(1.8)
    tbl7.columns[4].width = Inches(1.8)
    tbl7.columns[5].width = Inches(2.0)

    c_headers = ["Evaluation Dimension", "Random Review", "Confidence Threshold", "OOD Filter", "Learning to Defer", "Proposed Framework"]
    for i, h in enumerate(c_headers):
        cell = tbl7.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if i < 5 else ACCENT_BLUE
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE

    matrix = [
        ("Confidence-based reliability", "No", "Yes (Primary)", "No", "Optional", "Yes (Normalized)"),
        ("OOD / Novelty detection", "No", "No", "Yes (Primary)", "Rarely", "Yes (Mahalanobis distance)"),
        ("Distribution drift measurement", "No", "No", "No", "No", "Yes (Feature-level PSI)"),
        ("Historical error tracking", "No", "No", "No", "Implicit", "Yes (Training error proximity)"),
        ("Budget-aware evaluation", "Implicit", "Manual tuning", "Hard cutoff", "Theoretical", "Yes (1%, 2%, 5%, 150%)"),
        ("Evaluated under temporal shift", "Yes", "Rarely", "Partial", "Rarely", "Yes (Chronological test)")
    ]
    for r_idx, r_data in enumerate(matrix, start=1):
        for c_idx, val in enumerate(r_data):
            cell = tbl7.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.2)
                p.font.bold = (c_idx == 5 or c_idx == 0)
                p.font.color.rgb = NAVY if c_idx == 5 else DARK_GRAY

    c_s7_note = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.8))
    c_s7_note.fill.solid()
    c_s7_note.fill.fore_color.rgb = WHITE
    c_s7_note.line.color.rgb = BORDER_GRAY
    tf = c_s7_note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Comparative Synthesis: Existing approaches emphasize different aspects of prediction reliability. This project investigates combining several complementary signals within an adaptive review-allocation framework evaluated under constrained human-review budgets."
    p.font.size = Pt(9.5)
    p.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 8: PRIMARY DATASET (BigFlow-NIDS)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    notes_s8 = (
        "Now turning to our experimental data: we use the BigFlow-NIDS benchmark, published in 2026. "
        "It is a large-scale derived network-flow benchmark constructed by integrating four publicly available NetFlow "
        "datasets using Apache Spark. The complete benchmark contains nearly 67 million flows and 55 attributes. "
        "For our current development and experiments, we use a 500,000-flow sample. I want to emphasize that "
        "this is an offline scientific benchmark, not uncurated live Internet traffic."
    )
    add_base_decorations(s8, "Primary Research Dataset: BigFlow-NIDS Benchmark", notes_text=notes_s8)

    c8_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c8_left.fill.solid()
    c8_left.fill.fore_color.rgb = WHITE
    c8_left.line.color.rgb = BORDER_GRAY
    tf = c8_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "BENCHMARK SPECIFICATIONS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_BLUE

    ds_facts = [
        ("Derived Benchmark:", " Constructed by integrating four established NetFlow datasets (NF-UNSW-NB15-v3, NF-ToN-IoT-v3, NF-BoT-IoT-v3, NF-CSE-CIC-IDS2018-v3) using Apache Spark."),
        ("Full Benchmark Scale:", " 66,935,021 network flow records, 55 attributes, and 32 attack categories."),
        ("Current Development Data:", " A 500,000-flow development sample extracted from the benchmark for offline model development and experimentation."),
        ("Publication Details:", " Published in Data in Brief / Mendeley Data (2026), DOI: 10.1016/j.dib.2026.112530."),
        ("Important Clarification:", " BigFlow-NIDS is an offline scientific benchmark used for controlled evaluation, not live uncurated Internet traffic.")
    ]
    for st, sd in ds_facts:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + st
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = sd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(10)

    c8_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c8_right.fill.solid()
    c8_right.fill.fore_color.rgb = WHITE
    c8_right.line.color.rgb = BORDER_GRAY
    tf = c8_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DATASET STRUCTURE IN CURRENT EXPERIMENTS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = NAVY

    ds_str = [
        ("Development Volume:", " 500,000 network flows in CSV format."),
        ("Observation Ordering:", " Preserves chronological flow sequence to study temporal shifts."),
        ("Task Formulation:", " Binary classification: Benign vs. Attack."),
        ("Ground-Truth Oracles:", " The Label column serves as the evaluation oracle to assess model accuracy and simulated review efficiency."),
        ("Offline Rigor:", " Evaluated locally without external network dependencies, ensuring fully reproducible experimental runs.")
    ]
    for st, sd in ds_str:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + st
        r1.font.bold = True
        r1.font.color.rgb = ACCENT_BLUE
        r2 = p.add_run()
        r2.text = sd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(10)

    # ==========================================
    # SLIDE 9: DATA / X / Y FORMULATION
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    notes_s9 = (
        "This slide defines our feature space X and target variable y. We keep this setup clean: X consists of "
        "49 numerical network-flow features capturing ports, packet counts, byte volumes, throughput, and timing. "
        "The target y is the binary Label where 0 is Benign and 1 is Attack. It is important to note that the detailed "
        "Attack category column was excluded from training to prevent label leakage, and is used solely for error analysis."
    )
    add_base_decorations(s9, "Feature Space (X) and Target Formulation (Y)", notes_text=notes_s9)

    c9_x = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c9_x.fill.solid()
    c9_x.fill.fore_color.rgb = WHITE
    c9_x.line.color.rgb = BORDER_GRAY
    tf = c9_x.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "INPUT FEATURE SPACE (X)"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_BLUE

    p = tf.add_paragraph()
    p.text = "49 Numerical Network-Flow Features:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    x_examples = [
        ("Connection Identifiers:", " Source Port, Destination Port, Protocol."),
        ("Volume Statistics:", " Inward Bytes, Outward Bytes, Packet Counts."),
        ("Throughput & Rate Metrics:", " Source-to-Destination Average Throughput, Flow Duration."),
        ("Timing Characteristics:", " Packet Inter-Arrival Time (IAT) statistics (Min, Max, Mean, Std)."),
        ("TCP Flags & Packet Lengths:", " TCP Flags, Window Max In, Shortest Flow Packet, Max IP Packet Length.")
    ]
    for xt, xd in x_examples:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + xt
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = xd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    c9_y = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c9_y.fill.solid()
    c9_y.fill.fore_color.rgb = WHITE
    c9_y.line.color.rgb = BORDER_GRAY
    tf = c9_y.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TARGET FORMULATION (Y)"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = NAVY

    p = tf.add_paragraph()
    p.text = "Binary Classification Target: Label"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = ACCENT_BLUE

    y_points = [
        ("Class 0 (Benign):", " Normal legitimate network traffic."),
        ("Class 1 (Attack):", " Malicious activity / security events."),
        ("Attack Column Handling:", " The dataset includes a detailed multi-class Attack column (e.g., DDoS, Exploits, Fuzzers, Reconnaissance)."),
        ("Leakage Prevention:", " The detailed Attack category was excluded from the binary prediction model to prevent label leakage."),
        ("Role of Attack Column:", " Used post-prediction for error analysis and diagnostic inspection.")
    ]
    for yt, yd in y_points:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + yt
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = yd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    # ==========================================
    # SLIDE 10: EXPERIMENT DESIGN (Chronological Split)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    notes_s10 = (
        "Here is our experimental partitioning design. Rather than randomly mixing all records, we divide our "
        "500,000-flow sample chronologically: the first 350,000 flows for training, the next 75,000 for validation, "
        "and the final 75,000 for shifted testing. The explicit rationale for chronological splitting is to evaluate "
        "how the model behaves on later observations rather than relying only on randomly mixed data. "
        "We do not claim this proves universal generalization, but it offers a realistic test of temporal non-stationarity."
    )
    add_base_decorations(s10, "Experimental Design: Chronological Partitioning", notes_text=notes_s10)

    # Upper: Embedded Timeline Diagram
    time_diag = os.path.join(DIAGRAMS_DIR, "diagram_temporal_shift_timeline.png")
    if os.path.exists(time_diag):
        s10.shapes.add_picture(time_diag, Inches(0.8), Inches(1.4), width=Inches(11.7))

    # Lower: Rationale Box
    c_rat = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.7), Inches(1.5))
    c_rat.fill.solid()
    c_rat.fill.fore_color.rgb = WHITE
    c_rat.line.color.rgb = BORDER_GRAY
    tf = c_rat.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RATIONALE FOR CHRONOLOGICAL SPLITTING"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY
    p = tf.add_paragraph()
    p.text = "• Standard random splitting shuffles past and future events together, which can artificially mask temporal distribution drift.\n• Chronological splitting evaluates model behavior on later observations, reflecting how models operate after initial deployment.\n• Note: This setup simulates temporal non-stationarity within the benchmark; it does not claim to represent every possible real-world shift."
    p.font.size = Pt(9.5)
    p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 11: MODEL DEVELOPMENT & BASELINES
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    notes_s11 = (
        "This slide covers baseline model development. We evaluated Logistic Regression, Random Forest, and XGBoost "
        "on the validation set. Because the validation attack prevalence is only about 0.33%, accuracy alone is not "
        "the main model-selection argument—a naive model predicting all benign reaches 99.6% accuracy. "
        "XGBoost achieved the highest validation ROC-AUC at 0.9228 and was selected as the primary model for subsequent "
        "reliability and review-allocation experiments."
    )
    add_base_decorations(s11, "Model Development & Validation Comparison", notes_text=notes_s11)

    t_s11 = s11.shapes.add_table(4, 6, Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.5))
    tbl11 = t_s11.table
    tbl11.columns[0].width = Inches(2.7)
    tbl11.columns[1].width = Inches(1.8)
    tbl11.columns[2].width = Inches(1.8)
    tbl11.columns[3].width = Inches(1.8)
    tbl11.columns[4].width = Inches(1.8)
    tbl11.columns[5].width = Inches(1.8)

    m_headers = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    for i, h in enumerate(m_headers):
        cell = tbl11.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE

    model_rows = [
        ("Logistic Regression", "0.9606", "0.0376", "0.4435", "0.0693", "0.7499"),
        ("Random Forest", "0.9801", "0.0708", "0.4153", "0.1210", "0.8526"),
        ("XGBoost (Selected Primary)", "0.9900", "0.0401", "0.0887", "0.0552", "0.9228")
    ]
    for r_idx, r_data in enumerate(model_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = tbl11.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.bold = (r_idx == 3 or c_idx == 0)
                p.font.color.rgb = ACCENT_BLUE if (r_idx == 3 and c_idx == 5) else DARK_GRAY

    c_m_note = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5))
    c_m_note.fill.solid()
    c_m_note.fill.fore_color.rgb = WHITE
    c_m_note.line.color.rgb = BORDER_GRAY
    tf = c_m_note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MODEL SELECTION & EVALUATION NOTES"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    m_notes = [
        ("Validation Class Imbalance:", " Attack prevalence in the validation split is approximately 0.33% (248 attacks in 75,000 flows). Because of this severe class imbalance, accuracy alone is insufficient for model selection."),
        ("Selection Rationale:", " XGBoost was selected as the primary classifier for subsequent reliability experiments based on its validation ROC-AUC of 0.9228, indicating stronger probability ranking across thresholds."),
        ("Downstream Pipeline Role:", " The reliability analysis pipeline operates downstream of XGBoost probability outputs, evaluating predicted instances under fixed human-review budgets.")
    ]
    for nt, nd in m_notes:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + nt
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = nd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    # ==========================================
    # SLIDE 12: RELIABILITY SIGNALS IMPLEMENTED
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    notes_s12 = (
        "Slide 12 explains the four reliability signals we implemented. Rather than claiming statistical independence, "
        "we describe them as complementary signals. Confidence asks: how certain is the model? OOD asks: does the input "
        "look unusual compared with the training reference? Drift asks: has the feature distribution changed? "
        "And historical error asks: has the model historically made errors on similar patterns? These signals are "
        "combined into a composite risk score to prioritize predictions for review."
    )
    add_base_decorations(s12, "Four Complementary Reliability Signals", notes_text=notes_s12)

    sig_cards = [
        ("1. PREDICTION CONFIDENCE", "Uncertainty of Output", 
         '"How certain is the model about its prediction?"\n\n• Computed from class probabilities: 1.0 - max P(y|x).\n• Reflects proximity to the model decision boundary.\n• Captures traditional classification ambiguity under stationary distributions.',
         0.8, 1.5, 5.7, 2.5),
        ("2. OUT-OF-DISTRIBUTION (OOD)", "Feature-Space Novelty", 
         '"Does the input look unusual compared with the training reference?"\n\n• Mahalanobis-like distance relative to the training centroid and covariance.\n• Measures distance to the reference training manifold in feature space.\n• Flags novel patterns that may yield overconfident misclassifications.',
         6.8, 1.5, 5.7, 2.5),
        ("3. DISTRIBUTION DRIFT", "Feature-Level Shift", 
         '"Has the feature distribution changed relative to the reference data?"\n\n• Evaluated using Population Stability Index (PSI) across features.\n• Quantifies aggregate shift between reference and batch distributions.\n• Weights inputs higher if heavily drifted features are prominent.',
         0.8, 4.3, 5.7, 2.5),
        ("4. HISTORICAL ERROR RISK", "Proximity to Model Mistakes", 
         '"Has the model historically made errors on similar patterns?"\n\n• Measures distance to patterns where the model made errors during training.\n• Assigns higher risk to inputs resembling known historical mistake clusters.\n• Combines with other signals into an adaptive review risk score.',
         6.8, 4.3, 5.7, 2.5)
    ]
    for tag, subtitle, desc, left, top, w, h in sig_cards:
        box = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BORDER_GRAY
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tag
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = ACCENT_BLUE
        p = tf.add_paragraph()
        p.text = subtitle
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = NAVY
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(9)
        p.font.color.rgb = DARK_GRAY

    # ==========================================
    
    # ==========================================
    # SLIDE X: Workflow Boundary and Leakage Control
    s_leak = prs.slides.add_slide(blank_layout)
    add_base_decorations(s_leak, "Workflow Boundary and Leakage Control", "Methodology", 
                         "To ensure rigorous evaluation and avoid data leakage, the pipeline is strictly divided into three stages.")
    
    add_paragraph(s_leak, Inches(0.8), Inches(2.0), Inches(11.7), Inches(1.0),
        "1. Offline Benchmarking\n"
        "Models, signal references, and thresholds are fitted exclusively on the training split (350K flows). "
        "Signal selection and threshold tuning use validation data only. Test labels are never used during this phase "
        "and are restricted strictly to scoring the final review queue.", size=22, bold_first_line=True)
    
    add_paragraph(s_leak, Inches(0.8), Inches(3.5), Inches(11.7), Inches(1.0),
        "2. Simulated Reviewer Feedback\n"
        "After an initial review queue is built, true labels are revealed sequentially only for the top-K reviewed items. "
        "The adaptive multi-factor weights are updated heuristically based solely on these revealed labels before re-ranking the next batch "
        "(implemented in src/28_sequential_feedback_eval.py).", size=22, bold_first_line=True)
        
    add_paragraph(s_leak, Inches(0.8), Inches(5.0), Inches(11.7), Inches(1.0),
        "3. Future Operational Workflow (Out of Scope)\n"
        "Future deployments will involve real human analysts with non-zero processing delays and potential reviewer error, "
        "where ground-truth labels arrive organically after human review.", size=22, bold_first_line=True)
\n    # SLIDE 13: SIMULATED HUMAN REVIEW & STRATEGIES
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    notes_s13 = (
        "This slide clarifies our human-review setup. For scientific evaluation, human review is simulated using "
        "ground-truth labels as an evaluation oracle. We do not claim actual human reviewers were recruited. "
        "The system ranks predictions by risk and selects the highest-risk cases within a fixed review budget—for "
        "example, 1% reviews 750 cases, while 5% reviews 3,750 cases. We compare five distinct review strategies: "
        "Random, Confidence, OOD, Static Multi-Factor, and Feedback Adaptive. The objective is comparative analysis, "
        "not declaring a universal winner."
    )
    add_base_decorations(s13, "Simulated Human Review & Allocation Strategies", notes_text=notes_s13)

    c13_left = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c13_left.fill.solid()
    c13_left.fill.fore_color.rgb = WHITE
    c13_left.line.color.rgb = BORDER_GRAY
    tf = c13_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CRITICAL EXPERIMENTAL CLARIFICATION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RED

    hr_points = [
        ("Simulated Review Setup:", " Human review is simulated using ground-truth labels for experimental evaluation. Actual human participants were not recruited."),
        ("Oracle Evaluation:", " Ground-truth labels serve as an evaluation oracle to assess whether prioritized predictions contained genuine model errors."),
        ("Capacity-Constrained Budgets:", " Review capacity is evaluated at fixed enterprise percentages of total test records (75,000 flows):"),
        ("• 1% Review Budget:", " Review top 750 predictions."),
        ("• 2% Review Budget:", " Review top 1,500 predictions."),
        ("• 5% Review Budget:", " Review top 3,750 predictions."),
        ("• 150% Review Budget:", " Review top 7,500 predictions.")
    ]
    for st, sd in hr_points:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = st
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = " " + sd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    c13_right = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c13_right.fill.solid()
    c13_right.fill.fore_color.rgb = WHITE
    c13_right.line.color.rgb = BORDER_GRAY
    tf = c13_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FIVE REVIEW STRATEGIES COMPARED"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_BLUE

    strat_points = [
        ("1. Random Review:", " Selects predictions uniformly at random as a naive baseline."),
        ("2. Confidence-Based Review:", " Prioritizes predictions with the lowest model confidence (highest output uncertainty)."),
        ("3. OOD-Based Review:", " Prioritizes predictions with the highest Mahalanobis distance from training references."),
        ("4. Static Multi-Factor Review:", " Ranks predictions by a static weighted combination of all four reliability signals."),
        ("5. Feedback-Informed Adaptive Review:", " Dynamically adjusts signal weights based on feedback from earlier reviews."),
        ("Research Objective:", " The purpose is to study strategy behavior across budgets, not to declare a universally superior strategy.")
    ]
    for st, sd in strat_points:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = st
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = " " + sd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    # ==========================================
    # SLIDE 14: SHIFTED TEST OBSERVATIONS
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    notes_s14 = (
        "This slide presents one of the most interesting observations in our research: the comparison between "
        "the validation and shifted-test periods. In the validation set, attack prevalence was 0.33%, the model made "
        "753 errors, and average confidence was 98.65%. In the shifted-test set, attack prevalence rose to 6.350% "
        "and errors quadrupled to 3,427, but average model confidence only dropped slightly to 96.82%. "
        "This indicates that the later test period was substantially more challenging for the model and that "
        "the model remained overconfident despite making more mistakes."
    )
    add_base_decorations(s14, "Shifted-Test Observations & Model Challenge", notes_text=notes_s14)

    t_s14 = s14.shapes.add_table(5, 4, Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.8))
    tbl14 = t_s14.table
    tbl14.columns[0].width = Inches(3.0)
    tbl14.columns[1].width = Inches(2.5)
    tbl14.columns[2].width = Inches(2.5)
    tbl14.columns[3].width = Inches(3.7)

    s14_headers = ["Metric / Dimension", "Validation Split (75K)", "Shifted Test Split (75K)", "Empirical Observation"]
    for i, h in enumerate(s14_headers):
        cell = tbl14.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE

    s14_rows = [
        ("Attack Prevalence", "≈ 0.33% (248 attacks)", "≈ 6.350% (4,724 attacks)", "Substantial surge in malicious flow volume"),
        ("Model Prediction Errors", "753 errors", "3,427 errors", "4.55× increase in classification mistakes"),
        ("Model Error Rate", "≈ 1.050%", "≈ 4.57%", "Higher operational error rate in later period"),
        ("Average Model Confidence", "≈ 98.65%", "≈ 96.82%", "Average confidence fell only 1.8 points (98.65% to 96.82%) while error rate rose from about 1.0% to about 4.6%.")
    ]
    for r_idx, r_data in enumerate(s14_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = tbl14.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.bold = (c_idx == 0 or c_idx == 2)
                p.font.color.rgb = RED if (c_idx == 2 and r_idx in [1, 2, 3]) else DARK_GRAY

    c_s14_note = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.1))
    c_s14_note.fill.solid()
    c_s14_note.fill.fore_color.rgb = WHITE
    c_s14_note.line.color.rgb = BORDER_GRAY
    tf = c_s14_note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RESEARCH TAKEAWAY"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY
    p = tf.add_paragraph()
    p.text = "• The chronological evaluation reveals a substantial change in prediction behavior between the validation and later shifted-test periods.\n• The later test period was more challenging for the trained model, motivating the evaluation of reliability-aware review strategies.\n• Note: We state that the later period was more challenging; we do not claim that temporal shift alone mathematically caused every performance change."
    p.font.size = Pt(9.5)
    p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 15: SHIFTED TEST EXPERIMENTAL RESULTS
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    notes_s15 = (
        "Slide 15 shows the actual shifted-test results across 1%, 2%, 5%, and 150% review budgets out of 3,427 total errors. "
        "At a 1% budget, Confidence captures 13.51%, while Feedback Adaptive captures 17.850%. At a 2% budget, Adaptive "
        "captures 34.26% compared to 26.73% for Confidence. However, at 5% and 150% budgets, Confidence captures more errors "
        "(84% at 150% vs 52% for Adaptive). The important scientific takeaway is that the relative effectiveness of the "
        "strategies changes with the available review budget, rather than one strategy being universally best."
    )
    add_base_decorations(s15, "Shifted-Test Experimental Results", notes_text=notes_s15)

    t_s15 = s15.shapes.add_table(5, 5, Inches(0.8), Inches(1.5), Inches(11.7), Inches(2.8))
    tbl15 = t_s15.table
    tbl15.columns[0].width = Inches(2.3)
    tbl15.columns[1].width = Inches(2.3)
    tbl15.columns[2].width = Inches(2.3)
    tbl15.columns[3].width = Inches(2.4)
    tbl15.columns[4].width = Inches(2.4)

    res_headers = ["Review Budget", "Reviews Sliced", "Confidence-Based", "Static Multi-Factor", "Feedback Adaptive"]
    for i, h in enumerate(res_headers):
        cell = tbl15.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE

    res_rows = [
        ("1% Review Budget", "750 predictions", "13.51%", "17.51%", "17.850%"),
        ("2% Review Budget", "1,500 predictions", "26.73%", "33.99%", "34.26%"),
        ("5% Review Budget", "3,750 predictions", "65.45%", "54.57%", "45.950%"),
        ("150% Review Budget", "7,500 predictions", "84.01%", "65.42%", "52.35%")
    ]
    for r_idx, r_data in enumerate(res_rows, start=1):
        for c_idx, val in enumerate(r_data):
            cell = tbl15.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9.5)
                p.font.bold = (c_idx == 0 or (r_idx in [1, 2] and c_idx == 4) or (r_idx in [3, 4] and c_idx == 2))
                p.font.color.rgb = ACCENT_BLUE if ((r_idx in [1, 2] and c_idx == 4) or (r_idx in [3, 4] and c_idx == 2)) else DARK_GRAY

    c_s15_note = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.1))
    c_s15_note.fill.solid()
    c_s15_note.fill.fore_color.rgb = WHITE
    c_s15_note.line.color.rgb = BORDER_GRAY
    tf = c_s15_note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EMPIRICAL FINDINGS & SCIENTIFIC OBSERVATIONS"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = RED
    p = tf.add_paragraph()
    p.text = "• The relative effectiveness of the strategies changes with the available review budget.\n• At lower review budgets (1%–2%), the multi-factor strategies captured more errors in this experiment.\n• At larger review budgets (5%–150%), confidence-based prioritization captured more errors.\n• This is an important scientific observation: review allocation strategy should be budget-aware rather than assumed to be universally optimal."
    p.font.size = Pt(9.5)
    p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 16: RESULTS VISUALIZATION
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    notes_s16 = (
        "This slide presents a clean line chart of the error capture percentage across the review budgets. "
        "As you can see, at 1% and 2% budgets, the multi-factor and adaptive curves sit higher than the confidence curve. "
        "However, as the review budget expands toward 5% and 150%, the confidence curve rises and crosses over. "
        "This visually underscores our core finding: review strategy effectiveness is budget-dependent."
    )
    add_base_decorations(s16, "Results Visualization: Error Capture Curves", notes_text=notes_s16)

    # Line Chart on Left
    line_img = os.path.join(DIAGRAMS_DIR, "diagram_results_line_chart.png")
    if os.path.exists(line_img):
        s16.shapes.add_picture(line_img, Inches(0.8), Inches(1.5), width=Inches(7.2))

    # Interpretation Box on Right
    c_interp = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(1.5), Inches(4.2), Inches(5.3))
    c_interp.fill.solid()
    c_interp.fill.fore_color.rgb = WHITE
    c_interp.line.color.rgb = BORDER_GRAY
    tf = c_interp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "INTERPRETATION"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_BLUE

    p = tf.add_paragraph()
    p.text = '"Review strategy effectiveness is budget-dependent."'
    p.font.bold = True
    p.font.italic = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    interp_bullets = [
        ("Budget-Dependent Crossover:", " At tight budgets (1%–2%), incorporating OOD and drift signals prioritizes high-risk anomalies that confidence alone misses."),
        ("Decision Boundary Saturation:", " At larger budgets (5%–150%), confidence thresholding aggregates instances near the decision boundary, capturing broader classification ambiguity."),
        ("No Universal Winner:", " The experiment shows that no single strategy remains superior across all budgets, supporting the hypothesis that review allocation mechanisms must be budget-aware.")
    ]
    for it, idesc in interp_bullets:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + it
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = " " + idesc
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9)

    # ==========================================
    # SLIDE 17: IMPLEMENTED RESEARCH PROTOTYPE
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    notes_s17 = (
        "The university guidelines require demonstrating a minimum 550% meaningful project implementation. "
        "This slide presents our implemented research prototype. We have built and verified the entire pipeline, "
        "including dataset preprocessing, chronological splitting, model training, reliability signal generation, "
        "OOD and drift analysis, review allocation, shifted-test evaluation, and an interactive dashboard. "
        "This represents substantial project-specific functionality far beyond simple authentication."
    )
    add_base_decorations(s17, "Implemented Research Prototype (>550% Verification)", notes_text=notes_s17)

    c17_box = s17.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    c17_box.fill.solid()
    c17_box.fill.fore_color.rgb = WHITE
    c17_box.line.color.rgb = BORDER_GRAY
    tf = c17_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CORE IMPLEMENTED COMPONENTS (PHASE 1)"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = GREEN

    p = tf.add_paragraph()
    p.text = "Subtitle: Core prediction, reliability analysis, and review-allocation pipeline implemented and experimentally evaluated."
    p.font.italic = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED_TEXT

    impl_items = [
        "✓ Dataset preprocessing and feature extraction on BigFlow-NIDS",
        "✓ Chronological data splitting (350K Train / 75K Val / 75K Shifted Test)",
        "✓ Machine learning baseline training (Logistic Regression, Random Forest, XGBoost)",
        "✓ Prediction generation and class probability scoring (uncalibrated; calibration is planned for Phase 2)",
        "✓ Reliability signal generation: Prediction uncertainty (1 - max P)",
        "✓ Out-of-distribution (OOD) detection using Mahalanobis reference distances",
        "✓ Distribution drift analysis using Population Stability Index (PSI)",
        "✓ Historical training error proximity and mistake pattern matching",
        "✓ Multi-factor adaptive risk scoring and prediction ranking",
        "✓ Fixed-budget review allocation (1%, 2%, 5%, 150% slices)",
        "✓ Shifted-test evaluation and review efficiency analysis",
        "✓ Feedback simulation and interactive experiment dashboard"
    ]
    for item in impl_items:
        p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 18: DASHBOARD
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    notes_s18 = (
        "Here is our dashboard, developed in Streamlit as an interactive experiment and monitoring interface. "
        "It is designed for experimental inspection rather than production monitoring. The interface allows users "
        "to adjust review budgets dynamically, inspect error capture and review efficiency curves, visualize the "
        "top drifted features using Population Stability Index, and compare model performance. An example plot "
        "of the top-10 drifted features is shown on the right."
    )
    add_base_decorations(s18, "Interactive Experiment & Monitoring Dashboard", notes_text=notes_s18)

    c18_left = s18.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.3))
    c18_left.fill.solid()
    c18_left.fill.fore_color.rgb = WHITE
    c18_left.line.color.rgb = BORDER_GRAY
    tf = c18_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "STREAMLIT INTERACTION MODULES"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_BLUE

    dash_bullets = [
        ("Interface Characterization:", " Built as an interactive experiment and monitoring interface for research inspection (not a production monitoring platform)."),
        ("Review Budget Tuning:", " Dynamic slider allowing evaluation across 1%, 2%, 5%, and 150% review allocations."),
        ("Errors Captured Display:", " Real-time metric cards and curves showing captured errors across strategies."),
        ("Review Efficiency Tracking:", " Errors captured per 1,000 reviews evaluated across budgets."),
        ("Distribution Drift Viewer:", " Ranks and visualizes features by Population Stability Index (PSI)."),
        ("Model Comparison View:", " Confusion matrices, ROC curves, and classification metrics for LR, RF, and XGBoost.")
    ]
    for dt, dd in dash_bullets:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + dt
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = " " + dd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    drift_img = os.path.join(RESULTS_DIR, "top10_drift_features.png")
    if os.path.exists(drift_img):
        s18.shapes.add_picture(drift_img, Inches(6.5), Inches(1.5), width=Inches(6.0))

    # ==========================================
    # SLIDE 19: REQUIREMENTS (Functional & Non-Functional)
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    notes_s19 = (
        "Slide 19 outlines our functional and non-functional requirements. Functional requirements FR1 through FR10 "
        "cover loading data, training models, generating predictions, calculating the four reliability signals, "
        "ranking predictions, applying budgets, comparing strategies, and visualizing results. All 10 are fully "
        "implemented. Our non-functional requirements emphasize practical attributes such as reproducibility with "
        "fixed seeds, modular architecture, and interpretability, without claiming unverified performance metrics."
    )
    add_base_decorations(s19, "Functional & Non-Functional Requirements", notes_text=notes_s19)

    t_s19 = s19.shapes.add_table(11, 3, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tbl19 = t_s19.table
    tbl19.columns[0].width = Inches(1.2)
    tbl19.columns[1].width = Inches(4.2)
    tbl19.columns[2].width = Inches(1.4)

    fr_headers = ["ID", "Functional Requirement Description", "Status"]
    for i, h in enumerate(fr_headers):
        cell = tbl19.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(9)
            p.font.color.rgb = WHITE

    fr_rows = [
        ("FR1", "Load and preprocess network-flow benchmark data", "IMPLEMENTED"),
        ("FR2", "Train ML classification models (LR, RF, XGBoost)", "IMPLEMENTED"),
        ("FR3", "Generate predictions and class probabilities", "IMPLEMENTED"),
        ("FR4", "Calculate 4 complementary reliability signals", "IMPLEMENTED"),
        ("FR5", "Calculate adaptive risk score from signals", "IMPLEMENTED"),
        ("FR6", "Rank predictions for human-review prioritization", "IMPLEMENTED"),
        ("FR7", "Apply fixed review budgets (1%, 2%, 5%, 150%)", "IMPLEMENTED"),
        ("FR8", "Compare review strategies against ground truth", "IMPLEMENTED"),
        ("FR9", "Evaluate performance under shifted temporal data", "IMPLEMENTED"),
        ("FR10", "Visualize experimental results on dashboard", "IMPLEMENTED"),
        ("FR11", "Historical Error Modeling", "IMPLEMENTED"),
        ("FR12", "Shifted-Test Evaluation", "IMPLEMENTED"),
        ("FR13", "Feedback-Adaptive Allocation", "IMPLEMENTED"),
        ("FR14", "Analytics Dashboard", "Partial")
    ]
    for r_idx, (frid, frdesc, frstat) in enumerate(fr_rows, start=1):
        tbl19.cell(r_idx, 0).text = frid
        tbl19.cell(r_idx, 1).text = frdesc
        tbl19.cell(r_idx, 2).text = frstat
        for c in range(3):
            cell = tbl19.cell(r_idx, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else RGBColor(241, 245, 249)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(8.2)
                p.font.color.rgb = GREEN if c == 2 else DARK_GRAY
                if c == 2 or c == 0:
                    p.font.bold = True

    c19_nfr = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(1.5), Inches(4.6), Inches(5.3))
    c19_nfr.fill.solid()
    c19_nfr.fill.fore_color.rgb = WHITE
    c19_nfr.line.color.rgb = BORDER_GRAY
    tf = c19_nfr.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NON-FUNCTIONAL REQUIREMENTS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_BLUE

    nfrs = [
        ("Reproducibility:", " Deterministic seed setting across model training and chronological splitting."),
        ("Scalability for Dev Data:", " Efficient processing of the 500,000-flow sample on local workstations."),
        ("Interpretability:", " Transparent decomposition of risk scores into confidence, OOD, drift, and historical factors."),
        ("Modular Architecture:", " Decoupled modules for preprocessing, modeling, reliability, and evaluation."),
        ("Data Privacy Awareness:", " Offline processing preventing sensitive network header transmission."),
        ("Maintainability & Usability:", " Clean script modularity with clear parameter configuration in dashboard.")
    ]
    for nt, nd in nfrs:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + nt
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = " " + nd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9)

    # ==========================================
    # SLIDE 20: ARCHITECTURE & PSEUDOCODE
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    notes_s20 = (
        "This slide presents the high-level architecture and conceptual implementation pseudocode. "
        "The architecture flows linearly from BigFlow data through preprocessing, model training, prediction, "
        "and reliability extraction. The pseudocode demonstrates how for each prediction, we calculate confidence, "
        "OOD distance, drift, and historical error, combine them into a risk score, rank predictions, select top-K "
        "cases based on review budget, and compare with ground truth to evaluate error capture."
    )
    add_base_decorations(s20, "High-Level Architecture & Conceptual Pseudocode", notes_text=notes_s20)

    c20_arch = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c20_arch.fill.solid()
    c20_arch.fill.fore_color.rgb = WHITE
    c20_arch.line.color.rgb = BORDER_GRAY
    tf = c20_arch.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HIGH-LEVEL ARCHITECTURE"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_BLUE

    p = tf.add_paragraph()
    p.text = (
        "BIGFLOW DATA (500K)\n"
        "        ↓\n"
        "PREPROCESSING (Scaling & Splitting)\n"
        "        ↓\n"
        "ML MODEL (XGBoost)\n"
        "        ↓\n"
        "PREDICTIONS & PROBABILITIES\n"
        "        ↓\n"
        "RELIABILITY ENGINE\n"
        "├── Prediction Confidence\n"
        "├── Mahalanobis OOD\n"
        "├── Feature Drift (PSI)\n"
        "└── Historical Error Proximity\n"
        "        ↓\n"
        "ADAPTIVE RISK SCORE\n"
        "        ↓\n"
        "REVIEW BUDGET (1%, 2%, 5%, 150%)\n"
        "        ↓\n"
        "TOP-K REVIEW PRIORITIZATION\n"
        "        ↓\n"
        "EVALUATION & DASHBOARD"
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = NAVY

    c20_pc = s20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c20_pc.fill.solid()
    c20_pc.fill.fore_color.rgb = RGBColor(241, 245, 249)
    c20_pc.line.color.rgb = BORDER_GRAY
    tf = c20_pc.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CONCEPTUAL IMPLEMENTATION PSEUDOCODE"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    pc_text = (
        "FOR each prediction x_i:\n"
        "    calculate prediction confidence: s_conf\n"
        "    calculate OOD signal: s_ood\n"
        "    calculate drift signal: s_drift\n"
        "    calculate historical error risk: s_hist\n"
        "    combine reliability signals\n"
        "    calculate risk score: Risk(x_i)\n\n"
        "SORT predictions descending by risk score\n\n"
        "SELECT top K predictions based on available\n"
        "    review budget B: K = floor(B * N)\n\n"
        "COMPARE reviewed cases with ground truth\n\n"
        "CALCULATE:\n"
        "    errors captured\n"
        "    coverage rate\n"
        "    review efficiency (errors/1000 reviews)"
    )
    p = tf.add_paragraph()
    p.text = pc_text
    p.font.size = Pt(9)
    p.font.color.rgb = DARK_GRAY

    # ==========================================
    # SLIDE 21: LIMITATIONS
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    notes_s21 = (
        "An important demonstration of research maturity is being completely transparent about limitations. "
        "We clearly identify eight constraints of the current work: we use a 500K development sample rather than "
        "all 67 million flows; human review is simulated using ground truth; signal combination weights are currently "
        "heuristic rather than optimally learned; the current task is binary classification; and our shifted evaluation "
        "is a temporal test within one benchmark. Acknowledging these boundaries defines our research roadmap."
    )
    add_base_decorations(s21, "Experimental & Methodological Limitations", notes_text=notes_s21)

    c21_box = s21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    c21_box.fill.solid()
    c21_box.fill.fore_color.rgb = WHITE
    c21_box.line.color.rgb = BORDER_GRAY
    tf = c21_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "RESEARCH LIMITATIONS IDENTIFIED IN CURRENT PROTOTYPE"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = RED

    limits = [
        ("1. Development Sample Size:", " Current experiments evaluate a 500,000-flow development sample rather than the full 66.9M BigFlow benchmark."),
        ("2. Simulated Review Oracle:", " Human review is simulated using ground-truth labels rather than recruiting actual human analysts."),
        ("3. Heuristic Signal Weights:", " Current review-allocation weights are heuristic rather than learned through an optimal loss formulation."),
        ("4. Binary Task Formulation:", " Current classification evaluates binary Benign vs. Attack; multi-class attack classification remains future work."),
        ("5. Temporal Sample Shift:", " Shifted evaluation represents a chronological test within the benchmark sample, not cross-dataset validation."),
        ("6. Streaming Simulation:", " Real-time streaming is currently simulated from benchmark buffers rather than live production traffic."),
        ("7. Tabular Generalization:", " Generalization to arbitrary tabular domains requires additional dataset testing and automated validation."),
        ("8. Strategy Trade-Offs:", " Current experiments do not establish universal superiority of one strategy, highlighting budget dependency.")
    ]
    for lt, ld in limits:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = lt
        r1.font.bold = True
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = ld
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    # ==========================================
    # SLIDE 22: PHASE 2 (PLANNED EXTENSIONS)
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    notes_s22 = (
        "Slide 22 outlines Phase 2, which is our planned extension to generalize the prototype into a dataset-agnostic "
        "reliability platform. Everything on this slide is explicitly planned. The goal is to allow users to upload "
        "any tabular dataset in CSV, Excel, or Parquet format, automatically profile the data, detect the task type, "
        "train baseline models, and apply our reliability analysis. Planned advanced features include SHAP explainability, "
        "conformal prediction, and cost-aware review allocation."
    )
    add_base_decorations(s22, "Phase 2: Planned Dataset-Agnostic Platform", notes_text=notes_s22)

    # Upper: Embedded Phase 2 Flowchart
    p2_img = os.path.join(DIAGRAMS_DIR, "diagram_phase2_platform.png")
    if os.path.exists(p2_img):
        s22.shapes.add_picture(p2_img, Inches(0.8), Inches(1.4), width=Inches(11.7))

    # Lower: Planned Capabilities Box
    c22_sub = s22.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.1))
    c22_sub.fill.solid()
    c22_sub.fill.fore_color.rgb = WHITE
    c22_sub.line.color.rgb = BORDER_GRAY
    tf = c22_sub.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PLANNED FUNCTIONALITY ROADMAP (PHASE 2)"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = ACCENT_BLUE

    p2_bullets = [
        ("Data Formats & Tasks [PLANNED]:", " Support CSV, Excel, and Parquet; auto-detect binary, multi-class, and regression tasks."),
        ("Model Comparison [PLANNED]:", " Train baseline suites and compare performance across models."),
        ("Explainability (SHAP) [PLANNED]:", " Provide feature attributions explaining why specific cases were prioritized for human review."),
        ("Conformal Prediction [PLANNED]:", " Implement distribution-free uncertainty intervals with statistical coverage guarantees."),
        ("Cost-Aware Review Queues [PLANNED]:", " Optimize review queues factoring inspection costs versus penalty of undetected errors.")
    ]
    for pt, pd in p2_bullets:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + pt
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = " " + pd
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(8.8)

    # ==========================================
    # SLIDE 23: FINAL RESEARCH SUMMARY & CONCLUSION
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    notes_s23 = (
        "To conclude, this slide summarizes our Phase-1 research contributions and central finding. "
        "We implemented a reliability-aware prediction pipeline, combined multiple complementary signals, "
        "evaluated review strategies under temporal shift, studied budget-dependent effectiveness, and built an "
        "interactive dashboard. Our central finding is that review allocation effectiveness depends on both "
        "the signals used and the available budget. The current work provides an experimental foundation for "
        "further research as we transition to Phase 2. Thank you."
    )
    add_base_decorations(s23, "Research Summary & Current Contributions", notes_text=notes_s23)

    c23_left = s23.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c23_left.fill.solid()
    c23_left.fill.fore_color.rgb = WHITE
    c23_left.line.color.rgb = BORDER_GRAY
    tf = c23_left.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CURRENT RESEARCH CONTRIBUTIONS"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_BLUE

    contribs = [
        "1. Implemented a reliability-aware ML prediction pipeline on benchmark data.",
        "2. Combined multiple complementary reliability signals for review prioritization.",
        "3. Evaluated review strategies under a later chronological temporal test period.",
        "4. Studied experimentally how review effectiveness changes with review budget.",
        "5. Built an interactive dashboard for experimental analysis and monitoring."
    ]
    for c in contribs:
        p = tf.add_paragraph()
        p.text = c
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_GRAY

    p = tf.add_paragraph()
    p.text = "\nCURRENT RESEARCH FINDING:"
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    p = tf.add_paragraph()
    p.text = '"The experiments indicate that the effectiveness of review allocation depends on both the reliability signals used and the available review budget."'
    p.font.italic = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_BLUE

    c23_right = s23.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3))
    c23_right.fill.solid()
    c23_right.fill.fore_color.rgb = WHITE
    c23_right.line.color.rgb = BORDER_GRAY
    tf = c23_right.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRANSITION TO PHASE 2"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = NAVY

    p = tf.add_paragraph()
    p.text = "From Research Prototype to Dataset-Agnostic Platform:"
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = ACCENT_BLUE

    trans_pts = [
        ("Current State:", " Core reliability and human-review allocation pipeline implemented and validated on benchmark data."),
        ("Next Step:", " Generalize, test across diverse tabular datasets, and evaluate additional human-AI reliability mechanisms."),
        ("Final Concluding Statement:", " \"The current work provides an experimental foundation for further investigation of adaptive human-review allocation under distribution shift.\"")
    ]
    for tt, td in trans_pts:
        p = tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "• " + tt
        r1.font.bold = True
        r1.font.color.rgb = DARK_GRAY
        r2 = p.add_run()
        r2.text = " " + td
        r2.font.color.rgb = DARK_GRAY
        p.font.size = Pt(9.5)

    p = tf.add_paragraph()
    p.text = "\nThank you.\nOpen to questions and guidance from the committee."
    p.font.bold = True
    p.font.size = Pt(10.5)
    p.font.color.rgb = NAVY

    # ==========================================
    # SLIDE 24: REFERENCES
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    notes_s24 = (
        "Here are the references cited throughout the presentation, formatted according to IEEE guidelines. "
        "These include peer-reviewed publications from ICML, NeurIPS, IEEE TPAMI, and Mendeley Data. "
        "Thank you for your time and guidance."
    )
    add_base_decorations(s24, "References (IEEE Standard Format)", notes_text=notes_s24)

    c24_box = s24.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.3))
    c24_box.fill.solid()
    c24_box.fill.fore_color.rgb = WHITE
    c24_box.line.color.rgb = BORDER_GRAY
    tf = c24_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PEER-REVIEWED ACADEMIC REFERENCES"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = ACCENT_BLUE

    refs = [
        "[1] Mendeley Data, 'BigFlow-NIDS: A large-scale derived benchmark for network intrusion detection,' Data in Brief, V2, 2026. DOI: 10.1016/j.dib.2026.112530.",
        "[2] H. Mozannar and D. Sontag, 'Consistent estimators for learning to defer to an expert,' in Proc. 37th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 119, 2020, pp. 7076–7087.",
        "[3] D. Wei et al., 'Deep learning to defer with multiple experts,' in Proc. 41st Int. Conf. Mach. Learn. (ICML), PMLR, vol. 235, 2024.",
        "[4] Y. Geifman and R. El-Yaniv, 'Selective classification for deep neural networks,' in Adv. Neural Inf. Process. Syst. 30 (NeurIPS), 2017.",
        "[5] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, 'On calibration of modern neural networks,' in Proc. 34th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 70, 2017, pp. 1321–1330.",
        "[6] A. N. Angelopoulos and S. Bates, 'A gentle introduction to conformal prediction and distribution-free uncertainty quantification,' arXiv preprint arXiv:2107.07511, 2021.",
        "[7] J. Yang et al., 'Generalized out-of-distribution detection: A survey,' IEEE Trans. Pattern Anal. Mach. Intell. (TPAMI), 2024.",
        "[8] P. W. Koh et al., 'WILDS: A benchmark of in-the-wild distribution shifts,' in Proc. 38th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 139, 2021, pp. 5637–5664.",
        "[9] K. Lee, K. Lee, H. Lee, and J. Shin, 'A simple unified framework for detecting out-of-distribution samples and adversarial attacks,' in Adv. Neural Inf. Process. Syst. 31 (NeurIPS), 2018.",
        "[10] M. Charusaie et al., 'Sample efficient learning of predictors that complement humans,' in Adv. Neural Inf. Process. Syst. 35 (NeurIPS), 2022."
    ]
    for r in refs:
        p = tf.add_paragraph()
        p.text = r
        p.font.size = Pt(8.3)
        p.font.color.rgb = DARK_GRAY

    prs.save(PPTX_PATH)
    print(f"Successfully generated PowerPoint presentation at: {PPTX_PATH}")

if __name__ == "__main__":
    build_deck()
