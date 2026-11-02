from report_src.docx_helper import add_h1, add_h2, add_h3, add_p, add_bullet, add_image, create_table
import os
from docx.shared import Inches

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"

def build_section_9_functional(doc):
    add_h1(doc, "9. Functional Requirements")
    add_p(doc,
        "The functional requirements define the explicit system capabilities, operational workflows, and computational transformations implemented across the 26 sequential Python scripts in the project.")

    add_h2(doc, "9.1 Users / Actors")
    add_bullet(doc, "Configures dataset partitions, initiates preprocessing pipelines, trains baseline and primary classifiers, extracts reliability signals, and tunes triage scoring parameters.", bold_prefix="1. ML Practitioner / Engineer: ")
    add_bullet(doc, "Simulated via ground-truth oracle in Phase-I; receives the prioritized triage review queue, inspects high-risk network flows, confirms or corrects predictions, and logs verification outcomes.", bold_prefix="2. Security Analyst / Review Oracle: ")
    add_bullet(doc, "Executes cross-strategy comparative benchmarks, evaluates error capture rates across discrete review budgets (1%–10%), inspects feature drift distributions, and audits system reproducibility.", bold_prefix="3. System Evaluator / Researcher: ")

    add_h2(doc, "9.2 Modules")
    add_bullet(doc, "Module 1: Ingestion & Temporal Splitting (Scripts 01, 02, 26) — Validates raw flow attributes, enforces chronological order, and partitions data into train, validation, and shifted-test sets.", bold_prefix="M1: ")
    add_bullet(doc, "Module 2: Data Preprocessing & Model Training (Scripts 03, 04) — Handles missing values, performs scaling, trains Logistic Regression, Random Forest, and XGBoost classifiers, and serializes model artifacts.", bold_prefix="M2: ")
    add_bullet(doc, "Module 3: Multi-Signal Reliability Extraction (Scripts 05, 07, 10, 11, 14, 15, 17) — Extracts prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake neighborhoods.", bold_prefix="M3: ")
    add_bullet(doc, "Module 4: Risk Scoring & Review Allocation Engine (Scripts 06, 08, 09, 12, 13) — Computes static and multi-factor composite risk scores, constructing prioritized review queues under fixed capacity budgets.", bold_prefix="M4: ")
    add_bullet(doc, "Module 5: Shifted Evaluation & Feedback Loop (Scripts 16, 18, 19, 20, 21, 22, 23, 24, 25) — Benchmarks five allocation strategies on shifted test data and dynamically updates weights using simulated reviewer feedback.", bold_prefix="M5: ")
    add_bullet(doc, "Module 6: Exploratory Analytics Dashboard (dashboard/app.py) — Interactive local Streamlit web application for visual analysis of strategies, drift metrics, and efficiency trends.", bold_prefix="M6: ")

    add_h2(doc, "9.3 Functionalities")
    add_p(doc,
        "Table 9.1 enumerates the complete Functional Requirements (FR1 to FR14), mapping each requirement to its implementing script, primary actor, and verified implementation status.")

    headers = ["Module", "User / Actor", "Functionality", "Description", "Current Status"]
    rows = [
        ["M1", "ML Engineer", "FR1: Ingestion & Integrity", "Loads 500K BigFlow-NIDS flows, verifies 55 attributes, logs SHA-256 hashes (src/01_test_dataset.py, src/26_verify_bigflow_sample.py).", "Implemented"],
        ["M1", "ML Engineer", "FR2: Chronological Splitting", "Enforces strict temporal sorting; partitions into 350K train, 75K val, 75K shifted test (src/02_create_splits.py).", "Implemented"],
        ["M1", "ML Engineer", "FR3: Preprocessing & Imputation", "Imputes missing values with train medians; scales features for linear models; eliminates leakage (src/03_preprocess.py).", "Implemented"],
        ["M2", "ML Engineer", "FR4: Classifier Training", "Trains Logistic Regression, Random Forest, and XGBoost; logs validation ROC-AUC metrics (src/04_train_models.py).", "Implemented"],
        ["M3", "ML Engineer", "FR5: Prediction Signal Extraction", "Extracts class probabilities and confidence scores for validation inferences (src/05_generate_prediction_signals.py).", "Implemented"],
        ["M4", "Reviewer", "FR6: Confidence Review Strategy", "Ranks validation predictions by lowest confidence (1 - conf) across budgets (src/06_confidence_review_strategy.py).", "Implemented"],
        ["M3", "ML Engineer", "FR7: Mahalanobis OOD Extraction", "Computes regularized Mahalanobis distance from training centroid (src/07_ood_detection.py, src/08_ood_review_strategy.py).", "Implemented"],
        ["M4", "Reviewer", "FR8: Static Multi-Factor Review", "Synthesizes confidence and OOD percentile scores with static equal weighting (src/09_static_multifactor_strategy.py).", "Implemented"],
        ["M3", "ML Engineer", "FR9: PSI Feature Drift Analysis", "Calculates Population Stability Index across 49 features; generates drift risk mapping (src/10_measure_drift.py, src/11_create_drift_risk.py).", "Implemented"],
        ["M4", "Reviewer", "FR10: Adaptive Risk Scoring", "Combines confidence, OOD, and drift into adaptive score; evaluates on validation set (src/12_adaptive_risk_score.py, src/13_adaptive_review_strategy.py).", "Implemented"],
        ["M3", "ML Engineer", "FR11: Historical Error Modeling", "Estimates mistake likelihood based on feature decile neighborhoods (src/14_historical_error_risk.py, src/15_four_factor_risk.py).", "Implemented"],
        ["M5", "Evaluator", "FR12: Shifted-Test Evaluation", "Extracts signals on shifted test; benchmarks Random, Confidence, OOD, Multi-Factor (src/16 to src/22).", "Implemented"],
        ["M5", "Evaluator", "FR13: Feedback-Adaptive Allocation", "Simulates review audit; adjusts historical error weight based on error concentration (src/23_review_feedback_loop.py, src/24_shifted_feedback_evaluation.py).", "Implemented"],
        ["M6", "Evaluator", "FR14: Analytics Dashboard", "Streamlit dashboard (dashboard/app.py) providing interactive charts; full multi-dataset web portal planned for Phase 2.", "Implemented (Demo) / Phase-2 (Full)"]
    ]
    col_w = [0.6, 1.0, 1.5, 2.4, 1.0]
    create_table(doc, headers, rows, col_w)

def build_section_10_non_functional(doc):
    add_h1(doc, "10. Non-Functional Requirements")
    add_p(doc,
        "The system adheres to rigorous software engineering and scientific standards, quantified across six core non-functional dimensions:")
    add_bullet(doc, "Signal extraction across 75,000 test inferences completes in ~48 seconds on an 8-core CPU. Multi-strategy review sorting and evaluation across all four budgets completes in 1.60 seconds. Vectorized NumPy array slicing guarantees sub-second queue generation.", bold_prefix="1. Computational Performance: ")
    add_bullet(doc, "All experiments enforce a fixed random seed (seed=42) and deterministic chronological index sorting. Cryptographic SHA-256 checksums verify raw data integrity, guaranteeing exact bit-for-bit repeatability across independent runs.", bold_prefix="2. Reproducibility & Integrity: ")
    add_bullet(doc, "The codebase is organized into 26 discrete, sequentially decoupled Python scripts in src/. Intermediate outputs are persisted as standardized CSV tables, enabling isolated execution, testing, and modification of individual modules without pipeline breakage.", bold_prefix="3. Modularity & Maintainability: ")
    add_bullet(doc, "Memory footprint remains below 4 GB RAM during 500K flow batch processing. The priority queue algorithms operate with O(N log N) computational complexity, scaling linearly with inference stream volume.", bold_prefix="4. Scalability: ")
    add_bullet(doc, "The framework avoids black-box neural allocation policies. All composite risk scores are computed via transparent linear combinations of bounded, normalized signals (0.0 to 1.0), providing clear auditability for operational analysts.", bold_prefix="5. Transparency & Interpretability: ")
    add_bullet(doc, "File-based storage avoids database server downtime. The Streamlit dashboard operates independently on localhost:8501, offering responsive client-side chart re-rendering via Plotly.", bold_prefix="6. Availability & Usability: ")

def build_section_11_system_design(doc):
    add_h1(doc, "11. System / Software Design")
    add_p(doc,
        "The system architecture employs a decoupled, multi-stage pipeline designed for modular reliability assessment, cost-constrained triage, and post-audit feedback.")

    add_h2(doc, "11.1 Architecture Diagram")
    add_p(doc,
        "Figure 11.1 illustrates the end-to-end multi-tier system architecture, encompassing raw flow ingestion, baseline classifier training, four-factor reliability signal extraction, composite risk scoring, priority queue allocation, and feedback adaptation.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_architecture.png"), 
              "Figure 11.1: Multi-Tier System Architecture for Adaptive Human-Review Allocation.", width=Inches(6.2))
    add_p(doc,
        "The architecture consists of five interconnected tiers: (1) Data Ingestion Tier partitions raw flows chronologically; (2) ML & Preprocessing Tier trains XGBoost, Random Forest, and Logistic Regression models; (3) Reliability Engineering Tier extracts the four orthogonal reliability signals; (4) Allocation & Triage Tier builds the priority queue under budget constraints; and (5) Audit & Feedback Tier simulates oracle review and updates historical weighting parameters.")

    add_h2(doc, "11.2 Use-Case Diagram")
    add_p(doc,
        "Figure 11.2 presents the UML Use-Case Diagram depicting the functional interactions between the primary actors (ML Engineer, Security Analyst/Review Oracle, System Evaluator) and the system boundaries.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_use_case.png"),
              "Figure 11.2: UML Use-Case Diagram Depicting System Actors and Operational Workflows.", width=Inches(5.8))
    add_p(doc,
        "The ML Engineer manages data preparation, model training, and signal parameter configuration. The Review Oracle inspects prioritized predictions and confirms ground-truth outcomes. The Evaluator executes comparative benchmarks and analyzes review efficiency across budgets.")

    add_h2(doc, "11.3 Activity / Sequence Diagram")
    add_p(doc,
        "The operational sequence for inference triage follows a deterministic multi-step lifecycle:",
        bold_prefix="Operational Execution Sequence: ")
    add_bullet(doc, "Step 1: Test instance arrives from the shifted telemetry stream and passes through the primary classifier (XGBoost) to generate class probability P(y=1|x) and binary prediction.")
    add_bullet(doc, "Step 2: Signal extraction modules compute confidence risk (1 - max P), regularized Mahalanobis OOD distance, feature drift vulnerability (PSI mapping), and historical mistake decile proximity.")
    add_bullet(doc, "Step 3: The Risk Scoring Engine computes the composite score R(x) and inserts the record into the sorted Priority Review Queue.")
    add_bullet(doc, "Step 4: The top-K instances matching the operational review budget quota (B) are allocated to the simulated review oracle.")
    add_bullet(doc, "Step 5: The oracle inspects true labels, identifies captured errors, logs review efficiency, and triggers the feedback loop to update historical weights for subsequent batches.")

    add_h2(doc, "11.4 Process Flow / Methodology")
    add_p(doc,
        "Figure 11.3 details the comprehensive process flow from raw data ingestion through baseline modeling, signal extraction, strategy benchmarking, and report generation.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_process_flow.png"),
              "Figure 11.3: End-to-End Methodological Process Flow Diagram.", width=Inches(6.0))
    add_p(doc,
        "The process flow ensures that training, validation, and shifted test sets remain strictly isolated. Feature scalers, covariance matrices, and drift baselines are fitted exclusively on training data to prevent data leakage.")

    add_h2(doc, "11.5 ML / Data Processing Pipeline")
    add_p(doc,
        "Figure 11.4 illustrates the detailed machine learning and data transformation pipeline.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_ml_pipeline.png"),
              "Figure 11.4: Detailed Machine Learning and Feature Processing Pipeline.", width=Inches(5.8))
    add_p(doc,
        "The pipeline highlights the feature transformation path: median imputation, StandardScaler transformation (for Logistic Regression), model inference, four-factor signal extraction, and percentile ranking.")

    add_h2(doc, "11.6 DL Model Architecture, where applicable")
    add_p(doc,
        "Not Applicable. The current system relies on gradient-boosted decision trees (XGBoost) and ensemble tree methods (Random Forest) as primary classifiers. Tabular network flow benchmarks consistently demonstrate that gradient boosted trees achieve superior predictive performance, faster training, and greater numerical stability than deep neural networks on tabular security data. A custom deep learning architecture is therefore not applicable to Phase-I.",
        bold_prefix="Status: ")

    add_h2(doc, "11.7 Network / IoT Block Diagram, where applicable")
    add_p(doc,
        "Not Applicable. The proposed research operates at the software and algorithmic level on structured PCAP flow records pre-captured from network traffic. The framework does not interface directly with physical IoT microcontrollers, sensor nodes, or embedded networking hardware. A physical network/IoT block diagram is therefore not applicable.",
        bold_prefix="Status: ")
