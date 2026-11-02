# FOLDER GUIDE: Project Directory Layout & Viva Navigation Roadmap

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Guide:** Dilip Kumar Maripuri  
**Department of Computer Applications, PES University, Bengaluru**  

---

## 1. Directory Structure at a Glance

The project folder is organized into functional zones designed to separate final submission deliverables, presentations, technical audits, offline utilities, and the active machine learning runtime.

| Directory / Item | Risk Classification | What It Contains | Primary User / Audience |
|:---|:---:|:---|:---|
| **`00_START_HERE/`** | Safe | Project overview, folder guide, file index CSV, organization changelog | Student, Mentor, Viva Panel |
| **`01_FINAL_SUBMISSION/`** | Tier C | Final review report (PDF/DOCX), official presentation, mentor-ready code ZIP, LaTeX source ZIP | Mentor, University Exam Cell |
| **`02_PRESENTATION_SLIDES/`** | Tier B/C | Alternate v2 slide decks, high-res slide previews, presentation assets | Student during viva presentation |
| **`03_REPORTS_AND_DOCS/`** | Tier C | Full report drafts, viva defense cheatsheet, paper summaries, walkthrough guides | Student viva prep, mentor review |
| **`04_CODE_PIPELINE/`** | Safe Doc | Architecture documentation & stage-by-stage guide for the 30-script pipeline | Developers, technical examiners |
| **`05_DASHBOARD/`** | Safe Doc | Architecture documentation for the Streamlit human-in-the-loop review cockpit | Viva demonstration |
| **`06_PROJECT_DOCUMENTATION/`** | Tier B/C | 15 comprehensive technical audits (`docs/`), leakage proofs, statistical validations | In-depth technical verification |
| **`07_LATEX_SOURCE/`** | Tier B | Complete modular LaTeX project (`PES1PG25CA101-KARANSHETTYKN-Report/`) & chapter files | Academic publication & archival |
| **`08_DIAGRAMS_AND_MEDIA/`** | Tier B/C | 21 high-resolution system diagrams (`diagrams/`), extracted media, PES logo | Report and presentation figures |
| **`09_BUILD_AND_UTILITY_SCRIPTS/`** | Tier C | 63 offline document builders, report formatters, text scrapers, and test scripts | Build automation (offline) |
| **`10_HISTORICAL_AND_ALTERNATE_VERSIONS/`** | Tier C | Intermediate template dumps, test documents, logs, and legacy files | Historical archive (do not edit) |
| **`mentor_ready_copy/`** | Tier A (Replica) | Self-contained, fully verified mentor copy with independent test suite | Mentor backup and external review |
| **`src/`** | **Tier A (Runtime)** | **Canonical 30-stage Python ML pipeline** | **Machine Learning Engine** |
| **`dashboard/`** | **Tier A (Runtime)** | **Canonical Streamlit application (`app.py`)** | **Interactive Review Cockpit** |
| **`tests/`** | **Tier A (Runtime)** | **16 automated pytest unit and invariant tests** | **Quality Assurance** |
| **`models/`** | **Tier A (Runtime)** | Serialized XGBoost models, scalers, and preprocessors | Inference & triage scoring |
| **`results/`** | **Tier A (Runtime)** | Chronological split CSVs, metrics, and strategy evaluation tables | Ground truth experimental results |
| **`BigFlow_sample.csv`** | **Tier A (Runtime)** | 500,000-flow benchmark network intrusion dataset | Raw experimental data |

---

## 2. Safe Execution & Dependency Guarantee (Why Core Code Stays at Root)

### The Absolute Preservation Rule
To prevent path breakage, import errors, and execution failures, all **Tier A** files and directories (`src/`, `dashboard/`, `tests/`, `models/`, `results/`, `BigFlow_sample.csv`, `requirements.txt`, `README.md`, and `.gitignore`) are **retained directly at the root level**.

### Technical Justification
1. **Relative Path Integrity:** Multiple scripts in `src/` use direct relative paths to load and save data (e.g., `results/train.csv`, `models/xgb_model.joblib`, `results/shifted_test_all_signals.csv`).
2. **Dashboard Base Resolution:** `dashboard/app.py` resolves its data directory via:
   ```python
   BASE = Path(__file__).resolve().parent.parent
   RESULTS_DIR = BASE / "results"
   ```
   Keeping `dashboard/` and `results/` at the root ensures this resolution path works identically on any machine without path configuration.
3. **Automated Test Suite Discovery:** Standard testing commands (`pytest tests/`) rely on finding `tests/`, `src/`, and `results/` relative to the execution root.
4. **Zero-Breakage Guarantee:** Moving only the surrounding documents, slides, reports, media, and offline utilities while preserving the canonical core at root guarantees **100% execution stability** while delivering a pristine, uncluttered directory structure.

---

## 3. Viva Defense Navigation Roadmap (Quick-Access for Student)

During your viva examination, when the panel or mentor asks a specific question, use this exact roadmap to immediately open the right file:

```
VIVA QUESTION CATEGORY            EXACT FILE TO OPEN / COMMAND TO RUN
─────────────────────────────────────────────────────────────────────────────────────────────────
1. Final Capstone Report           --> 01_FINAL_SUBMISSION/Adaptive_Human_Review_Allocation_Review_II_FINAL.pdf
2. Official Presentation Slides   --> 01_FINAL_SUBMISSION/PES1PG25CA101_KARANSHETTYKN_REVIEW_PPT.pdf
3. Fast Viva Q&A Cheatsheet       --> 03_REPORTS_AND_DOCS/Viva_Cheatsheet.md
4. Mathematical 4-Signal Proof    --> 06_PROJECT_DOCUMENTATION/docs/SIGNAL_VALIDATION_AND_ABLATION.md
5. Data Leakage Prevention Proof  --> 06_PROJECT_DOCUMENTATION/docs/DATA_SPLIT_AND_LEAKAGE_AUDIT.md
6. Statistical Significance & CIs --> 06_PROJECT_DOCUMENTATION/docs/STATISTICAL_VALIDATION.md
7. Why FR14 is 92.9% Implemented   --> 06_PROJECT_DOCUMENTATION/docs/FR14_REMAINING_WORK.md
8. Run All 16 Automated Tests     --> Command: pytest tests/
9. Authoritative Verification     --> Command: python src/30_verify_results.py
10. Launch Interactive Cockpit    --> Command: streamlit run dashboard/app.py
11. Run Live Batch Triage Demo    --> Command: python src/run_demo_batch.py
12. Modular LaTeX Source Code     --> 07_LATEX_SOURCE/PES1PG25CA101-KARANSHETTYKN-Report/
13. Architecture Diagrams (PNG)   --> 08_DIAGRAMS_AND_MEDIA/diagrams/
14. Complete Inventory & Hashes   --> 00_START_HERE/FILE_INDEX.csv
─────────────────────────────────────────────────────────────────────────────────────────────────
```

---

## 4. What Not to Edit (Preservation Guidelines)

- **Do NOT edit files in `results/`:** These CSV files contain the verified ground truth experimental outcomes. Modifying them will cause `pytest tests/` and `python src/30_verify_results.py` to fail.
- **Do NOT edit models in `models/`:** These are trained preprocessors and XGBoost classifiers.
- **Do NOT edit `01_FINAL_SUBMISSION/` files:** These represent the finalized, frozen submission deliverables.
- **Do NOT edit `10_HISTORICAL_AND_ALTERNATE_VERSIONS/`:** Kept purely for forensic and historical reference.
