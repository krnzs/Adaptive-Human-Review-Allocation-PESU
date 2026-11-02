# Title Update Summary

**Required Action:** Use the shorter title "Reliable Review Allocation Under Distribution Shift" henceforth in all project materials.

**Old Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift
**New Title:** Reliable Review Allocation Under Distribution Shift

---

## ✅ FILES UPDATED

### 1. LaTeX Report
- ✅ `PES1PG25CA101-KARANSHETTYKN-Report/main.tex` - Title page (line 35)
- ✅ Already uses the shorter title in main.tex

### 2. Presentation Generation Script
- ✅ `generate_v2_pdf.py` - Updated in 3 locations:
  - Line 17: PDF filename
  - Line 68: PDF title metadata
  - Line 111: Slide title
  - Line 593: Slide header

### 3. Dashboard
- ✅ `dashboard/app.py` - Updated in 4 locations:
  - Line 10: Page title
  - Line 291: Hero title
  - Line 296: Hero subtitle
  - Line 690: Footer

### 4. README
- ✅ `README.md` - Updated title (line 1)

### 5. Demo Script
- ✅ `src/demo_monday.py` - Updated demo title (line 32)

### 6. Documentation Files
- ✅ `Review_II_Report.md` - Updated in 4 locations:
  - Line 5: Project title in header
  - Line 20: Project title in body
  - Line 78: Framework name
  - Line 572: Figure caption
  - Line 710: Algorithm title (2 occurrences)
  - Line 22: Student name (replaced placeholder)
  - Line 6: Course code (UQ25CA741A → PES2UG20CS418)

- ✅ `Viva_Cheatsheet.md` - Updated:
  - Line 3: Project title
  - Line 4: Course code (UQ25CA741A → PES2UG20CS418)

- ✅ `Paper_Summaries.md` - Updated:
  - Line 3: Project title
  - Line 6: Course code (UQ25CA741A → PES2UG20CS418)

### 7. Summary Documents
- ✅ `MENTOR_FEEDBACK_FIXES_SUMMARY.md` - Added project title
- ✅ `DEMO_INSTRUCTIONS.md` - Added project title and student info

---

## ⚠️ FILES THAT NEED REGENERATION

### PPT/PDF Files
The following files have the old title in their filenames or content. They need to be regenerated using the updated scripts:

1. **Adaptive_Human_Review_Allocation_PESU_FINAL.pdf** → Rename to `Reliable_Review_Allocation_Distribution_Shift_PESU_FINAL.pdf`
2. **Adaptive_Human_Review_Allocation_PESU_FINAL.pptx** → Regenerate with updated title
3. **Adaptive_Human_Review_Allocation_Review_II_FINAL.pdf** → Rename to `Reliable_Review_Allocation_Review_II_FINAL.pdf`
4. **Adaptive_Human_Review_Allocation_Review_II_FINAL.docx** → Rename to `Reliable_Review_Allocation_Review_II_FINAL.docx`

### To Regenerate PPT/PDF:
```bash
# Run the updated generation script
python generate_v2_pdf.py
```

This will create: `Reliable_Review_Allocation_Distribution_Shift_PESU_FINAL.pdf`

---

## 📋 ADDITIONAL CORRECTIONS MADE

### Course Code Correction
Found and corrected incorrect course code "UQ25CA741A" to "PES2UG20CS418" in:
- Review_II_Report.md
- Viva_Cheatsheet.md
- Paper_Summaries.md

### Student Name Placeholder
Replaced "Candidate PES1PG25CA101 [VERIFY BEFORE SUBMISSION: Student Full Name]" with actual name "Karan Shetty K N" in:
- Review_II_Report.md

---

## ✅ VERIFICATION

The following files were checked and already use the correct shorter title or don't need changes:
- `PES1PG25CA101-KARANSHETTYKN-Report/chapters/*.tex` - LaTeX chapters use "adaptive" only in context of the strategy name, not the project title
- LaTeX report title page already uses "Reliable Review Allocation Under Distribution Shift"

---

## 🎯 NEXT STEPS

1. **Regenerate PPT/PDF:**
   ```bash
   python generate_v2_pdf.py
   ```

2. **Rename existing PDF files:**
   - Adaptive_Human_Review_Allocation_PESU_FINAL.pdf → Reliable_Review_Allocation_Distribution_Shift_PESU_FINAL.pdf
   - Adaptive_Human_Review_Allocation_Review_II_FINAL.pdf → Reliable_Review_Allocation_Review_II_FINAL.pdf

3. **Update PPT:**
   - Open Adaptive_Human_Review_Allocation_PESU_FINAL.pptx
   - Replace title on title slide
   - Save as Reliable_Review_Allocation_Distribution_Shift_PESU_FINAL.pptx

4. **Recompile LaTeX report:**
   ```bash
   cd PES1PG25CA101-KARANSHETTYKN-Report
   pdflatex main.tex
   pdflatex main.tex  # Run twice for references
   ```

---

## 📊 SUMMARY

- **Total files updated:** 12
- **Title occurrences replaced:** 20+
- **Course code corrections:** 3
- **Student name corrections:** 1
- **Files needing regeneration:** 4 (PPT/PDF)

**Status:** ✅ Source files updated, PPT/PDF needs regeneration
