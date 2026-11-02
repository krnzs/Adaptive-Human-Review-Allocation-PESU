from report_src.docx_helper import add_h1, add_h2, add_h3, add_p, add_bullet, add_image, create_table
import os
from docx.shared import Inches

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"

def build_section_12_database(doc):
    add_h1(doc, "12. Database / Data Design")
    add_p(doc,
        "The project implements a file-based storage architecture. In production data science pipelines, structured CSV tables and serialized binary objects offer high throughput, transparent audit trails, and seamless integration with NumPy and pandas without the operational overhead of a relational database server. To maintain rigorous conceptual integrity, the data architecture is formally modeled using an Entity-Relationship (ER) conceptual schema.")

    add_h2(doc, "12.1 ER Diagram")
    add_p(doc,
        "Figure 12.1 illustrates the conceptual Entity-Relationship Diagram representing the logical relationships between inferences, reliability signals, review queues, trained models, and drift metrics.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_er_diagram.png"),
              "Figure 12.1: Conceptual Entity-Relationship Diagram for the File-Based Storage Architecture.", width=Inches(6.0))
    add_p(doc,
        "The schema links PREDICTIONS to SIGNALS and REVIEW_QUEUE via a 1:1 relationship on prediction_id. MODELS stores metadata and serialization paths for trained estimators, while DRIFT_ANALYSIS maintains feature-level drift statistics.")

    add_h2(doc, "12.2 Conceptual Schema")
    add_p(doc,
        "The logical schema maps to discrete CSV and binary artifacts residing in results/ and models/. Table 12.1 outlines the primary entities, attributes, data types, and integrity constraints.")

    headers = ["Entity / File", "Field Name", "Data Type", "Constraint", "Description"]
    rows = [
        ["PREDICTIONS", "prediction_id", "Integer", "PK, Unique", "Deterministic zero-indexed inference ID."],
        ["PREDICTIONS", "true_label", "Integer (0/1)", "NOT NULL", "Ground-truth class (0=Benign, 1=Attack)."],
        ["PREDICTIONS", "predicted_label", "Integer (0/1)", "NOT NULL", "Classifier decision at 0.5 threshold."],
        ["PREDICTIONS", "confidence", "Float [0,1]", "NOT NULL", "Max class posterior max(P, 1-P)."],
        ["PREDICTIONS", "actual_error", "Integer (0/1)", "NOT NULL", "Binary indicator (1 if y_true != y_pred)."],
        ["SIGNALS", "prediction_id", "Integer", "FK, PK", "Reference to PREDICTIONS table."],
        ["SIGNALS", "confidence_risk", "Float [0,1]", "NOT NULL", "Normalized uncertainty (1 - confidence)."],
        ["SIGNALS", "ood_percentile", "Float [0,1]", "NOT NULL", "Empirical rank of Mahalanobis distance."],
        ["SIGNALS", "drift_risk", "Float [0,1]", "NOT NULL", "Feature-weighted PSI vulnerability."],
        ["SIGNALS", "historical_risk", "Float [0,1]", "NOT NULL", "Mistake density in feature decile bin."],
        ["REVIEW_QUEUE", "prediction_id", "Integer", "FK, PK", "Reference to PREDICTIONS table."],
        ["REVIEW_QUEUE", "composite_risk", "Float [0,1]", "NOT NULL", "Synthesized four-factor score."],
        ["REVIEW_QUEUE", "budget_tier", "Float", "NOT NULL", "Operational capacity (0.01, 0.02, 0.05, 0.10)."],
        ["REVIEW_QUEUE", "audit_confirmed", "Integer (0/1)", "NOT NULL", "Simulated oracle verified error status."],
        ["DRIFT_ANALYSIS", "feature_name", "String", "PK", "Network flow attribute name."],
        ["DRIFT_ANALYSIS", "psi_value", "Float", "NOT NULL", "Population Stability Index metric."],
        ["DRIFT_ANALYSIS", "drift_category", "String", "NOT NULL", "Negligible (<0.1), Moderate, or Severe (>0.25)."]
    ]
    col_w = [1.2, 1.3, 1.1, 1.1, 1.8]
    create_table(doc, headers, rows, col_w)

    add_h2(doc, "12.3 NoSQL / Document Structure")
    add_p(doc,
        "Not Applicable. Network flow telemetry metrics are fundamentally tabular, numerical, and fixed-schema records. The operational pipeline relies entirely on structured tabular CSV matrices and NumPy arrays; no unstructured JSON document collections or NoSQL document stores are required.",
        bold_prefix="Status: ")

    add_h2(doc, "12.4 Dataset / Data Schema, where applicable")
    add_p(doc,
        "The project utilizes the BigFlow-NIDS benchmark (Uddin & Arefin, Data in Brief 2026). Table 12.2 provides representative sample attributes from the 49 numerical flow features used for modeling.")

    headers_ds = ["Attribute Name", "Data Type", "Statistical Description", "Example Value"]
    rows_ds = [
        ["flow_duration", "Float64", "Total duration of network flow in microseconds.", "104,230.0"],
        ["total_fwd_packets", "Int64", "Total packets transmitted in forward direction.", "12"],
        ["total_bwd_packets", "Int64", "Total packets transmitted in backward direction.", "8"],
        ["fwd_packet_length_mean", "Float64", "Mean size of packets in forward direction (bytes).", "432.50"],
        ["bwd_packet_length_std", "Float64", "Standard deviation of backward packet lengths.", "189.24"],
        ["flow_iat_mean", "Float64", "Mean inter-arrival time between consecutive packets.", "12,450.8"],
        ["flow_bytes_per_sec", "Float64", "Throughput rate in bytes per second.", "45,120.3"],
        ["fwd_header_length", "Int64", "Total bytes utilized for forward IP headers.", "240"],
        ["init_win_bytes_forward", "Int64", "Initial TCP window advertisement size (bytes).", "29,200"],
        ["Label", "Int64 (Target)", "Binary target: 0 for Benign traffic, 1 for Attack.", "0"]
    ]
    col_w_ds = [1.6, 1.1, 2.6, 1.2]
    create_table(doc, headers_ds, rows_ds, col_w_ds)

def build_section_13_methodology(doc):
    add_h1(doc, "13. Detailed Methodology")
    add_p(doc,
        "The methodological foundation of the Adaptive Human-Review Allocation Framework establishes an end-to-end, mathematically rigorous pipeline for selective error mitigation under temporal distribution shift.")

    add_h2(doc, "13.1 Overall Workflow")
    add_p(doc,
        "The technical workflow proceeds across five sequential stages: (1) Ingestion and chronological 70/15/15 partitioning; (2) Data preprocessing and primary classifier training (XGBoost); (3) Four-factor reliability signal extraction on validation and shifted test splits; (4) Multi-factor composite risk scoring and priority review queue generation across budgets (1%–10%); and (5) Evaluation of review efficiency and dynamic feedback adaptation based on audit outcomes.")

    add_h2(doc, "13.2 Algorithms / Processing Steps")
    add_p(doc,
        "The mathematical formulation governing each reliability signal is defined as follows:",
        bold_prefix="Signal Mathematical Formulations: ")
    
    add_p(doc,
        "1. Confidence Risk (S_conf): Let f(x) denote the predicted class probability P(y=1|x) from the classifier. Confidence is defined as C(x) = max(f(x), 1 - f(x)). The normalized confidence risk is:\n"
        "   S_conf(x) = 1 - C(x)\n"
        "where S_conf(x) ranges from 0.0 (maximum certainty) to 0.5 (maximum ambiguity at boundary).")

    add_p(doc,
        "2. Mahalanobis OOD Distance (S_ood): Let mu denote the empirical mean vector of training features and Sigma denote the regularized covariance matrix (Sigma = Cov(X_train) + epsilon * I, where epsilon = 1e-6). The squared distance is:\n"
        "   D_M^2(x) = (x - mu)^T * Sigma^(-1) * (x - mu)\n"
        "To ensure scale compatibility with other signals, D_M^2 is mapped to its empirical percentile rank over the validation set: S_ood(x) = Percentile(D_M^2(x)) in [0, 1].")

    add_p(doc,
        "3. Feature Drift Magnitude (S_drift): For each numerical feature j, the Population Stability Index (PSI) between training distribution P and validation/test distribution Q over K=10 quantile bins is computed as:\n"
        "   PSI_j = sum_{k=1}^K (Q_jk - P_jk) * ln(Q_jk / P_jk)\n"
        "The composite drift risk for an instance x is computed as the normalized sum of feature deviations weighted by their respective PSI values: S_drift(x) = sum_j (PSI_j * |z_j|) / sum_j PSI_j.")

    add_p(doc,
        "4. Historical Error Proximity (S_hist): Training and validation instances are partitioned into decile bins across key predictive features. The historical error density within the matching feature neighborhood is assigned to instance x, mapped to percentile rank: S_hist(x) = Percentile(ErrorDensity(x)) in [0, 1].")

    add_p(doc,
        "5. Composite Multi-Factor Score: The static multi-factor score is computed as a weighted linear combination:\n"
        "   R_static(x) = w_conf * S_conf(x) + w_ood * S_ood(x) + w_drift * S_drift(x) + w_hist * S_hist(x)\n"
        "where baseline static weights are w_conf=0.40, w_ood=0.15, w_drift=0.20, and w_hist=0.25.")

    add_p(doc,
        "6. Dynamic Feedback Weight Adaptation: Following audit of review batch B, the error concentration gamma is computed as the ratio of reviewed error rate to baseline error rate: gamma = ErrorRate(B) / BaselineError. The historical error weight is updated dynamically:\n"
        "   w_hist' = min(w_hist * (1 + 0.10 * min(gamma, 5.0)), 0.35)\n"
        "The weights are re-normalized such that sum(w_i) = 1.0, and subsequent instances are scored using the updated configuration.")

    add_h2(doc, "13.3 Pseudocode")
    add_p(doc, "Algorithm 1 details the complete algorithmic procedure for multi-factor priority queue allocation and feedback-driven adaptation.")

    pseudo_lines = [
        "Algorithm 1: Adaptive Multi-Factor Human-Review Allocation and Feedback Triage",
        "Input: Test inference set X_test, Trained classifier f(x), Training distribution parameters (mu, Sigma),",
        "       Historical error map H, Review budget fraction B in {0.01, 0.02, 0.05, 0.10}, Heuristic weights w",
        "Output: Priority review queue Q_review, Captured error count E_caught, Updated weights w'",
        "1:  N <- Total instances in X_test;  K <- floor(N * B)",
        "2:  Initialize empty array Scores of length N",
        "3:  For each instance x_i in X_test do:",
        "4:      p_i <- f(x_i)  // Predict posterior probability",
        "5:      S_conf[i] <- 1.0 - max(p_i, 1.0 - p_i)  // Confidence risk",
        "6:      D_sq <- (x_i - mu)^T * Sigma^(-1) * (x_i - mu)",
        "7:      S_ood[i] <- PercentileRank(D_sq, D_validation)  // OOD risk",
        "8:      S_drift[i] <- ComputePSIDriftRisk(x_i, PSI_weights)",
        "9:      S_hist[i] <- LookupHistoricalErrorDensity(x_i, H)",
        "10:     Scores[i] <- w_conf * S_conf[i] + w_ood * S_ood[i] + w_drift * S_drift[i] + w_hist * S_hist[i]",
        "11: End For",
        "12: Sort indices of Scores in descending order: Sorted_Idx <- ArgsortDescending(Scores)",
        "13: Q_review <- {x_j | j in Sorted_Idx[1 : K]}  // Select top-K instances within budget",
        "14: E_caught <- Sum_{j in Q_review} ActualError(x_j)  // Simulated review oracle",
        "15: gamma <- (E_caught / K) / BaselineErrorRate  // Error concentration ratio",
        "16: w_hist_new <- min(w_hist * (1.0 + 0.10 * min(gamma, 5.0)), 0.35)",
        "17: Re-normalize weights w' = {w_conf', w_ood', w_drift', w_hist_new} to sum to 1.0",
        "18: Return Q_review, E_caught, w'"
    ]
    for line in pseudo_lines:
        add_p(doc, line, italic="Algorithm 1" not in line)

def build_section_14_implementation(doc):
    add_h1(doc, "14. Current Implementation")
    add_p(doc,
        "The project has achieved substantial, verifiable implementation progress far exceeding the university's mandatory 50% milestone for Phase-I Review-II.")

    add_h2(doc, "14.1 Current Completion Percentage")
    add_p(doc,
        "Overall Phase-I Implementation Completion: 92.9% (13 of 14 core functional modules fully implemented, verified, and empirically evaluated across 26 sequential Python scripts).",
        bold_prefix="Status: ")

    add_h2(doc, "14.2 Completed Modules")
    add_bullet(doc, "Module 1 (FR1–FR3): Ingestion, SHA-256 verification, chronological splitting, and zero-leakage median imputation.", bold_prefix="1. Data Pipeline: ")
    add_bullet(doc, "Module 2 (FR4): Training and serialization of Logistic Regression, Random Forest, and XGBoost classifiers.", bold_prefix="2. Model Development: ")
    add_bullet(doc, "Module 3 (FR5, FR7, FR9, FR11): Mathematical extraction of all four reliability signals (confidence, Mahalanobis OOD, PSI drift, historical mistakes).", bold_prefix="3. Reliability Engine: ")
    add_bullet(doc, "Module 4 (FR6, FR8, FR10, FR13): Priority queue construction and strategy execution across 1%, 2%, 5%, and 10% review budgets.", bold_prefix="4. Triage Allocator: ")
    add_bullet(doc, "Module 5 (FR12): Shifted test evaluation benchmarking five distinct allocation strategies across 75,000 temporal predictions.", bold_prefix="5. Empirical Benchmarking: ")

    add_h2(doc, "14.3 Modules Under Development")
    add_p(doc,
        "Module 6 (FR14): The interactive Streamlit exploratory analytics dashboard (dashboard/app.py) is fully operational in the local development environment for Review-II demonstration. However, extending the dashboard into a generalized, multi-dataset, production-grade web portal with live SHAP attribution is designated as an ongoing Phase-II deliverable.",
        bold_prefix="Exploratory Dashboard & Web Portal: ")

    add_h2(doc, "14.4 Pending Modules")
    add_p(doc,
        "The following capabilities are formally scheduled for Phase-II: (1) Cross-domain validation across additional tabular datasets; (2) Automated bilevel optimization or reinforcement learning for signal weight discovery; (3) Post-hoc probability calibration (Temperature Scaling); and (4) Live packet stream ingestion.",
        bold_prefix="Future Phase-II Work: ")

    add_h2(doc, "14.5 Implementation Screenshots")
    add_p(doc,
        "Figure 14.1 presents the Module Implementation Status matrix documenting the verified status of all 14 project modules.")
    add_image(doc, os.path.join(BASE_DIR, "diagrams", "v2_module_status.png"),
              "Figure 14.1: Implementation Status Matrix of Core Functional Modules (FR1–FR14).", width=Inches(6.0))
    
    add_p(doc,
        "Figure 14.2 displays the primary empirical results chart comparing the Error Capture Rate across review budgets (1%, 2%, 5%, 10%) for all five evaluation strategies.")
    add_image(doc, os.path.join(BASE_DIR, "results", "error_capture_vs_budget.png"),
              "Figure 14.2: Empirical Comparison of Error Capture Rate vs. Review Budget on Shifted Test Data.", width=Inches(5.8))

    add_p(doc,
        "Figure 14.3 illustrates the top 10 features exhibiting the highest Population Stability Index (PSI) drift under temporal shift.")
    add_image(doc, os.path.join(BASE_DIR, "results", "top10_drift_features.png"),
              "Figure 14.3: Top 10 Network Flow Features Ranked by Population Stability Index (PSI).", width=Inches(5.8))

    add_h2(doc, "14.6 Explanation of Demonstrable Functionality")
    add_p(doc,
        "During the live Phase-I Review-II examination, the following end-to-end functionality can be directly demonstrated from the workspace terminal and browser:",
        bold_prefix="Demonstrable Capabilities: ")
    add_bullet(doc, "Execution of src/25_final_strategy_comparison.py demonstrating instantaneous sub-2-second evaluation of all five review strategies across 75,000 shifted predictions.")
    add_bullet(doc, "Inspection of results/final_shifted_strategy_comparison.csv showing exact error capture counts (e.g., 610 errors at 1% for Feedback Adaptive vs 463 for Confidence).")
    add_bullet(doc, "Live walkthrough of the Streamlit analytics application (dashboard/app.py) demonstrating interactive slider adjustment of review budgets and dynamic rendering of Plotly capture curves.")
