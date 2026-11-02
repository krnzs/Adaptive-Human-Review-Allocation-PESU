# PRESENTATION-3 ACTUAL PROJECT IMPLEMENTATION AUDIT

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Prof. Dilip Kumar Maripuri  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Department & Institution:** Department of Computer Applications, PES University, Bengaluru  
**Audit Standard:** Strict Forensic Source Code & Result Verification  
**Audit Date:** 2026-11-02  

---

## 1. Executive Summary of Codebase & Test Verification

This audit examines the actual physical source code in `src/`, automated tests in `tests/`, trained models in `models/`, serialized results in `results/`, and the dashboard in `dashboard/` to verify that the project meets and exceeds the PES University Presentation-3 requirement of **at least 80% implementation**.

### Authoritative Verification Commands & Real Execution Outcomes:

#### A. Automated Test Suite (`pytest tests/`)
```powershell
PS C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project> pytest tests/
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project
plugins: anyio-4.10.0
collected 16 items

tests\test_evaluation.py ....                                            [ 25%]
tests\test_results_consistency.py ...                                    [ 43%]
tests\test_signals_and_scoring.py .....                                  [ 75%]
tests\test_splits_and_leakage.py ....                                    [100%]

============================= 16 passed in 8.82s ==============================
```
- **Outcome:** **16 of 16 tests PASSED (100% pass rate, 0 failures, 0 warnings)**.
- **Coverage:** Data split sizes, temporal disjointness, absence of target leakage, signal value ranges, composite score upper bound ($R \le 0.825$), budget slicing quotas, and five-strategy error consistency.

#### B. Canonical Result Invariant Engine (`python src/30_verify_results.py`)
```powershell
PS C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project> python src/30_verify_results.py
================================================================================
  PES UNIVERSITY MCA CAPSTONE -- AUTHORITATIVE RESULT VERIFICATION
  Student: Karan Shetty (PES1PG25CA101) | Guide: Dilip Kumar Maripuri
  Project: Adaptive Human-Review Allocation Under Distribution Shift
================================================================================

[1] Verifying Five-Strategy Review Allocations (final_shifted_strategy_comparison.csv):
  [PASS] Budget  1.0% | Random               ->   40 errors ( 1.17%)
  [PASS] Budget  1.0% | Confidence           ->  463 errors (13.51%)
  [PASS] Budget  1.0% | OOD                  ->    1 errors ( 0.03%)
  [PASS] Budget  1.0% | Static_MultiFactor   ->  600 errors (17.51%)
  [PASS] Budget  1.0% | Feedback_Adaptive    ->  610 errors (17.80%)
  [PASS] Budget  2.0% | Random               ->   73 errors ( 2.13%)
  [PASS] Budget  2.0% | Confidence           ->  916 errors (26.73%)
  [PASS] Budget  2.0% | OOD                  ->    9 errors ( 0.26%)
  [PASS] Budget  2.0% | Static_MultiFactor   -> 1165 errors (33.99%)
  [PASS] Budget  2.0% | Feedback_Adaptive    -> 1174 errors (34.26%)
  [PASS] Budget  5.0% | Random               ->  189 errors ( 5.52%)
  [PASS] Budget  5.0% | Confidence           -> 2243 errors (65.45%)
  [PASS] Budget  5.0% | OOD                  ->   12 errors ( 0.35%)
  [PASS] Budget  5.0% | Static_MultiFactor   -> 1870 errors (54.57%)
  [PASS] Budget  5.0% | Feedback_Adaptive    -> 1573 errors (45.90%)
  [PASS] Budget 10.0% | Random               ->  340 errors ( 9.92%)
  [PASS] Budget 10.0% | Confidence           -> 2879 errors (84.01%)
  [PASS] Budget 10.0% | OOD                  ->   12 errors ( 0.35%)
  [PASS] Budget 10.0% | Static_MultiFactor   -> 2242 errors (65.42%)
  [PASS] Budget 10.0% | Feedback_Adaptive    -> 1794 errors (52.35%)

[2] Verifying Honest Crossover Behavior:
  [PASS] 1% Budget: Adaptive (610) strictly beats Confidence (463) [+31.7% gain]
  [PASS] 5% Budget: Honest Crossover confirmed -> Confidence (2243) beats Adaptive (1573)

[3] Verifying Extended Statistical Metrics (extended_model_metrics.csv):
  [PASS] Shifted Test PR-AUC         -> 0.7444 (matches benchmark 0.7444)
  [PASS] Shifted Test Balanced Acc    -> 0.7321 (matches benchmark 0.7321)
  [PASS] Shifted Test ECE             -> 0.0200 (matches benchmark 0.0200)
  [PASS] 1% Budget 95% Bootstrap CI  -> [+3.45%, +5.28%] (matches [+3.45%, +5.28%], p < 0.001)

[4] Verifying Data Split Integrity & Millisecond Boundaries (split_audit.csv):
  [PASS] Train partition:      350,000 flows (6.10% attacks) | Errors: 12,392 (3.54%)
  [PASS] Validation partition:  75,000 flows (0.33% attacks) | Errors:    753 (1.00%)
  [PASS] Shifted Test set:      75,000 flows (6.30% attacks) | Errors:  3,427 (4.57%)
  [PASS] Temporal Shift Surge: Test error rate is 4.55x higher than validation (4.57% vs 1.00%)
  [PASS] Boundary Train->Val:  Strict +25.0ms gap (Train strictly BEFORE Validation)
  [PASS] Boundary Val->Test:   Strict +39.0ms gap (Validation strictly BEFORE Test)

[5] Verifying Controlled Uncertainty Normalization Impact (1% Budget):
  [PASS] Variant 1 (Current unscaled u in [0, 0.50]): 610 errors caught (17.80%)
  [PASS] Variant 2 (Linear 2*u in [0, 1.00]):         527 errors caught (15.38%) [-13.6% degradation]
  [PASS] Variant 3 (Rank-normalized in [0, 1.00]):    280 errors caught ( 8.17%) [-54.1% degradation]
  [PASS] Mathematical scaling justification confirmed: unscaled u prevents false-alarm flooding.

[6] Verifying Sequential 5-Batch Online Feedback (sequential_feedback.csv):
  [PASS] Sequential Adaptive (5 batches x 150 reviews): 183 errors caught (24.40% yield)
  [PASS] Static Comparator (equal weights):             168 errors caught (22.40% yield)
  [PASS] Sequential Adaptive beats static comparator (+15 additional errors caught)

================================================================================
  OVERALL VERIFICATION STATUS: [SUCCESS] ALL 6 INVARIANTS CONFIRMED
  Academic Status:
  '13 of 14 functional requirements are fully implemented;
   FR14 is partially implemented (92.9% fully implemented).'
================================================================================
```
- **Exit Code:** **0 (Clean verification)**.

#### C. User Interface Verification (`dashboard/app.py`)
- Python AST syntax parse: **Clean, 0 errors**.
- Streamlit application executes on `http://localhost:8501` rendering capacity sliders, crossover charts, signal distribution plots, and sequential feedback weight traces.

---

## 2. Requirement-by-Requirement Implementation Traceability

| FR ID | Requirement Name | Expected Functionality | Actual Source Code File | Test & Verification Evidence | Status |
|:---:|:---|:---|:---|:---|:---:|
| **FR01** | Raw Ingestion & Integrity | Ingest 500k flows from BigFlow-NIDS; verify schema & SHA-256 fingerprint against 14GB source. | `src/01_test_dataset.py`, `src/26_verify_bigflow_sample.py` | `BigFlow_sample.csv` (91.2MB, 500k rows) verified identical to raw partition. | **FULLY IMPLEMENTED** |
| **FR02** | Chronological Partitioning | Sort by flow timestamp; split into 70% Train (350k), 15% Val (75k), 15% Shifted Test (75k). | `src/02_create_splits.py`, `src/02_temporal_split.py` | `tests/test_splits_and_leakage.py::test_split_sizes_and_prevalences` passed. | **FULLY IMPLEMENTED** |
| **FR03** | Zero-Leakage Controls | Enforce strict forward time gaps and verify zero duplicate rows across partitions. | `src/03_leakage_audit.py`, `src/03_preprocess.py` | `tests/test_splits_and_leakage.py` (+25.0ms, +39.0ms gaps, 0 duplicates confirmed). | **FULLY IMPLEMENTED** |
| **FR04** | Base Model Training | Train supervised XGBoost classifier, Random Forest, and Logistic Regression on Train split only. | `src/04_train_models.py`, `src/05_train_baseline_model.py` | `models/xgboost.pkl` (Val ROC-AUC = 0.9228, Test ROC-AUC = 0.9510). | **FULLY IMPLEMENTED** |
| **FR05** | Prediction Signal Extraction | Extract prediction probability $P(y \vert x)$, confidence, and Shannon entropy. | `src/05_generate_prediction_signals.py`, `src/16_shifted_test_predictions.py` | `results/extended_model_metrics.csv` (Val ECE = 0.0120, Test ECE = 0.0200). | **FULLY IMPLEMENTED** |
| **FR06** | Confidence Review Strategy | Implement Least-Confidence review allocation across 1%, 2%, 5%, 10% budgets. | `src/06_confidence_review_strategy.py`, `src/08_compute_uncertainty.py` | `tests/test_evaluation.py::test_confidence_strategy_allocations` passed (463 errs @ 1%). | **FULLY IMPLEMENTED** |
| **FR07** | Mahalanobis OOD Distance | Compute regularized Mahalanobis distance relative to 50k training reference flows. | `src/07_ood_detection.py`, `src/09_train_mahalanobis_ood.py` | `results/shifted_test_all_signals.csv` (`ood_percentile` in $[0, 1.00]$). | **FULLY IMPLEMENTED** |
| **FR08** | Feature Drift Scoring (PSI) | Measure 10-bin Population Stability Index across 49 features; identify high drift features. | `src/10_measure_drift.py`, `src/11_compute_psi_drift.py` | `results/drift_results.csv` (7 features with PSI $\ge 0.10$, SHORTEST_PKT=0.766). | **FULLY IMPLEMENTED** |
| **FR09** | Historical Error Proximity | Partition feature space into 10 deciles based on training mistakes to score mistake risk. | `src/14_historical_error_risk.py`, `src/12_compute_slice_errors.py` | `results/shifted_test_all_signals.csv` (`historical_error_risk` in $[0, 1.00]$). | **FULLY IMPLEMENTED** |
| **FR10** | Composite Risk Scoring | Synthesize 4 signals: $R = 0.35u + 0.15s_{\text{ood}} + 0.25s_{\text{drift}} + 0.25s_{\text{hist}} \le 0.825$. | `src/15_four_factor_risk.py`, `src/16_generate_composite_scores.py` | `tests/test_signals_and_scoring.py` ($R \in [0, 0.825]$ strictly bounded). | **FULLY IMPLEMENTED** |
| **FR11** | Review Budget Slicing | Rank composite scores; enforce hard capacity quotas $K = \lfloor B \cdot N \rfloor$ for $B \in \{1\%, 2\%, 5\%, 10\%\}$. | `src/17_budget_triage_simulation.py`, `src/20_shifted_budget_allocation.py` | `tests/test_evaluation.py::test_budget_quotas_and_slicing` passed. | **FULLY IMPLEMENTED** |
| **FR12** | Strategy Benchmarking | Benchmark Random, Confidence, OOD, Static Multi-Factor, and Feedback Adaptive. | `src/18_benchmark_strategies.py`, `src/25_final_strategy_comparison.py` | `results/final_shifted_strategy_comparison.csv` (All 20 allocations verified). | **FULLY IMPLEMENTED** |
| **FR13** | Sequential Feedback Adaptation | 5-batch sequential review with post-selection label revelation and dynamic weight updates. | `src/23_review_feedback_loop.py`, `src/24_sequential_feedback_sim.py` | `results/sequential_feedback.csv` (183 errors / 24.40% yield vs 168 / 22.40% static). | **FULLY IMPLEMENTED** |
| **FR14** | Interactive Web Dashboard | Provide interactive UI with budget sliders, strategy comparison, and flow inspection. | `dashboard/app.py` | Streamlit application operational for Phase-I; multi-dataset cloud ingestion deferred to Phase-II. | **PARTIALLY IMPLEMENTED** |

---

## 3. Detailed Verification of the 16 Algorithmic Pipeline Steps

The system implementation maps 1:1 to the 16-step pseudocode presented in Slide 17 of the presentation:

### Phase 1: Ingestion & Baseline Calibration (Steps 1–5)
- **Step 1:** Ingest 500,000 NetFlow records from BigFlow-NIDS (`src/01_test_dataset.py`, verified file size 91.2 MB).
- **Step 2:** Sort chronologically by `flow_start_time` without dropping records.
- **Step 3:** Split into Train (350k, 70%), Val (75k, 15%), Shifted Test (75k, 15%) (`src/02_create_splits.py`).
- **Step 4:** Fit median imputer and StandardScaler strictly on Train partition (`src/03_preprocess.py`).
- **Step 5:** Train baseline XGBoost classifier (ROC-AUC = 0.9228); fit reference covariance matrix ($\lambda = 10^{-4}$ Tikhonov regularization); map training mistake deciles.

### Phase 2: Signal Extraction (Steps 6–10)
- **Step 6:** Compute class posteriors $P_i = f_\theta(x_i)$ for shifted test flows ($N = 75,000$).
- **Step 7:** Calculate margin uncertainty $s_{\text{conf}} = 1 - \max(P_i, 1 - P_i) \in [0.0, 0.50]$.
- **Step 8:** Compute regularized Mahalanobis distance $d_M(x_i)$ relative to 50k training reference samples; transform to percentile rank $s_{\text{ood}} \in [0, 1]$.
- **Step 9:** Compute 10-bin Population Stability Index across 49 features; weight per-instance z-score deviations to produce $s_{\text{drift}} \in [0, 1]$.
- **Step 10:** Query nearest feature mistake decile to retrieve historical mistake risk $s_{\text{hist}} \in [0, 1]$.

### Phase 3: Risk Fusion & Budget Allocation (Steps 11–13)
- **Step 11:** Compute composite risk score $R_i = \sum_{j=1}^4 w_j s_{j,i}$ with $\sum w_j = 1.0$ and $R_{\max} = 0.825$.
- **Step 12:** Sort instances descending by composite risk $R_i$: $\text{Indices} = \text{argsort}(R)$.
- **Step 13:** Slice top-$K$ instances into review queue $\mathcal{Q}_{\text{review}}$ for $K = \lfloor B \cdot N \rfloor$ ($B \in \{1\%, 2\%, 5\%, 10\%\}$); dispatch remaining $N - K$ to autonomous decision.

### Phase 4: Simulated Oracle & Feedback Adaptation (Steps 14–16)
- **Step 14:** Query test ground-truth labels for instances in $\mathcal{Q}_{\text{review}}$ (simulating expert human audit without live subjects).
- **Step 15:** Compute Error Capture Rate $\text{ECR} = (\text{CaughtErrors} / 3,427) \times 100\%$ and Review Efficiency.
- **Step 16:** In feedback adaptive mode, scale historical error weight based on reviewed error concentration: $w_4 = \min(0.40, w_4 \times 1.15)$; re-normalize $\sum w = 1.0$ forward in time.

---

## 4. Implementation Percentage Calculation

### Official Functional Requirements Score:
- Total functional requirements defined in specification: **14**
- Fully implemented requirements: **13** (FR01 through FR13 = 100% complete)
- Partially implemented requirements: **1** (FR14 = ~50% complete)

$$\text{Strict Fully Implemented Rate} = \frac{13}{14} \times 100\% = \mathbf{92.86\%} \approx \mathbf{92.9\%}$$

$$\text{Approved Weighted Implementation Score} = \frac{13 + 0.50}{14} \times 100\% = \frac{13.5}{14} \times 100\% = \mathbf{96.43\%} \approx \mathbf{96.4\%}$$

### Compliance with PES University Milestone Threshold:
- **University Requirement for Presentation-3:** **Minimum 80% implementation** (with 100% as the maximum expected level).
- **Our Verified Implementation Level:** **92.9% fully implemented** (or **96.4% weighted**).
- **Audit Finding:** The actual codebase comfortably exceeds the university's 80% threshold by **+12.9 percentage points** (strict) and **+16.4 percentage points** (weighted).
- **Official Preserved Statement:**
  > **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**
