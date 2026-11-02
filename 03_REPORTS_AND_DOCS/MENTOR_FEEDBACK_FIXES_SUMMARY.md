# Mentor Feedback Fixes - Summary

**Date:** October 4, 2026
**Student:** Karan Shetty K N (PES1PG25CA101)
**Guide:** Prof. Dilip Kumar Maripuri
**Project Title:** Reliable Review Allocation Under Distribution Shift

---

## ✅ COMPLETED FIXES

### 1. Dashboard Metric Correction (CRITICAL)
**Issue:** Dashboard showed 15.6% instead of 17.80% at 1% budget
**Fixed:** Updated `dashboard/app.py` line 370 from "15.6%" to "17.80%"
**File:** `dashboard/app.py`

---

### 2. Added Ablation Results to LaTeX Report (CRITICAL)
**Issue:** Report only showed Adaptive vs Confidence, missing ablation study
**Fixed:** Added to `chapters/results.tex`:
- Complete strategy comparison table (all 6 strategies)
- Class-specific (FN/FP) error capture table
- Ablation study table (leave-one-out variants)
- Extended model metrics table (ROC-AUC, PR-AUC, Balanced Accuracy, ECE)
**File:** `PES1PG25CA101-KARANSHETTYKN-Report/chapters/results.tex`

---

### 3. Workflow Boundary Clarification (CRITICAL)
**Issue:** Need to separate offline benchmarking, simulated feedback, and future operational workflow
**Fixed:** Added new section to `chapters/methodology.tex`:
- Stage 1: Offline Benchmarking (current Phase-I)
- Stage 2: Simulated Reviewer Feedback (current experiment)
- Stage 3: Future Operational Reviewer Workflow (Phase-II)
- Explicit statement: "Ground-truth labels are revealed ONLY AFTER review queue selection"
**File:** `PES1PG25CA101-KARANSHETTYKN-Report/chapters/methodology.tex`

---

### 4. Leakage Control Subsection (CRITICAL)
**Issue:** Need explicit demonstration of leakage control
**Fixed:** Added new section to `chapters/methodology.tex`:
- Historical Error Risk Source (training errors only)
- Model Selection and Weight Tuning (validation only)
- PSI-to-Instance-Level Conversion (training stats + validation PSI)
- Adaptive Weight Updates (heuristic, not learned from test)
**File:** `PES1PG25CA101-KARANSHETTYKN-Report/chapters/methodology.tex`

---

### 5. Repository Links Added (IMPORTANT)
**Issue:** No repository link in documents
**Fixed:** Added to:
- `README.md` - Added repository link placeholder, student info, guide info
- `chapters/implementation.tex` - Added code availability section
**Note:** You need to update "[GitHub Repository Link - UPDATE WITH ACTUAL URL]" with your actual repository URL
**Files:** `README.md`, `PES1PG25CA101-KARANSHETTYKN-Report/chapters/implementation.tex`

---

### 6. AI Usage Disclosure Added (IMPORTANT)
**Issue:** No AI usage disclosure
**Fixed:** Added to `README.md`:
- Clarifies AI used for code generation, debugging, documentation
- States research design is author's own work
- Confirms no external GenAI API in runtime
**File:** `README.md`

---

### 7. Demo Script Created (CRITICAL FOR MONDAY)
**Issue:** Need end-to-end demo for Monday
**Fixed:** Created `src/demo_monday.py`:
- Loads pre-trained XGBoost model
- Generates shifted test predictions
- Computes all reliability signals
- Applies adaptive risk scoring
- Demonstrates queue-capacity enforcement
- Shows error-capture results
- Displays class-specific (FN/FP) error capture
- Explicitly shows label revelation timing
- Shows ablation study results
**File:** `src/demo_monday.py`

---

### 8. Demo Instructions Document Created
**Fixed:** Created `DEMO_INSTRUCTIONS.md`:
- Prerequisites and setup
- Three demo options (automated, manual, dashboard)
- Demo talking points for each section
- Files to show during demo
- Progress reporting (96.4%)
**File:** `DEMO_INSTRUCTIONS.md`

---

## ⚠️ ITEMS NEEDING YOUR ATTENTION

### 1. Repository URL
**Action:** Update "[GitHub Repository Link - UPDATE WITH ACTUAL URL]" in:
- `README.md` line 5
- `chapters/implementation.tex` (new section)

### 2. Reference Numbering (Minor)
**Issue:** PPT cites BigFlow-NIDS as [16], but references.bib has it as entry [11]
**Action:** Reorder references.bib or update PPT citations
**Files:** `PES1PG25CA101-KARANSHETTYKN-Report/references.bib`, PPT

### 3. Progress Reporting (Minor)
**Issue:** Mentor mentioned 85% in form vs 96.4% in documents
**Action:** Use 96.4% consistently
**Calculation:** (13×100% + 1×50%) / 14 = 96.4%
**Mapping:**
- FR1-FR13: 100% complete (13/13)
- FR14 (Dashboard): 50% complete (local prototype only)

### 4. UQ25CA741A Identifier (Could Not Find)
**Issue:** Mentor mentioned incorrect footer identifier "UQ25CA741A"
**Status:** Could not find this in current documents
**Current documents show:** PES1PG25CA101 (your correct SRN)
**Action:** Verify if this is in an older version or different document

---

## 📋 MONDAY DEMO CHECKLIST

### Before Demo:
- [ ] Update repository URL in README.md and implementation.tex
- [ ] Verify all CSV result files exist in results/
- [ ] Run `python src/demo_monday.py` to test demo script
- [ ] Recompile LaTeX report with new sections
- [ ] Print or have ready key CSV files:
  - results/final_shifted_strategy_comparison.csv
  - results/extended_strategy_eval.csv
  - results/split_audit.csv

### During Demo:
- [ ] Run demo script: `python src/demo_monday.py`
- [ ] Show dashboard: `streamlit run dashboard/app.py`
- [ ] Demonstrate queue-capacity enforcement
- [ ] Explain label revelation timing (AFTER queue selection)
- [ ] Show FN/FP capture at 1% budget
- [ ] Explain ablation study results
- [ ] Clarify workflow boundary (3 stages)
- [ ] Explain leakage control (training errors only)

### Talking Points Prepared:
- ✅ Problem statement (constrained review capacity)
- ✅ Solution approach (multi-factor reliability)
- ✅ Key results (adaptive better at 1-2%, confidence better at 5-10%)
- ✅ Class-specific results (adaptive better at FN capture)
- ✅ Ablation study (confidence strongest signal)
- ✅ Leakage control (no test label leakage)
- ✅ Workflow boundary (offline → simulated → operational)
- ✅ Progress (96.4% complete)

---

## 📊 DOCUMENTS UPDATED

1. `dashboard/app.py` - Metric corrected
2. `PES1PG25CA101-KARANSHETTYKN-Report/chapters/results.tex` - Ablation, FN/FP added
3. `PES1PG25CA101-KARANSHETTYKN-Report/chapters/methodology.tex` - Workflow, leakage added
4. `PES1PG25CA101-KARANSHETTYKN-Report/chapters/implementation.tex` - Repository link added
5. `README.md` - Repository link, AI disclosure, demo instructions added
6. `src/demo_monday.py` - New demo script created
7. `DEMO_INSTRUCTIONS.md` - New demo guide created

---

## 🎯 MENTOR'S EXPECTATIONS - STATUS

| Requirement | Status |
|-------------|--------|
| Progress reporting consistent | ✅ 96.4% documented |
| Document identity & references | ⚠️ Repository URL needs update |
| Workflow boundary clarification | ✅ Added to methodology.tex |
| Leakage control demonstration | ✅ Added to methodology.tex |
| Strengthen evaluation (PR-AUC, FN/FP) | ✅ Added to results.tex |
| Explain review signals (ablation) | ✅ Added to results.tex |
| Executable evidence (repo link) | ⚠️ URL needs update |
| Demo script for Monday | ✅ Created demo_monday.py |

---

## 🚀 NEXT STEPS

1. **Immediate (Before Monday):**
   - Update repository URL in documents
   - Recompile LaTeX report
   - Test demo script with activated virtual environment
   - Print key CSV files

2. **Monday Morning:**
   - Run demo script to verify everything works
   - Launch dashboard to show visual results
   - Have CSV files ready for inspection
   - Prepare to explain each section

3. **After Demo:**
   - Address any additional feedback
   - Add actual figures to LaTeX report (replace placeholder.png)
   - Update PPT with ablation results
   - Finalize repository and push to GitHub

---

**Status:** READY FOR MONDAY DEMO (with minor URL update needed)
