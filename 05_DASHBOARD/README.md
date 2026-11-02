# INTERACTIVE HUMAN-REVIEW DASHBOARD GUIDE

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Guide:** Dilip Kumar Maripuri  
**Department of Computer Applications, PES University, Bengaluru**  

---

## 1. Dashboard Location & Architecture

The production dashboard application is located in **`dashboard/app.py`**.

> **Why `dashboard/` is maintained at root:**  
> The dashboard application resolves paths dynamically relative to its parent directory:
> ```python
> BASE = Path(__file__).resolve().parent.parent
> RESULTS_DIR = BASE / "results"
> ```
> Keeping `dashboard/` and `results/` directly at the project root guarantees seamless data loading with zero manual configuration.

---

## 2. How to Launch the Dashboard

Open PowerShell in the root project directory and execute:

```powershell
streamlit run dashboard/app.py
```

The application will start immediately and open in your default browser at `http://localhost:8501`.

---

## 3. Interactive Cockpit Features

The dashboard provides a comprehensive visual cockpit designed for human review supervisors and viva examiners:

1. **Review Allocation Cockpit (Tab 1):**
   - Interactive budget slider (0.5% to 10.0%).
   - Real-time comparison across all 5 strategies: Random, Confidence, OOD, Static Multi-Factor, and Feedback Adaptive.
   - Highlights the **Honest Crossover** where Adaptive triage dominates at tight budgets (1% and 2%) and Least-Confidence recovers at loose budgets (5% and 10%).

2. **Signal Breakdown & Distributions (Tab 2):**
   - Visual inspection of the 4 composite triage signals: Margin Uncertainty ($u$), OOD Mahalanobis Percentile ($z_{\text{ood}}$), PSI Drift ($z_{\text{psi}}$), and Slice Error Risk ($z_{\text{hist}}$).
   - Demonstrates why unscaled uncertainty prevents false-alarm noise from overwhelming the review queue.

3. **Online Sequential Feedback Simulation (Tab 3):**
   - Step-by-step 5-batch streaming simulation (15,000 flows/batch).
   - Demonstrates dynamic weight adaptation over time (183 errors caught, 24.40% yield vs 168 static comparator).

4. **Live Flow Inspector & Audit Queue (Tab 4):**
   - High-priority audit queue explorer showing top-ranked flows with composite score $R$, flow duration, packet rates, and predicted attack types.
   - Enables examiners to inspect high-confidence classification errors caught by the multi-signal score.
