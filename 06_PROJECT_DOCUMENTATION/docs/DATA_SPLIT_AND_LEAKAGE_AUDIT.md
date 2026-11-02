# Data Split Integrity & Data Leakage Prevention Audit

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  
**Date of Audit:** 2026-10-27  

---

## 1. Split Boundary Timestamp & Disjointness Analysis

### The "Shared Timestamp" Question Resolved
In previous summaries and high-level reports, the partition boundaries were reported with seconds rounded (e.g., `16:22:36` and `17:01:20`), creating the appearance that adjacent splits shared boundary timestamps.  
A forensic millisecond inspection of the underlying NetFlow timestamp column (`FLOW_START_MILLISECONDS` and `timestamp`) resolves this:

```
[Partition 1: Training Set]
  Row Count:        350,000 flows (70.0%)
  Min Timestamp:    2019-04-23 14:09:50.632 (1556028590632 ms)
  Max Timestamp:    2019-04-23 16:22:35.978 (1556036555978 ms)
  Attack Flows:     21,344 (6.098% attack prevalence)
  Errors Made:      12,392 (3.541% error rate: 4,302 FP, 8,090 FN)

                      ▲
                      │  [Strict Gap: +25.0 milliseconds]
                      ▼

[Partition 2: Validation Set]
  Row Count:        75,000 flows (15.0%)
  Min Timestamp:    2019-04-23 16:22:36.003 (1556036556003 ms)
  Max Timestamp:    2019-04-23 17:01:20.431 (1556038880431 ms)
  Attack Flows:     248 (0.331% attack prevalence -- natural attack lull)
  Errors Made:      753 (1.004% error rate: 527 FP, 226 FN)

                      ▲
                      │  [Strict Gap: +39.0 milliseconds]
                      ▼

[Partition 3: Shifted Test Set]
  Row Count:        75,000 flows (15.0%)
  Min Timestamp:    2019-04-23 17:01:20.470 (1556038880470 ms)
  Max Timestamp:    2019-04-24 03:27:14.233 (1556076434233 ms)
  Attack Flows:     4,724 (6.299% attack prevalence -- attack wave surge)
  Errors Made:      3,427 (4.569% error rate: 960 FP, 2,467 FN)
```

### Key Empirical Findings
1. **Strict Monotonic Ordering:**
   $$T_{\text{train}}^{\max} (16:22:35.978) < T_{\text{val}}^{\min} (16:22:36.003) < T_{\text{val}}^{\max} (17:01:20.431) < T_{\text{test}}^{\min} (17:01:20.470)$$
   There is a genuine +25 ms gap between Train and Validation, and a +39 ms gap between Validation and Shifted Test. Timestamps are **strictly non-overlapping**.
2. **Row Disjointness:**
   - Train[-1] and Val[0] differ in **13 of 56 columns** (source IP, destination IP, ports, byte sizes, throughput, timestamps). They are distinct network flows.
   - Val[-1] and Test[0] differ in **7 of 56 columns** (different ports, destination IPs, protocol, timestamps).
3. **Zero Duplicate Rows:**
   - Train internal duplicates: **0**
   - Validation internal duplicates: **0**
   - Shifted Test internal duplicates: **0**
   - Across-split duplicate overlap: **0**

---

## 2. Comprehensive Data Leakage Barrier Audit

| Pipeline Layer | Potential Leakage Vector | Implemented Defense Mechanism | Evidence in Code | Verification Status |
| :--- | :--- | :--- | :--- | :---: |
| **Splitting** | Future-to-past information leakage | Strict chronological ordering by `FLOW_START_MILLISECONDS` before index slicing | `src/02_create_splits.py#L35` | Verified |
| **Imputation** | Median/mean calculated across test data | `SimpleImputer.fit()` called strictly on `X_train` | `src/03_preprocess.py#L44` | Verified |
| **Feature Scaling** | Test $\mu, \sigma$ leaking into normalization | `StandardScaler.fit()` called strictly on `X_train`; `scaler.transform()` on Val/Test | `src/03_preprocess.py#L48` | Verified |
| **Model Fitting** | Model sees test samples | Models trained strictly on `(X_train, y_train)` | `src/04_train_models.py#L32` | Verified |
| **OOD Calibration** | Covariance matrix or PCA seeing test instances | Centroid $\boldsymbol{\mu}_{\text{train}}$ and covariance $\boldsymbol{\Sigma}_{\text{train}}^{-1}$ computed strictly on `X_train` | `src/07_ood_detection.py#L25` | Verified |
| **PSI Drift Reference** | Quantile bin edges fitted to test distribution | Reference quantile bins computed strictly on `X_train` | `src/10_measure_drift.py#L35` | Verified |
| **Historical Error Memory** | Error index containing test set mistakes | $E_{\text{train}} = \{\mathbf{x}_i \in X_{\text{train}} \mid \hat{y}_i \ne y_i\}$ built exclusively from training misclassifications | `src/14_historical_error_risk.py#L30` | Verified |
| **Review Queue Selection** | Ground-truth test labels used to sort queue | Queue sorting uses only $R(\mathbf{x})$. Ground truth $y_{\text{test}}$ is never passed to sorting function | `src/25_final_strategy_comparison.py#L55` | Verified |
| **Sequential Feedback** | Future batch labels leaking into current batch | Ground truth revealed strictly for reviewed flows *after* selection; weights updated only for batch $t+1$ | `src/28_sequential_feedback_eval.py#L68` | Verified |

---

## 3. Label Invariance Assertion (Automated Test Proof)

In [`tests/test_splits_and_leakage.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/tests/test_splits_and_leakage.py), we maintain the automated assertion `test_no_test_label_leakage_in_ranking`:
- We evaluate candidate review queues before and after completely inverting or zeroing ground-truth test labels ($y_{\text{test}} \leftarrow 1 - y_{\text{test}}$).
- The resulting review queue indices are **100% identical** ($\text{index}_1 == \text{index}_2$), proving that review queue triage does not leak or depend upon test target labels.
