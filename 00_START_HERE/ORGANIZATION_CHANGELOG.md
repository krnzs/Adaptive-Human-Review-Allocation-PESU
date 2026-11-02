# ORGANIZATION CHANGELOG: Meticulous Project Restructuring & Verification

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Candidate:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Execution Timestamp:** 2026-10-27 | **Workspace:** `C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project`  

---

## 1. Executive Summary of Changes

The project workspace originally contained 126 loose items at the root level (23 directories and 103 files), including ML runtime scripts, models, datasets, LaTeX source trees, presentation slides, temporary word processor dumps, offline report generators, and technical audit documents.

To prepare the repository for academic evaluation, mentor sign-off, and viva defense, the workspace was safely reorganized into dedicated functional folders following strict non-negotiable safety rules:
1. **Zero Content Modification:** Not a single byte of any Python script, model, dataset, CSV result, or LaTeX source was changed.
2. **Zero Deletions:** Exactly 0 files or directories were deleted.
3. **Zero Overwrites & Zero Renames:** All files retained their exact original filenames and timestamps.
4. **Zero Path Breakages (Tier A Root Retention):** The canonical ML pipeline (`src/`, `dashboard/`, `tests/`, `models/`, `results/`, `BigFlow_sample.csv`, `requirements.txt`, `README.md`, `.gitignore`) was preserved directly at the root, ensuring all relative file paths and import statements remain 100% operational.
5. **Bit-for-Bit Hash Verification:** Every moved file was verified via SHA256 checksums before and after the move, confirming 100% data integrity.

---

## 2. Quantitative Summary of Inventory & Movements

- **Total Items Inventoried:** 126
  - **Directories:** 23
  - **Files:** 103
- **Items Retained in Place at Root (Tier A):** 20 items
  - Environment / VCS: `.git`, `.venv`, `.venv-1`, `.venv-2`, `.vscode`, `.pytest_cache`, `__pycache__` (7)
  - Core ML Pipeline: `src/`, `dashboard/`, `tests/`, `models/`, `results/`, `data/`, `BigFlow_sample.csv`, `requirements.txt`, `README.md`, `.gitignore` (10)
  - Live Demo Support: `demo_live/`, `demo_live_results.csv` (2)
  - Verified Replica: `mentor_ready_copy/` (1)
- **Items Safely Moved into Functional Directories:** 106 items
  - `01_FINAL_SUBMISSION/`: 7 items
  - `02_PRESENTATION_SLIDES/`: 4 items
  - `03_REPORTS_AND_DOCS/`: 12 items
  - `06_PROJECT_DOCUMENTATION/`: 6 items
  - `07_LATEX_SOURCE/`: 2 items
  - `08_DIAGRAMS_AND_MEDIA/`: 3 items
  - `09_BUILD_AND_UTILITY_SCRIPTS/`: 63 items
  - `10_HISTORICAL_AND_ALTERNATE_VERSIONS/`: 9 items
- **Unclassified / Review Required:** 0 items
- **SHA256 Match Rate:** **100.0% (106 / 106 moved items matched original checksums)**

---

## 3. Detailed Move Manifest by Destination Folder

### A. `01_FINAL_SUBMISSION/` (7 Items)
Final frozen deliverables for university examination cell and mentor archival:
- `Adaptive_Human_Review_Allocation_Review_II_FINAL.pdf` (88.6 KB)
- `Adaptive_Human_Review_Allocation_Review_II_FINAL.docx` (1,151.1 KB)
- `PES1PG25CA101_KARANSHETTYKN_REVIEW_PPT.pdf` (697.3 KB)
- `Adaptive_Human_Review_Allocation_PESU_FINAL.pdf` (697.2 KB)
- `Adaptive_Human_Review_Allocation_PESU_FINAL.pptx` (737.6 KB)
- `PES1PG25CA101_MentorReady_Code.zip` (88,445.3 KB) — Intact official submission zip
- `PES1PG25CA101_LaTeX_Source.zip` (3,583.4 KB) — Intact official LaTeX submission zip

### B. `02_PRESENTATION_SLIDES/` (4 Items)
Alternate slide versions and slide preview images:
- `Adaptive_Human_Review_Allocation_PESU_v2.pptx` (738.0 KB)
- `Adaptive_Human_Review_Allocation_PESU_v2_alt.pdf` (693.6 KB)
- `guide_preview/` (Directory with 5 slide preview files)
- `pdf_preview/` (Directory with 24 rendered PDF page previews)

### C. `03_REPORTS_AND_DOCS/` (12 Items)
Comprehensive report drafts, paper summaries, and viva study materials:
- `Adaptive_Human_Review_Allocation_Review_II_Report.docx` (1,127.2 KB)
- `Adaptive_Human_Review_Allocation_Review_II_Report.pdf` (94.8 KB)
- `Review_II_Report.md` (86.5 KB)
- `Viva_Cheatsheet.md` (11.7 KB)
- `Capstone_Phase1_Easy_Explanation_Complete_Guide.pdf` (25.3 KB)
- `Capstone_Phase1_Mentor_Walkthrough_Guide.pdf` (20.3 KB)
- `Paper_Summaries.md` (67.3 KB)
- `Paper_Summaries.pdf` (59.8 KB)
- `references_check.md` (1.4 KB)
- `TITLE_UPDATE_SUMMARY.md` (4.2 KB)
- `MENTOR_FEEDBACK_FIXES_SUMMARY.md` (7.5 KB)
- `DEMO_INSTRUCTIONS.md` (4.0 KB)

### D. `06_PROJECT_DOCUMENTATION/` (6 Items)
Exhaustive forensic audits, leakage proofs, statistical notes, and technical guides:
- `docs/` (Directory containing 15 in-depth technical markdown documents)
- `DOCS_CHANGELOG.md` (5.6 KB)
- `DOCS_FACTS.md` (1.4 KB)
- `EXISTING_FILES_AUDIT.md` (13.4 KB)
- `LEAKAGE_AUDIT.md` (3.3 KB)
- `CHANGES_NEEDED.md` (1.5 KB)

### E. `07_LATEX_SOURCE/` (2 Items)
Modular Overleaf-ready LaTeX project source code:
- `PES1PG25CA101-KARANSHETTYKN-Report/` (Modular LaTeX directory, 58 files)
- `report_src/` (LaTeX source assets directory, 15 files)

### F. `08_DIAGRAMS_AND_MEDIA/` (3 Items)
High-resolution architectural diagrams and visual media:
- `diagrams/` (Directory containing 21 high-resolution system architecture PNG diagrams)
- `extracted_media/` (Directory containing 2 extracted presentation images)
- `pes_logo.png` (10.2 KB) — Official university crest

### G. `09_BUILD_AND_UTILITY_SCRIPTS/` (63 Items)
Offline build generators, docx formatters, LaTeX exporters, and test utilities (decoupled from ML pipeline):
- Report Builders & Exporters: `build_complete_report.py`, `build_exact_mentor_report.py`, `build_latex_project.py`, `build_markdown_report.py`, `build_use_case.py`, `compile_report_pdf.py`, `populate_mentor_template_final.py`, `strip_instructions_from_template.py`, `remove_instructions.py`, `trim_report.py`
- Presentation & Diagram Generators: `build_full_v2_deck.py`, `build_charts.py`, `generate_presentation_deck.py`, `generate_presentation_pdf.py`, `generate_15slide_deck.py`, `generate_15slide_pdf.py`, `generate_19slide_deck.py`, `generate_19slide_diagrams.py`, `generate_19slide_pdf.py`, `generate_corrected_pdf.py`, `generate_diagrams.py`, `generate_v2_diagrams.py`, `generate_v2_pdf.py`, `generate_mentor_guide_pdf.py`, `generate_paper_summaries_pdf.py`
- LaTeX Converters & Post-processors: `extract_to_latex.py`, `extract_to_latex2.py`, `generate_latex.py`, `latex_postprocess.py`, `insert_images_report.py`
- Inspection & Patch Utilities: `apply_fixes.py`, `check_bigflow.py`, `check_full_bigflow.py`, `check_ppt.py`, `dump_template_map.py`, `extract_pptx_text.py`, `fix_bigflow.py`, `fix_paren.py`, `fix_ppt_refs.py`, `fix_pptx_audit.py`, `fix_pptx_pass2.py`, `fix_pptx_pass3.py`, `fix_refs.py`, `fix_syntax.py`, `fix_v2_diag.py`, `get_refs.py`, `inspect_docx_full.py`, `inspect_exact_template.py`, `inspect_workspace.py`, `patch_builder.py`, `patch_content.py`, `patch_section1.py`, `report_content_dict.py`, `report_content_part1.py`, `report_content_part2.py`, `save_summary.py`
- Unit Testing / Mock Utilities: `test_direct_populator.py`, `test_docx_load.py`, `test_env.py`, `test_insert_p.py`, `test_scan.py`, `test_style.py`, `test_template_mod.py`

### H. `10_HISTORICAL_AND_ALTERNATE_VERSIONS/` (9 Items)
Forensic text dumps, temporary inspection files, intermediate documents, and build logs:
- `ppt_text_dump.txt` (64.8 KB)
- `template_map.txt` (15.4 KB)
- `template_parsed.txt` (9.2 KB)
- `test.pdf` (1.6 KB)
- `test_template_mod.docx` (16.3 KB)
- `test_template_mod2.docx` (16.3 KB)
- `texput.log` (0.7 KB)
- `FINAL_AUDIT_REPORT.txt` (2.8 KB)
- `devin/` (Directory, 0 files)

---

## 4. Post-Reorganization Verification Results

Immediately following the reorganization, three independent verification commands were executed to confirm system health:

### Verification 1: Automated Test Suite (`pytest tests/`)
```
============================= test session starts =============================
platform win32 -- Python 3.13.9, pytest-8.4.2, pluggy-1.5.0
rootdir: C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project
collected 16 items

tests\test_evaluation.py ....                                            [ 25%]
tests\test_results_consistency.py ...                                    [ 43%]
tests\test_signals_and_scoring.py .....                                  [ 75%]
tests\test_splits_and_leakage.py ....                                    [100%]

============================= 16 passed in 4.75s ==============================
```
**Result:** 16 passed, 0 failed.

### Verification 2: Authoritative 6-Invariant Check (`python src/30_verify_results.py`)
```
[1] Verifying Five-Strategy Review Allocations: ALL 20 STRATEGY-BUDGET PAIRS CONFIRMED
[2] Verifying Honest Crossover Behavior: CONFIRMED (Adaptive wins at 1%, Confidence at 5%)
[3] Verifying Extended Statistical Metrics: PR-AUC 0.7444, Bal Acc 0.7321, ECE 0.0200, 95% CI [+3.45%, +5.28%]
[4] Verifying Data Split Integrity: Train (350k), Val (75k), Test (75k), strict +25ms and +39ms gaps
[5] Verifying Controlled Uncertainty Normalization Impact: Unscaled u = 610, 2u = 527, Rank-norm = 280
[6] Verifying Sequential 5-Batch Online Feedback: Adaptive caught 183 errors vs 168 static comparator
OVERALL VERIFICATION STATUS: [SUCCESS] ALL 6 INVARIANTS CONFIRMED
```
**Result:** Exit Code 0, all 6 research invariants verified.

### Verification 3: Dashboard Syntax & Compilation (`python -m py_compile dashboard/app.py`)
**Result:** Exit Code 0, clean bytecode compilation with zero errors.

---

## 5. Verification Sign-Off

The workspace is clean, robust, and fully prepared for mentor evaluation and university viva defense.
All original files, models, datasets, and results are 100% intact with bit-level verification.
