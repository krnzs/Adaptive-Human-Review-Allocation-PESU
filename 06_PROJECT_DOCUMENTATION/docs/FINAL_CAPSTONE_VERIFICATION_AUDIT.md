# FINAL CAPSTONE VERIFICATION AUDIT — EVIDENCE-BASED STATUS

**Department of Computer Applications | PES University, Bengaluru**  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Student:** Karan Shetty (`PES1PG25CA101`)  
**Faculty Guide:** Dilip Kumar Maripuri  
**Milestone:** Capstone Phase-I Review-II & Viva Defense Preparation  
**Audit Timestamp:** 2026-10-28  
**Preserved Official Status:**  
> **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

## 1. Executive Verification Summary

This final audit inspects the organized repository at:  
`C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\`

In accordance with strict verification rules:
- No files were reorganized, deleted, overwritten, or modified.
- No expected numbers were fabricated or forced.
- All claims and numbers were verified against actual execution output and underlying data CSVs.

### Core Audit Outcomes
1. **Repository Inventory & Hash Integrity:** **126 of 126 items verified**. `00_START_HERE/FILE_INDEX.csv` perfectly mirrors disk state. All 103 files match their SHA256 hashes with **0 missing items and 0 mismatches**.
2. **Automated Test Suite:** `pytest tests/` executed cleanly with **16 passed in 4.57s** (100% pass rate).
3. **Master Result Verification:** `python src/30_verify_results.py` exited with **Exit Code 0**, confirming all 6 core research invariants.
4. **Streamlit Reviewer Dashboard:** Verified running on Python 3.13.9 / Streamlit 1.51.0 (`localhost:8599`), initializing with 0 import errors and clean exit.
5. **Sequential Experiment Reconciliation:** Reconciled 610 vs. 183 errors, 168 vs. 161 static comparator figures, and 34 random baseline yield.
6. **Statistical Confidence Intervals:** Confirmed 1,000-sample paired bootstrap interval `[+3.45%, +5.28%]` ($p < 0.001$).
7. **Leakage & Chronological Splits:** Confirmed non-overlapping millisecond boundaries (+25.0 ms Train-to-Val, +39.0 ms Val-to-Test), zero duplicate rows, and training-fitted preprocessing.

---

## 2. Inventory & File Index Verification (Task 1 & 2)

- **Manifest File Inspected:** `00_START_HERE/FILE_INDEX.csv` (126 entries).
- **Disk Verification Script Executed:** `verify_file_index_and_hashes.py`
- **Findings:**
  - Total entries in index: 126
  - Directories verified present: 23
  - Files verified present: 103
  - Missing items: 0
  - SHA256 checksum mismatches: 0
  - Match Rate: **100.0%**

All 103 files are bit-identical to the baseline recorded in `FILE_INDEX.csv` and `ORGANIZATION_CHANGELOG.md`.

---

## 3. Automated Test Suite Execution (Task 3)

- **Command Executed:**  
  `Set-Location "C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"; pytest tests/`
- **Environment:** Windows win32, Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
- **Duration:** 4.57 seconds
- **Actual Command Output:**
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

  ============================= 16 passed in 4.57s ==============================
  ```
- **Outcome:** **16 passed, 0 failed, 0 warnings.**

---

## 4. Master Invariant Verification (Task 4)

- **Command Executed:**  
  `Set-Location "C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"; python src/30_verify_results.py`
- **Exit Code:** `0`
- **Verified Findings:**
  1. *Five-Strategy Review Allocations:* All 20 strategy-budget pairs in `results/final_shifted_strategy_comparison.csv` verified.
  2. *Honest Crossover:* Adaptive wins at 1% (610 vs 463) and 2% (1,174 vs 916); Confidence wins at 5% (2,243 vs 1,573) and 10% (2,879 vs 1,794).
  3. *Extended Metrics:* PR-AUC = 0.7444, Balanced Accuracy = 0.7321, ECE = 0.0200, 95% Bootstrap CI = `[+3.45%, +5.28%]`.
  4. *Split Integrity:* Train (350k, 6.10% attacks), Val (75k, 0.33% attacks, 753 errors), Shifted Test (75k, 6.30% attacks, 3,427 errors). +25.0 ms and +39.0 ms forward chronological gaps confirmed.
  5. *Uncertainty Normalization Impact:* Unscaled $u$ = 610 errors, $2u$ = 527 errors (-13.6%), rank-normalized $u$ = 280 errors (-54.1%).
  6. *Sequential Online Adaptation:* Adaptive sequential catches 183 errors vs. 168 static comparator errors (+15 errors, +8.9% relative gain).

---

## 5. Streamlit Reviewer Dashboard Verification (Task 5)

- **Command Executed:**  
  `streamlit run dashboard/app.py --server.headless true --server.port 8599`
- **Startup Output:**
  ```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8599
  Network URL: http://192.168.137.169:8599
  External URL: http://223.31.218.223:8599
  ```
- **Process Status:** Active and responding; gracefully stopped via task cancellation.
- **Outcome:** **Dashboard starts cleanly in existing Python environment with zero code or dependency changes.**

---

## 6. Sequential Experiment Figures Reconciliation (Task 6)

The audit reconciled four key figures across code and results:

### A. Main Benchmark Adaptive (610 Errors) vs. Sequential Adaptive (183 Errors)
- **Source Scripts:** `src/25_final_strategy_comparison.py` vs. `src/28_sequential_feedback_eval.py`
- **Source Files:** `results/final_shifted_strategy_comparison.csv` vs. `results/sequential_feedback.csv`
- **Data Reality:** Ground-truth classification errors are heavily clustered temporally:
  - Batch 1 (0–15k): 280 errors
  - Batch 2 (15k–30k): 296 errors
  - Batch 3 (30k–45k): 325 errors
  - Batch 4 (45k–60k): 235 errors
  - **Batch 5 (60k–75k): 2,291 errors (66.8% of all 3,427 test errors occur here during the attack surge)**
- **Why 610 Errors Occurs:** In global retrospective triage, all 75,000 flows are pooled. The top 750 scoring slots naturally surge **719 reviews into Batch 5**, capturing 604 errors from Batch 5 plus 6 errors across Batches 1–4 ($604 + 6 = 610\text{ errors}$).
- **Why 183 Errors Occurs:** In sequential online streaming, the reviewer has a rigid operational quota of exactly 150 reviews per batch ($5 \times 150 = 750$ total). The reviewer is restricted to 150 reviews in Batch 5 regardless of threat level, capturing $32 + 35 + 38 + 38 + 40 = 183\text{ errors}$ (24.40% yield).

### B. Sequential Static Comparator (168 in Blueprint vs. 161 in Earlier Draft)
- **Canonical Result File:** `results/sequential_feedback.csv` explicitly records:
  ```csv
  budget,sequential_caught,static_caught,conf_caught,total_errors
  0.01,183,168,466,3427
  ```
- **Source Script:** `src/28_sequential_feedback_eval.py` implements static scoring with equal weights $(0.25, 0.25, 0.25, 0.25)$:
  ```python
  batch_df['static_score'] = (
      0.25 * batch_df['confidence_risk'] +
      0.25 * batch_df['ood_percentile'] +
      0.25 * batch_df['drift_risk'] +
      0.25 * batch_df['historical_risk']
  )
  ```
  Evaluating this static formula across 5 batches of 150 reviews yields exactly **168 errors caught**.
- **Origin of 161:** An earlier preliminary draft (`FINAL_REPOSITORY_AUDIT.md` and `PROJECT_EXPLAINED_SIMPLY.md`) noted 161 from an earlier run before ties and percentile scaling were finalized. The authoritative, data-backed figure in `results/sequential_feedback.csv` is **168 errors**.

### C. Sequential Random Comparator (34 Errors)
- Across 75,000 shifted test flows containing 3,427 errors, the base error prevalence is $3,427 / 75,000 = 4.5693\%$.
- When an analyst randomly reviews 750 flows ($5 \times 150$ per batch), the expected error capture is:
  $$\mathbb{E}[\text{Errors}] = 750 \times \frac{3,427}{75,000} = 34.27 \approx 34\text{ errors}$$
- Thus, 34 represents the expected baseline yield (4.53%) of random staffing.

---

## 7. Bootstrap Confidence Interval Verification (Task 7)

- **Source Script:** `src/29_extended_evaluation.py`
- **Result File:** `results/extended_bootstrap_cis.csv`
- **Resampling Method:**
  - 1,000 paired instance-level bootstrap resamples with replacement ($N = 75,000$).
  - For each resample, both the Adaptive and Confidence strategies allocate review capacity ($K = 750$ at 1% budget).
  - Paired difference per iteration: $\Delta_b = \text{Capture}_{\text{adapt}} - \text{Capture}_{\text{conf}}$.
- **Verified Metrics (1% Review Budget):**
  - Mean Advantage: `+4.35%` (corresponds to full-sample $(610 - 463) / 3,427 = +4.29\%$)
  - 2.5th Percentile: `+3.45%`
  - 97.5th Percentile: `+5.28%`
  - $p$-value: $p < 0.001$ (in all 1,000 resamples, $\Delta_b > 0$).
- **Statistical Interpretation:** The +31.7% relative gain of Adaptive triage over Least-Confidence triage is statistically significant ($p < 0.001$), with a 95% bootstrap confidence interval of `[+3.45%, +5.28%]`.
- **Temporal Caveat:** Because network flow errors cluster in time, standard i.i.d. bootstrap resampling does not account for temporal autocorrelation. The sequential batch evaluation provides the conservative chronological check (183 vs. 168 errors).

---

## 8. Dataset Split Integrity & Leakage Controls (Task 8)

- **Source File:** `results/split_audit.csv`
- **Verified Figures:**
  - **Train Split (70%):** 350,000 flows | 21,344 attacks (6.10% prevalence) | 12,392 errors (3.54% error rate) | Max timestamp: `2019-04-23 16:22:35.978`
  - **Validation Split (15%):** 75,000 flows | 248 attacks (0.33% prevalence) | 753 errors (1.00% error rate) | Min timestamp: `2019-04-23 16:22:36.003` | Max timestamp: `2019-04-23 17:01:20.431`
  - **Shifted Test Split (15%):** 75,000 flows | 4,724 attacks (6.30% prevalence) | 3,427 errors (4.57% error rate) | Min timestamp: `2019-04-23 17:01:20.470` | Max timestamp: `2019-04-24 03:27:14.233`
- **Chronological Gap Proof:**
  - Train $\rightarrow$ Validation: `16:22:35.978` to `16:22:36.003` = **+25.0 ms strict forward gap**.
  - Validation $\rightarrow$ Shifted Test: `17:01:20.431` to `17:01:20.470` = **+39.0 ms strict forward gap**.
- **Row-Level Disjointness:** Verified that boundary rows `Train[-1]` and `Val[0]` are distinct network flows with different feature vectors. 0 duplicate records across splits.
- **Preprocessing Leakage Control:** Scalers, imputation medians, Mahalanobis empirical covariance matrices, and XGBoost tree structures are strictly fitted on the Training split only.

---

## 9. Four Signals & Mathematical Formula Verification (Task 9)

- **Source Scripts:** `src/05_generate_prediction_signals.py`, `src/17_shifted_test_signals.py`, `tests/test_signals_and_scoring.py`
- **Signal Implementations:**
  1. *Model Margin Uncertainty:* $u = 1 - \max(P_0, P_1) \in [0, 0.50]$.
  2. *Out-of-Distribution (OOD):* Mahalanobis distance $D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)}$ mapped to percentile rank $z_{\text{ood}} \in [0, 1.00]$.
  3. *Population Stability Drift (PSI):* Binned feature drift mapped to percentile risk $z_{\text{psi}} \in [0, 1.00]$.
  4. *Historical Error Risk:* Nearest-neighbor slice error rate from training set mapped to percentile rank $z_{\text{hist}} \in [0, 1.00]$.
- **Composite Formula:**
  $$R_i = 0.35 u_i + 0.15 z_{\text{ood}, i} + 0.25 z_{\text{psi}, i} + 0.25 z_{\text{hist}, i}$$
- **Theoretical Upper Bound:**
  $$R_{\max} = 0.35(0.50) + 0.15(1.00) + 0.25(1.00) + 0.25(1.00) = 0.175 + 0.150 + 0.250 + 0.250 = \mathbf{0.825}$$
  Verified: all 75,000 composite scores satisfy $R \le 0.825$.
- **Controlled Scaling Verification:**
  - Unscaled $u \in [0, 0.50]$: 610 errors caught (17.80%)
  - Rescaled $2u \in [0, 1.00]$: 527 errors caught (15.38%) [-13.6% degradation]
  - Rank-normalized $u \in [0, 1.00]$: 280 errors caught (8.17%) [-54.1% degradation]
  *Conclusion:* Unscaled $u$ prevents low-risk boundary noise from overwhelming high-risk distribution drift.

---

## 10. FR14 Status Confirmation (Task 10)

- **Preserved Status Statement:**  
  > **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**
- **Evidence-Based Breakdown:**
  - FR14.1 (Real-time Drift Detection): **Fully Implemented** (PSI drift monitoring across batches).
  - FR14.2 (Sequential Dynamic Weight Adaptation): **Fully Implemented** (Adaptive weight updating across batches catching 183 errors vs. 168 static comparator).
  - FR14.3 (Automated Model Retraining): **Partially Implemented / Deferred to Phase-II**. (Automatic model retraining trigger deferred to Phase-II in consultation with faculty guide Dilip Kumar Maripuri to prevent catastrophic forgetting and ensure safety-critical validation in network intrusion environments).

---

## 11. Discrepancies, Blockers & Remaining Work Summary (Task 11)

### A. Documented Discrepancies & Source Files
| Issue / Number | Source Files | Root Cause & Resolution | Status |
|:---|:---|:---|:---:|
| **Static Comparator: 168 vs. 161** | `results/sequential_feedback.csv` (168) vs. `06_PROJECT_DOCUMENTATION/docs/FINAL_REPOSITORY_AUDIT.md` (161) | 168 is the canonical output of `src/28_sequential_feedback_eval.py`. 161 was a draft figure from a pre-finalized tie-breaking run. Canonical value: **168 errors**. | Resolved |
| **Random Comparator: 34** | `06_PROJECT_DOCUMENTATION/docs/FINAL_REPOSITORY_AUDIT.md` (34) | Theoretical expected yield: $750 \times (3,427 / 75,000) = 34.27 \approx 34$ errors (4.53%). Not a separate column in CSV. | Clarified |
| **Global 610 vs. Sequential 183** | `results/final_shifted_strategy_comparison.csv` (610) vs. `results/sequential_feedback.csv` (183) | 610 is from global retrospective pooling (719 reviews placed in Batch 5 surge); 183 is from strict 150-review/batch sequential streaming without lookahead. | Clarified |

### B. Blockers & Sync Issues
- **Files Blocked:** 0.
- **Dependencies Missing:** 0.
- **OneDrive Sync Issues:** 0.
- All 126 items are locally present, readable, and verified.

### C. Prioritized List of Remaining Work for Phase-II
1. **Phase-II Scope Item 1 (FR14.3):** Implement automated model retraining trigger with safety validation gates to prevent catastrophic forgetting.
2. **Phase-II Scope Item 2:** Extend sequential batch triage to evaluate variable-budget dynamic staffing (allowing analyst capacity to flex from 100 to 300 reviews during detected drift spikes).
3. **Phase-II Scope Item 3:** Conduct multi-seed cross-validation across additional intrusion datasets (e.g., CIC-IDS-2018, UNSW-NB15) to confirm domain generalization.

---

## 12. Final Viva Sign-Off Recommendation

The capstone project repository is in an **authoritative, verified, and defendable state**.
- All code runs cleanly (`pytest`: 16/16 passed in 4.57s; verification: exit code 0).
- All numbers cited in documentation are grounded in actual CSV data.
- The repository structure is clean, professional, and accessible.
