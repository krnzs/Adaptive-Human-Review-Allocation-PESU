from report_src.docx_helper import add_h1, add_h2, add_h3, add_p, add_bullet, create_table

def build_section_5_synthesis(doc):
    add_h1(doc, "5. Literature Review Synthesis")
    add_p(doc,
        "Rather than treating the literature as isolated studies, this synthesis examines the broader scientific landscape spanning five intersecting domains: selective classification, probability calibration, out-of-distribution detection, concept drift monitoring, and collaborative human-AI learning-to-defer.")

    add_h2(doc, "5.1 Background Study")
    add_p(doc,
        "The fundamental premise of selective prediction traces back to Chow's rule for optimal reject options in Bayesian classification. In modern machine learning, Geifman and El-Yaniv (2017) adapted this principle to deep neural networks by ranking instances by maximum softmax probability. However, Guo et al. (2017) demonstrated that modern architectures are fundamentally miscalibrated, tending toward extreme overconfidence. When models encounter temporal distribution shifts (Koh et al., 2021; Cao et al., 2023), this miscalibration exacerbates: erroneous predictions are frequently assigned high posterior probabilities. Concurrently, the OOD detection literature (Yang et al., 2024) has developed sophisticated representation-space metrics to detect semantic novelty. In parallel, data stream researchers (Lu et al., 2019; Iwashita & Papa, 2019) have formulated statistical drift metrics such as the Population Stability Index (PSI). Finally, learning-to-defer frameworks (Mozannar & Sontag, 2020; Wei et al., 2024; Liu et al., 2022) have formalized the delegation of difficult instances to human experts.")

    add_h2(doc, "5.2 Major Approaches Identified")
    add_bullet(doc, "Relies on output probabilities (max P(y|x)) or entropy to reject low-confidence instances. While computationally efficient, it fails when the classifier is confidently wrong.", bold_prefix="1. Confidence-Based Rejection: ")
    add_bullet(doc, "Measures feature divergence from the training centroid using distance metrics (Mahalanobis distance) or energy functions. Excels at detecting novelty, but novel samples do not necessarily correlate with prediction errors.", bold_prefix="2. Geometric & Representation OOD Detection: ")
    add_bullet(doc, "Monitors population-level distribution changes across batches (e.g., PSI, Wasserstein distance). However, these metrics are macroscopic aggregates and cannot directly score individual predictions for operational triage.", bold_prefix="3. Statistical Distribution Drift Monitoring: ")
    add_bullet(doc, "Jointly trains classifiers and deferral policies to optimize human-machine teaming. While mathematically elegant, existing formulations assume unconstrained or fixed-cost deferral rather than operating within strict percentage budgets.", bold_prefix="4. Learning-to-Defer (L2D): ")

    add_h2(doc, "5.3 Major Findings")
    add_p(doc,
        "Three critical consensus findings emerge across the reviewed literature:",
        bold_prefix="Cross-Literature Consensus: ")
    add_bullet(doc, "Overconfidence is pervasive in modern classifiers, making single-signal confidence filtering structurally vulnerable under real-world shifts.")
    add_bullet(doc, "Geometric feature novelty does not equal misclassification vulnerability: in tabular domains, out-of-distribution samples often represent benign high-volume variations rather than attacker evasion.")
    add_bullet(doc, "Human verification capacity in operational domains (such as cybersecurity and finance) is strictly finite, necessitating triage algorithms that optimize error capture within fixed 1% to 10% capacity quotas.")

    add_h2(doc, "5.4 Limitations of Existing Work")
    add_p(doc,
        "Despite significant advances, existing paradigms suffer from critical operational limitations:",
        bold_prefix="Methodological Gaps: ")
    add_bullet(doc, "Isolation of Failure Indicators: Existing research explores confidence, OOD distance, drift monitoring, and historical mistakes in separate silos without examining how they interact.")
    add_bullet(doc, "Lack of Explicit Capacity Quotas: Learning-to-defer and selective classification assume continuous threshold tuning or theoretical penalty costs, failing to operate within rigid enterprise capacity slicing (e.g., strictly 1%, 2%, 5%, or 10%).")
    add_bullet(doc, "Uncalibrated Posteriors Under Shift: Selective classification baselines rely on stationary probability distributions and degrade severely when temporal shift alters class prevalence.")

    add_h2(doc, "5.5 Identified Research / Application Gap")
    add_p(doc,
        "Grounded strictly in the surveyed literature, the identified research gap is formulated across five core statements:",
        bold_prefix="The Research Gap: ")
    add_bullet(doc, "1. Prior selective classification and reject-option literature relies predominantly on softmax prediction probabilities, which become severely uncalibrated and overconfident under real-world distribution shifts.")
    add_bullet(doc, "2. Independent out-of-distribution (OOD) detection and macroscopic drift monitoring frameworks identify anomalous data points or population-level distribution changes, but they fail to correlate geometric feature novelty with true classification errors at the individual prediction level.")
    add_bullet(doc, "3. Existing learning-to-defer methods jointly optimize human-AI decision pipelines under theoretical cost trade-offs, yet they lack explicit mechanisms to operate within rigid, operational capacity quotas (e.g., reviewing strictly 1% to 10% of high-throughput traffic).")
    add_bullet(doc, "4. Network intrusion detection research has explored active learning and adversarial robustness in isolation, but it lacks an empirical framework benchmarking how heterogeneous reliability signals interact under temporal data splits.")
    add_bullet(doc, "5. No existing system combines model uncertainty, instance-level OOD distance, macroscopic drift, and empirical error neighborhoods into an adaptive triage allocator that dynamically shifts weighting based on real-time reviewer feedback.")

    add_h2(doc, "5.6 How the Proposed Project Addresses the Gap")
    add_p(doc,
        "This project directly bridges the identified gap by developing an integrated triage framework that: (1) normalizes and synthesizes four complementary reliability signals into a single unified risk score; (2) implements explicit top-K budget slicing corresponding to realistic enterprise constraints (1%, 2%, 5%, 10%); (3) evaluates performance under authentic chronological distribution shift on the BigFlow-NIDS benchmark; and (4) incorporates a feedback mechanism that updates signal importance dynamically based on verified audit error density.")

def build_section_6_comparative_study(doc):
    add_h1(doc, "6. Comparative Study of Existing Applications / Systems")
    add_p(doc,
        "To contextualize the proposed framework against current industry and research paradigms, Table 6.1 provides a structured comparative analysis across key functional dimensions.")

    headers = ["System / Application", "Major Features", "Technology / Approach", "Limitations", "Proposed Project Difference"]
    rows = [
        [
            "Pure Confidence-Based Selective Classification (Geifman & El-Yaniv, 2017)",
            "Ranks inferences by maximum softmax probability max(P(y|x)); abstains when confidence falls below threshold.",
            "Softmax Response (SR), SelectiveNet risk-coverage optimization.",
            "Vulnerable to uncalibrated overconfidence under distribution shift; high-confidence errors completely bypass triage.",
            "Combines confidence with geometric OOD distance, macroscopic drift, and historical mistake patterns to catch confident errors."
        ],
        [
            "Out-of-Distribution Filtering Systems (Yang et al., 2024)",
            "Detects semantic and covariate novelty in representation space to reject unfamiliar inputs.",
            "Regularized Mahalanobis distance, Energy-based scores, Maximum Softmax Probability.",
            "Novelty does not correlate with classification errors; flags benign novel traffic, yielding near-zero error capture (0.03% in experiments).",
            "Treats OOD distance as a secondary modulation factor rather than a sole filter, pairing it with historical mistake likelihood."
        ],
        [
            "Traditional Learning-to-Defer Systems (Mozannar & Sontag, 2020)",
            "Jointly learns classifier and rejection policy to defer difficult instances to human experts.",
            "Bayes-consistent surrogate loss functions, (K+1)-class classification.",
            "Assumes stationary data distributions and theoretical cost penalties; lacks explicit percentage capacity quota enforcement.",
            "Enforces strict fixed review budgets (1%, 2%, 5%, 10%) without requiring classifier retraining or specialized loss functions."
        ],
        [
            "Active Learning Human-in-the-Loop IDS (Kim et al., 2024)",
            "Routes high-uncertainty security alerts to SOC analysts to iteratively retrain intrusion classifiers.",
            "Sequential hypothesis testing, query-by-committee, uncertainty sampling.",
            "Focused primarily on retraining loops rather than safeguarding static deployed models under unretrained distribution shift.",
            "Operates as an operational post-deployment safety net, prioritizing error capture under temporal shift with real-time feedback."
        ]
    ]
    col_w = [1.2, 1.4, 1.3, 1.4, 1.2]
    create_table(doc, headers, rows, col_w)

def build_section_7_contributions(doc):
    add_h1(doc, "7. Proposed Contribution / Distinguishing Features")
    add_p(doc,
        "The proposed Adaptive Human-Review Allocation Framework establishes five concrete, verifiable contributions:",
        bold_prefix="Core Distinguishing Features: ")
    add_bullet(doc, "Unlike conventional systems relying solely on prediction probabilities or isolated anomaly scores, this framework mathematically normalizes and unifies four complementary failure indicators: model uncertainty, geometric OOD distance, macroscopic PSI drift, and empirical historical error proximity.", bold_prefix="1. Heterogeneous Multi-Signal Synthesis: ")
    add_bullet(doc, "Designed specifically to model realistic production constraints where human auditing capacity is strictly limited. The framework evaluates explicit 1%, 2%, 5%, and 10% budget quotas, ensuring practical operational utility.", bold_prefix="2. Explicit Capacity-Constrained Triage: ")
    add_bullet(doc, "Evaluated on a massive, real-world benchmark (BigFlow-NIDS) partitioned chronologically (70/15/15) to simulate genuine temporal shift, producing an authentic 4.55x error rate surge and 19.05x attack prevalence shift.", bold_prefix="3. Authentic Chronological Distribution Shift Benchmark: ")
    add_bullet(doc, "Incorporate an adaptive mechanism that assesses error concentration in completed review batches and dynamically shifts weight toward historical error patterns for subsequent inference queues.", bold_prefix="4. Dynamic Feedback Weight Adaptation: ")
    add_bullet(doc, "The report provides an honest empirical characterization of strategy performance, demonstrating that multi-factor allocation dominates at tight budgets (1%–2%), while pure confidence overtakes at broader budgets (5%–10%). This transparent crossover provides vital guidance for operational system designers.", bold_prefix="5. Empirical Discovery of Budget-Dependent Strategy Crossover: ")

def build_section_8_tools(doc):
    add_h1(doc, "8. Tools and Technologies Used")
    add_p(doc,
        "The project is engineered using a robust, modular, and fully open-source scientific computing stack in Python. All library versions have been verified directly against the production environment.")

    add_h2(doc, "8.1 Programming Languages")
    add_p(doc, "Python 3.11.x — Chosen for its mature scientific computing ecosystem, high-performance numerical libraries, and broad industry support.", bold_prefix="Language: ")

    add_h2(doc, "8.2 Frameworks")
    add_p(doc, "Streamlit (v1.51.0) — Utilized to build the interactive local exploratory analytics dashboard (dashboard/app.py) for exploring strategy comparisons, review budgets, and feature drift distributions.", bold_prefix="UI & Analytics Framework: ")

    add_h2(doc, "8.3 Libraries / Packages with Versions")
    add_bullet(doc, "pandas (v2.2.3): High-performance tabular data manipulation, chronological sorting, and signal dataset construction.")
    add_bullet(doc, "NumPy (v1.26.4): Vectorized array calculations, covariance matrix regularization, and Mahalanobis distance computation.")
    add_bullet(doc, "scikit-learn (v1.7.2): Baseline model training (LogisticRegression, RandomForestClassifier), StandardScaler preprocessing, and ROC-AUC evaluation.")
    add_bullet(doc, "XGBoost (v3.1.3): Primary gradient-boosted decision tree classifier (XGBClassifier) optimized for tabular network flow prediction.")
    add_bullet(doc, "SciPy (v1.15.3): Covariance inversion, empirical CDF ranking, and statistical calculations.")
    add_bullet(doc, "Plotly (v6.3.0): Interactive dark-mode analytical charts integrated into the Streamlit dashboard.")
    add_bullet(doc, "Matplotlib (v3.10.0): Generation of high-resolution publication figures and system design diagrams.")
    add_bullet(doc, "python-docx (v1.2.0) & ReportLab (v4.4.10): Programmatic compilation of academic report artifacts and presentation decks.")
    add_bullet(doc, "joblib (v1.4.2): Model serialization, scaler persistence, and covariance matrix storage.")
    add_bullet(doc, "hashlib: SHA-256 cryptographic verification of chronological dataset splits.")

    add_h2(doc, "8.4 Database / Storage")
    add_p(doc,
        "The current Phase-I architecture intentionally employs a file-based storage architecture rather than a heavyweight database server. Structured results, feature sets, extracted reliability signals, and review queues are persisted as standardized CSV files in results/, while trained classifiers and preprocessing transformers are stored as serialized joblib artifacts in models/. Logical record linkage is maintained via a unique, deterministic prediction_id key.",
        bold_prefix="File-Based Persistence Architecture: ")

    add_h2(doc, "8.5 Development Tools")
    add_p(doc, "Visual Studio Code, PowerShell 7, Git version control, and the Antigravity Agentic IDE.", bold_prefix="Development Environment: ")

    add_h2(doc, "8.6 Deployment Environment")
    add_p(doc, "Local execution workstation; offline batch inference pipeline. The Streamlit exploratory dashboard runs locally on localhost:8501. No external cloud infrastructure or database servers are currently active in Phase-I.", bold_prefix="Deployment Target: ")

    add_h2(doc, "8.7 Hardware Requirements")
    add_p(doc, "Development & Execution Workstation: Intel Core i7 / AMD Ryzen 8-core CPU (3.2 GHz+), 16 GB DDR4/DDR5 RAM, 512 GB NVMe SSD storage. Minimum Deployment Requirements: 4 CPU cores, 8 GB RAM, 20 GB free disk space.", bold_prefix="Hardware Specification: ")
