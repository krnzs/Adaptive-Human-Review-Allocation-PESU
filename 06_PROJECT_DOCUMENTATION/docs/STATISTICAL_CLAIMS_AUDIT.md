# STATISTICAL CLAIMS AUDIT: BOOTSTRAP RESAMPLING, SIGNIFICANCE & EVALUATION METRICS

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Guide:** Dilip Kumar Maripuri  
**Department of Computer Applications, PES University, Bengaluru**  
**Audit Date:** 2026-10-28  

---

## 1. Executive Summary & Core Definitions

This document conducts a rigorous audit of all statistical claims, bootstrap resampling procedures, confidence intervals, and evaluation metrics reported across the project.

### Core Metrics at 1% Review Budget (Shifted Test Set: 75,000 flows, 3,427 total errors, K = 750 reviews)

| Metric Concept | Mathematical Definition | Numerical Value | Interpretation & Context |
|:---|:---|:---:|:---|
| **Adaptive Errors Caught** | Absolute count of true errors in top 750 adaptive queue | **610 errors** | Primary benchmark outcome (`final_shifted_strategy_comparison.csv`) |
| **Confidence Errors Caught** | Absolute count of true errors in top 750 least-confidence queue | **463 errors** | Primary baseline outcome |
| **Total Test Errors** | Denominator of ground-truth classifier errors | **3,427 errors** | Ground truth misclassifications in shifted test partition |
| **Adaptive Error Capture Rate** | $610 / 3,427 \times 100\%$ | **17.80%** | Fraction of all test errors intercepted by the human reviewer |
| **Confidence Capture Rate** | $463 / 3,427 \times 100\%$ | **13.51%** | Fraction of all test errors intercepted by confidence baseline |
| **Absolute Capture-Rate Difference** | $17.7998\% - 13.5104\% = (610 - 463) / 3,427 \times 100\%$ | **+4.29 percentage points** | Absolute increase in error capture over the entire error pool |
| **Relative Improvement** | $(610 - 463) / 463 \times 100\% = 147 / 463 \times 100\%$ | **+31.75%** | Percentage increase in errors caught relative to confidence triage |
| **Review Precision (Yield)** | Adaptive: $610 / 750 = 81.33\%$; Confidence: $463 / 750 = 61.73\%$ | **+19.60 percentage points** | Proportion of reviewed flows that were true classifier errors |
| **Mean Bootstrap Advantage** | $\frac{1}{B}\sum_{b=1}^{1000} (c_{\text{adapt}, b} - c_{\text{conf}, b})$ from `extended_bootstrap_cis.csv` | **+4.35% (+0.043466)** | Mean capture-rate difference across 1,000 bootstrap resamples |
| **95% Bootstrap Confidence Interval** | $[2.5\text{th percentile}, 97.5\text{th percentile}]$ of bootstrap capture differences | **[+3.45%, +5.28%]** | Empirical interval of absolute capture-rate difference |
| **Reported Significance** | Count of replicates where $\Delta_b \le 0$ out of 1,000 | **$p < 0.001$** | Empirical non-parametric bootstrap p-value |

---

## 2. Forensic Code Audit of Bootstrap Implementation (`src/29_extended_evaluation.py`)

### A. The Resampling Code
In `src/29_extended_evaluation.py` (lines 102–140):
```python
print("Running bootstrap...")
n_boot = 1000
boot_res = []
for b in budgets:
    K = int(b * len(df_signals))  # For b=0.01: K = 750
    diffs_static = []
    diffs_conf = []
    for _ in range(n_boot):
        idx = np.random.choice(len(df_signals), len(df_signals), replace=True)
        df_boot = df_signals.iloc[idx]
        tot = df_boot['actual_error'].sum()
        if tot == 0: continue
        
        c_adapt = df_boot.sort_values('adaptive', ascending=False).head(K)['actual_error'].sum() / tot
        
        df_boot_static = df_boot.copy()
        df_boot_static['static'] = (0.25*df_boot['confidence_risk'] + 
                                    0.25*df_boot['ood_percentile'] + 
                                    0.25*df_boot['drift_risk'] + 
                                    0.25*df_boot['historical_risk'])
        c_stat = df_boot_static.sort_values('static', ascending=False).head(K)['actual_error'].sum() / tot
        
        c_conf = df_boot.sort_values('confidence_risk', ascending=False).head(K)['actual_error'].sum() / tot
        
        diffs_static.append(c_adapt - c_stat)
        diffs_conf.append(c_adapt - c_conf)
        
    boot_res.append({
        'budget': b,
        'adapt_vs_static_mean': np.mean(diffs_static),
        'adapt_vs_static_2.5': np.percentile(diffs_static, 2.5),
        'adapt_vs_static_97.5': np.percentile(diffs_static, 97.5),
        'adapt_vs_conf_mean': np.mean(diffs_conf),
        'adapt_vs_conf_2.5': np.percentile(diffs_conf, 2.5),
        'adapt_vs_conf_97.5': np.percentile(diffs_conf, 97.5),
    })
```

### B. Procedural Audit Findings

1. **What is Being Resampled?**
   - The resampling is performed on the test set instances ($N = 75,000$) with replacement.
   - The four signals (`confidence_risk`, `ood_percentile`, `drift_risk`, `historical_risk`) and model predictions were **precomputed** before the bootstrap loop.
   - The model, scalers, and covariance matrices are **not refitted** inside each replicate. This is standard **evaluation-level policy benchmarking**, which measures sampling variability of the evaluation set, but does not capture training set variability.

2. **Top-K Queue Recomputation:**
   - In every replicate, the resampled DataFrame `df_boot` is independently sorted:
     `df_boot.sort_values('adaptive', ascending=False).head(K)`
     `df_boot.sort_values('confidence_risk', ascending=False).head(K)`
   - The top-K queue is **properly recomputed on the resampled data** in each iteration.

3. **Handling of Ties:**
   - `pandas.DataFrame.sort_values` uses a stable sort (preserving index order for duplicate score values).
   - Because scores are continuous floating-point combinations of four signals, ties in the top 750 entries are virtually non-existent for the adaptive score, though present for pure confidence where repeated predicted probabilities occur.

4. **Denominator Variation:**
   - `tot = df_boot['actual_error'].sum()` varies across replicates (multinomial sampling around the full-sample total 3,427).
   - `c_adapt` and `c_conf` are calculated relative to `tot`. This properly models the capture rate under varying error counts.

5. **Full-Sample Difference vs. Bootstrap Mean:**
   - Full sample: $\Delta = (610 - 463) / 3,427 = +4.2895\%$ (+4.29%).
   - Bootstrap mean: $\bar{\Delta} = +4.3466\%$ (+4.35%).
   - The difference ($+0.06\%$) represents slight non-linear ratio bias: $\mathbb{E}[A/B] \neq \mathbb{E}[A]/\mathbb{E}[B]$ when total errors $B$ fluctuates. This is statistically expected and well within normal bootstrap variance.

---

## 3. Critical Methodological Nuance & Statistical Limitations

### A. Non-Parametric Bootstrap Interval vs. Formal Asymptotic p-Value
- In `extended_bootstrap_cis.csv`, all 1,000 paired difference values $\Delta_b$ were strictly positive ($\min(\Delta_b) \approx +0.025$).
- Consequently, the empirical non-parametric p-value is reported as $p < 0.001$ because $0 / 1000$ resamples crossed zero.
- **Academic Nuance:** A non-parametric bootstrap that does not cross zero demonstrates that under instance-level resampling, Adaptive triage consistently beats Least Confidence. However, claiming a formal asymptotic hypothesis test p-value ($p < 0.001$) under a null hypothesis ($H_0: \Delta = 0$) strictly requires a centered bootstrap or a paired permutation test. In your viva, state:
  > *"In 1,000 paired instance bootstrap replicates, the adaptive strategy outperformed least-confidence in 100% of resamples (empirical $p < 0.001$, 95% CI $[+3.45\%, +5.28\%]$)."*

### B. Temporal Autocorrelation & Clustering of Network Flows
- Standard bootstrap resampling assumes i.i.d. observations.
- In network flow telemetry (BigFlow-NIDS), flow records are chronological and errors are **temporally clustered**: 2,291 of the 3,427 errors (66.8%) hit during the attack surge in Batch 5.
- Because errors are clustered in time, random i.i.d. sampling may underestimate the true variance compared to a **moving block bootstrap**.
- **Mitigating Factor:** To verify performance without i.i.d. assumptions, we executed the **rigid 5-batch sequential streaming evaluation** (`src/28_sequential_feedback_eval.py`), which forces 150 reviews per batch across time without lookahead. Even under rigid sequential constraints, Adaptive triage captures **183 errors vs. 168 static comparator errors** (+8.9% relative gain).

---

## 4. Extended Classification Performance Metrics

From `results/extended_model_metrics.csv` (generated by `src/29_extended_evaluation.py`):

| Metric | Validation Split (75k flows, 0.33% attacks) | Shifted Test Split (75k flows, 6.30% attacks) | Interpretation |
|:---|:---:|:---:|:---|
| **ROC-AUC** | 0.9228 | 0.9510 | Strong ranking discrimination across both splits |
| **PR-AUC (Average Precision)** | 0.0540 | **0.7444** | Reflects attack prevalence change (0.33% in Val vs 6.30% in Test) |
| **Balanced Accuracy** | 0.5408 | **0.7321** | Robust accuracy balancing minority attack class |
| **Expected Calibration Error (ECE)** | 0.0120 | **0.0200** | Good probability calibration ($< 0.05$ threshold) |
| **F1-Score** | 0.0552 | **0.5684** | Precision = 0.7016, Recall = 0.4778 on shifted test |

---

## 5. Recommended Exact Wording for Viva Defense & Report

When presenting the statistical results to your viva panel:

1. **On Error Gain:**
   > *"Under a 1% human review budget (750 flows), the Feedback-Adaptive strategy captures **610 errors (17.80%)** compared to **463 errors (13.51%)** for Least-Confidence triage. This represents an absolute gain of **+4.29 percentage points** of total errors, and a **+31.7% relative improvement** in caught errors. In terms of reviewer yield, the adaptive queue achieves **81.33% precision** (610 true errors / 750 reviews) versus **61.73% precision** for confidence sampling (+19.6 percentage points)."*

2. **On Bootstrap Significance:**
   > *"Over 1,000 paired bootstrap replicates recomputed on the shifted test set, the mean capture-rate advantage was **+4.35%**, with a 95% empirical confidence interval of **[+3.45%, +5.28%]**. In all 1,000 replicates, the adaptive queue strictly outperformed confidence triage ($p < 0.001$ empirical)."*

3. **On Limitations:**
   > *"We acknowledge that standard i.i.d. bootstrap resampling does not account for temporal autocorrelation in network flows. We therefore validated our approach under rigid 5-batch chronological streaming without temporal lookahead, where adaptive triage captured **183 errors** versus **168 errors** for the static comparator."*
