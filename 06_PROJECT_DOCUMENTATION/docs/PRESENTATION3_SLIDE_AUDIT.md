# PRESENTATION-3 SLIDE-BY-SLIDE COMPLIANCE AUDIT

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Prof. Dilip Kumar Maripuri  
**Programme:** Master of Computer Applications (MCA) — Data Analytics  
**Department & Institution:** Department of Computer Applications, PES University, Bengaluru  
**Milestone:** Capstone Project Phase-I — Presentation-3 (Scheduled: November 2–6, 2026)  
**Audit Date:** 2026-11-02  

---

## 1. Executive Summary of Slide Audit

This audit evaluates the PowerPoint presentation against the official PES University MCA Department Presentation-3 guidelines across 11 core required sections:
1. Project Title
2. Abstract
3. Introduction (Scenario, Problem Statement, Purpose & Scope)
4. Detailed Literature Survey (10 IEEE/Scopus papers + Comparative Study)
5. Tools and Technologies
6. Functional Requirements (FR1 to FR14)
7. Non-Functional Requirements
8. High-Level Design Diagrams (Architecture, Process Flow, Schema, Pseudocode)
9. Implementation ($\ge 80\%$ required; verified project is at 92.9%)
10. Software Testing (Comparison of 2–3 models + automated test suite)
11. References (IEEE Format)

### Identification of Decks Audited:
- **Baseline Deck (Historical Submission):** [`01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_PESU_FINAL.pptx) (25 slides, titled "Presentation-2", missing recent verified research additions).
- **Target Presentation-3 Deck:** [`PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/PHASE_3_PRESENTATION/Adaptive_Human_Review_Allocation_Presentation_3.pptx) (28 slides, expanded to incorporate all 5 verified additions).

---

## 2. Slide-by-Slide Audit Matrix

| Slide | Topic | University Guideline Requirement | Status in Baseline (25-Slide) | Status in Enhanced (28-Slide) | Evidence Quality & Audit Findings | Missing / Improved Content |
|:---:|:---|:---|:---:|:---:|:---|:---|
| **01** | Title & Details | Title, student name, SRN, guide, department, milestone. | **PRESENT BUT INCORRECT** (Labeled Presentation-2) | **COMPLETE** | Excellent formatting; Guide and Student credentials verified. | Header corrected to `CAPSTONE PROJECT PHASE-1 (PRESENTATION-3)`. |
| **02** | Abstract & Research Question | Research problem, approach, dataset, results, research question. | **PARTIALLY PRESENT** (Missing 92.9% FR status) | **COMPLETE** | High-density executive abstract and framed research question. | Incorporated 92.9% implementation statement and bootstrap evidence. |
| **03** | Problem Scenario & Solution | Attention bottleneck, overconfidence under shift, proposed solution. | **COMPLETE** | **COMPLETE** | High-contrast side-by-side cards (Red vs Green) clearly defining the problem. | None. Perfectly aligned. |
| **04** | Purpose & Scope | Purpose, in-scope (Phase-I), out-of-scope, Phase-II scope. | **COMPLETE** | **COMPLETE** | Explicitly distinguishes offline benchmark simulation from live streaming. | None. Defensible scope boundaries established. |
| **05** | Background Study | Existing selective classification, OOD, drift, and deferral paradigms. | **COMPLETE** | **COMPLETE** | Covers 5 existing paradigms with verified citations ([1]–[14]). | None. Strong theoretical context. |
| **06** | Literature Survey (Part 1) | Minimum 5 papers with authors, title, venue, indexing, and summary. | **COMPLETE** | **COMPLETE** | Papers [1]–[5]: ICCV 2023, ICML 2020, ICML 2024, NeurIPS 2017, ICML 2017. IEEE/Scopus indexing verified. | Verified IEEE alternatives listed for PMLR publications. |
| **07** | Literature Survey (Part 2) | Minimum 5 papers with authors, title, venue, indexing, and summary. | **COMPLETE** | **COMPLETE** | Papers [6]–[10]: IEEE TIFS 2024, Sci Rep 2022, IJCV 2024, ICML 2021, IEEE COMST 2023. | Full DOIs and indexing verified. |
| **08** | Comparative Study | Comparative matrix across existing paradigms vs proposed framework. | **COMPLETE** | **COMPLETE** | 7 evaluation dimensions across 5 systems showing multi-factor advantage. | None. Comprehensive table format. |
| **09** | Users of the System | Primary stakeholders and user personas with system interactions. | **COMPLETE** | **COMPLETE** | ML Practitioner, Simulated Reviewer/Oracle, Research Evaluator. | None. Fulfills Section 6 stakeholder requirements. |
| **10** | Functional Requirements (1–7) | Detailed requirements specification with mapping to implementation. | **COMPLETE** | **COMPLETE** | FR1–FR7 mapped to exact scripts (`src/01` to `src/08`). | 100% implementation status verified. |
| **11** | Functional Requirements (8–14) | Detailed requirements specification with mapping to implementation. | **PARTIALLY PRESENT** (FR14 listed as 50% without official status) | **COMPLETE** | FR8–FR14 mapped to `src/09` to `src/24` and `dashboard/app.py`. | Updated to approved official statement: 13/14 complete (92.9%). |
| **12** | Non-Functional Requirements | Measurable NFRs: Reproducibility, Latency, Integrity, Modularity. | **COMPLETE** | **COMPLETE** | Backed by concrete measurements (1.60s execution, SHA-256 checks). | None. Realistic and measured. |
| **13** | Tools & Technologies | Languages, frameworks, ML libraries, scientific packages. | **COMPLETE** | **COMPLETE** | Python 3.10+, pandas, NumPy, XGBoost, scikit-learn, SciPy, pytest. | Added pytest test suite explicitly to testing category. |
| **14** | System Architecture Diagram | High-level system architecture showing 5 decoupled stages. | **COMPLETE** | **COMPLETE** | High-resolution image `v2_architecture.png` embedded cleanly. | None. Clear dataflow arrows and annotations. |
| **15** | ML Process Flow & Methodology | Preprocessing, chronological splitting, model inference flow. | **COMPLETE** | **COMPLETE** | High-resolution image `v2_process_flow.png` embedded cleanly. | Highlights temporal splitting safeguards. |
| **16** | Database Design / Schema | Conceptual schema and entity-relationship model. | **COMPLETE** | **COMPLETE** | High-resolution image `v2_data_schema.png` embedded cleanly. | Clarifies file-based relational CSV/joblib persistence. |
| **17** | Core Pipeline Pseudocode | 16-step algorithmic execution covering all 4 phases. | **COMPLETE** | **COMPLETE** | Detailed 2-column algorithm breakdown mapped to `src/01`–`src/26`. | Explicitly states simulated review oracle step. |
| **18** | Benchmark Dataset & Shift | BigFlow-NIDS details, feature set, chronological split numbers. | **PARTIALLY PRESENT** (Missing millisecond leakage proof) | **COMPLETE** | 500,000 flows (350K train, 75K val, 75K test); 4.55x error surge. | Added verified forward gaps (+25.0ms, +39.0ms) and zero duplicate proof. |
| **19** | Model Training & Validation | Comparison of 2–3 ML models on accuracy, precision, recall, F1, ROC-AUC. | **COMPLETE** | **COMPLETE** | XGBoost (0.9228), Random Forest (0.8526), Logistic Regression (0.7499). | Fulfills Section 10 model evaluation requirement. |
| **20** | Implementation Demo (Status) | Demonstration of implementation completeness ($\ge 80\%$). | **PARTIALLY PRESENT** (Reported 96.4% instead of official 92.9%) | **COMPLETE** | Embedded `v2_module_status.png` with verified breakdown. | Preserves approved statement: 13/14 complete (92.9% fully implemented). |
| **21** | Signal Extraction & Evidence | Demonstration of 4 extracted signals and measured shift evidence. | **COMPLETE** | **COMPLETE** | Details $u$, Mahalanobis $s_{\text{ood}}$, PSI drift, and historical mistake bins. | None. Strong scientific justification. |
| **22** | Controlled Normalization Study | Ablation study on signal normalization and scaling bounds. | **MISSING** (In baseline 25-slide deck) | **COMPLETE** | Unscaled $u$ (610 errors) vs Linear $2u$ (527 errors) vs Rank-norm (280 errors). | **NEW SLIDE** answering Mentor Priority 1 with false-alarm flooding proof. |
| **23** | Empirical Strategy Benchmark | Benchmark table (1%–10% budgets) and statistical validation. | **PARTIALLY PRESENT** (Missing 95% bootstrap CI and p-value) | **COMPLETE** | 5 strategies across 4 budgets; embedded `v2_results_chart.png`. | Added 1,000-bootstrap 95% CI `[+3.45%, +5.28%]`, $p < 0.001$, PR-AUC, ECE. |
| **24** | Sequential 5-Batch Streaming | Online adaptation dynamics and reconciliation of 610 vs 183 errors. | **MISSING** (In baseline 25-slide deck) | **COMPLETE** | 5 batches $\times$ 150 reviews; Adaptive (183 / 24.4%) vs Static (168 / 22.4%). | **NEW SLIDE** proving temporal clustering (66.8% in Batch 5) and online gain. |
| **25** | Software Engineering Testing | Comprehensive testing verification (unit tests, invariants, UI). | **MISSING** (In baseline 25-slide deck) | **COMPLETE** | `pytest tests/` (16/16 passed in 4.57s) + `src/30_verify_results.py` (Exit Code 0). | **NEW SLIDE** fulfilling Section 10 software testing requirements. |
| **26** | Limitations & Phase-2 Roadmap | Identified limitations and concrete Phase-2 extensions. | **COMPLETE** | **COMPLETE** | Honest limitations (simulated oracle, heuristic weights, single domain). | Defensible academic roadmap. |
| **27** | References (Research Papers) | Formal IEEE citations for 10 research papers. | **COMPLETE** | **COMPLETE** | Papers [1]–[10] formatted in strict IEEE format across 2 columns. | None. Zero text overflow. |
| **28** | References (Books & Software) | Formal citations for datasets, textbooks, and software packages. | **COMPLETE** | **COMPLETE** | BigFlow-NIDS [16], Hastie et al. [12], scikit-learn [17], SciPy [18], Python. | None. Clean, readable formatting. |

---

## 3. Analysis of Critical Deficiencies in Baseline Deck vs Enhanced Deck

### A. Title & Milestone Header (Slide 1 & Slide 2)
- **Deficiency in Baseline:** Baseline was generated during the Review-II milestone and bore the subtitle `CAPSTONE PROJECT PHASE-1 (PRESENTATION-2)`.
- **Resolution in Enhanced Deck:** Explicitly titled `CAPSTONE PROJECT PHASE-1 (PRESENTATION-3)` with updated presentation milestone dates and verified candidate/guide cards.

### B. Functional Requirements Completion Statement (Slide 11 & Slide 20)
- **Deficiency in Baseline:** Reported informal `96.4% Verified` by arbitrarily assigning 50% credit to FR14.
- **Resolution in Enhanced Deck:** Uses the approved official statement:
  > *"13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented)."*
  Explains clearly that 13 out of 14 modules are 100% operational, and FR14 is partially implemented as an offline Streamlit dashboard, while online streaming retraining is deferred to Phase-II.

### C. Controlled Uncertainty Normalization Proof (Slide 22 — NEW)
- **Deficiency in Baseline:** Baseline lacked the ablation experiment explaining why margin uncertainty $u \in [0, 0.50]$ must remain unscaled ($R_{\max} = 0.825$).
- **Resolution in Enhanced Deck:** Added dedicated Slide 22 featuring the mathematical bounds, the 3-variant ablation table (Unscaled $u$: 610 errors vs Linear $2u$: 527 errors vs Rank-norm: 280 errors), and the false-alarm flooding root-cause analysis.

### D. Statistical Confidence Intervals (Slide 23)
- **Deficiency in Baseline:** Baseline reported raw error counts without statistical confidence intervals.
- **Resolution in Enhanced Deck:** Added the verified 1,000 paired bootstrap 95% Confidence Interval `[+3.45%, +5.28%]` ($p < 0.001$), along with PR-AUC (0.7444), Balanced Accuracy (0.7321), and Expected Calibration Error (0.0200).

### E. Sequential Streaming & Discrepancy Reconciliation (Slide 24 — NEW)
- **Deficiency in Baseline:** Did not explain the difference between the 610 global errors and the 183 sequential errors.
- **Resolution in Enhanced Deck:** Added dedicated Slide 24 presenting the 5-batch $\times$ 150-review simulation results (183 vs 168 vs 34) and mathematically proving that 66.8% of ground-truth errors hit in Batch 5, explaining why global triage concentrated 719 reviews into Batch 5 while sequential triage enforced a realistic 150/batch quota.

### F. Software Engineering Testing Suite (Slide 25 — NEW)
- **Deficiency in Baseline:** Baseline only showed ML model performance tables, omitting automated software testing required by Section 10.
- **Resolution in Enhanced Deck:** Added dedicated Slide 25 documenting the automated test suite (`pytest tests/` passing 16 of 16 tests), the mathematical invariant verification engine (`python src/30_verify_results.py` with Exit Code 0), and Streamlit dashboard verification.

---

## 4. Slide Legibility, Formatting & Presentation Quality

- **Aspect Ratio:** Modern widescreen 16:9 (`13.333" x 7.5"`), preventing black letterboxing on seminar hall projectors.
- **Color Palette:** High-contrast University-compliant scheme (#0B192C Navy, #1E40AF Royal Blue, #16A34A Emerald Green, #DC2626 Warning Red, #F8FAFC Card Canvas).
- **Text Sizing & Margins:** Slide titles at 22pt bold, headings at 13–15pt bold, body copy at 11–12pt with 15pt line leading. Zero overlapping text boxes or truncated paragraphs.
- **Table Construction:** All table cells have explicit column widths and text padding (0.04" margin), preventing clipped numbers.
- **Speaker Notes:** Complete, word-for-word spoken narration scripts embedded in the notes field of all 28 slides.
