# Interactive Research Dashboard: User & Demonstration Guide

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Candidate:** Karan Shetty (`PES1PG25CA101`)  
**Guide:** Dilip Kumar Maripuri | **Institution:** PES University  

This guide provides step-by-step instructions for launching, navigating, and presenting the Streamlit research dashboard (`dashboard/app.py`) during viva and mentor reviews.

---

## 1. Quick Launch Instructions

### Prerequisites
Ensure your Python environment contains the required packages:
```powershell
pip install streamlit plotly pandas numpy
```

### Launch Command
From the project root directory, run:
```powershell
streamlit run dashboard/app.py
```
The browser will automatically open to `http://localhost:8501`.

---

## 2. Walkthrough of Dashboard Controls & Panels

### Panel 1: Top Hero & KPI Cards
- **What is displayed:**
  - `EVALUATION SET: 75,000` (Chronological Shifted Test partition).
  - `TOTAL PREDICTION ERRORS: 3,427` (4.57% error rate under attack surge).
  - `1% BUDGET ADAPTIVE CAPTURE: 610` (17.80% capture rate, 81.33% precision).
  - `PR-AUC / BALANCED ACC: 0.7444 / 0.7321` (Expected Calibration Error: 0.0200).
- **Viva Talking Point:** Highlight that the shifted test error rate (4.57%) is $4.55\times$ higher than the validation error rate (1.00%), proving temporal distribution shift.

---

### Panel 2: Interactive Strategy & Budget Explorer
- **Controls Available:**
  1. **Review Capacity Slider (`st.select_slider`):** Options: `1%`, `2%`, `5%`, `10%`.
  2. **Strategy Filter (`st.multiselect`):** Allows selecting/deselecting individual review strategies (`Feedback_Adaptive`, `Confidence`, `Static_MultiFactor`, `Random`, `OOD`).
- **Interactive Behavior:**
  - Selecting `1%` displays the horizontal bar chart showing **Feedback_Adaptive leading with 610 errors (17.8%)**, followed by Static (600), Confidence (463), Random (40), and OOD (1).
  - Selecting `5%` or `10%` demonstrates the **Honest Crossover**, where Confidence-Only takes the lead (2,243 errors at 5%, 2,879 at 10%).

---

### Panel 3: Review Efficiency (Yield Curve) & Distribution Shift
- **Left Chart (Yield Curve):**
  - Shows errors caught per 1,000 human reviews across budgets.
  - Demonstrates diminishing marginal returns as review budget increases.
  - At 1% budget, Adaptive review yields **813.3 errors per 1,000 reviews**.
- **Right Chart (PSI Drift Ranking):**
  - Displays the top-8 features exhibiting the strongest distribution shift measured by Population Stability Index.
  - Highlights `L4_SRC_PORT` and `IN_BYTES` as the primary drivers of temporal drift.

---

### Panel 4: Four Reliability Signals Diagnostic Expander
- **Action:** Click on `🔍 Inspect Four Reliability Signals & Mathematical Ranges`.
- **Content:**
  - **Uncertainty Card:** Displays range `[0, 0.50]`, formula $u = 1 - \max(P_0, P_1)$, and explains why unscaled margin prevents false alarm flooding under 1% budgets.
  - **Mahalanobis OOD Card:** Displays range `[0, 1.00]` and notes high correlation ($\rho = 0.8414$) with PSI drift.
  - **PSI Drift Card:** Displays range `[0, 1.00]` and explains marginal feature shift scoring.
  - **Historical Error Card:** Displays range `[0, 1.00]` and explains that removing this signal collapses 1% error capture from 17.80% to 0.73%.

---

### Panel 5: Sequential 5-Batch Online Adaptation Trace
- **Action:** Click on `⚡ Sequential 5-Batch Online Adaptation Trace`.
- **Content:**
  - Left Chart: Shows errors caught across the 5 sequential batches (32, 35, 38, 38, 40).
  - Right Chart: Shows the dynamic progression of historical error weight $w_{\text{hist}}$ increasing from $0.250 \rightarrow 0.288 \rightarrow 0.331 \rightarrow 0.380 \rightarrow 0.400$.

---

### Panel 6: Experiment Detail Table & CSV Download
- **Data Table:** Renders a clean summary table of active strategies, reviews, errors caught, capture percentage, and error yield per 1,000 reviews.
- **Download Button:** Click `📥 Download Full Strategy Comparison CSV` to export `final_shifted_strategy_comparison.csv` directly to your local downloads folder.

---

## 3. Demonstration Script for Viva / Presentation

1. **Step 1 (Open Dashboard):** Launch via `streamlit run dashboard/app.py`.
2. **Step 2 (Set Context):** Point to the Top KPI cards: *"Here we evaluate 75,000 network flows under temporal distribution shift, containing 3,427 actual model misclassifications."*
3. **Step 3 (Show 1% Budget Advantage):** Move the budget slider to `1%`: *"At a 1% budget (750 flows), standard confidence triage catches 463 errors. Our Feedback-Adaptive system catches 610 errors—a 31.7% relative improvement."*
4. **Step 4 (Demonstrate the Crossover):** Move the slider to `5%` and `10%`: *"Notice the honest crossover: as budget expands, confidence triage becomes superior. This proves our method is specifically optimized for resource-scarce operational regimes."*
5. **Step 5 (Show Sequential Adaptation):** Expand the Sequential 5-Batch trace: *"Here we demonstrate how the human review yield in earlier batches dynamically tunes the historical error weight from 0.25 up to 0.40 for subsequent batches."*

---

## 4. Troubleshooting

- **Error: `Port 8501 is already in use`:**
  Run `streamlit run dashboard/app.py --server.port 8502`.
- **Data Missing Warning:**
  Ensure the script is executed from the project root directory so relative paths to `results/` resolve properly.
- **Headless Environment Verification:**
  To verify dashboard syntax without opening a browser:
  ```powershell
  python -m py_compile dashboard/app.py
  ```
