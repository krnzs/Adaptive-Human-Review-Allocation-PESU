# PRESENTATION-3 FINAL COMPLIANCE SCORECARD

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Prof. Dilip Kumar Maripuri  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Department & Institution:** Department of Computer Applications, PES University, Bengaluru  
**Milestone:** Capstone Project Phase-I — Presentation-3 (Scheduled: November 2–6, 2026)  
**Evaluation Standard:** Independent Academic Audit Against Official PES University Guidelines  
**Audit Date:** 2026-11-02  

---

## 1. Executive Evaluation Summary & Decision

| Metric | Required Level | Baseline Deck (`01_FINAL_SUBMISSION`) | Enhanced Deck (`PHASE_3_PRESENTATION`) | Compliance Verdict |
|:---|:---:|:---:|:---:|:---:|
| **Score 1: University Guideline Coverage** | 100% of 11 Sections | **72.7%** (8/11 complete; 3 partial/missing) | **100.0%** (11/11 complete) | **PASS** (Enhanced Deck) |
| **Score 2: Actual Project Implementation** | $\ge 80.0\%$ | **92.9%** (13/14 FRs complete) | **92.9%** (13/14 FRs complete) | **STRONG PASS (+12.9% over min)** |
| **Score 3: Implementation Evidence in Slides** | $\ge 80.0\%$ | **71.4%** (Missing testing & normalization) | **92.9%** (Matches actual project state) | **STRONG PASS (+12.9% over min)** |
| **Milestone Banner Accuracy** | "Presentation-3" | **FAIL** (Marked "Presentation-2") | **PASS** (Marked "Presentation-3") | **PASS** (Enhanced Deck) |
| **Submission Readiness** | Ready for Viva Panel | **NOT READY** (Key gaps present) | **FULLY READY FOR DEFENSE** | **APPROVED** |

---

## 2. Detailed Scoring Breakdown

### SCORE 1: University Guideline Coverage
*Evaluates how thoroughly the PowerPoint slides satisfy the 11 formal sections specified in the PES University Presentation-3 Guidelines.*

- **Denominator:** 11 required sections (Title, Abstract, Introduction, Literature Survey, Tools & Tech, Functional Requirements, Non-Functional Requirements, System Design, Implementation $\ge 80\%$, Software Testing, References).
- **Scoring Method:** Each section is scored as Complete (1.0), Partially Complete (0.5), or Missing (0.0).

#### Baseline Deck (`01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx`):
- Section 1 (Title): 0.5 (Titled "Presentation-2")
- Section 2 (Abstract): 1.0 (Complete)
- Section 3 (Introduction: Scenario, Problem, Purpose, Scope): 1.0 (Complete)
- Section 4 (Literature Survey: 10 papers + Comparative Study): 1.0 (Complete)
- Section 5 (Tools & Technologies): 1.0 (Complete)
- Section 6 (Functional Requirements): 0.5 (Informal 96.4% instead of official 92.9%)
- Section 7 (Non-Functional Requirements): 1.0 (Complete)
- Section 8 (System Design: Architecture, Process Flow, Schema, Pseudocode): 1.0 (Complete)
- Section 9 (Implementation $\ge 80\%$): 0.5 (Lacks normalization study & millisecond leakage proof)
- Section 10 (Software Testing: 2-3 models + test suite): 0.5 (Only shows ML model comparison; omits automated testing)
- Section 11 (References: IEEE format): 1.0 (Complete)
- **Baseline Score 1:** $\frac{8.0}{11} \times 100\% = \mathbf{72.7\%}$

#### Enhanced Deck (`PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx`):
- Sections 1 through 11: All 11 sections fully addressed without omissions.
- **Enhanced Score 1:** $\frac{11.0}{11} \times 100\% = \mathbf{100.0\%}$

---

### SCORE 2: Actual Project Implementation
*Evaluates the physical implementation supported by real Python source code in `src/`, automated tests in `tests/`, serialized models in `models/`, and outputs in `results/`.*

- **Denominator:** 14 approved Functional Requirements (FR01 through FR14).
- **Scoring Method:**
  - Strict Binary Formulation: Fully Implemented (1.0), Partially Implemented (0.0).
  - Approved Weighted Formulation: Fully Implemented (1.0), Partially Implemented (0.50).

#### Actual Physical Codebase:
- **FR01 to FR13 (13 Requirements):** 100% Fully Implemented across 26 modular Python scripts, verified by automated unit tests and mathematical invariant checks.
- **FR14 (1 Requirement):** Partially Implemented (Local interactive Streamlit dashboard active and operational for Phase-I; multi-dataset cloud-native ingestion deferred to Phase-II).

$$\text{Strict Implementation Score} = \frac{13}{14} \times 100\% = \mathbf{92.86\%} \approx \mathbf{92.9\%}$$

$$\text{Weighted Implementation Score} = \frac{13 + 0.50}{14} \times 100\% = \frac{13.5}{14} \times 100\% = \mathbf{96.43\%} \approx \mathbf{96.4\%}$$

- **Compliance with University Requirement ($\ge 80\%$):** **EXCEEDED by +12.9% (strict) and +16.4% (weighted).**
- **Official Approved Statement (Preserved Exactly):**
  > **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

### SCORE 3: Implementation Evidence in the Presentation
*Evaluates whether the PowerPoint presentation convincingly demonstrates the actual implementation through pseudocode, architecture diagrams, module status, empirical benchmark tables, and testing evidence.*

- **Denominator:** 14 Functional Requirements that must be evidenced in slides.
- **Scoring Method:** Each requirement must be backed by concrete artifacts (pseudocode steps, diagram callouts, metric tables, or test outputs) in the presentation.

#### Baseline Deck (`01_FINAL_SUBMISSION`):
- Evidenced FRs: FR01 to FR10 fully evidenced (10 FRs). FR11–FR13 partially evidenced (no sequential reconciliation or bootstrap CI). FR14 evidenced as informal prototype.
- **Baseline Score 3:** $\frac{10.0}{14} \times 100\% = \mathbf{71.4\%}$ (Fails to demonstrate the full 80% threshold convincingly).

#### Enhanced Deck (`PHASE_3_PRESENTATION`):
- Evidenced FRs: All 13 fully implemented FRs are directly demonstrated across dedicated slides:
  - FR01–FR03: Slide 18 (BigFlow sample, chronological split, millisecond gaps).
  - FR04–FR05: Slide 19 (3-model comparison, validation metrics, ECE).
  - FR06–FR09: Slide 21 (4 reliability signals, PSI drift, mistake deciles).
  - FR10: Slide 22 (Composite scoring bounds, controlled normalization study).
  - FR11–FR12: Slide 23 (1%–10% strategy benchmark, 1,000-bootstrap CI, crossover).
  - FR13: Slide 24 (5-batch online streaming simulation, 183 vs 168 vs 34).
  - Software Testing: Slide 25 (`pytest tests/` 16/16 passed, `30_verify_results.py` Exit 0).
  - FR14: Slide 20 & 25 (Streamlit dashboard active; automated retraining roadmap).
- **Enhanced Score 3:** $\frac{13}{14} \times 100\% = \mathbf{92.86\%} \approx \mathbf{92.9\%}$ (Matches the true 92.9% project implementation level).

---

## 3. Authoritative Reference Numbers Check (Part E Reconciliation)

All numbers presented in the Enhanced Presentation-3 Deck have been verified against canonical CSV artifacts:

| Benchmark Parameter | Reference Value | Verified Source File | Presentation Slide | Status |
|---|:---:|:---|:---:|:---:|
| Total Ingested NetFlows | 500,000 | `BigFlow_sample.csv` | Slide 18 | **CONFIRMED** |
| Training Partition | 350,000 (70%) | `results/train.csv` | Slide 18 | **CONFIRMED** |
| Validation Partition | 75,000 (15%) | `results/val.csv` | Slide 18 | **CONFIRMED** |
| Shifted Test Partition | 75,000 (15%) | `results/shifted_test.csv` | Slide 18 | **CONFIRMED** |
| Validation Attack Prevalence | 0.33% (248 attacks) | `results/split_audit.csv` | Slide 18 | **CONFIRMED** |
| Shifted Test Attack Prevalence | 6.30% (4,724 attacks) | `results/split_audit.csv` | Slide 18 & 21 | **CONFIRMED** |
| Validation Errors (XGBoost) | 753 (1.004%) | `results/validation_predictions.csv` | Slide 19 | **CONFIRMED** |
| Shifted Test Errors (XGBoost) | 3,427 (4.569%) | `results/shifted_test_predictions.csv` | Slide 18, 21, 23 | **CONFIRMED** |
| Measured Error Surge | 4.551x | `results/split_audit.csv` | Slide 18 & 21 | **CONFIRMED** |
| Train $\rightarrow$ Val Time Gap | +25.0 ms | `results/split_audit.csv` | Slide 18 | **CONFIRMED** |
| Val $\rightarrow$ Test Time Gap | +39.0 ms | `results/split_audit.csv` | Slide 18 | **CONFIRMED** |
| Cross-Partition Duplicates | Exactly 0 | `tests/test_splits_and_leakage.py` | Slide 18 | **CONFIRMED** |
| 1% Budget Quota (750 Flows) | Random: 40 errors (1.17%) | `final_shifted_strategy_comparison.csv` | Slide 23 | **CONFIRMED** |
| 1% Budget Quota (750 Flows) | Least-Conf: 463 errors (13.51%) | `final_shifted_strategy_comparison.csv` | Slide 23 | **CONFIRMED** |
| 1% Budget Quota (750 Flows) | OOD-Only: 1 error (0.03%) | `final_shifted_strategy_comparison.csv` | Slide 23 | **CONFIRMED** |
| 1% Budget Quota (750 Flows) | Static Multi-Factor: 600 errors (17.51%) | `final_shifted_strategy_comparison.csv` | Slide 23 | **CONFIRMED** |
| 1% Budget Quota (750 Flows) | Feedback Adaptive: 610 errors (17.80%) | `final_shifted_strategy_comparison.csv` | Slide 23 | **CONFIRMED** |
| 1% Budget 95% Bootstrap CI | [+3.45%, +5.28%], p < 0.001 | `results/extended_bootstrap_cis.csv` | Slide 23 | **CONFIRMED** |
| Shifted Test PR-AUC | 0.7444 | `results/extended_model_metrics.csv` | Slide 23 | **CONFIRMED** |
| Shifted Test Balanced Accuracy | 0.7321 | `results/extended_model_metrics.csv` | Slide 23 | **CONFIRMED** |
| Expected Calibration Error | 0.0200 | `results/extended_model_metrics.csv` | Slide 23 | **CONFIRMED** |
| Uncertainty Normalization (1%) | Unscaled: 610; 2u: 527; Rank-norm: 280 | `src/22_uncertainty_scaling_study.py` | Slide 22 | **CONFIRMED** |
| Sequential 5-Batch Online Sim | Adaptive: 183; Static: 168; Random: ~34 | `results/sequential_feedback.csv` | Slide 24 | **CONFIRMED** |
| Automated Test Suite | 16 of 16 tests passing in 4.57s | `pytest tests/` | Slide 25 | **CONFIRMED** |
| Invariant Verification Script | Exit Code 0 (All 6 invariants confirmed) | `src/30_verify_results.py` | Slide 25 | **CONFIRMED** |

---

## 4. Final Submission Verdict & Recommendation

1. **Submission Readiness:**
   - The baseline file `01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx` is **NOT recommended for presentation** because it bears the "Presentation-2" header and lacks the Section 10 software testing suite, normalization ablation proof, and sequential streaming dynamics.
   - The enhanced file **`PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx`** is **100% COMPLIANT, FULLY DEFENDED, AND APPROVED FOR SUBMISSION**.
2. **Action for Candidate (Karan Shetty):**
   - Present using the 28-slide deck in `PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx`.
   - Deliver the five audit documents in `06_PROJECT_DOCUMENTATION/docs/` to your faculty guide Prof. Dilip Kumar Maripuri as undeniable documentary proof of rigor.
