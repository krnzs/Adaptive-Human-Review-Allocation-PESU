# Statistical Validation & Methodology Report

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  
**Date of Audit:** 2026-10-27  

---

## 1. Bootstrap Confidence Interval Methodology

### 1.1 Estimand & Paired Formulation
The primary statistical estimand is the **paired difference in error capture rate** between the Adaptive Multi-Factor strategy and the Confidence-Only strategy on the Shifted Test partition:
$$\Delta(B) = \frac{\sum_{i \in \mathcal{Q}_{\text{adapt}}(B)} \mathbb{I}(\hat{y}_i \ne y_i)}{\sum_{i=1}^N \mathbb{I}(\hat{y}_i \ne y_i)} - \frac{\sum_{i \in \mathcal{Q}_{\text{conf}}(B)} \mathbb{I}(\hat{y}_i \ne y_i)}{\sum_{i=1}^N \mathbb{I}(\hat{y}_i \ne y_i)}$$

Where:
- $N = 75,000$ (total shifted test flows).
- $B \in \{0.01, 0.02, 0.05, 0.10\}$ (review budget fraction).
- $\mathcal{Q}(B)$ is the top-$K$ review queue where $K = \lfloor B \times N \rfloor$.
- Total actual misclassifications in the sample: $\sum \mathbb{I}(\hat{y}_i \ne y_i) = 3,427$.

### 1.2 Resampling Procedure
Implemented in [`src/29_extended_evaluation.py#L113-L148`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/29_extended_evaluation.py#L113-L148):
1. **Replicate Count:** $n_{\text{boot}} = 1,000$ independent bootstrap iterations.
2. **Resampling Unit:** Instance-level rows sampled with replacement: $\mathcal{D}^{*(b)} \sim \text{Uniform}(\mathcal{D}_{\text{test}}, N)$.
3. **Paired Evaluation:** In each replicate $b$, the *exact same* resampled dataset $\mathcal{D}^{*(b)}$ is evaluated by both Adaptive and Confidence ranking functions, guaranteeing that sampling variance in error density affects both strategies identically.
4. **Interval Construction:** Non-parametric empirical percentile intervals:
   - Point Estimate (Mean): $+4.35\%$ capture percentage points.
   - Lower Bound (2.5th percentile): **$+3.45\%$**.
   - Upper Bound (97.5th percentile): **$+5.28\%$**.
5. **Empirical p-value:** Across all 1,000 paired bootstrap resamples, $\Delta^{*(b)} > 0$ for every replicate ($\min \Delta^{*(b)} = +2.61\% > 0$). Under the null hypothesis $H_0: \Delta \le 0$, the empirical p-value is:
   $$\hat{p} = \frac{1 + \sum_{b=1}^{1000} \mathbb{I}(\Delta^{*(b)} \le 0)}{1000 + 1} = \frac{1 + 0}{1001} < \mathbf{0.001}$$

---

## 2. Extended Statistical Metrics & Rationale

Evaluated on the 75,000 Shifted Test flows (3,427 errors, 4,724 attacks):

| Metric Name | Point Estimate | Mathematical Formula | Methodological Importance under Class Imbalance |
| :--- | :---: | :--- | :--- |
| **PR-AUC (Precision-Recall)** | **0.7444** | $\int_0^1 P(R) dR \approx \sum_k (R_k - R_{k-1}) P_k$ | Network attacks are rare (6.30% prevalence). Standard ROC-AUC can be deceptive because large benign true negatives inflate the score. PR-AUC evaluates precision strictly across positive recall levels. |
| **Balanced Accuracy** | **0.7321** | $\frac{1}{2} \left( \frac{\text{TP}}{\text{TP} + \text{FN}} + \frac{\text{TN}}{\text{TN} + \text{FP}} \right)$ | Avoids majority-class bias. A trivial classifier predicting all-benign achieves 93.70% raw accuracy but 50.0% Balanced Accuracy. Our model achieves Attack Recall 48.91% and Benign Specificity 97.51%. |
| **Expected Calibration Error (ECE)** | **0.0200** | $\sum_{m=1}^{M} \frac{\|B_m\|}{N} \|\text{acc}(B_m) - \text{conf}(B_m)\|$ | Confirms probability calibration reliability. An ECE of 0.020 indicates that predicted probabilities reflect empirical correctness within 2.0% across 10 quantile bins. |

---

## 3. Scientific Caveats & Methodological Critique

### Assumption of Independence in Bootstrap Resampling
- **Methodological Limitation:** The standard row-wise bootstrap assumes instances are independent and identically distributed. In real-world network NetFlow traffic, packet bursts and DoS attack flows exhibit temporal autocorrelation.
- **Impact:** Row-wise resampling may yield slightly narrower confidence intervals than a block bootstrap that resamples contiguous 5-minute time windows.
- **Academic Recommendation for Viva:** Acknowledge this property honestly. Pointing out that network flow data has temporal dependencies and that block bootstrap is a formal Phase-II refinement demonstrates advanced statistical maturity to academic examiners.
