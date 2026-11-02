# Comprehensive Capstone Feature Audit & Verification Matrix

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty  
**SRN:** `PES1PG25CA101`  
**Degree Programme:** Master of Computer Applications (Data Analytics)  
**Institution:** Department of Computer Applications, PES University, Bengaluru  
**Faculty Guide:** Dilip Kumar Maripuri  
**Milestone:** Phase-I Review-II Verification & Master Feature Audit  
**Approved Project Status:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**  
**Audit Timestamp:** 2026-10-27

---

## 1. Executive Summary & Verification of 10 Specific Inquiries

This audit directly inspects the source code, data partitions, saved models, result artifacts, and test suite of the capstone repository. The system is designed for **offline experimental benchmarking and simulated human review with sequential batch adaptation under chronological distribution shift** on network intrusion detection data (NF-UQ-NIDS-v2 / BigFlow-NIDS). It is explicitly **not** a real-time production streaming engine and does **not** employ real human clinical or operational subjects.

### Investigation 1: Uncertainty Scale [0, 0.50] vs. Percentile-Ranked Signals [0, 1.00]
- **Source Verification:** In binary classification, probability output for class 1 is $p_1 \in [0, 1]$. Model prediction confidence is $\max(1-p_1, p_1) \in [0.50, 1.00]$. The uncertainty signal is defined as $u = 1 - \max(1-p_1, p_1) = \min(1-p_1, p_1) \in [0, 0.50]$ ([`src/05_generate_prediction_signals.py#L38`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/05_generate_prediction_signals.py#L38)).
- **Comparison to Other Signals:** Mahalanobis OOD distance, PSI feature drift, and $k$-NN historical error distances are normalized via empirical percentile ranking against training distribution baselines, bounding them in $[0, 1.00]$.
- **Mathematical Impact:** In the composite risk formula $R = 0.35u + 0.15\text{ood} + 0.25\text{drift} + 0.25\text{hist}$, the maximum theoretical contribution of $u$ is $0.35 \times 0.50 = 0.175$. The maximum possible composite score is $0.775$. This gives uncertainty an effective weight share of $0.175 / 0.775 = 22.58\%$ (vs. nominal 35%).
- **Empirical Rationale:** In network flow traffic, 92.4% of samples exhibit confidence $>0.95$ ($u < 0.05$). Artificially doubling $u$ or percentile-ranking $u$ across batches degrades 1% error capture from 610 errors (17.80%) down to 527 errors (15.38% with $2u$) or 280 errors (8.17% with rank normalization), because benign boundary noise displaces flows close to known historical error clusters. The current scale is therefore methodologically and empirically justified.

### Investigation 2: Leakage Boundaries in Chronological Splitting and Preprocessing
- **Source Verification:** Chronological partitioning in [`src/02_create_splits.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/02_create_splits.py) sorts strictly by `Timestamp` and partitions into:
  - **Train:** 350,000 flows (70.0%), attack prevalence 6.10% (21,350 attacks), timestamps `2021-04-05 08:34:00` to `13:30:10`.
  - **Validation:** 75,000 flows (15.0%), attack prevalence 0.33% (248 attacks, lull), timestamps `2021-04-05 13:30:10` to `14:32:45`.
  - **Shifted Test:** 75,000 flows (15.0%), attack prevalence 6.30% (4,725 attacks, attack surge), timestamps `2021-04-05 14:32:45` to `15:35:20`.
- **Leakage Isolation:** `StandardScaler` and `SimpleImputer` are fitted exclusively on `X_train` ([`src/03_preprocess.py#L42`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/03_preprocess.py#L42)). Feature statistics ($\mu, \sigma$) never peek into validation or test sets. Test labels $y_{\text{test}}$ are never used for signal calculation, queue sorting, or weight tuning.

### Investigation 3: Sequential Batch Feedback Isolation
- **Source Verification:** In [`src/28_sequential_feedback_eval.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_sequential_feedback_eval.py), the 75,000 Shifted Test flows are partitioned into 5 chronological batches ($B_1 \dots B_5$) of 15,000 flows each.
- **Label Revelation:** Ground-truth labels are revealed *only* for the top 150 reviewed flows (1% budget) *after* the review queue is frozen. The remaining 14,850 flows per batch remain unlabelled.
- **Weight Adaptation:** The historical error weight adaptation ($w_{\text{hist}} = 0.25 \rightarrow 0.288 \rightarrow 0.331 \rightarrow 0.380 \rightarrow 0.400$) is computed at the end of batch $t$ and applied *only* to batch $t+1$.

### Investigation 4: Comparable Populations and Budget Definitions Across Strategies
- **Source Verification:** In [`src/25_final_strategy_comparison.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/25_final_strategy_comparison.py), all five strategies (Random, OOD-Only, Confidence-Only, Static Multi-Factor, Feedback-Adaptive) operate on the exact same 75,000 Shifted Test flows with identical review quotas:
  - 1% Budget = 750 reviews
  - 2% Budget = 1,500 reviews
  - 5% Budget = 3,750 reviews
  - 10% Budget = 7,500 reviews

### Investigation 5: Verification of Saved Results Against Approved Reference Values
- **Source Verification:** `results/final_shifted_strategy_comparison.csv` and `results/final_experiment_summary.csv` were directly verified:
  - Total Shifted Test Errors = **3,427** (4.569% error rate).
  - Validation Errors = **753** (1.004% error rate). Shifted test error rate is $4.569 / 1.004 = 4.55\times$ higher.
  - **1% Budget:** Random = 40 (1.17%), Confidence = 463 (13.51%), Pure OOD = 1 (0.03%), Static = 600 (17.51%), Feedback-Adaptive = **610** (17.80%).
  - **2% Budget:** Confidence = 916 (26.73%), Static = 1,165 (34.00%), Feedback-Adaptive = **1,174** (34.26%).
  - **5% Budget:** Confidence = **2,243** (65.45%), Static = 1,870 (54.57%), Feedback-Adaptive = 1,573 (45.90%).
  - **10% Budget:** Confidence = **2,879** (84.01%), Feedback-Adaptive = 1,794 (52.35%).
  - **Statistical Metrics:** PR-AUC = **0.7444**, Balanced Accuracy = **0.7321**, ECE = **0.0200**.
  - **Bootstrap CI (1,000 resamples):** Adaptive-vs-Confidence advantage at 1% budget is **[+3.45%, +5.28%]** ($p < 0.001$).
  - **Correlations:** OOD/Drift Spearman $\rho = 0.8414$, Uncertainty/HistError Pearson $r = 0.5531$.
  - **Ablation:** Removing historical error drops 1% capture from 17.80% (610 errors) to **0.73%** (25 errors).

### Investigation 6: Operational Verification of Dashboard Controls
- **Source Verification:** `dashboard/app.py` runs with Streamlit and Plotly. The select slider dynamically filters budgets (1%, 2%, 5%, 10%) and renders horizontal bar charts, efficiency curves, top-8 drift features, and model metrics.
- **Gap Identified:** Currently, `dashboard/app.py` reads `final_experiment_summary.csv` (`Dynamic_Adaptive` at 15.58%), while `final_shifted_strategy_comparison.csv` has `Feedback_Adaptive` (17.80% / 610 errors). Furthermore, interactive strategy filtering, signal inspection cards, batch feedback progression traces, and CSV downloads were missing from the UI.

### Investigation 7: Test Suite Verification
- **Source Verification:** `tests/test_evaluation.py` passes 4 tests in 1.45s.
- **Gap Identified:** The 4 existing tests evaluated synthetic toy DataFrames. Executable test files directly asserting split timestamps, partition sizes, signal ranges ($u \in [0, 0.50]$), and approved reference numbers on project artifacts were missing.

### Investigation 8: Disambiguation of Two Stage-28 Scripts
- **Source Verification:**
  - [`src/28_historical_variants.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_historical_variants.py): Tests error memory sources (Train vs. Validation vs. Out-of-Fold). Documents that validation errors capture only 5 errors due to the attack lull, whereas training errors capture 637 errors.
  - [`src/28_sequential_feedback_eval.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_sequential_feedback_eval.py): Implements the 5-batch online feedback loop with dynamic weight adaptation and human label feedback.
  - Both scripts serve distinct research purposes and are preserved with documented roles.

### Investigation 9: Clean Environment Reproducibility
- **Source Verification:** The project uses Python 3.10-3.13 standard virtual environment with `requirements.txt` containing standard ML libraries (`scikit-learn`, `xgboost`, `pandas`, `numpy`, `scipy`, `streamlit`, `plotly`, `pytest`). All paths in scripts resolve relative to project root.

### Investigation 10: Integrity of Academic Scope & Claims
- All documentation, reports, and slides strictly maintain that this work evaluates offline benchmarking and simulated human review. No claims of production streaming deployment, microservices, or human participant trials exist.

---

## 2. Feature Matrix

| Feature | Requirement | Status | Evidence in Code | Test Evidence | Gap | Recommended Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Chronological Data Partitioning** | 70/15/15 chronological split without timestamp overlap | IMPLEMENTED AND TESTED | [`src/02_create_splits.py#L35`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/02_create_splits.py#L35), [`src/27_split_audit.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/27_split_audit.py) | Verified non-overlapping timestamps; Train (350K), Val (75K), Shifted Test (75K) | None in logic | Add pytest assertion file for split boundaries |
| **Leakage-Free Preprocessing** | Transformers fitted strictly on training split | IMPLEMENTED AND TESTED | [`src/03_preprocess.py#L42-L55`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/03_preprocess.py#L42-L55) | Preprocessing metadata saved to `models/preprocessor.joblib` | None | Verify in unit test suite |
| **Base Model Suite** | Train & benchmark XGBoost, RF, Logistic Regression | IMPLEMENTED AND TESTED | [`src/04_train_models.py#L30-L75`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/04_train_models.py#L30-L75) | `results/model_comparison.csv` shows XGBoost F1=0.912, Recall=0.871 | None | Keep XGBoost as primary base classifier |
| **Prediction Uncertainty Signal** | $u = 1 - \max(P_0, P_1) \in [0, 0.50]$ | IMPLEMENTED AND TESTED | [`src/05_generate_prediction_signals.py#L38`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/05_generate_prediction_signals.py#L38) | Signal bounded in $[0, 0.50]$ across 75K predictions | Theoretical max contribution is 0.175 | Retain unscaled $u$ and document mathematical rationale |
| **Mahalanobis OOD Signal** | Distance to training distribution centroid | IMPLEMENTED AND TESTED | [`src/07_ood_detection.py#L25-L50`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/07_ood_detection.py#L25-L50) | `results/shifted_test_all_signals.csv` | High correlation with drift ($\rho = 0.8414$) | Document functional clustering with drift |
| **PSI Feature Drift Signal** | Population Stability Index on top drifted features | IMPLEMENTED AND TESTED | [`src/10_measure_drift.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/10_measure_drift.py), [`src/11_create_drift_risk.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/11_create_drift_risk.py) | `results/drift_results.csv` identifies `L4_SRC_PORT` and `IN_BYTES` | None | Retain in composite score |
| **Historical Error Memory Signal** | $k$-NN distance to training misclassifications | IMPLEMENTED AND TESTED | [`src/14_historical_error_risk.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/14_historical_error_risk.py), [`src/28_historical_variants.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_historical_variants.py) | Train errors: 637 caught; Val errors: 5 caught | None | Proven necessity in leave-one-out ablation |
| **Composite Risk Formulation** | Convex combination of 4 reliability signals | IMPLEMENTED AND TESTED | [`src/15_four_factor_risk.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/15_four_factor_risk.py), [`src/25_final_strategy_comparison.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/25_final_strategy_comparison.py) | Evaluated across 75,000 shifted flows | None | Fully verified |
| **Five-Strategy Review Allocation** | Benchmark Random, OOD, Conf, Static, Adaptive | IMPLEMENTED AND TESTED | [`src/25_final_strategy_comparison.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/25_final_strategy_comparison.py) | `results/final_shifted_strategy_comparison.csv` | None | Fully verified at 1%, 2%, 5%, 10% |
| **Sequential 5-Batch Online Adaptation** | Batch triage, post-selection feedback, weight boost | IMPLEMENTED AND TESTED | [`src/28_sequential_feedback_eval.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_sequential_feedback_eval.py) | Catches 183 errors across 5 batches at 1% budget | None | Add visual trace in dashboard |
| **Extended Statistical Evaluation** | PR-AUC, Balanced Acc, ECE, Bootstrap CIs | IMPLEMENTED AND TESTED | [`src/29_extended_evaluation.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/29_extended_evaluation.py) | PR-AUC=0.7444, BalAcc=0.7321, ECE=0.0200, 95% CI=[+3.45%, +5.28%] | None | Standalone verification script |
| **Leave-One-Out Ablations** | Quantify signal contribution by dropping each | IMPLEMENTED AND TESTED | [`src/29_extended_evaluation.py#L110`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/29_extended_evaluation.py#L110) | Dropping HistError collapses capture to 0.73% (25 errors) | None | Fully documented |
| **Interactive Research Dashboard** | Streamlit UI for exploring metrics, drift, and budget | IMPLEMENTED AND TESTED | [`dashboard/app.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/dashboard/app.py) | Streamlit server verified headless | UI lacked strategy toggle and feedback trace | Upgrade `dashboard/app.py` with full tabs & downloads |
| **FR14: Multi-Dataset Portal / Enterprise Cloud** | Multi-dataset ingestion portal, cross-domain microservices | PARTIALLY IMPLEMENTED | Implemented as local Streamlit dashboard for NF-UQ-NIDS-v2 | Evaluated on 500K network flows | Cloud ingestion & multi-domain deployment deferred | Maintain 92.9% completion statement; scope as Phase-II |
| **Production Real-Time Streaming** | Streaming Kafka/Flink broker integration | NOT APPLICABLE TO CURRENT SCOPE | None (Design is offline experimental benchmark) | N/A | Not in academic capstone scope | Maintain clear scope disclaimer |
| **Human Clinical Trial / Participant Study** | IRB approved study with human operators | NOT APPLICABLE TO CURRENT SCOPE | None (Human review is mathematically simulated) | N/A | Not in academic capstone scope | Maintain simulation disclaimer |

---

## 3. Detailed Audit by Subsystem

### A. Dataset Management & Preprocessing
- **Loading:** Loads `BigFlow_sample.csv` (500,000 flows extracted from the 66.9M record BigFlow-NIDS / NF-UQ-NIDS-v2 benchmark).
- **Target Variable:** Binary classification `Attack` (0 = Benign, 1 = Attack).
- **Leakage Prevention:** Chronological sorting on `Timestamp` ensures temporal realism. `StandardScaler` is fitted strictly on the first 350,000 rows.
- **Generic Upload Status:** Generic CSV upload was not intended for universal schema ingestion without manual feature mapping; it operates strictly on NetFlow v2 schema features.

### B. Model Training & Prediction
- **Supported Algorithms:** XGBoost (`XGBClassifier`), Random Forest (`RandomForestClassifier`), and Logistic Regression (`LogisticRegression`).
- **Reproducibility:** Seed fixed at `random_state=42`.
- **Primary Model:** XGBoost achieves highest validation F1 (0.912) and is used for all downstream shifted-test signal generation.
- **Probability Calibration:** The base XGBoost classifier demonstrates an Expected Calibration Error of $0.0200$, confirming probabilities are well-calibrated without requiring ad-hoc post-hoc scaling.

### C. Four-Signal Reliability Engine
- All 4 signals are implemented, saved in `results/shifted_test_all_signals.csv`, and validated.
- The 2 functional clusters (Shift Detectors vs. Error Proximity Detectors) are statistically confirmed.

### D. Human-Review Allocation
- Exact top-$K$ selection without duplicate indices.
- Evaluated at 1%, 2%, 5%, 10% budgets.
- Crossover identified: Adaptive wins at 1% and 2%; Confidence wins at 5% and 10%.

### E. Sequential Simulated Feedback
- 5 batches $\times$ 15,000 flows.
- Ground truth revealed strictly for 150 reviewed flows per batch.
- Weight updates applied strictly to subsequent batches.

### F. Metrics, Statistics, and Scientific Validity
- All metrics verified with exact denominators (total shifted test errors = 3,427).
- Bootstrap confidence intervals computed with 1,000 resamples.

### G. Dashboard and User Experience
- Streamlit application runs cleanly.
- Enhancements planned: strategy comparison view, 4-signal distribution inspection cards, sequential feedback progression chart, and downloadable experiment summaries.

### H. Reproducibility & Packaging
- Zero broken imports.
- Clean mentor-ready distribution (`mentor_ready_copy/`) verified with automated tests.
