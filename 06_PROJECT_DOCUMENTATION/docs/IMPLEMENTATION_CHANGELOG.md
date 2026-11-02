# Implementation Changelog

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`)  
**Institution:** PES University, Department of Computer Applications  
**Guide:** Dilip Kumar Maripuri  
**Status Statement:** “13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”  

---

## Change Record: 2026-10-27

### 1. Verification & Diagnostics Suite (`src/30_verify_results.py`)
- **Action:** Created new authoritative verification module `src/30_verify_results.py`.
- **Rationale:** Mentors required independent execution proof for all reported benchmarks (total 3,427 errors, all 20 budget-strategy allocations, PR-AUC 0.7444, Balanced Acc 0.7321, ECE 0.0200, 95% bootstrap CI [+3.45%, +5.28%], and chronological split boundaries).
- **Files Affected:** `src/30_verify_results.py` (New).
- **Execution Evidence:** Command `python src/30_verify_results.py` exits 0 with all 20 benchmark combinations passed.

### 2. Comprehensive Pytest Test Suite (`tests/`)
- **Action:** Extended test suite from 4 synthetic mock tests to 13 rigorous, verified assertions.
- **Files Created:**
  - `tests/test_splits_and_leakage.py`: Asserts partition counts (350K/75K/75K), attack prevalences (6.10%/0.33%/6.30%), strictly ordered timestamps ($T_{\text{train}}^{\max} \le T_{\text{val}}^{\min} < T_{\text{val}}^{\max} \le T_{\text{test}}^{\min}$), and label invariance during queue ranking.
  - `tests/test_signals_and_scoring.py`: Asserts uncertainty range $u \in [0, 0.50]$, OOD, Drift, and Historical Error percentiles in $[0, 1.00]$, composite score upper bound $0.825$, and empirical signal correlations ($\rho = 0.8414$, $r = 0.5531$).
  - `tests/test_results_consistency.py`: Asserts exact error counts across all strategies and budgets, the honest crossover behavior, PR-AUC, Balanced Accuracy, ECE, and bootstrap confidence intervals.
- **Files Preserved:** `tests/test_evaluation.py` (preserved intact).
- **Execution Evidence:** `pytest tests/` runs in 5.66s, 13 passed, 0 failed.

### 3. Interactive Research Dashboard Upgrade (`dashboard/app.py`)
- **Action:** Upgraded Streamlit operational dashboard while preserving original version as `dashboard/app_legacy.py`.
- **Enhancements:**
  - Dynamically loads `results/final_shifted_strategy_comparison.csv` to ensure displayed table matches approved reference benchmarks (610 errors / 17.80% at 1% budget).
  - Added multiselect strategy filter for custom strategy comparisons.
  - Added expandable 4-Signal Diagnostic Panel explaining mathematical ranges ($u \in [0, 0.50]$ vs. percentile signals in $[0, 1.00]$).
  - Added interactive Sequential 5-Batch Online Adaptation Trace visualizing error capture per batch and historical error weight updates ($w_{\text{hist}} = 0.25 \rightarrow 0.40$).
  - Added direct CSV export button via `st.download_button`.
  - Embedded explicit academic notices clarifying offline simulation scope and zero-leakage constraints.
- **Compilation Evidence:** `python -m py_compile dashboard/app.py` exits 0.

### 4. Preservation of Core Experimental Data & Pipelines
- **Preserved Artifacts:** All existing models (`models/xgb_model.joblib`, `models/preprocessor.joblib`), raw results (`results/final_shifted_strategy_comparison.csv`, `results/extended_model_metrics.csv`, `results/extended_bootstrap_cis.csv`, `results/split_audit.csv`), and numbered pipeline scripts (`src/01_...` to `src/29_...`) were preserved intact.
- **Zero Fabrication:** No experimental numbers were altered, synthesized, or forced.
