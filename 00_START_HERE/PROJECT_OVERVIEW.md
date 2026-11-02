# PROJECT OVERVIEW: Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift

**Department of Computer Applications | PES University, Bengaluru**  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Milestone:** Capstone Phase-I Review-II & Viva Defense  

---

## 1. Project Identification & Credentials

- **Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift
- **Student Name:** Karan Shetty
- **Student SRN:** `PES1PG25CA101`
- **Faculty Guide / Mentor:** Dilip Kumar Maripuri
- **Academic Department:** Department of Computer Applications, PES University, Ring Road Campus, Bengaluru
- **Official Functional Status:**
  > **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

## 2. Core Problem & Academic Contribution

In production machine learning systems deployed in high-throughput adversarial domains (such as Network Intrusion Detection Systems — NIDS), distribution shift causes model degradation, miscalibration, and silent classification failures. Organizations cannot manually audit every decision; human verification bandwidth is typically constrained to **1% to 5%** of incoming traffic.

Standard confidence-based triage (**Least-Confidence Sampling**) prioritizes instances solely near the decision boundary ($P \approx 0.50$). Under sudden distribution shifts (such as zero-day attack floods), modern overparameterized classifiers frequently make **high-confidence errors** (silent failures with $P > 0.90$).

### Key Contributions of this Capstone
1. **Four-Signal Composite Scoring Architecture:** Synthesizes model uncertainty ($u$), out-of-distribution distance (OOD Mahalanobis distance $z_{\text{ood}}$), population stability drift ($\text{PSI}$ drift $z_{\text{psi}}$), and historical slice error rate ($z_{\text{hist}}$) into a unified triage priority score:
   $$R_i = w_u u_i + w_{\text{ood}} z_{\text{ood}, i} + w_{\text{psi}} z_{\text{psi}, i} + w_{\text{hist}} z_{\text{hist}, i}$$
2. **Honest Crossover Phenomenon:** Proves empirically that under tight operational budgets ($\le 2\%$), our multi-signal adaptive framework dramatically outperforms confidence triage (+31.7% relative error catch at 1%), while at loose budgets ($\ge 5\%$), confidence sampling recovers due to exhaustive boundary sweep.
3. **Mathematical Scaling Justification:** Formally validates why raw margin uncertainty $u = 1 - \max(P_0, P_1) \in [0, 0.50]$ must remain unscaled. Linear scaling ($2u$) degrades 1% error catch by -13.6% (527 errors), and percentile rank normalization degrades catch by -54.1% (280 errors) due to false-alarm flooding of low-risk boundary noise.
4. **Leakage-Free Online Sequential Feedback:** Implements a strict 5-batch streaming simulation where human feedback reveals labels only for audited samples, updating signal weights strictly forward in time (catching 183 errors vs. 168 static comparator errors).
5. **Interactive Streamlit Reviewer Dashboard:** Provides a fully operational triage cockpit with real-time budget sliders, live queue exploration, drift monitoring, and batch triage simulation.

---

## 3. Authoritative Research Facts & Invariants

All figures below are mathematically verified, cross-checked across the test suite (`pytest tests/`), and verified via `src/30_verify_results.py`:

### A. Dataset & Strict Chronological Split
- **Benchmark:** BigFlow-NIDS with a 500,000-flow chronological evaluation sample.
- **Training Set (70%):** 350,000 flows | 6.10% attack prevalence (21,350 attacks) | 12,392 training errors (3.54%).
- **Validation Set (15%):** 75,000 flows | 0.33% attack prevalence (248 attacks) | 753 validation errors (1.004%).
- **Shifted Test Set (15%):** 75,000 flows | 6.30% attack prevalence (4,725 attacks) | 3,427 test errors (4.569%).
- **Temporal Shift Surge:** Test error rate is **4.55x higher** than validation (4.569% vs 1.004%), modeling severe real-world attack surges.
- **Zero-Leakage Millisecond Boundaries:**
  - Train Max: `2019-04-23 16:22:35.978`
  - Validation Min: `2019-04-23 16:22:36.003` (**+25.0 ms strict forward gap**)
  - Validation Max: `2019-04-23 17:01:20.431`
  - Test Min: `2019-04-23 17:01:20.470` (**+39.0 ms strict forward gap**)
  - Exactly 0 duplicate rows, 0 timestamp overlaps, and 0 future data leakage.

### B. Strategy Comparison & Error Detection (Shifted Test Set, 3,427 Total Errors)
| Review Budget | Random Triage | Least Confidence | Pure OOD | Static Multi-Factor | Feedback Adaptive | Adaptive vs Confidence Gain |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1.0% (750 flows)** | 40 (1.17%) | 463 (13.51%) | 1 (0.03%) | 600 (17.51%) | **610 (17.80%)** | **+31.7% relative (+4.29% abs)** |
| **2.0% (1,500 flows)** | 73 (2.13%) | 916 (26.73%) | 9 (0.26%) | 1,165 (33.99%) | **1,174 (34.26%)** | **+28.2% relative (+7.53% abs)** |
| **5.0% (3,750 flows)** | 189 (5.52%) | **2,243 (65.45%)** | 12 (0.35%) | 1,870 (54.57%) | 1,573 (45.90%) | *Crossover: Confidence wins* |
| **10.0% (7,500 flows)**| 340 (9.92%) | **2,879 (84.01%)** | 12 (0.35%) | 2,242 (65.42%) | 1,794 (52.35%) | *Crossover: Confidence wins* |

### C. Extended Statistical Metrics & Significance
- **Shifted Test PR-AUC:** `0.7444` (XGBoost baseline)
- **Shifted Test Balanced Accuracy:** `0.7321`
- **Expected Calibration Error (ECE):** `0.0200`
- **95% Bootstrap Confidence Interval (1% Budget Gain):** `[+3.45%, +5.28%]`, $p < 0.001$ over 1,000 paired resamples, confirming statistical significance.

### D. Understanding 610 Errors vs. 183 Errors
- **610 Errors Caught (17.80%):** Global offline benchmark allocation across the entire 75,000 flows. Because 2,291 of the 3,427 errors (66.8%) occur during the attack surge in Batch 5, an unconstrained global allocation assigns 719 of the 750 reviews into Batch 5.
- **183 Errors Caught (24.40% Yield):** Realistic sequential streaming triage across 5 equal batches (15,000 flows/batch) with an enforced budget of 150 reviews per batch (750 total). Without future knowledge, the online adaptive queue captures 183 errors, beating the equal-weight static comparator (168 errors).

---

## 4. Master Folder Structure & Navigation

The workspace is organized into clean, dedicated directories designed for immediate viva presentation:

```
Capstone Project/
├── 00_START_HERE/                     <-- Core documentation hub, folder guide, file index, changelog
├── 01_FINAL_SUBMISSION/               <-- Final PDF/DOCX reports, PPT slides, and official code/latex ZIPs
├── 02_PRESENTATION_SLIDES/            <-- Alternate decks (v2), slide renderings, and visual guide previews
├── 03_REPORTS_AND_DOCS/               <-- Comprehensive report drafts, viva cheatsheet, and paper summaries
├── 04_CODE_PIPELINE/                  <-- Pipeline architecture documentation & execution instructions
├── 05_DASHBOARD/                      <-- Interactive Streamlit reviewer dashboard guide
├── 06_PROJECT_DOCUMENTATION/          <-- 15 in-depth technical audits, leakage proofs, and tutor guides
├── 07_LATEX_SOURCE/                   <-- Modular Overleaf-compatible LaTeX project & chapter sources
├── 08_DIAGRAMS_AND_MEDIA/             <-- High-res architecture diagrams, workflow figures, and logo
├── 09_BUILD_AND_UTILITY_SCRIPTS/      <-- Offline document generators, report builders, and formatting scripts
├── 10_HISTORICAL_AND_ALTERNATE_VERSIONS/<-- Intermediate drafts, test documents, logs, and legacy dumps
├── mentor_ready_copy/                 <-- Standalone verified mentor replica with independent test suite
├── src/                               <-- Canonical 30-stage ML pipeline (Kept at root for zero-breakage)
├── dashboard/                         <-- Canonical Streamlit application (Kept at root for zero-breakage)
├── tests/                             <-- Automated pytest suite (16 tests, all passing)
├── models/                            <-- Serialized XGBoost models, scalers, and preprocessors
├── results/                           <-- Verified CSV datasets, evaluation matrices, and figure plots
└── BigFlow_sample.csv                 <-- Benchmark 500,000-flow dataset
```

---

## 5. How to Run & Verify the Project

Open PowerShell in the project directory:

```powershell
# 1. Run all 16 automated tests:
pytest tests/

# 2. Run the authoritative 6-invariant verification script:
python src/30_verify_results.py

# 3. Launch the interactive Streamlit dashboard:
streamlit run dashboard/app.py

# 4. Run the live demo batch triage:
python src/run_demo_batch.py
```

All commands execute cleanly with exit code 0.
