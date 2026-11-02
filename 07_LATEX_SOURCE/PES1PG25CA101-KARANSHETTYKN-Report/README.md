# PES1PG25CA101-KARANSHETTYKN-Report

## Capstone Project
**Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty  
**SRN:** PES1PG25CA101  
**Programme:** Master of Computer Applications (MCA)  
**Guide:** Dilip Kumar Maripuri  
**Department:** Department of Computer Applications, PES University  
**Milestone:** Phase-I Review-II / Presentation-2 Report  

---

## 1. Project Structure
```text
PES1PG25CA101-KARANSHETTYKN-Report/
├── main.tex              # Master LaTeX entry point
├── references.bib        # 11 verified IEEE citations with DOIs
├── README.md             # Compilation instructions & documentation notes
├── chapters/             # 13 structured chapters converted from report
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── literature_review.tex
│   ├── background.tex
│   ├── comparative_study.tex
│   ├── requirements.tex
│   ├── methodology.tex
│   ├── system_design.tex
│   ├── data_design.tex
│   ├── implementation.tex
│   ├── results.tex
│   ├── limitations.tex
│   └── conclusion.tex
├── figures/              # Verified PNG figures copied from project artifacts
│   ├── v2_architecture.png
│   ├── v2_use_case.png
│   ├── v2_process_flow.png
│   ├── v2_ml_pipeline.png
│   ├── v2_er_diagram.png
│   ├── v2_module_status.png
│   ├── v2_results_chart.png
│   ├── top10_drift_features.png
│   └── review_efficiency_vs_budget.png
└── tables/               # Dedicated directory for extracted table assets
```

---

## 2. Compilation Instructions

### Required LaTeX Distribution
You can compile this project using any modern LaTeX distribution:
- **Windows:** MiKTeX (recommended) or TeX Live
- **Linux:** TeX Live (`sudo apt install texlive-latex-extra texlive-science texlive-fonts-recommended`)
- **macOS:** MacTeX
- **Online:** Overleaf (upload the entire `PES1PG25CA101-KARANSHETTYKN-Report` folder)

### Standard Packages Used
The report relies exclusively on standard LaTeX packages:
`geometry`, `graphicx`, `booktabs`, `longtable`, `array`, `amsmath`, `float`, `hyperref`, `caption`, `subcaption`, `xcolor`, `setspace`, and `titlesec`.

### Compilation Commands
From inside the `PES1PG25CA101-KARANSHETTYKN-Report/` directory:

#### Using `latexmk` (One-step build):
```bash
latexmk -pdf main.tex
```

#### Using standard CLI tools (`pdflatex` + `bibtex`):
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 3. Important Notes for Manual Review Before Submission

> **IMPORTANT:** The contents of this LaTeX project have been mechanically converted and structured directly from the verified Phase-I Review-II report files and source code artifacts. Please perform a manual review before final submission to confirm the following points:

1. **Implementation Status:**
   - As verified from the codebase, **13 of 14 functional requirements are fully implemented**; FR14 (*Interactive Streamlit Analytics Dashboard*) is partially implemented (92.9% fully implemented). 
   - No claim of 100% completion is made.

2. **Historical Error Risk Formulation (`chapters/methodology.tex` and `chapters/implementation.tex`):**
   - The underlying script `src/14_historical_error_risk.py` computes proximity to **training classification errors** using a `KNeighborsClassifier` fitted on `(X_train, y_train != y_train_pred)`.
   - Any legacy mentions of "validation errors" from early drafts have been flagged in the LaTeX comments with `% REVIEW NOTE / INCONSISTENCY:`.

3. **Feedback Loop Formulation (`chapters/methodology.tex`):**
   - The offline benchmark script `src/25_final_strategy_comparison.py` uses heuristic regime weights to simulate dynamic allocation.
   - Sequential batch-by-batch review feedback was evaluated in `src/28_sequential_feedback_eval.py`.
   - Ensure the textual description matches your planned explanation to the guide.

4. **Figure Placeholders:**
   - Only figures with genuine source files in `diagrams/` and `results/` are embedded via `\includegraphics`.
   - Sections without existing diagrams (e.g., Sequence Diagram, DL Model Architecture, UI Screenshots) contain explicit `% TODO:` placeholder comments. Do not fabricate diagrams.
