from report_src.docx_helper import add_h1, add_h2, add_h3, add_p, add_bullet, create_table

def build_section_1_abstract(doc):
    add_h1(doc, "1. Abstract")
    add_p(doc, 
        "Machine learning (ML) models deployed in high-throughput, mission-critical environments—such as network intrusion detection, financial fraud monitoring, and automated clinical screening—inevitably experience performance degradation due to temporal distribution shifts. In these real-world settings, human-review capacity is strictly constrained by operational overhead, analyst fatigue, and financial cost, typically allowing only 1% to 10% of total inferences to be manually audited. Existing selective classification frameworks prioritize audit queues relying almost exclusively on model output probabilities (confidence). However, deep and complex classifiers frequently exhibit uncalibrated overconfidence under covariate and concept shift, resulting in critical, high-confidence misclassifications that silently bypass conventional confidence-based safety filters.")
    add_p(doc,
        "This project presents an adaptive, multi-factor human-review allocation framework designed to reliably detect and prioritize high-risk model errors under distribution shift within strict operational inspection budgets. The framework synergistically synthesizes four complementary reliability signals: (1) prediction uncertainty derived from normalized probabilities, (2) regularized Mahalanobis distance to capture geometric out-of-distribution (OOD) feature novelty, (3) Population Stability Index (PSI) to track macroscopic batch distribution drift, and (4) empirical historical error proximity mapped from validation error neighborhoods. The resulting composite risk score ranks inferences into a dynamic priority review queue, with a feedback mechanism adjusting signal weighting based on verified audit outcomes.")
    add_p(doc,
        "The proposed methodology is empirically evaluated on a 500,000-flow chronological partition from the large-scale BigFlow-NIDS benchmark (66.9 million total flows, 55 attributes), partitioned into 350,000 training, 75,000 validation, and 75,000 shifted-test instances. Under temporal shift, while model accuracy degrades and error rate surges 4.55x from 1.004% to 4.569%, the multi-factor allocation strategy captures 17.80% of total shifted errors at a 1% review budget (versus 13.51% for pure confidence) and 34.26% of errors at a 2% budget (versus 26.73% for pure confidence). Crucially, empirical findings reveal an honest budget-dependent crossover: while multi-factor allocation dominates under tight review constraints (1%–2%), pure confidence overtakes at broader budgets (5%–10%), capturing 65.45% and 84.01% of errors respectively. To date, 13 of 14 functional modules (92.9%) have been fully implemented and verified across 26 sequential Python scripts, supported by an interactive Streamlit exploratory analytics dashboard.")

def build_section_2_introduction(doc):
    add_h1(doc, "2. Introduction")
    add_p(doc,
        "The deployment of machine learning algorithms in production systems has transitioned from experimental automation to mission-critical infrastructure. Across enterprise cybersecurity, payment networks, and healthcare diagnostic pipelines, automated decision systems process tens of thousands to millions of transactions and network events daily. However, the foundational statistical assumption governing supervised machine learning—that training and operational test data are independent and identically distributed (i.i.d.)—is routinely violated in real-world environments. Network traffic patterns evolve, threat actors engineer novel evasion techniques, and user behavior shifts over time, introducing substantial covariate and concept drift.")

    add_h2(doc, "2.1 Problem Scenario")
    add_p(doc,
        "In production security operations centers (SOCs) and high-volume data pipelines, machine learning systems face two interconnected operational challenges:",
        bold_prefix="The Operational Bottleneck: ")
    add_bullet(doc, 
        "Human analysts have finite cognitive and temporal bandwidth. Security teams can realistically inspect only a tiny fraction (typically 1% to 5%, and rarely exceeding 10%) of daily alerts without inducing severe alert fatigue, increased latency, and missed incidents.",
        bold_prefix="Severe Review Capacity Constraints: ")
    add_bullet(doc,
        "Modern complex classifiers (including deep neural networks and gradient boosted decision trees) frequently output poorly calibrated probabilities. Under temporal distribution shift, models maintain average confidence levels exceeding 96.8% despite their error rates surging by more than 4.5-fold. Consequently, false negatives and false positives occur with high model confidence, making them invisible to traditional confidence thresholding.",
        bold_prefix="Silent Overconfidence Failure Mode: ")
    add_bullet(doc,
        "In the absence of principled triage, teams often resort to uniform random auditing or static confidence thresholding. In our empirical evaluations, random sampling captured only 1.17% of shifted-test errors at a 1% budget, rendering it ineffective as a safety mechanism.",
        bold_prefix="Inefficacy of Naive Audits: ")
    add_bullet(doc,
        "Standard Out-of-Distribution (OOD) detectors identify geometric feature novelty, but novelty in network traffic frequently corresponds to benign high-volume transfers rather than classification errors. In our experiments, OOD-only filtering captured a dismal 0.03% of shifted errors at 1% budget, performing substantially worse than random guessing.",
        bold_prefix="Failure of Isolated Signals: ")

    add_h2(doc, "2.2 Proposed Solution")
    add_p(doc,
        "To resolve these limitations, this project designs, implements, and evaluates an Adaptive Human-Review Allocation Framework. Rather than relying on any single failure indicator, the system unifies four heterogeneous, complementary reliability signals into a holistic, composite risk score:",
        bold_prefix="Multi-Signal Reliability Engine: ")
    add_bullet(doc, "Quantifies classifier uncertainty derived from class posterior probabilities, scaled inversely such that borderline predictions receive higher inspection priority.", bold_prefix="1. Prediction Uncertainty (Confidence Risk): ")
    add_bullet(doc, "Computes regularized Mahalanobis distance from training feature centroids in numerical representation space, capturing semantic and geometric feature divergence.", bold_prefix="2. Out-of-Distribution (OOD) Distance: ")
    add_bullet(doc, "Tracks macroscopic population-level feature drift across chronological batches using the Population Stability Index (PSI), projecting batch drift into per-instance vulnerability scores.", bold_prefix="3. Feature Drift Magnitude: ")
    add_bullet(doc, "Maps test instances into historical feature deciles to assess whether incoming records resemble training-set mistake clusters.", bold_prefix="4. Historical Error Proximity: ")
    add_p(doc,
        "The composite risk score dynamically ranks all incoming inferences into a strict priority queue. The top-K instances corresponding exactly to the designated operational capacity budget (e.g., 1%, 2%, 5%, or 10%) are routed to the human review queue. Furthermore, a feedback loop dynamically adjusts signal weights based on verified audit error concentrations, optimizing subsequent triage batches.")

    add_h2(doc, "2.3 Purpose")
    add_p(doc,
        "The primary purpose of this research is to establish a rigorous, mathematically sound, and empirically validated methodology for capacity-constrained error mitigation in machine learning under distribution shift. Specifically, the project aims to:",
        bold_prefix="Research Objectives: ")
    add_bullet(doc, "Empirically evaluate whether multi-factor reliability scoring improves error capture over pure confidence ranking under tight operational budgets (1%–2%).")
    add_bullet(doc, "Bridge the theoretical gap between selective classification (which assumes stationary data), OOD detection (which identifies novelty rather than mistakes), and learning-to-defer (which lacks hard capacity quotas).")
    add_bullet(doc, "Provide a fully reproducible, modular software pipeline that production teams can adopt to safeguard high-throughput classifiers without requiring model retraining or architectural redesign.")

    add_h2(doc, "2.4 Scope")
    add_p(doc,
        "To ensure scientific rigor and clear engineering execution, the project scope is formally demarcated between completed Phase-I deliverables and planned Phase-II extensions:",
        bold_prefix="Phase Boundary Delineation: ")
    add_bullet(doc, 
        "Evaluation conducted on a 500,000-flow chronological partition of the BigFlow-NIDS benchmark; binary classification (Benign vs. Attack); 49 numerical flow features; three baseline classifiers (Logistic Regression, Random Forest, XGBoost); offline simulated review oracle using test ground truth; four discrete review budgets (1%, 2%, 5%, 10%); local Streamlit exploratory analytics dashboard.",
        bold_prefix="In-Scope (Phase-I Implemented): ")
    add_bullet(doc, 
        "Live network packet capture / inline hardware sniffing; real human subjects in the loop (simulated ground-truth oracle utilized for objective, reproducible benchmarking); multi-class attack categorization (the detailed 32-class attack column was excluded to eliminate label leakage); automated bilevel optimization of signal weights (heuristic weights evaluated).",
        bold_prefix="Out-of-Scope (Phase-I): ")
    add_bullet(doc, 
        "Cross-domain tabular generalization across financial fraud and clinical datasets; post-hoc probability calibration (Temperature Scaling); SHAP-based feature attribution for human-audited cases; full production-grade web application with multi-user authentication.",
        bold_prefix="Planned Scope (Phase-II): ")

def build_section_3_review1(doc):
    add_h1(doc, "3. Review-I Recommendations and Action Taken")
    add_p(doc,
        "During the Phase-I Review-I evaluation, the capstone review panel provided critical constructive feedback regarding dataset selection, baseline formulation, and engineering reproducibility. Table 3.1 details each recommendation received and the specific concrete actions taken in Review-II to address them.")

    headers = ["Sl No", "Review-I Recommendation", "Action Taken in Review-II", "Status"]
    rows = [
        [
            "1",
            "Clearly define the scope of distribution shift and select a realistic, large-scale benchmark dataset rather than synthetic perturbations.",
            "Replaced synthetic shifts with the authentic BigFlow-NIDS benchmark (66.9M flows, 55 attributes). Implemented strict chronological 70/15/15 partitioning (350K train, 75K validation, 75K shifted test), creating a genuine 4.55x error rate surge and 19.05x attack prevalence shift.",
            "Addressed"
        ],
        [
            "2",
            "Move beyond isolated thresholding; implement competitive baselines and explicit operational capacity constraints for review allocation.",
            "Formulated and implemented five distinct allocation strategies (Uniform Random, Pure Confidence, OOD-Only, Static Multi-Factor, and Feedback Adaptive) benchmarked across four realistic operational budgets (1%, 2%, 5%, and 10%).",
            "Addressed"
        ],
        [
            "3",
            "Ensure complete engineering reproducibility with documented source code, deterministic seeds, and persistent data verification.",
            "Developed 26 sequential, modular Python scripts in src/. Enforced deterministic sorting, fixed random seed (seed=42), SHA-256 dataset verification, and complete CSV artifact logging across all stages.",
            "Addressed"
        ],
        [
            "4",
            "Provide an interactive demonstration of the allocation mechanics and analytical findings.",
            "Engineered a fully functional Streamlit exploratory analytics dashboard (dashboard/app.py) featuring interactive Plotly visualizations, budget toggles, PSI drift inspection, and efficiency metrics.",
            "Addressed"
        ]
    ]
    col_w = [0.6, 2.3, 2.7, 0.9]
    create_table(doc, headers, rows, col_w)
