# Final Repository & Architecture Audit

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Candidate:** Karan Shetty | **SRN:** `PES1PG25CA101`  
**Guide:** Dilip Kumar Maripuri  
**Institution:** Department of Computer Applications, PES University, Bengaluru  
**Milestone:** Capstone Review-II Final Audit  
**Approved Academic Status:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**  
**Audit Date:** 2026-10-27  

---

## 1. Repository Inventory & Canonical Entry Points

The repository consists of 30 structured numbered pipeline stages in `src/`, automated pytest suites in `tests/`, research dashboard in `dashboard/`, evaluation artifacts in `results/`, trained models in `models/`, LaTeX source in `PES1PG25CA101-KARANSHETTYKN-Report/`, and documentation in `docs/`.

### Canonical Pipeline Execution Sequence

| Stage | Script Name | Canonical Role | Inputs | Key Generated Outputs | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **01** | `src/01_test_dataset.py` | Dataset verification | `BigFlow_sample.csv` | Console log | Verified |
| **02** | `src/02_create_splits.py` | Chronological 70/15/15 split | `BigFlow_sample.csv` | `results/train.csv`, `val.csv`, `shifted_test.csv` | Verified |
| **03** | `src/03_preprocess.py` | Train-only scaling & imputation | `results/*.csv` | `models/preprocessor.joblib`, `results/X_*.csv` | Verified |
| **04** | `src/04_train_models.py` | Model training & selection | `results/X_train.csv` | `models/xgb_model.joblib`, `model_comparison.csv` | Verified |
| **05** | `src/05_generate_prediction_signals.py` | Validation signal generation | `models/xgb_model.joblib` | `results/validation_signals.csv` | Verified |
| **06** | `src/06_confidence_review_strategy.py` | Baseline confidence triage | Validation signals | `results/confidence_review_results.csv` | Verified |
| **07** | `src/07_ood_detection.py` | Mahalanobis OOD fitting | `X_train.csv`, `X_val.csv` | `results/validation_signals_ood.csv` | Verified |
| **08** | `src/08_ood_review_strategy.py` | OOD-only review strategy | OOD signals | `results/ood_review_results.csv` | Verified |
| **09** | `src/09_static_multifactor_strategy.py` | 3-factor static baseline | Signal CSVs | `results/static_multifactor_results.csv` | Verified |
| **10** | `src/10_measure_drift.py` | Feature-level PSI drift | `X_train.csv`, `X_val.csv` | `results/drift_results.csv` | Verified |
| **11** | `src/11_create_drift_risk.py` | Instance drift-risk mapping | `drift_results.csv` | `results/validation_signals_drift.csv` | Verified |
| **12** | `src/12_adaptive_risk_score.py` | Dynamic risk formulation | Signals | `results/adaptive_risk_signals.csv` | Verified |
| **13** | `src/13_adaptive_review_strategy.py` | Validation adaptive triage | Adaptive signals | `results/adaptive_review_results.csv` | Verified |
| **14** | `src/14_historical_error_risk.py` | $k$-NN error memory index | `X_train.csv`, $E_{\text{train}}$ | `results/validation_signals_historical.csv` | Verified |
| **15** | `src/15_four_factor_risk.py` | 4-factor composite risk | All 4 signals | `results/four_factor_risk_signals.csv` | Verified |
| **16** | `src/16_shifted_test_predictions.py` | Shifted test model inference | `X_shifted_test.csv` | `results/shifted_test_signals.csv` | Verified |
| **17** | `src/17_shifted_test_signals.py` | Shifted test 4 signals | Test predictions & model | `results/shifted_test_all_signals.csv` | Verified |
| **18** | `src/18_shifted_review_comparison.py` | Shifted test strategy eval | Test signals | `results/shifted_review_comparison.csv` | Verified |
| **19** | `src/19_adaptive_shifted_test.py` | Adaptive shifted test eval | Test signals | `results/adaptive_shifted_review_results.csv` | Verified |
| **20** | `src/20_dynamic_adaptive_strategy.py` | Dynamic thresholding eval | Signals | `results/dynamic_adaptive_results.csv` | Verified |
| **21** | `src/21_review_efficiency.py` | Yield curves calculation | Comparison results | `results/review_efficiency.csv` | Verified |
| **22** | `src/22_final_experiment_summary.py` | Initial summary generation | All results | `results/final_experiment_summary.csv` | Verified |
| **23** | `src/23_review_feedback_loop.py` | Validation feedback simulation | Validation signals | `results/review_feedback_results.csv` | Verified |
| **24** | `src/24_shifted_feedback_evaluation.py` | Global 4-factor adaptive eval | `shifted_test_all_signals.csv` | `results/shifted_feedback_adaptive_results.csv` | Verified |
| **25** | `src/25_final_strategy_comparison.py` | Authoritative 5-strategy eval | All shifted results | `results/final_shifted_strategy_comparison.csv` | **Canonical** |
| **26** | `src/26_verify_bigflow_sample.py` | BigFlow schema verification | Raw sample | Console summary | Verified |
| **27** | `src/27_split_audit.py` | Split timestamps & prevalence | `train`, `val`, `test` | `results/split_audit.csv` | **Canonical** |
| **28A**| `src/28_historical_variants.py` | Error memory source comparison | Train vs. Val errors | `results/historical_error_variants.csv` | **Specialized** |
| **28B**| `src/28_sequential_feedback_eval.py` | 5-batch online adaptation | 5 chronological batches | `results/sequential_feedback.csv` | **Specialized** |
| **29** | `src/29_extended_evaluation.py` | PR-AUC, BalAcc, ECE, CIs | Shifted test signals | `extended_model_metrics.csv`, `bootstrap_cis.csv` | **Canonical** |
| **30** | `src/30_verify_results.py` | Single-click benchmark verifier | All result artifacts | Console verification report | **Master Entry** |

---

## 2. Disambiguation of the Two Stage-28 Scripts

The repository intentionally contains two scripts prefixed with `28`, each addressing a distinct mentor research requirement:

1. **`src/28_historical_variants.py` (Historical Memory Source Analysis):**
   - **Research Question:** *"Should historical error memory be computed from Training errors ($E_{\text{train}}$) or Validation errors ($E_{\text{val}}$)?"*
   - **Empirical Evidence:** Using $E_{\text{train}}$ captures **637 errors**, whereas using $E_{\text{val}}$ captures only **5 errors**.
   - **Methodological Cause:** The validation split coincides with a severe attack lull (0.33% prevalence, only 248 attacks total). $E_{\text{val}}$ has insufficient attack failure modes to construct an effective nearest-neighbor memory. $E_{\text{train}}$ contains 21,344 attack flows and 12,392 misclassifications, providing dense coverage of classifier vulnerabilities.

2. **`src/28_sequential_feedback_eval.py` (Five-Batch Online Adaptation):**
   - **Research Question:** *"How does sequential batch review with post-selection label revelation perform under rigid per-batch review quotas?"*
   - **Empirical Evidence:** Evaluates 5 chronological batches of 15,000 flows each with $K_t = 150$ reviews per batch.
   - **Operational Trace:** Demonstrates $w_{\text{hist}}$ dynamically increasing from $0.250 \rightarrow 0.288 \rightarrow 0.331 \rightarrow 0.380 \rightarrow 0.400$, capturing 183 errors total (vs. 161 static and 34 random).

**Recommendation:** Both scripts are preserved with their original filenames to maintain backwards compatibility, with their distinct roles clearly documented in project execution guides.

---

## 3. Discrepancy Resolution: Global 610 Errors vs. Sequential 183 Errors

A critical question raised in the audit is:  
> *"Why does the main benchmark report 610 adaptive captures at a 1% budget, while the sequential 5-batch experiment reports 183 captures at the same nominal 1% budget?"*

### Root Cause Analysis via Data Inspection

1. **Temporal Clustering of Ground-Truth Errors:**
   Across the 75,000 Shifted Test flows, there are 3,427 total classification errors. However, they are **extremely non-uniformly distributed over time**:
   - Batch 1 (Flows 0–15,000): 280 errors (1.87% error rate)
   - Batch 2 (Flows 15,000–30,000): 296 errors (1.97% error rate)
   - Batch 3 (Flows 30,000–45,000): 325 errors (2.17% error rate)
   - Batch 4 (Flows 45,000–60,000): 235 errors (1.57% error rate)
   - **Batch 5 (Flows 60,000–75,000): 2,291 errors (15.27% error rate — the attack wave hits here!)**
   Over **66.8% of all errors** in the shifted test set occur during Batch 5.

2. **Global Pool Ranking (`src/24_shifted_feedback_evaluation.py`):**
   - The entire 75,000-flow test set is ranked globally.
   - The top 750 slots are allocated without batch boundaries.
   - The allocation engine naturally concentrates **719 of the 750 reviews into Batch 5**, capturing 604 errors from Batch 5 alone, plus 6 errors across Batches 1–4, yielding **610 errors total**.
   - *Operational Model:* A retrospective, flexible triage queue where review capacity dynamically surges when threat levels rise.

3. **Sequential Local Batch Quotas (`src/28_sequential_feedback_eval.py`):**
   - The analyst has a **rigid per-batch review capacity** of exactly 150 flows per time window ($K_t = 150$).
   - The analyst is forced to review 150 flows in Batch 1 (where only 280 errors exist), 150 in Batch 2, 150 in Batch 3, 150 in Batch 4, and only 150 in Batch 5 (despite 2,291 errors occurring in Batch 5).
   - Capture totals per batch: $32 + 35 + 38 + 38 + 40 = \mathbf{183\text{ errors}}$.
   - *Operational Model:* A rigid staffing model where an analyst cannot borrow review hours from the past or future.

### Summary Comparison Table

| Feature / Dimension | Main Benchmark (`src/24` & `src/25`) | Sequential 5-Batch Simulation (`src/28_seq`) |
| :--- | :--- | :--- |
| **Operational Paradigm** | Global Retrospective Triage | Rigid Sequential Shift Scheduling |
| **Total Review Budget** | 750 reviews (1% of 75,000) | 750 reviews ($5 \times 150$ reviews per batch) |
| **Batch Allocation Quota** | Dynamic ($1, 2, 4, 24, \mathbf{719}$ reviews) | Fixed ($150, 150, 150, 150, \mathbf{150}$ reviews) |
| **Initial Weights** | $w = (0.35, 0.15, 0.25, 0.25)$ | $w = (0.25, 0.25, 0.25, 0.25)$ |
| **Weight Adaptation** | Pre-tuned heuristic weights | Online feedback boost ($w_{\text{hist}} \rightarrow 0.40$) |
| **Adaptive Errors Caught** | **610 errors (17.80%)** | **183 errors (24.40% batch precision)** |
| **Static Comparator** | 600 errors | 161 errors |
| **Random Comparator** | 40 errors | 34 errors |
| **Relative Gain over Static**| +1.7% | **+13.7%** |
| **Output File** | `final_shifted_strategy_comparison.csv` | `sequential_feedback.csv` |

**Conclusion:** The two numbers represent two distinct, scientifically valid operational protocols. They do not contradict each other; they reflect the difference between dynamic global queue prioritization and rigid per-window review staffing.
