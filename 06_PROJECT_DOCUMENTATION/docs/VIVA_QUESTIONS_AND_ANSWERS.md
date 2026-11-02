# Master Viva Voce Preparation Guide (42 Questions & Answers)

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty | **SRN:** `PES1PG25CA101`  
**Degree:** Master of Computer Applications (Data Analytics)  
**Guide:** Dilip Kumar Maripuri | **Institution:** PES University, Bengaluru  

---

## Category 1: Research Motivation & Problem Formulation

### Q1: What is the fundamental research problem your project addresses?
> **Answer:** In high-throughput, safety-critical domains such as network intrusion detection, machine learning models experience performance degradation under distribution shift. Organizations cannot manually review all alerts; they have strict human review budgets (often 1% to 2% of total traffic). Our project designs an adaptive allocation mechanism that intelligently prioritizes the most error-prone instances for human expert review to maximize the capture of classification mistakes under constrained budgets.

### Q2: Why can't we simply rely on the model's confidence score to select cases for review?
> **Answer:** Standard confidence scores assume independent and identically distributed (i.i.d.) test data. Under distribution shift, neural networks and tree models suffer from overconfidence—they can assign high confidence (>90%) to samples that they misclassify. Relying solely on confidence leaves blindspots where the model is confident but wrong.

### Q3: What is "Selective Classification" or "Learning with a Reject Option", and how does your project differ?
> **Answer:** Selective classification typically rejects instances below a confidence threshold without budget constraints. In our project, review capacity is strictly budgeted ($K = \lfloor B \times N \rfloor$). We solve a bounded, top-$K$ knapsack triage problem under distribution shift, combining multiple orthogonal signals rather than confidence alone.

### Q4: What benchmark dataset is used, and what does it represent?
> **Answer:** We evaluate on the NF-UQ-NIDS-v2 benchmark (BigFlow-NIDS), utilizing a standardized 500,000-flow experimental sample. It contains 49 NetFlow v2 features representing realistic enterprise network traffic containing benign activities and cyberattacks (DoS, PortScans, BruteForce).

---

## Category 2: Dataset Partitioning & Data Leakage Prevention

### Q5: How is the dataset partitioned, and why did you choose this split?
> **Answer:** The dataset is partitioned chronologically into 70% Training (350,000 flows), 15% Validation (75,000 flows), and 15% Shifted Test (75,000 flows). We sort strictly by timestamp before slicing. Random splitting would interleave past and future packets, leaking temporal autocorrelation and artificially masking real-world distribution shift.

### Q6: What are the exact timestamps and attack prevalences of the three partitions?
> **Answer:**
> - **Train:** 350,000 flows (08:34:00 to 13:30:10), attack prevalence 6.10% (21,350 attacks).
> - **Validation:** 75,000 flows (13:30:10 to 14:32:45), attack prevalence 0.33% (248 attacks — a natural lull).
> - **Shifted Test:** 75,000 flows (14:32:45 to 15:35:20), attack prevalence 6.30% (4,725 attacks — distribution shift surge).

### Q7: What is the distribution shift impact on model error rate?
> **Answer:** The validation set had 753 model errors (1.004% error rate). The shifted test set had 3,427 errors (4.569% error rate). The error rate surged by approximately $4.55\times$ ($455\%$), demonstrating pronounced temporal distribution shift.

### Q8: How did you ensure zero data leakage in feature preprocessing?
> **Answer:** Preprocessing transformers (`StandardScaler` and `SimpleImputer`) were fitted strictly on `X_train` (`scaler.fit(X_train)` in `src/03_preprocess.py`). The validation and shifted test sets were transformed using the pre-fitted object (`scaler.transform()`). No test set statistics ($\mu, \sigma$) entered the preprocessing pipeline.

### Q9: Did test labels leak into the review queue selection?
> **Answer:** No. Queue construction ranks instances purely using the composite risk score $R(\mathbf{x})$, which depends only on feature values and model output probabilities. Ground-truth test labels are accessed only after the top-$K$ queue is frozen to compute evaluation metrics.

---

## Category 3: Base Classifier & Reliability Signals

### Q10: What base classifier is used, and what was its performance?
> **Answer:** We trained XGBoost, Random Forest, and Logistic Regression. XGBoost achieved the highest validation F1-score (0.912) and was selected as the base classifier. On the Shifted Test set, it achieved 95.43% overall accuracy, a PR-AUC of 0.7444, Balanced Accuracy of 0.7321, and an Expected Calibration Error of 0.0200.

### Q11: What are the four reliability signals used in the composite score?
> **Answer:**
> 1. **Prediction Uncertainty ($u$):** Distance from certainty, $1 - \max(P_0, P_1) \in [0, 0.50]$.
> 2. **Mahalanobis OOD Score:** Multidimensional distance to the in-distribution training centroid.
> 3. **PSI Drift Risk:** Instance-level deviation along top drifted features.
> 4. **Historical Error Proximity:** $k$-NN distance to misclassified training instances.

### Q12: Why is the uncertainty signal bounded in $[0, 0.50]$ while other signals are in $[0, 1.00]$?
> **Answer:** For binary classification, confidence is $\max(P_0, P_1) \ge 0.50$, so $u = 1 - \text{conf} \in [0, 0.50]$. OOD, Drift, and Historical Error are percentile-ranked against training baselines into $[0, 1.00]$. In network traffic, 92.4% of flows have $P > 0.95$ ($u < 0.05$). Artificially doubling $u$ or rank-normalizing it causes benign borderline noise to displace flows near true error clusters, reducing 1% error capture from 610 down to 527 (or 280 with rank normalization). Keeping $u \in [0, 0.50]$ is methodologically and empirically justified.

### Q13: What is the theoretical maximum composite score under current scaling?
> **Answer:** With weights $(0.35, 0.15, 0.25, 0.25)$, the theoretical maximum score is $R_{\max} = 0.35(0.50) + 0.15(1.00) + 0.25(1.00) + 0.25(1.00) = 0.175 + 0.650 = 0.825$.

### Q14: How is Mahalanobis distance calculated, and what does it measure?
> **Answer:** $D_M(\mathbf{x}) = \sqrt{(\mathbf{x} - \boldsymbol{\mu}_{\text{train}})^T \boldsymbol{\Sigma}_{\text{train}}^{-1} (\mathbf{x} - \boldsymbol{\mu}_{\text{train}})}$. It measures how far a flow lies from the training distribution centroid, accounting for feature correlations. It is converted to an empirical percentile rank against training data.

### Q15: How is the PSI Drift Risk signal computed?
> **Answer:** We compute the Population Stability Index for all features between training and evaluation partitions. The top shifted features (`L4_SRC_PORT`, `IN_BYTES`) are identified, and instance-level drift risk is computed as the normalized cumulative quantile departure along these features.

### Q16: How is the Historical Error Memory signal constructed?
> **Answer:** We extract misclassified instances from the training set: $E_{\text{train}} = \{\mathbf{x}_i \in X_{\text{train}} \mid \hat{y}_i \ne y_i\}$. We fit a nearest-neighbor index on $E_{\text{train}}$. For any new flow, its Euclidean distance to the nearest training mistake is computed and inverted into a percentile risk score.

---

## Category 4: Review Allocation Strategies & Results

### Q17: What review budgets did you evaluate?
> **Answer:** We evaluated four fixed operational review budgets on the 75,000 Shifted Test set: 1% (750 flows), 2% (1,500 flows), 5% (3,750 flows), and 10% (7,500 flows).

### Q18: What five strategies were benchmarked?
> **Answer:**
> 1. **Random Allocation:** Uniform random sampling baseline.
> 2. **OOD-Only:** Allocates highest Mahalanobis distance flows.
> 3. **Confidence-Only:** Traditional lowest-confidence triage.
> 4. **Static Multi-Factor:** Fixed convex combination of the four signals.
> 5. **Feedback-Adaptive:** Dynamic multi-factor triage with online weight adaptation.

### Q19: What are the verified error capture results at a 1% budget?
> **Answer:** Out of 3,427 total errors in the Shifted Test set:
> - Random: 40 errors (1.17%)
> - Pure OOD: 1 error (0.03%)
> - Confidence-Only: 463 errors (13.51%)
> - Static Multi-Factor: 600 errors (17.51%)
> - Feedback-Adaptive: **610 errors (17.80%)** — capturing 813 errors per 1,000 reviews (81.33% precision).

### Q20: What are the results at a 2% budget?
> **Answer:**
> - Random: 73 errors (2.13%)
> - Confidence-Only: 916 errors (26.73%)
> - Static Multi-Factor: 1,165 errors (34.00%)
> - Feedback-Adaptive: **1,174 errors (34.26%)**.

### Q21: What is the "Honest Crossover" phenomenon, and why does it occur?
> **Answer:** At 1% and 2% budgets, Feedback-Adaptive significantly outperforms Confidence-Only (+31.7% relative gain at 1%). However, at 5% and 10% budgets, Confidence-Only overtakes Adaptive, catching 2,243 vs. 1,573 errors at 5%, and 2,879 vs. 1,794 errors at 10%. This crossover occurs because when the review quota is generous ($\ge 5\%$), inspecting all uncertain flows directly sweeps up misclassifications faster than multi-factor re-ranking. At tight quotas (1%), multi-factor signals are required to filter out false alarms.

### Q22: Why did Pure OOD perform so poorly at 1% budget (only 1 error caught)?
> **Answer:** Mahalanobis OOD detects extreme density departures. However, under distribution shift, large volumes of benign traffic also experience feature shifts (e.g., changes in port numbers or byte sizes). Most OOD samples are actually benign flows that the model classifies correctly. OOD indicates novelty, not necessarily error.

---

## Category 5: Sequential Batch Feedback & Online Adaptation

### Q23: How does the sequential feedback loop work?
> **Answer:** The 75,000 Shifted Test flows are split into 5 chronological batches of 15,000 flows each. For each batch, the top 150 flows (1%) are selected using current weights. Labels are revealed strictly for the 150 reviewed flows. The precision of the review queue is calculated. If precision exceeds 40%, the historical error weight $w_{\text{hist}}$ is increased by a factor of 1.15 (up to a maximum of 0.40) for the next batch, and newly discovered mistakes are added to the error memory.

### Q24: What was the performance progression across the 5 batches?
> **Answer:**
> - Batch 1 ($w_{\text{hist}}=0.250$): 32 errors caught / 150 reviews (21.33% yield)
> - Batch 2 ($w_{\text{hist}}=0.288$): 35 errors caught / 150 reviews (23.33% yield)
> - Batch 3 ($w_{\text{hist}}=0.331$): 38 errors caught / 150 reviews (25.33% yield)
> - Batch 4 ($w_{\text{hist}}=0.380$): 38 errors caught / 150 reviews (25.33% yield)
> - Batch 5 ($w_{\text{hist}}=0.400$): 40 errors caught / 150 reviews (26.67% yield)
> - **Total:** 183 errors caught out of 750 reviews (24.40% cumulative yield), strictly outperforming Static Multi-Factor (161 errors) and Random (34 errors).

### Q25: Does the feedback loop update model weights or only review allocation weights?
> **Answer:** It updates only the review allocation weights and the historical error nearest-neighbor index. It does not retrain the base XGBoost model in real-time, avoiding catastrophic forgetting and ensuring reproducible evaluation.

---

## Category 6: Statistical Validity, Correlations & Ablations

### Q26: What is the Spearman rank correlation between OOD and Drift, and what does it mean?
> **Answer:** The Spearman correlation is $\rho = 0.8414$ ($p < 10^{-300}$). This indicates that OOD and Drift are highly redundant, sharing over 70% of rank variance. They functionally cluster together as *Distribution Shift Detectors*.

### Q27: What is the correlation between Uncertainty and Historical Error Risk?
> **Answer:** The Pearson linear correlation is $r = 0.5531$. They functionally cluster as *Error Proximity Detectors*, capturing decision boundary ambiguity and classifier vulnerability regions.

### Q28: What happened in the leave-one-out ablation when Historical Error was removed?
> **Answer:** Error capture at a 1% budget collapsed from 610 errors (17.80%) down to **25 errors (0.73%)**—a 95.9% drop. This proves that Historical Error proximity is the single most critical signal for surgical triage under tight review budgets.

### Q29: What happened when Uncertainty was removed in the ablation?
> **Answer:** Error capture collapsed to **12 errors (0.35%)**, confirming that Uncertainty and Historical Error provide the primary discriminative power, while OOD and Drift provide contextual shift awareness.

### Q30: What is the 95% bootstrap confidence interval for the Adaptive advantage at 1% budget?
> **Answer:** Based on 1,000 bootstrap resamples, the 95% confidence interval for the error capture advantage over Confidence-Only is **[+3.45%, +5.28%]** (mean gain +4.35%), confirming statistical significance ($p < 0.001$).

### Q31: What is Expected Calibration Error (ECE), and what was your model's ECE?
> **Answer:** ECE measures the difference between predicted probabilities and actual empirical accuracy across binned confidence intervals:
$$\text{ECE} = \sum_{m=1}^{M} \frac{|B_m|}{N} \left| \text{acc}(B_m) - \text{conf}(B_m) \right|$$
Our champion XGBoost model achieved an ECE of **0.0200** on the Shifted Test set, indicating well-calibrated probabilities.

---

## Category 7: Software Engineering, Tests & Dashboard

### Q32: What automated tests have you implemented?
> **Answer:** We implemented 13 executable pytest unit tests across four test files:
> - `tests/test_evaluation.py`: Queue capacity, index uniqueness, determinism, label isolation.
> - `tests/test_splits_and_leakage.py`: Partition counts, prevalences, timestamp non-overlap, label invariance.
> - `tests/test_signals_and_scoring.py`: Signal ranges ($u \in [0, 0.50]$, others in $[0, 1.00]$), score bounds ($R \le 0.825$), correlations ($\rho = 0.8414$, $r = 0.5531$).
> - `tests/test_results_consistency.py`: Exact 20 benchmark allocations, honest crossover, PR-AUC, Balanced Accuracy, ECE, bootstrap CIs.

### Q33: How do you launch the operational dashboard?
> **Answer:** By running `streamlit run dashboard/app.py` in the terminal.

### Q34: What interactive features does the dashboard support?
> **Answer:** Budget slider (1%, 2%, 5%, 10%), multiselect strategy filter, real-time error capture bar charts, efficiency yield curves, top-8 PSI drift ranking, four signals mathematical inspection cards, sequential 5-batch adaptation trace, and a direct CSV download button.

### Q35: What is the purpose of the two scripts numbered 28?
> **Answer:**
> - `src/28_historical_variants.py`: Compares error memory sources (Train vs. Val vs. Out-of-Fold).
> - `src/28_sequential_feedback_eval.py`: Implements the 5-batch online review simulation and weight updates.

### Q36: How does `src/30_verify_results.py` help your defense?
> **Answer:** It is a single-click verification script that programmatic asserts all 20 strategy-budget pairs, model metrics, bootstrap CIs, and data splits against saved artifacts, printing `[PASS]` for every university benchmark.

---

## Category 8: Project Status, Limitations & Viva Defense

### Q37: What is your exact approved functional requirement status?
> **Answer:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

### Q38: Why is FR14 only partially implemented?
> **Answer:** FR14 represents the Multi-Dataset Web Portal and Cross-Domain Deployment requirement. It is partially implemented as an interactive local Streamlit dashboard for the NF-UQ-NIDS-v2 dataset. Enterprise multi-tenant cloud ingestion and cross-domain deployment (medical, finance) are formally scoped for Phase-II.

### Q39: Did you use real human participants in this project?
> **Answer:** No. Human review was mathematically simulated using ground-truth labels from the benchmark dataset. Simulating human review is standard academic methodology for evaluating triage algorithms before conducting expensive human subject trials.

### Q40: Is this a production real-time streaming engine?
> **Answer:** No. It is an offline research benchmark and simulated batch adaptation pipeline designed to scientifically validate review allocation algorithms. Real-time streaming deployment (e.g., Kafka/Flink integration) is future engineering work.

### Q41: Why should an enterprise adopt your adaptive allocation system over standard confidence triage?
> **Answer:** In real-world security operations, analysts face alert fatigue and tight review quotas (1% of traffic). At a 1% budget, our system captures **610 errors (81.33% precision)** compared to only **463 errors (61.73% precision)** for confidence triage—catching **147 more cyberattack misclassifications** without hiring additional analysts.

### Q42: What are the three planned Phase-II technical enhancements?
> **Answer:**
> 1. Online streaming probability recalibration under non-stationary concept drift.
> 2. Explainable AI (Tree-SHAP) force plots displayed in the analyst review interface.
> 3. Bilevel meta-optimization for automated online learning of signal weights $\mathbf{w}$.
