# Comprehensive Feature Traceability Matrix

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  
**Official Status:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**  

---

## 1. Traceability Matrix

| ID | Feature Description | Status | Primary Source Files | How to Demonstrate | How to Test | Scope Category |
| :---: | :--- | :---: | :--- | :--- | :--- | :---: |
| **FR01** | **Chronological Splitting:** 70/15/15 non-overlapping partitions ordered by timestamp | **Completed** | `src/02_create_splits.py`, `src/27_split_audit.py` | Run `python src/27_split_audit.py` to view timestamps and prevalences | `pytest tests/test_splits_and_leakage.py::test_split_sizes_and_prevalences` | Core Phase-I |
| **FR02** | **Leakage-Free Preprocessing:** Standardizer and imputer fitted strictly on training data | **Completed** | `src/03_preprocess.py`, `models/preprocessor.joblib` | Inspect `models/preprocessor.joblib` and training fitting logs | `pytest tests/test_splits_and_leakage.py::test_no_test_label_leakage_in_ranking` | Core Phase-I |
| **FR03** | **Supervised Base Models:** XGBoost champion, Random Forest, Logistic Regression | **Completed** | `src/04_train_models.py`, `models/xgb_model.joblib` | View validation F1-scores in `results/model_comparison.csv` | `python src/30_verify_results.py` | Core Phase-I |
| **FR04** | **Uncertainty Signal Engine:** Probability margin $u = 1 - \max(P_0, P_1) \in [0, 0.50]$ | **Completed** | `src/05_generate_prediction_signals.py`, `src/17_shifted_test_signals.py` | Open `dashboard/app.py` Four Signals expander | `pytest tests/test_signals_and_scoring.py::test_signal_ranges_and_bounds` | Core Phase-I |
| **FR05** | **Confidence Review Strategy:** Triage lowest-confidence predictions first | **Completed** | `src/06_confidence_review_strategy.py`, `src/25_final_strategy_comparison.py` | Select 'Confidence' in Dashboard budget explorer | `pytest tests/test_results_consistency.py::test_approved_strategy_error_captures` | Core Phase-I |
| **FR06** | **Mahalanobis OOD Engine:** Covariance distance to in-distribution training centroid | **Completed** | `src/07_ood_detection.py`, `src/17_shifted_test_signals.py` | Inspect `ood_percentile` in `results/shifted_test_all_signals.csv` | `pytest tests/test_signals_and_scoring.py::test_signal_ranges_and_bounds` | Core Phase-I |
| **FR07** | **OOD Review Strategy:** Triage highest OOD distance instances | **Completed** | `src/08_ood_review_strategy.py`, `src/25_final_strategy_comparison.py` | Compare OOD vs. Random in Dashboard bar chart | `pytest tests/test_results_consistency.py::test_approved_strategy_error_captures` | Core Phase-I |
| **FR08** | **Feature PSI Drift Scoring:** Population Stability Index on NetFlow features | **Completed** | `src/10_measure_drift.py`, `results/drift_results.csv` | View Top Shifted Features horizontal chart in Dashboard | `python src/30_verify_results.py` | Core Phase-I |
| **FR09** | **Instance Drift Risk Mapping:** Cumulative quantile deviation mapping | **Completed** | `src/11_create_drift_risk.py`, `src/17_shifted_test_signals.py` | Inspect `drift_risk` column in `results/shifted_test_all_signals.csv` | `pytest tests/test_signals_and_scoring.py::test_signal_ranges_and_bounds` | Core Phase-I |
| **FR10** | **Historical Error Memory:** $k$-NN distance to misclassified training samples | **Completed** | `src/14_historical_error_risk.py`, `src/28_historical_variants.py` | Run `python src/28_historical_variants.py` to compare Train vs. Val | `pytest tests/test_signals_and_scoring.py::test_signal_correlations` | Core Phase-I |
| **FR11** | **Static Multi-Factor Strategy:** Convex four-signal combination with fixed weights | **Completed** | `src/15_four_factor_risk.py`, `src/25_final_strategy_comparison.py` | Select 'Static_MultiFactor' in Dashboard | `pytest tests/test_signals_and_scoring.py::test_composite_score_formula_and_upper_bound` | Core Phase-I |
| **FR12** | **Multi-Budget Comparative Benchmarking:** Evaluation at 1%, 2%, 5%, 10% | **Completed** | `src/25_final_strategy_comparison.py` | Drag budget slider in Dashboard to observe crossover | `pytest tests/test_results_consistency.py::test_honest_crossover_behavior` | Core Phase-I |
| **FR13** | **Sequential Simulated Feedback:** 5-batch online review, post-selection labels, weight updates | **Completed** | `src/28_sequential_feedback_eval.py` | Expand Sequential Feedback panel in Dashboard | `python src/28_sequential_feedback_eval.py` | Core Phase-I |
| **FR14** | **Multi-Dataset Web Portal & Cross-Domain Deployment** | **Partially Implemented** | `dashboard/app.py` | Run `streamlit run dashboard/app.py` (Local interactive portal for NF-UQ-NIDS-v2) | `python -m py_compile dashboard/app.py` | 92.9% Progress (Cloud multi-tenancy & cross-domain in Phase-II) |

---

## 2. Statistical Metrics & Verification Assertions

| Evaluation Metric | Benchmark Target | Actual Verified Result | Verification Script | Pytest Suite |
| :--- | :---: | :---: | :--- | :--- |
| **Shifted Test Total Errors** | 3,427 errors | **3,427 errors** | `src/30_verify_results.py` | `tests/test_splits_and_leakage.py` |
| **Validation Total Errors** | 753 errors | **753 errors** | `src/30_verify_results.py` | `tests/test_splits_and_leakage.py` |
| **Error Rate Surge Ratio** | 4.55x | **4.55x (4.569% vs 1.004%)** | `src/27_split_audit.py` | `tests/test_splits_and_leakage.py` |
| **1% Adaptive Error Capture** | 610 errors (17.80%) | **610 errors (17.80%)** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **1% Confidence Error Capture** | 463 errors (13.51%) | **463 errors (13.51%)** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **1% Bootstrap 95% Confidence Interval** | [+3.45%, +5.28%] | **[+3.45%, +5.28%]** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **5% Confidence Error Capture (Crossover)** | 2,243 errors (65.45%) | **2,243 errors (65.45%)** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **10% Confidence Error Capture (Crossover)**| 2,879 errors (84.01%) | **2,879 errors (84.01%)** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **Shifted Test PR-AUC** | 0.7444 | **0.7444** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **Shifted Test Balanced Accuracy** | 0.7321 | **0.7321** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **Expected Calibration Error (ECE)** | 0.0200 | **0.0200** | `src/30_verify_results.py` | `tests/test_results_consistency.py` |
| **OOD vs. Drift Spearman Correlation** | 0.8414 | **0.8414** | `src/29_extended_evaluation.py` | `tests/test_signals_and_scoring.py` |
| **Uncertainty vs. Hist Error Pearson Correlation** | 0.5531 | **0.5531** | `src/29_extended_evaluation.py` | `tests/test_signals_and_scoring.py` |
| **Historical Error Ablation (1% Budget)** | 25 errors (0.73%) | **25 errors (0.73%)** | `src/29_extended_evaluation.py` | `docs/PROJECT_STATUS.md` |
