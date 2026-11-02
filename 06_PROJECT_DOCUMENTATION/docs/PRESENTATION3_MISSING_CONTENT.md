# PRESENTATION-3 GAP ANALYSIS & MISSING CONTENT RESOLUTION

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Prof. Dilip Kumar Maripuri  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Department & Institution:** Department of Computer Applications, PES University, Bengaluru  
**Audit Purpose:** Controlled Identification & Resolution of Presentation Gaps  
**Audit Date:** 2026-11-02  

---

## 1. Summary of Identified Gaps in the Baseline Submission

An audit of the baseline PowerPoint deck ([`01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx), 25 slides) against the official PES University Presentation-3 guidelines revealed **6 critical deficiencies**:

1. **Incorrect Milestone Heading (Slides 1 & 2):**
   - *Baseline Issue:* Labeled as `CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)` and `Phase-1 Capstone Presentation-2`.
   - *Impact:* Evaluators reviewing Presentation-3 will immediately penalize a deck marked "Presentation-2".
2. **Inaccurate Implementation Status Statement (Slides 11 & 20):**
   - *Baseline Issue:* Claimed an arbitrary `96.4% Verified` based on informal 50% credit for FR14, contradicting the approved official specification.
   - *Impact:* Viva committee members scrutinizing FR14 require exact adherence to the approved wording.
3. **Missing Controlled Normalization & Uncertainty Scaling Study (Mentor Priority 1):**
   - *Baseline Issue:* The deck lacked an ablation proof explaining why margin uncertainty $u \in [0, 0.50]$ must remain unscaled ($R_{\max} = 0.825$) rather than being normalized to $[0, 1.00]$.
   - *Impact:* The viva panel could question whether the multi-factor score is mathematically flawed due to different signal scales.
4. **Missing Statistical Significance & Bootstrap Confidence Intervals (Slide 22/23):**
   - *Baseline Issue:* The 1% budget error capture figures (610 vs 463) were presented without statistical significance testing ($p$-values or bootstrap confidence intervals).
   - *Impact:* Advanced evaluators often challenge whether a 147-error difference is statistically significant or random variance.
5. **Missing Sequential 5-Batch Streaming Dynamics & Error Discrepancy Reconciliation:**
   - *Baseline Issue:* The deck showed 610 errors at 1% budget in the global benchmark, but omitted the sequential online simulation (183 errors vs 168 static comparator).
   - *Impact:* Left an unexplained numerical contradiction between the 610 global errors and the 183 sequential errors documented in report artifacts.
6. **Missing Software Engineering Testing Suite (Section 10 of Guidelines):**
   - *Baseline Issue:* Section 10 of the university guidelines strictly mandates software testing. The baseline deck only presented ML model comparison tables (XGBoost vs RF vs LR), completely omitting software unit tests, invariant checks, and runtime verification.
   - *Impact:* Fails Section 10 software testing compliance.

---

## 2. Item-by-Item Gap Resolution Matrix

The table below outlines the exact content required to resolve each gap, and points to its verified implementation in the newly generated 28-slide deck ([`PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx)):

| Gap # | Deficient Area | University Guideline / Mentor Requirement | Exact Missing Content | Resolution in Enhanced Presentation-3 Deck |
|:---:|:---|:---|:---|:---|
| **1** | Title & Category Banners | Section 1 (Project Title & Milestone) | Must reflect Presentation-3 milestone and current academic date. | **Slides 1 & 2:** Updated banners to `CAPSTONE PROJECT PHASE-1 (PRESENTATION-3)` and candidate milestone to `Phase-1 Presentation-3`. |
| **2** | Official Status Statement | Section 6 & 9 (FR Specification & Implementation) | Must state the approved official wording: *"13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented)."* | **Slides 11 & 20:** Preserves exact 92.9% official wording; details Phase-I local Streamlit completion vs Phase-II automated retraining deferral. |
| **3** | Normalization & Scaling Bounds | Section 9 (Implementation & Algorithmic Rigor) | Mathematical bounds ($u \in [0, 0.50]$, $R_{\max} = 0.825$) and ablation comparison (Unscaled $u$ vs $2u$ vs Rank-norm). | **Slide 22 (NEW SLIDE):** Added dedicated slide with mathematical proof and 3-variant table (610 vs 527 vs 280) explaining false-alarm flooding. |
| **4** | Statistical Significance | Section 10 (Empirical Evaluation & Rigor) | 1,000 paired bootstrap 95% Confidence Interval, empirical $p$-value, PR-AUC, and Expected Calibration Error. | **Slide 23:** Added 1,000 paired bootstrap 95% CI `[+3.45%, +5.28%]` ($p < 0.001$), PR-AUC = 0.7444, and ECE = 0.0200. |
| **5** | Sequential Streaming Dynamics | Section 9 & 10 (Dynamic Adaptation & Evaluation) | 5 batches $\times$ 150 reviews; 183 vs 168 vs 34; reconciliation of 610 global vs 183 sequential errors. | **Slide 24 (NEW SLIDE):** Added dedicated slide showing 24.40% yield (183/750) and explaining temporal error clustering (66.8% hit in Batch 5). |
| **6** | Software Testing Suite | Section 10 (Software Testing Verification) | Automated test suite execution, unit test pass counts, mathematical invariant verification script. | **Slide 25 (NEW SLIDE):** Added dedicated slide showing `pytest tests/` (16/16 passed in 4.57s), `src/30_verify_results.py` (Exit Code 0), and UI testing. |

---

## 3. Slide-by-Slide Content Recommendations for Final Review

### Slide 18: Benchmark Dataset & Temporal Distribution Shift
- **Recommendation:** Add a prominent "Leakage Prevention Verification" card to the right side of the slide.
- **Exact Content Added:**
  - Forward chronological gaps: Train $\rightarrow$ Val is strictly `+25.0 ms` (`16:22:35.978` to `16:22:36.003`); Val $\rightarrow$ Shifted Test is strictly `+39.0 ms` (`17:01:20.431` to `17:01:20.470`).
  - Zero duplicate rows across partitions verified via SHA-256 hashes (100% row-level disjointness).
  - Preprocessing parameters (median imputation, scalers, reference covariance) fitted solely on Train split.

### Slide 22: Controlled Normalization & Uncertainty Scaling Study (NEW)
- **Recommendation:** Insert immediately after Slide 21 (Signal Extraction) to provide mathematical foundation before empirical benchmark tables.
- **Exact Content Added:**
  - Formula: $R(x) = 0.35u(x) + 0.15s_{\text{ood}}(x) + 0.25s_{\text{drift}}(x) + 0.25s_{\text{hist}}(x) \le 0.825$.
  - Controlled 1% Budget Ablation Table:
    - Unscaled $u \in [0, 0.50]$ (Our Method): **610 errors (17.80%)** | Rank 1 (Optimal)
    - Linear Scaling $2u \in [0, 1.00]$: **527 errors (15.38%)** | -13.6% loss
    - Rank-Normalized $u \in [0, 1.00]$: **280 errors (8.17%)** | -54.1% collapse
  - Scientific explanation of false-alarm flooding: Artificially boosting uncertainty floods the top-K queue with borderline noise, crowding out true OOD and drift signals.

### Slide 23: Empirical Results & Strategy Benchmark
- **Recommendation:** Update card beneath the benchmark table to display statistical rigor metrics.
- **Exact Content Added:**
  - 1,000 paired bootstrap 95% Confidence Interval: `[+3.45%, +5.28%]` ($p < 0.001$).
  - Mean advantage over pure confidence: `+4.35%`.
  - Shifted-test discriminative metrics: PR-AUC = 0.7444, Balanced Accuracy = 0.7321, ECE = 0.0200.

### Slide 24: Sequential 5-Batch Online Adaptation & Streaming Dynamics (NEW)
- **Recommendation:** Insert after Slide 23 to demonstrate sequential online adaptation and resolve the 610 vs 183 figure discrepancy.
- **Exact Content Added:**
  - 5-batch setup: 75,000 flows partitioned into 5 sequential chronological batches of 15,000 flows each, with a rigid budget of 150 reviews per batch (750 total).
  - Performance: Feedback Adaptive (183 errors / 24.40% yield) vs Static Comparator (168 errors / 22.40% yield) vs Random Audit (~34 errors / 4.53% yield).
  - Mathematical Reconciliation: Errors are temporally concentrated—2,291 of 3,427 errors (66.8%) hit during Batch 5. Global triage concentrates 719 reviews into Batch 5 (catching 610 errors), while sequential streaming enforces a rigid 150/batch quota (catching 183 errors). Both figures are verified and defensible.

### Slide 25: Software Engineering Testing: Automated Invariant & Pipeline Verification (NEW)
- **Recommendation:** Insert after Slide 24 to complete Section 10 of the university guidelines.
- **Exact Content Added:**
  - Automated test execution: `pytest tests/` passing 16 of 16 tests in 4.57s (split integrity, zero leakage, signal bounding, quota allocation).
  - Invariant engine: `python src/30_verify_results.py` validating 6 core mathematical invariants with Exit Code 0.
  - Interactive UI: Streamlit local dashboard verified syntax-clean and operational on local runtime.
