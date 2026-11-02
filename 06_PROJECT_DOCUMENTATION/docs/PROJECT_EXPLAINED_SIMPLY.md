# Project Explained Simply: The Complete MCA Tutor Guide

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty | **SRN:** `PES1PG25CA101`  
**Guide:** Dilip Kumar Maripuri | **Institution:** PES University, Bengaluru  
**Degree:** Master of Computer Applications (Data Analytics)  

---

## 1. The Operational Problem

### Simple Definition
In real-world security operations (like a Security Operations Center, or SOC), machine learning models scan millions of network connections to detect cyberattacks. However, models are not perfect: they make mistakes (false alarms and missed attacks). Organizations employ human cybersecurity analysts to review alerts, but analysts can only manually inspect a tiny fraction—often just **1% or 2%**—of total traffic due to human cognitive limits and time constraints.

### Why It Is Needed
If you only have time to inspect 1% of predictions (e.g., 750 network flows out of 75,000), how do you choose which 750 flows to give to the human analyst? If you pick randomly, you find almost zero errors. If you pick only based on the model's confidence, you miss dangerous attacks where the model was confident but completely wrong.

### Viva-Ready Explanation
> *"In high-throughput environments like network intrusion detection, human review capacity is severely constrained. Our project designs an intelligent allocation engine that routes the most error-prone network flows to human analysts under strict operational review budgets."*

---

## 2. Why Distribution Shift Matters

### Simple Definition
Distribution shift occurs when the real-world data seen during live operation looks different from the historical data used to train the model.

### Concrete Example in This Project
In our dataset (`BigFlow_sample.csv`, 500,000 flows from NF-UQ-NIDS-v2):
- **Training Period:** 6.10% attacks. Normal business hours.
- **Validation Period:** 0.33% attacks. A natural lull in network attacks; the model made 753 errors (1.00% error rate).
- **Shifted Test Period:** 6.30% attacks. A major surge in cyberattacks and traffic bursts. The model made **3,427 errors (4.57% error rate)**—a **4.55-fold surge in error rate**!
- Key features like `L4_SRC_PORT` and `IN_BYTES` shifted dramatically (PSI > 0.50).

### Formula: Population Stability Index (PSI)
$$\text{PSI} = \sum_{b=1}^{B} \left( P_b - Q_b \right) \ln\left( \frac{P_b}{Q_b} \right)$$
Where $P_b$ is the proportion of validation/test data in bin $b$, and $Q_b$ is the training reference proportion. $\text{PSI} > 0.25$ indicates significant distribution shift.

### Viva-Ready Explanation
> *"Under distribution shift, machine learning models experience silent performance degradation. In our benchmark, temporal shift increased the model error rate by 455%. Standard confidence scores become miscalibrated, making multi-factor reliability triage necessary."*

---

## 3. The Dataset and Chronological Split

### Partition Design
- **Source File:** [`src/02_create_splits.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/02_create_splits.py)
- **Dataset:** NF-UQ-NIDS-v2 / BigFlow-NIDS (500,000 netflow records, 49 features).
- **Sorting:** Chronologically sorted by `Timestamp` prior to index slicing.

| Partition | Row Count | Percentage | Timestamp Window | Attack Prevalence | Model Errors |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **Train** | 350,000 | 70.0% | 2021-04-05 08:34:00 to 13:30:10 | 6.10% (21,350) | 12,392 (3.54%) |
| **Validation** | 75,000 | 15.0% | 2021-04-05 13:30:10 to 14:32:45 | 0.33% (248) | 753 (1.00%) |
| **Shifted Test** | 75,000 | 15.0% | 2021-04-05 14:32:45 to 15:35:20 | 6.30% (4,725) | 3,427 (4.57%) |

### Viva-Ready Explanation
> *"We enforce a strict chronological 70/15/15 split. Random train-test splitting would interleave past and future packets, leaking temporal structure and underestimating real-world error rates."*

---

## 4. Data Leakage and Its Prevention

### Simple Definition
Data leakage occurs when information from the evaluation or future data is accidentally used during data preparation, model training, or signal calibration.

### How We Prevent Leakage
1. **Preprocessing (`src/03_preprocess.py`):** `StandardScaler.fit()` and `SimpleImputer.fit()` run exclusively on the 350,000 training flows. Validation and Shifted Test features are transformed using `scaler.transform()`.
2. **Signal Fitting:** OOD mean/covariance, PSI reference bins, and historical error centroids are computed strictly on training data.
3. **Queue Sorting:** The review queue is ranked purely using composite risk $R(\mathbf{x})$, which uses model predictions and features. The ground-truth test labels ($y_{\text{test}}$) are never passed to the sorting algorithm.
4. **Sequential Feedback:** Labels are revealed *only* for the 150 items chosen for review in batch $t$, and weight updates are applied *only* to batch $t+1$.

---

## 5. The Classifier and Its Predictions

### Architecture
- **Source File:** [`src/04_train_models.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/04_train_models.py)
- **Primary Model:** Extreme Gradient Boosting (`XGBClassifier`) with trees trained on class-imbalanced NetFlow traffic.
- **Shifted Test Performance:**
  - Accuracy: 95.43%
  - PR-AUC: 0.7444
  - Balanced Accuracy: 0.7321
  - Expected Calibration Error (ECE): 0.0200
  - Attack Precision: 87.12%, Attack Recall: 48.91%

---

## 6. The Four Reliability Signals

Our triage engine computes four complementary signals for every incoming network flow:

### Signal 1: Prediction Uncertainty ($u$)
- **Formula:** $u = 1 - \max(P_0, P_1) = \min(P_0, P_1) \in [0, 0.50]$
- **What it captures:** Decision boundary ambiguity. When $P(y=1) = 0.50$, uncertainty reaches its maximum of $0.50$.
- **Why it is unscaled:** In network traffic, 92.4% of flows have $P > 0.95$ ($u < 0.05$). Artificially multiplying by 2 or rank-normalizing causes benign boundary noise to overwhelm the top 1% queue. Keeping $u \in [0, 0.50]$ bounds its nominal weight contribution to 0.175 (22.58% effective share).

### Signal 2: Mahalanobis Out-of-Distribution Risk ($\text{OOD}$)
- **Formula:** $D_M(\mathbf{x}) = \sqrt{(\mathbf{x} - \boldsymbol{\mu}_{\text{train}})^T \boldsymbol{\Sigma}_{\text{train}}^{-1} (\mathbf{x} - \boldsymbol{\mu}_{\text{train}})}$, normalized to empirical percentile rank $\in [0, 1.00]$.
- **What it captures:** Joint multidimensional distance from normal training traffic.

### Signal 3: Distribution Drift Risk ($\text{Drift}$)
- **Formula:** Instance-level PSI mapping across top drifted features (`L4_SRC_PORT`, `IN_BYTES`), converted to percentile rank $\in [0, 1.00]$.
- **What it captures:** Marginal feature distribution shifts during attack waves.

### Signal 4: Historical Error Proximity ($\text{Hist}$)
- **Formula:** $k$-NN distance to misclassified training samples $E_{\text{train}} = \{\mathbf{x}_i \in X_{\text{train}} \mid \hat{y}_i \ne y_i\}$, percentile-ranked $\in [0, 1.00]$.
- **What it captures:** Proximity to known model blindspots and classifier vulnerabilities.

---

## 7. Composite Risk Calculation

The composite risk score $R(\mathbf{x})$ combines all four signals via convex weighting:
$$R(\mathbf{x}) = 0.35 \cdot u(\mathbf{x}) + 0.15 \cdot \text{OOD}(\mathbf{x}) + 0.25 \cdot \text{Drift}(\mathbf{x}) + 0.25 \cdot \text{Hist}(\mathbf{x})$$

- Because $u \in [0, 0.50]$ and the other three are in $[0, 1.00]$, the theoretical maximum composite score is:
$$R_{\max} = 0.35(0.50) + 0.15(1.00) + 0.25(1.00) + 0.25(1.00) = 0.175 + 0.650 = 0.825$$

---

## 8. Human Review Allocation & The Honest Crossover

### Review Budgets
Review budgets specify what percentage of predictions a human analyst can inspect:
- 1% Budget = 750 flows
- 2% Budget = 1,500 flows
- 5% Budget = 3,750 flows
- 10% Budget = 7,500 flows

### The Five Strategies Compared
1. **Random Review:** Baseline uniform sampling. Catches 40 errors (1.17%) at 1%.
2. **Mahalanobis OOD-Only:** Sorts by OOD distance. Catches 1 error (0.03%) at 1% because most OOD flows are benign traffic shifts!
3. **Confidence-Only:** Traditional lowest-confidence triage. Catches 463 errors (13.51%) at 1%.
4. **Static Multi-Factor:** Fixed four-signal weighting. Catches 600 errors (17.51%) at 1%.
5. **Feedback-Adaptive:** Dynamic multi-factor triage with online weight adaptation. Catches **610 errors (17.80%)** at 1%.

### The Honest Crossover
- **At 1% and 2% budgets:** Feedback-Adaptive is the clear winner (**610 vs. 463 errors at 1%**, +31.7% relative gain; **1,174 vs. 916 errors at 2%**, +28.2% relative gain).
- **At 5% and 10% budgets:** Confidence-Only overtakes Adaptive (**2,243 vs. 1,573 errors at 5%**, and **2,879 vs. 1,794 errors at 10%**).
- **Why this crossover happens:** At generous review budgets ($\ge 5\%$), inspecting all uncertain flows directly captures misclassifications faster than multi-factor re-ranking. At tight budgets (1%), multi-factor signals are required to filter out false alarms.

---

## 9. Sequential 5-Batch Online Adaptation

- **Source File:** [`src/28_sequential_feedback_eval.py`](file:///C:/Users/Admin%20CDS/OneDrive/Desktop/Capstone%20Project/src/28_sequential_feedback_eval.py)
- The 75,000 Shifted Test flows are partitioned into 5 chronological batches of 15,000 flows each.
- In each batch, 150 flows (1%) are reviewed by the simulated analyst.
- When an analyst confirms errors, the historical error weight $w_{\text{hist}}$ is increased:
  - Batch 1: $w_{\text{hist}} = 0.250 \rightarrow 32$ errors caught
  - Batch 2: $w_{\text{hist}} = 0.288 \rightarrow 35$ errors caught
  - Batch 3: $w_{\text{hist}} = 0.331 \rightarrow 38$ errors caught
  - Batch 4: $w_{\text{hist}} = 0.380 \rightarrow 38$ errors caught
  - Batch 5: $w_{\text{hist}} = 0.400 \rightarrow 40$ errors caught
- **Total:** 183 errors caught across 5 batches (24.40% yield), beating static allocation (161 errors) and random review (34 errors).

---

## 10. Signal Correlations and Ablation Findings

### High Correlation ($\rho = 0.8414$) Between OOD and Drift
- Spearman rank correlation between Mahalanobis OOD percentile and PSI Drift risk is **+0.8414** ($>70\%$ shared rank variance).
- They both act as *Distribution Shift Detectors*.

### Ablation Collapse: Dropping Historical Error
- In leave-one-out ablations at 1% budget:
  - Full System: 610 errors (17.80%)
  - Without Historical Error: **25 errors (0.73%)** — a **95.9% collapse**!
- **Reason:** OOD and Drift flag over 15,000 shifted flows. Without Historical Error to pinpoint known classifier failure zones, the 750 review slots are diluted by correctly classified benign shifted flows.

---

## 11. Limitations and Future Work (Phase-II)

1. **Simulated vs. Real Humans:** Review is mathematically simulated using ground truth; no real human user study was conducted.
2. **Offline Benchmark:** Evaluated on the BigFlow-NIDS NetFlow dataset; not a real-time streaming pipeline.
3. **Phase-II Extensions:**
   - Real-time probability recalibration (streaming isotonic regression).
   - SHAP explanation cards for human analysts.
   - Bilevel meta-optimization for dynamic weight updates.
