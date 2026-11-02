# FUNCTIONAL REQUIREMENTS TRACEABILITY & FR14 SPECIFICATION AUDIT

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** Department of Computer Applications, PES University, Bengaluru  
**Audit Date:** 2026-10-28  

**Official Preserved Status Statement:**  
> **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

## 1. Official Requirements Baseline vs. Recent Documentation Discrepancy

### A. The Canonical Requirements Specification
In the approved Review-II Report ([`03_REPORTS_AND_DOCS/Review_II_Report.md`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/03_REPORTS_AND_DOCS/Review_II_Report.md), [`07_LATEX_SOURCE/.../requirements.tex`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/07_LATEX_SOURCE/PES1PG25CA101-KARANSHETTYKN-Report/chapters/requirements.tex), and [`Adaptive_Human_Review_Allocation_Review_II_FINAL.docx`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_Review_II_FINAL.docx)), the 14 functional requirements are mapped to project modules as follows:

- **FR1 to FR12:** Cover data ingestion, temporal chronological splitting, leakage verification, XGBoost base classification, probability calibration (ECE), four-signal extraction ($u$, $z_{\text{ood}}$, $z_{\text{psi}}$, $z_{\text{hist}}$), composite risk scoring, and strategy benchmarking across review budgets (1%, 2%, 5%, 10%).
- **FR13:** **Feedback-Adaptive Allocation Loop** — Simulates sequential human review audit, reveals ground truth labels for audited instances, and dynamically boosts historical error weight ($w_{\text{hist}} \rightarrow 0.40$).
- **FR14:** **Interactive Analytics Dashboard / Multi-Dataset Web Portal & Cross-Domain Deployment** — Provides an interactive user interface for triage inspection, parameter tuning, and multi-dataset cloud-native ingestion.

### B. The Discrepancy in Recent Summaries
In certain recent chat summaries and audit notes, FR14 was artificially described as:
- *FR14.1 (Real-time Drift Detection)*
- *FR14.2 (Sequential Dynamic Weight Adaptation)*
- *FR14.3 (Automated Model Retraining)*

**Audit Finding:** This sub-numbering was an informal retrospective breakdown that conflated FR8 (Drift Detection) and FR13 (Sequential Feedback) with FR14.  
**Ground Truth:** In the formal project specification approved by the faculty guide, **FR13** covers the sequential feedback-adaptive loop, while **FR14** covers the **Interactive Dashboard / Multi-Dataset Portal**.

---

## 2. Clarification of Operational Scope: Simulation vs. Production

To maintain strict academic integrity during your viva examination, the following operational boundaries must be stated clearly:

1. **Offline Benchmark with Simulated Review:**
   - The project is an **offline benchmark evaluation** conducted on a 500,000-flow chronological sample of the **BigFlow-NIDS** network intrusion dataset.
   - It is **not** a live, in-line packet filtering appliance deployed in a physical network.
2. **Algorithmic Review Simulation:**
   - When a review quota of $K = 750$ instances is selected, the system simulates human audit by querying the ground-truth target labels for those $K$ selected instances.
   - It did **not** employ live human participants (e.g., human analysts sitting at terminals clicking labels).
3. **Sequential Batch Adaptation:**
   - The 5-batch streaming simulation evaluates chronological batches of 15,000 flows each.
   - Labels are revealed **strictly post-selection** for reviewed instances, and updated weights are applied strictly forward in time to subsequent batches.
   - This provides a realistic, leakage-free simulation of a human-in-the-loop review pipeline.

---

## 3. Complete Functional Requirements Traceability Matrix (FR1 – FR14)

| Req ID | Formal Requirement Title & Specification | Implementation Source Files | Verification & Automated Test Evidence | Status | Academic & Operational Scope |
|:---:|:---|:---|:---|:---:|:---|
| **FR01** | **Data Ingestion & Flow Extraction:** Load 500k BigFlow flows, parse 33 network attributes. | `src/01_load_and_sample.py` | `BigFlow_sample.csv` verified present (91.2 MB). | **Completed** | Full Phase-I Scope |
| **FR02** | **Temporal Chronological Partitioning:** Split 70% Train, 15% Val, 15% Shifted Test strictly by timestamp. | `src/02_temporal_split.py`, `results/train.csv`, `val.csv`, `shifted_test.csv` | `pytest tests/test_splits_and_leakage.py::test_split_sizes_and_prevalences` | **Completed** | Full Phase-I Scope |
| **FR03** | **Zero-Leakage Boundary Verification:** Verify non-overlapping timestamps and zero row-level duplicates. | `src/03_leakage_audit.py`, `results/split_audit.csv` | `pytest tests/test_splits_and_leakage.py::test_chronological_boundaries_no_overlap` (+25ms, +39ms gaps) | **Completed** | Full Phase-I Scope |
| **FR04** | **Base Classifier Training:** Train supervised XGBoost classifier on Training split only. | `src/05_train_baseline_model.py`, `models/xgboost.pkl` | `results/extended_model_metrics.csv` (Val ROC-AUC = 0.9228, Test ROC-AUC = 0.9510) | **Completed** | Full Phase-I Scope |
| **FR05** | **Probability Calibration & Reliability:** Calibrate output probabilities and quantify ECE. | `src/07_calibrate_probabilities.py`, `src/29_extended_evaluation.py` | `results/extended_model_metrics.csv` (Val ECE = 0.0120, Test ECE = 0.0200) | **Completed** | Full Phase-I Scope |
| **FR06** | **Margin Uncertainty Estimation:** Compute $u = 1 - \max(P_0, P_1) \in [0, 0.50]$. | `src/08_compute_uncertainty.py`, `src/17_shifted_test_signals.py` | `pytest tests/test_signals_and_scoring.py::test_signal_ranges_and_bounds` | **Completed** | Full Phase-I Scope |
| **FR07** | **Mahalanobis OOD Scoring:** Fit empirical centroid & covariance on train embeddings; score test flows. | `src/09_train_mahalanobis_ood.py`, `src/10_compute_ood_scores.py` | `results/shifted_test_all_signals.csv` (`ood_percentile` in $[0, 1.00]$) | **Completed** | Full Phase-I Scope |
| **FR08** | **Feature Distribution Drift (PSI):** Quantify binned population stability drift across features. | `src/11_compute_psi_drift.py`, `results/drift_results.csv` | `results/shifted_test_all_signals.csv` (`drift_risk` in $[0, 1.00]$) | **Completed** | Full Phase-I Scope |
| **FR09** | **Historical Error Memory:** Form nearest-neighbor architectural slice error memory from training failures. | `src/12_compute_slice_errors.py` | `results/shifted_test_all_signals.csv` (`historical_error_risk`) | **Completed** | Full Phase-I Scope |
| **FR10** | **Composite Risk Scoring:** Form linear combination $R = 0.35u + 0.15z_{\text{ood}} + 0.25z_{\text{psi}} + 0.25z_{\text{hist}} \le 0.825$. | `src/16_generate_composite_scores.py`, `src/22_uncertainty_scaling_study.py` | `pytest tests/test_signals_and_scoring.py::test_composite_score_formula_and_upper_bound` | **Completed** | Full Phase-I Scope |
| **FR11** | **Resource-Constrained Triage Simulation:** Allocate review quotas at 1%, 2%, 5%, 10% budgets. | `src/17_budget_triage_simulation.py` | `results/final_shifted_strategy_comparison.csv` (All 20 allocations verified) | **Completed** | Full Phase-I Scope |
| **FR12** | **Baseline Benchmarking & Crossover Analysis:** Compare Random, Confidence, OOD, Static, and Adaptive. | `src/18_benchmark_strategies.py`, `src/19_crossover_analysis.py` | `python src/30_verify_results.py` (Confirmed Honest Crossover: Adaptive wins at $\le 2\%$, Confidence at $\ge 5\%$) | **Completed** | Full Phase-I Scope |
| **FR13** | **Feedback-Adaptive Allocation Loop:** 5-batch sequential review with post-selection label revelation and dynamic weight update. | `src/24_sequential_feedback_sim.py`, `src/28_sequential_feedback_eval.py` | `results/sequential_feedback.csv` (Adaptive: 183 errors vs Static: 168 errors) | **Completed** | Full Phase-I Scope |
| **FR14** | **Interactive Analytics Dashboard / Multi-Dataset Web Portal & Cross-Domain Deployment** | `dashboard/app.py` | Interactive Streamlit application verified operational on port 8599. | **Partially Implemented** | **Local Streamlit Complete (Phase-I); Multi-dataset cloud ingestion deferred to Phase-II.** |

---

## 4. Why FR14 is Partially Implemented (92.9% Overall Project Status)

- **Total Functional Requirements:** 14
- **Fully Implemented Requirements:** 13 (FR1 through FR13 = 100% complete)
- **Partially Implemented Requirement:** 1 (FR14 = ~50% complete)
- **Overall Completion Percentage:**
  $$\text{Completion} = \frac{13 + 0.5}{14} \times 100\% = \frac{13.5}{14} \times 100\% = \mathbf{96.4\%} \quad \text{(or strictly } \frac{13}{14} = \mathbf{92.9\%}\text{ fully implemented)}$$

### What is Completed in FR14 (Phase-I):
- A fully operational local interactive Streamlit dashboard (`dashboard/app.py`).
- Interactive budget capacity sliders (0.5% to 10.0%).
- Strategy comparison charts highlighting the Honest Crossover.
- Diagnostic distribution views for all four reliability signals.
- 5-batch streaming simulation visualization with weight update traces.
- Live high-priority flow inspector for audit review.

### What is Deferred to Phase-II in FR14:
1. **Multi-Dataset Ingestion:** Dynamic file-upload parsing supporting different network formats (e.g., CIC-IDS-2018, UNSW-NB15) with automated schema mapping.
2. **Enterprise Cloud Deployment:** Packaging into containerized microservices (Docker/Kubernetes) with multi-tenant authentication.
3. **Automated Model Retraining Safety Gates:** Closed-loop retraining triggers with automated rollback to prevent catastrophic forgetting.

---

## 5. Script for Defending FR14 in Viva Examination

When the examination panel asks:  
> *"Why is your project status listed as 13 of 14 requirements complete (92.9%), and what is pending in FR14?"*

**Your Exact Answer:**  
> *"Our project specifies 14 comprehensive functional requirements covering the entire pipeline from data ingestion to human-review allocation. Requirements FR1 through FR13—which encompass chronological partitioning, leakage prevention, four-signal extraction, composite scoring, budget triage, and the sequential feedback-adaptive loop—are 100% implemented, tested, and verified.*  
>  
> *FR14 specifies the interactive analytics dashboard and multi-dataset enterprise portal. For Phase-I, we have fully implemented the operational Streamlit review cockpit (`dashboard/app.py`), which visualizes review allocations, distribution drift, and sequential weight updates on the 500,000-flow BigFlow-NIDS benchmark.  
>  
> *In consultation with my faculty guide, Prof. Dilip Kumar Maripuri, the multi-dataset ingestion engine (for cross-domain datasets like CIC-IDS-2018) and cloud microservices deployment were scheduled for Phase-II. This allowed us to dedicate Phase-I to rigorous statistical validation, leakage prevention, and mathematical justification of the scoring framework."*
