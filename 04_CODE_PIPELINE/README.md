# CODE PIPELINE ARCHITECTURE & EXECUTION GUIDE

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Guide:** Dilip Kumar Maripuri  
**Department of Computer Applications, PES University, Bengaluru**  

---

## 1. Pipeline Location & Zero-Breakage Design

The canonical executable Python scripts reside directly in the root directory under **`src/`**.

> **Why `src/` is maintained at root:**  
> The machine learning pipeline relies on relative file paths to read and write models (`models/`), raw datasets (`BigFlow_sample.csv`), and output CSV results (`results/`). Preserving `src/` directly at the repository root guarantees zero path breakage, 100% test compatibility (`pytest tests/`), and clean CLI invocation.

---

## 2. Complete 30-Stage Execution Flow

The ML pipeline is cleanly structured into 30 numbered stages executed sequentially:

```
STAGE   SCRIPT FILENAME                       PURPOSE & INPUT/OUTPUT
─────────────────────────────────────────────────────────────────────────────────────────────────
01      src/01_load_and_sample.py             Loads BigFlow_sample.csv (500k flows) & parses features.
02      src/02_temporal_split.py              Performs chronological splitting: Train (350k), Val (75k), Test (75k).
03      src/03_leakage_audit.py               Audits timestamp boundaries (+25ms, +39ms gaps) & verifies zero duplicates.
04      src/04_feature_engineering.py         Extracts network flow features (rates, durations, byte counts).
05      src/05_train_baseline_model.py        Trains the baseline XGBoost classifier on training split only.
06      src/06_evaluate_baseline.py           Computes baseline metrics on Val (0.33% attacks) and Test (6.30% attacks).
07      src/07_calibrate_probabilities.py     Calibrates probabilities via isotonic regression and computes ECE.
08      src/08_compute_uncertainty.py         Calculates margin uncertainty u = 1 - max(P0, P1) in [0, 0.50].
09      src/09_train_mahalanobis_ood.py       Fits empirical covariance & centroid on training embeddings.
10      src/10_compute_ood_scores.py          Computes Mahalanobis OOD distance and percentile rank z_ood in [0, 1].
11      src/11_compute_psi_drift.py           Calculates Population Stability Index (PSI) drift across features.
12      src/12_compute_slice_errors.py        Calculates historical error risk per flow feature slice z_hist.
13      src/13_merge_all_signals.py           Merges all 4 signals into shifted_test_all_signals.csv.
14      src/14_signal_correlation_audit.py    Computes Spearman/Pearson inter-signal correlations.
15      src/15_signal_weight_optimization.py  Optimizes composite scoring weights (w_u=0.35, w_ood=0.15, w_psi=0.25, w_hist=0.25).
16      src/16_generate_composite_scores.py   Generates composite review score R for shifted test samples.
17      src/17_budget_triage_simulation.py    Simulates review allocation at 1%, 2%, 5%, and 10% budgets.
18      src/18_benchmark_strategies.py        Evaluates Random, Confidence, OOD, Static Multi-Factor, and Adaptive.
19      src/19_crossover_analysis.py          Analyzes the Honest Crossover (Adaptive wins at <=2%, Confidence at >=5%).
20      src/20_bootstrap_significance.py      Computes 1,000 paired bootstrap resamples (95% CI: [+3.45%, +5.28%], p < 0.001).
21      src/21_signal_ablation_study.py       Conducts leave-one-signal-out ablation experiments.
22      src/22_uncertainty_scaling_study.py   Evaluates unscaled u vs 2*u vs rank-normalization (610 vs 527 vs 280).
23      src/23_temporal_batch_split.py        Splits shifted test into 5 sequential chronological batches (15k flows each).
24      src/24_sequential_feedback_sim.py     Simulates online feedback where audited samples reveal labels forward in time.
25      src/25_online_weight_adaptation.py    Updates signal weights dynamically across batches (183 vs 168 static comparator).
26      src/26_generate_evaluation_tables.py  Formats authoritative CSV result tables in results/.
27      src/27_generate_evaluation_figures.py Generates high-resolution PNG plots in results/ and diagrams/.
28_seq  src/28_sequential_feedback_eval.py    Evaluates batch-constrained triage yield (24.40% vs 22.40%).
28_stat src/28_statistical_tests.py          Calculates PR-AUC (0.7444), Balanced Acc (0.7321), and ECE (0.0200).
29      src/29_export_report_metrics.py       Exports LaTeX and Markdown metric macros for documentation.
30      src/30_verify_results.py              Authoritative verifier: checks all 6 research invariants.
DEMO    src/run_demo_batch.py                 Interactive CLI live demo script for viva presentation.
─────────────────────────────────────────────────────────────────────────────────────────────────
```

---

## 3. How to Execute & Verify

All commands should be executed from the root directory:

```powershell
# Run the complete test suite:
pytest tests/

# Run the authoritative invariant verification check:
python src/30_verify_results.py

# Run a live batch demonstration:
python src/run_demo_batch.py
```
