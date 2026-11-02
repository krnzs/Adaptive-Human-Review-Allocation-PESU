# Test & Validation Report

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Candidate:** Karan Shetty (`PES1PG25CA101`)  
**Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  
**Date of Validation:** 2026-10-27  
**Official Status Statement:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**  

---

## 1. Test Execution Summary

The test suite was executed in the project environment (Python 3.13, pytest 8.4) with the command:
```powershell
pytest tests/
```

### Execution Log Output
```
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project
plugins: anyio-4.10.0
collected 16 items

tests\test_evaluation.py ....                                            [ 25%]
tests\test_results_consistency.py ...                                    [ 43%]
tests\test_signals_and_scoring.py .....                                  [ 75%]
tests\test_splits_and_leakage.py ....                                    [100%]

============================= 16 passed in 3.77s ==============================
```

---

## 2. Granular Breakdown of All 16 Test Items

### Module 1: `tests/test_evaluation.py` (Core Review Allocation Logic)
- `test_queue_capacity`: Confirms exact top-$K$ queue sizing across budgets $B \in \{0.01, 0.02, 0.05, 0.10\}$ where $K = \lfloor B \times N \rfloor$. `[PASSED]`
- `test_no_duplicate_indices`: Asserts queue selection contains zero duplicate flow indices even under tied risk scores. `[PASSED]`
- `test_determinism`: Confirms random seed reproducibility under fixed initializations (`random_state=42`). `[PASSED]`
- `test_sequential_no_leakage`: Proves ranking order is strictly invariant to label changes. `[PASSED]`

### Module 2: `tests/test_splits_and_leakage.py` (Dataset Partitioning & Millisecond Boundaries)
- `test_split_sizes_and_prevalences`: Confirms 350,000 training flows (6.10% attacks), 75,000 validation flows (0.33% attacks, 753 errors), and 75,000 shifted test flows (6.30% attacks, 3,427 errors). `[PASSED]`
- `test_chronological_boundaries_no_overlap`: Asserts $T_{\text{train}}^{\max} < T_{\text{val}}^{\min} < T_{\text{val}}^{\max} < T_{\text{test}}^{\min}$ with strict millisecond gaps (+25.0ms gap between Train and Val; +39.0ms gap between Val and Test). `[PASSED]`
- `test_row_level_disjointness_at_boundaries`: Confirms boundary rows (Train[-1] vs. Val[0] and Val[-1] vs. Test[0]) are physically distinct netflow records, differing in IPs, ports, and byte sizes. `[PASSED]`
- `test_no_test_label_leakage_in_ranking`: Asserts ground-truth labels do not influence queue selection. `[PASSED]`

### Module 3: `tests/test_signals_and_scoring.py` (Reliability Signals, Normalization & Bounds)
- `test_signal_ranges_and_bounds`: Confirms uncertainty $u \in [0, 0.50]$, OOD percentile $\in [0, 1.00]$, PSI drift risk $\in [0, 1.00]$, and Historical error percentile $\in [0, 1.00]$. `[PASSED]`
- `test_composite_score_formula_and_upper_bound`: Confirms composite formula $R = 0.35u + 0.15\text{ood} + 0.25\text{drift} + 0.25\text{hist}$ and verifies theoretical maximum score is $0.825$. `[PASSED]`
- `test_signal_correlations`: Confirms OOD vs. Drift Spearman rank correlation is $\rho = 0.8414$ and Uncertainty vs. Historical Error Pearson correlation is $r = 0.5531$. `[PASSED]`
- `test_controlled_uncertainty_scaling_impact`: Proves that current unscaled $u$ captures **610 errors** at 1%, while $2u$ drops to **527 errors** (-13.6%) and rank-normalized $u$ drops to **280 errors** (-54.1%). `[PASSED]`
- `test_sequential_5batch_error_capture`: Confirms sequential 5-batch simulation captures **183 errors** at 1% budget, strictly beating the static comparator (**168 errors**). `[PASSED]`

### Module 4: `tests/test_results_consistency.py` (Approved Benchmarks & Crossover)
- `test_approved_strategy_error_captures`: Asserts all 20 strategy-budget pairs match the approved reference benchmarks:
  - 1% Budget: Random (40), Confidence (463), OOD (1), Static (600), Feedback Adaptive (610). `[PASSED]`
  - 2% Budget: Random (73), Confidence (916), OOD (9), Static (1165), Feedback Adaptive (1174). `[PASSED]`
  - 5% Budget: Random (189), Confidence (2243), OOD (12), Static (1870), Feedback Adaptive (1573). `[PASSED]`
  - 10% Budget: Random (340), Confidence (2879), OOD (12), Static (2242), Feedback Adaptive (1794). `[PASSED]`
- `test_honest_crossover_behavior`: Asserts Adaptive strictly outperforms Confidence at 1% and 2%, while Confidence strictly outperforms Adaptive at 5% and 10%. `[PASSED]`
- `test_extended_metrics_and_bootstrap_cis`: Asserts PR-AUC (0.7444), Balanced Accuracy (0.7321), ECE (0.0200), and 1% bootstrap CI [+3.45%, +5.28%]. `[PASSED]`

---

## 3. Dedicated Master Verification: `src/30_verify_results.py`

Command executed:
```powershell
python src/30_verify_results.py
```
Output:
```
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
