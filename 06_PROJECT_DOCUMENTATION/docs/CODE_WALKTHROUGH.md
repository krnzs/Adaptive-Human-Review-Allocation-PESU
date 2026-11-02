# Code Walkthrough & Source Inventory Guide

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  

This document provides a line-by-line and module-by-module walkthrough of the primary source files in `src/`, their execution dependencies, inputs, outputs, and critical mathematical sections.

---

## 1. Data Ingestion & Preprocessing Pipeline

### `src/01_test_dataset.py`
- **Purpose:** Verifies that the raw dataset file `BigFlow_sample.csv` exists, checks header columns, and validates sample count (500,000 flows).
- **Inputs:** `BigFlow_sample.csv` (in project root or `data/`).
- **Outputs:** Console verification message.

### `src/02_create_splits.py`
- **Purpose:** Performs chronological sorting and creates the non-overlapping 70/15/15 train/validation/test partitions.
- **Inputs:** `BigFlow_sample.csv`.
- **Main Logic:**
  - `df['Timestamp'] = pd.to_datetime(df['Timestamp'])`
  - `df = df.sort_values(by='Timestamp')`
  - Slices indices: `0:350000` (Train), `350000:425000` (Val), `425000:500000` (Shifted Test).
- **Outputs Generated:** `results/train.csv`, `results/validation.csv`, `results/shifted_test.csv`.
- **Before Editing:** Do not alter the chronological sorting or split boundaries; doing so invalidates temporal realism and changes attack prevalences.

### `src/03_preprocess.py`
- **Purpose:** Imputes missing values and standardizes numeric feature distributions.
- **Inputs:** `results/train.csv`, `results/validation.csv`, `results/shifted_test.csv`.
- **Main Logic:**
  - `scaler = StandardScaler()`
  - `scaler.fit(X_train)` (Fitted strictly on training data).
  - `X_val_scaled = scaler.transform(X_val)`
  - `X_test_scaled = scaler.transform(X_test)`
- **Outputs Generated:** `models/preprocessor.joblib`, `results/X_train.csv`, `results/X_validation.csv`, `results/X_shifted_test.csv`, and corresponding `y_*.csv`.
- **Before Editing:** Never call `scaler.fit()` on validation or test sets; that would introduce feature distribution leakage.

---

## 2. Supervised Model Training & Signal Engines

### `src/04_train_models.py`
- **Purpose:** Trains and benchmarks XGBoost, Random Forest, and Logistic Regression on training NetFlow traffic.
- **Inputs:** `results/X_train.csv`, `results/y_train.csv`.
- **Main Logic:** Fits models with `random_state=42`, evaluates validation metrics, and selects XGBoost as champion based on F1-score (0.912).
- **Outputs Generated:** `models/xgb_model.joblib`, `results/model_comparison.csv`.

### `src/05_generate_prediction_signals.py`
- **Purpose:** Computes model prediction probabilities, confidence, uncertainty, and entropy on validation traffic.
- **Key Formula:** `uncertainty = 1.0 - np.maximum(prob_0, prob_1)`
- **Outputs Generated:** `results/validation_signals.csv`.

### `src/07_ood_detection.py`
- **Purpose:** Computes Mahalanobis out-of-distribution distance to the training distribution centroid.
- **Inputs:** `models/xgb_model.joblib`, `results/X_train.csv`, `results/X_validation.csv`.
- **Outputs Generated:** `results/validation_signals_ood.csv`.

### `src/10_measure_drift.py` & `src/11_create_drift_risk.py`
- **Purpose:** Calculates Population Stability Index (PSI) per feature between training reference bins and evaluation data, then maps instance-level drift risk.
- **Outputs Generated:** `results/drift_results.csv`, `results/validation_signals_drift.csv`.

### `src/14_historical_error_risk.py`
- **Purpose:** Extracts misclassified training samples $E_{\text{train}}$ and indexes them using a nearest-neighbor tree to score proximity of new flows to known failure modes.
- **Outputs Generated:** `results/validation_signals_historical.csv`.

### `src/15_four_factor_risk.py`
- **Purpose:** Integrates the four reliability signals into the static composite risk score:
  $$R(\mathbf{x}) = 0.35 \cdot u + 0.15 \cdot \text{OOD} + 0.25 \cdot \text{Drift} + 0.25 \cdot \text{Hist}$$
- **Outputs Generated:** `results/four_factor_risk_signals.csv`.

---

## 3. Shifted Test Set Evaluation & Benchmarking

### `src/16_shifted_test_predictions.py` & `src/17_shifted_test_signals.py`
- **Purpose:** Executes the full inference and reliability signal extraction pipeline across all 75,000 Shifted Test flows.
- **Outputs Generated:** `results/shifted_test_all_signals.csv` (14 columns including all raw and percentile-ranked signals).

### `src/25_final_strategy_comparison.py`
- **Purpose:** Evaluates all five review strategies (Random, OOD-Only, Confidence-Only, Static Multi-Factor, Feedback-Adaptive) across 1%, 2%, 5%, and 10% review budgets.
- **Outputs Generated:** `results/final_shifted_strategy_comparison.csv`.
- **Key Assertions:** Confirms 610 errors at 1% budget, 1,174 at 2%, 2,243 at 5%, 2,879 at 10%, and demonstrates the honest crossover.

### `src/27_split_audit.py`
- **Purpose:** Audits partition boundaries, timestamps, sample counts, attack prevalences, and confusion matrices.
- **Outputs Generated:** `results/split_audit.csv`.

### `src/28_historical_variants.py`
- **Purpose:** Compares alternative sources for historical error memory (Training vs. Validation vs. Out-of-Fold errors).
- **Core Finding:** Training errors yield 637 captured errors; validation errors yield only 5 errors due to the 0.33% validation attack lull.

### `src/28_sequential_feedback_eval.py`
- **Purpose:** Simulates the 5-batch online review process (15,000 flows / batch, 150 reviews / batch) with post-selection label revelation and dynamic $w_{\text{hist}}$ boosting.
- **Outputs Generated:** `results/sequential_feedback.csv`.

### `src/29_extended_evaluation.py`
- **Purpose:** Computes advanced statistical metrics (PR-AUC 0.7444, Balanced Acc 0.7321, ECE 0.0200), 1,000-resample bootstrap confidence intervals, signal correlation matrices, and leave-one-out ablations.
- **Outputs Generated:** `results/extended_model_metrics.csv`, `results/extended_bootstrap_cis.csv`, `results/extended_evaluation.md`.

### `src/30_verify_results.py`
- **Purpose:** Master verification script for mentors and evaluators. Directly checks all 20 benchmark allocations and statistical metrics with automated pass/fail console assertions.

---

## 4. Dashboard & User Interface

### `dashboard/app.py`
- **Purpose:** Interactive Streamlit operational research dashboard.
- **Features:** Budget slider, strategy multiselect filter, efficiency curve, drift ranking, four signals inspection cards, sequential feedback trace, and downloadable CSV exports.
- **Execution Command:** `streamlit run dashboard/app.py`.
- **Backup Copy:** `dashboard/app_legacy.py` preserves the earlier dashboard version.
