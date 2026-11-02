# VIVA CLAIM REFERENCE GUIDE: DEFENDING YOUR CAPSTONE WITH EVIDENCE

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Department of Computer Applications, PES University, Bengaluru**  
**Milestone:** Capstone Phase-I Review-II & Viva Defense  

**Official Preserved Status Statement:**  
> **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

## Overview

During your viva examination, university examiners will test whether you truly understand the mathematics, data distributions, experimental anomalies, and limitations of your work. 

This guide provides concise, evidence-backed answers to the **8 most critical questions** your panel will ask. For every question, the answer is partitioned into:
1. **Verified Fact:** Direct, empirical evidence from your code and CSV data.
2. **Interpretation:** The underlying theoretical and engineering rationale.
3. **Unresolved Limitation:** Honest academic acknowledgment of assumptions or scope boundaries.
4. **Exact Viva Script:** A polished, confident 30-to-45 second spoken response.

---

## Question 1: Why does Adaptive Triage capture significantly more errors than Least-Confidence at low review budgets (1% and 2%)?

- **Verified Fact:**  
  At a 1.0% review budget (750 flows out of 75,000), Adaptive triage captures **610 errors (17.80%)**, while Least-Confidence triage captures only **463 errors (13.51%)**. This represents an absolute increase of **+4.29 percentage points** of total errors, and a **+31.7% relative improvement** in error detection (`results/final_shifted_strategy_comparison.csv`). At 2.0% budget, Adaptive captures **1,174 errors (34.26%)** vs. **916 errors (26.73%)** (+28.2% relative gain).
- **Interpretation:**  
  Under distribution shift, overparameterized classifiers frequently make **high-confidence errors** (silent failures where the model predicts Benign with $P > 0.90$ on zero-day attacks). Least-confidence sampling is completely blind to these instances because its score ($1 - \max(P_0, P_1)$) ranks them at the very bottom of the audit queue. Our adaptive score incorporates Mahalanobis distance ($z_{\text{ood}}$), PSI feature drift ($z_{\text{psi}}$), and slice failure risk ($z_{\text{hist}}$), which flags these anomalous instances regardless of model overconfidence.
- **Unresolved Limitation:**  
  The weights $(0.35, 0.15, 0.25, 0.25)$ were evaluated on the shifted test partition. While each individual signal is computed without test labels, hyperparameter optimization across weights is sensitive to the specific attack types present in BigFlow-NIDS.
- **Exact Viva Script:**  
  > *"At low review budgets like 1%, human review capacity is extremely scarce—only 750 flows out of 75,000. Under distribution shift, classifiers frequently fail silently with high confidence on zero-day attacks. Least-confidence triage only looks at the decision boundary, completely missing these high-confidence errors. By augmenting uncertainty with Mahalanobis out-of-distribution distance and feature drift, our adaptive framework intercepts these silent failures, capturing 610 errors versus 463 for confidence triage—a verified 31.7% relative improvement."*

---

## Question 2: Why does Confidence-Only triage overtake Adaptive allocation at larger review budgets (5% and 10%)? (The Honest Crossover)

- **Verified Fact:**  
  At a 5.0% review budget (3,750 flows), Confidence triage captures **2,243 errors (65.45%)**, strictly beating Adaptive triage's **1,573 errors (45.90%)**. At a 10.0% budget (7,500 flows), Confidence triage captures **2,879 errors (84.01%)** vs. **1,794 errors (52.35%)** (`results/final_shifted_strategy_comparison.csv`).
- **Interpretation:**  
  This is the **Honest Crossover Phenomenon**. While high-confidence errors dominate the extreme tail of failures, the vast majority of classification errors in any probabilistic model are still standard boundary misclassifications ($P \approx 0.50$). When review capacity expands to 5% or 10%, confidence triage can exhaustively audit the entire boundary region, catching 84% of all errors. In contrast, multi-factor scoring continues allocating slots to high-drift but correctly predicted outliers.
- **Unresolved Limitation:**  
  A fixed linear weighting scheme cannot dynamically transition between low-budget anomaly detection and high-budget boundary sweeping. A budget-dependent dynamic weighting function ($w(B)$) is required to prevent crossover degradation at higher budgets.
- **Exact Viva Script:**  
  > *"This reflects what we term the 'Honest Crossover Phenomenon.' Documenting this crossover is proof of our research integrity: we do not claim our method wins under all conditions. When review bandwidth is plentiful—such as 10%—the absolute majority of classifier errors reside in the boundary margin, allowing least-confidence triage to sweep 84% of all errors. However, in real-world SOC environments where human bandwidth is strictly constrained to 1% or 2%, our adaptive approach is vastly superior. For Phase-II, we are exploring budget-conditioned weights to bridge this gap."*

---

## Question 3: Why does global triage report 610 captures at 1% budget, while the sequential 5-batch simulation reports 183 captures?

- **Verified Fact:**  
  In global triage (`src/25`), 750 reviews across 75,000 flows catch **610 errors**. In sequential streaming (`src/28_seq`), 5 batches of 15,000 flows with 150 reviews each catch **183 errors** (`results/sequential_feedback.csv`).
- **Interpretation:**  
  Ground-truth errors in the shifted test set are heavily clustered temporally due to a concentrated attack surge in Batch 5:
  - Batches 1–4: Only 280, 296, 325, and 235 errors (error rate $\approx 1.8\%$).
  - **Batch 5: 2,291 errors (15.27% error rate — 66.8% of all test errors occur here!).**  
  In global triage, the algorithm pools all 75,000 flows retrospectively and naturally concentrates **719 of the 750 reviews into Batch 5**, capturing 604 errors in Batch 5 alone. In sequential streaming, the reviewer is bound to a rigid operational quota of exactly 150 reviews per batch. Even though 2,291 errors hit in Batch 5, the reviewer can only audit 150 flows, catching 40 errors from Batch 5 ($32 + 35 + 38 + 38 + 40 = 183$ errors).
- **Unresolved Limitation:**  
  The current sequential evaluation assumes fixed per-batch staffing quotas. It does not yet evaluate flexible dynamic capacity allocation (e.g., borrowing review hours when drift spikes).
- **Exact Viva Script:**  
  > *"These two numbers represent two distinct operational models. In the shifted test set, attacks are temporally clustered: over 66% of all errors hit during the attack wave in Batch 5. Global triage represents retrospective prioritization where review capacity naturally surges to follow threat density, placing 719 reviews into Batch 5 to capture 610 errors. Sequential streaming represents rigid shift scheduling where an analyst has a fixed quota of 150 reviews per batch and cannot borrow future hours. Even under this rigid constraint, our online adaptive feedback captures 183 errors, outperforming the static comparator's 168 errors."*

---

## Question 4: Why is margin uncertainty kept unscaled in $[0, 0.50]$ instead of normalized to $[0, 1.00]$?

- **Verified Fact:**  
  At a 1% review budget on the 75,000 Shifted Test flows (`tests/test_signals_and_scoring.py`):
  - **Unscaled $u \in [0, 0.50]$:** **610 errors caught (17.80%)**
  - **Linear $2u \in [0, 1.00]$:** **527 errors caught (15.38%)** (-13.6% degradation)
  - **Rank-Normalized $u \in [0, 1.00]$:** **280 errors caught (8.17%)** (-54.1% degradation)
- **Interpretation:**  
  In binary classification, predicted margin uncertainty $u = 1 - \max(P_0, P_1)$ is naturally bounded in $[0, 0.50]$. The other three signals ($z_{\text{ood}}$, $z_{\text{psi}}$, $z_{\text{hist}}$) are percentile ranks in $[0, 1.00]$. The effective weight of uncertainty is $w_u \times \text{scale} = 0.35 \times 0.50 = 0.175$. When uncertainty is rescaled to $[0, 1.00]$, its effective weight doubles, flooding the top 750 slots with low-risk boundary noise and crowding out severe distribution-drift attacks. Keeping $u$ unscaled preserves the optimal balance.
- **Unresolved Limitation:**  
  The upper bound of the composite score becomes $R_{\max} = 0.35(0.50) + 0.15(1.0) + 0.25(1.0) + 0.25(1.0) = 0.825$ rather than 1.00. While mathematically sound, examiners may ask why min-max scaling was not used; the empirical ablation provides the definitive answer.
- **Exact Viva Script:**  
  > *"We conducted a controlled normalization experiment specifically to answer this question. In binary classification, margin uncertainty naturally ranges from 0 to 0.50. When we rescaled uncertainty to 0-to-1 using linear doubling, error capture at 1% dropped from 610 to 527—a 13.6% loss. When we rank-normalized it, error capture collapsed to 280—a 54.1% loss! Rescaling uncertainty gives boundary noise disproportionate weight, flooding the triage queue with low-confidence false alarms and drowning out genuine zero-day attacks. Unscaled uncertainty is both mathematically grounded and empirically essential."*

---

## Question 5: Exactly how was data leakage prevented across the data partitions and scoring pipeline?

- **Verified Fact:**  
  The 500,000 BigFlow sample is strictly partitioned chronologically:
  - Train: 350,000 flows (ends at `2019-04-23 16:22:35.978`)
  - Validation: 75,000 flows (starts at `16:22:36.003`, ends at `17:01:20.431`) $\rightarrow$ **+25.0 ms forward gap**.
  - Shifted Test: 75,000 flows (starts at `17:01:20.470`, ends at `03:27:14.233`) $\rightarrow$ **+39.0 ms forward gap**.
  - Exactly 0 row-level duplicates exist across partitions (`test_splits_and_leakage.py`).
  - Imputation medians, standard scalers, Mahalanobis empirical covariance matrices, and XGBoost models are fitted exclusively on the Training set.
- **Interpretation:**  
  Standard random k-fold cross-validation in network traffic causes catastrophic temporal leakage because packets from the same TCP connection appear in both train and test splits. Strict millisecond chronological separation guarantees that no future network states bleed into past training.
- **Unresolved Limitation:**  
  While operational leakage (labels in features) was strictly prevented, method selection bias exists because the normalization ablation study was evaluated on the shifted test partition.
- **Exact Viva Script:**  
  > *"Leakage prevention was our highest architectural priority. We enforced strict forward chronological splitting with non-overlapping millisecond boundaries: a 25-millisecond gap between Train and Validation, and a 39-millisecond gap between Validation and Test, with zero duplicate flows. All preprocessing transforms—standardization scalers, imputation medians, Mahalanobis covariance matrices, and XGBoost trees—were fitted strictly on training data. Furthermore, in sequential feedback, test labels are revealed strictly post-selection for reviewed samples only."*

---

## Question 6: What does the 1,000-sample bootstrap confidence interval establish, and what are its statistical limitations?

- **Verified Fact:**  
  Over 1,000 paired instance bootstrap replicates on the shifted test set (`src/29_extended_evaluation.py`, `results/extended_bootstrap_cis.csv`), the mean capture rate advantage of Adaptive over Confidence triage was **+4.35 percentage points**, with an empirical 95% confidence interval of **[+3.45%, +5.28%]**. In 1,000 of 1,000 replicates, $\Delta_b > 0$ ($p < 0.001$ empirical).
- **Interpretation:**  
  The full-sample absolute advantage is $(610 - 463) / 3,427 = +4.29\%$ (+31.75% relative gain). The bootstrap resamples instances with replacement and recomputes the top-750 queue in each iteration. Because the 95% interval strictly excludes zero, it confirms that the adaptive advantage is statistically robust to sample variation.
- **Unresolved Limitation:**  
  An unweighted i.i.d. bootstrap assumes independent observations. Network flows exhibit temporal clustering, meaning i.i.d. resampling understates true variance compared to a block bootstrap. Additionally, $p < 0.001$ reflects empirical non-zero frequency in 1,000 replicates rather than a formal asymptotic hypothesis test.
- **Exact Viva Script:**  
  > *"To ensure our 1% budget advantage was not an artifact of random sampling, we conducted 1,000 paired bootstrap replicates where both queues were recomputed on resampled test data. The 95% confidence interval for the capture rate gain is [+3.45%, +5.28%], with a mean of +4.35%, strictly outperforming confidence triage across all 1,000 resamples. We acknowledge that standard bootstrap treats flows as independent, so we also validated our model under rigid 5-batch chronological streaming, where adaptive triage maintained an 8.9% lead over the static comparator."*

---

## Question 7: What does Functional Requirement 14 (FR14) still lack, and why is the project status 92.9% complete?

- **Verified Fact:**  
  The formal project specification (Table 9.1 of the Review-II Report) defines 14 functional requirements. Requirements FR1 through FR13 (data ingestion, temporal splits, leakage verification, XGBoost base classifier, ECE calibration, four signals, composite scoring, budget simulation, crossover analysis, and the sequential feedback loop) are **100% implemented**. FR14 covers the **Interactive Analytics Dashboard & Multi-Dataset Web Portal**.
- **Interpretation:**  
  In Phase-I, we fully implemented the local interactive Streamlit review dashboard (`dashboard/app.py`), which visualizes review allocations, distribution drift, and sequential feedback traces on the 500,000-flow BigFlow-NIDS benchmark. What is deferred to Phase-II is multi-dataset ingestion (supporting CIC-IDS-2018 and UNSW-NB15 with dynamic schema mapping) and cloud-native microservice deployment. Because FR14 is partially complete (~50%), 13 of 14 requirements are fully implemented ($13 / 14 = 92.86\% \approx 92.9\%$).
- **Unresolved Limitation:**  
  The dashboard currently runs locally on a single machine; enterprise multi-tenant authentication and live packet capture ingestion are deferred to Phase-II.
- **Exact Viva Script:**  
  > *"Our project status stands at 13 of 14 functional requirements fully implemented, with FR14 partially implemented (92.9% complete). FR1 through FR13 cover the entire machine learning, signal processing, and triage pipeline—all of which are fully operational. FR14 specified the interactive dashboard and multi-dataset enterprise portal. We have completed the full Streamlit review dashboard for Phase-I. In consultation with my guide, Prof. Dilip Kumar Maripuri, multi-dataset automated schema ingestion and cloud microservices deployment were scheduled for Phase-II."*

---

## Question 8: What are the primary academic and experimental limitations of your current evidence?

- **Verified Fact & Academic Honesty:**  
  A truly defensible master's capstone acknowledges its scope boundaries:
  1. **Offline Simulation vs. Live Production:** Evaluated on benchmark network traces with simulated label revelation; not deployed as an in-line physical firewall.
  2. **Algorithmic Review vs. Live Human Study:** Assumes human review is 100% accurate once assigned; does not model human reviewer fatigue or labeling errors.
  3. **Method Selection on Shifted Test Set:** The signal weights $(0.35, 0.15, 0.25, 0.25)$ and unscaled uncertainty decision were validated on the shifted test set.
  4. **Single-Domain Benchmark:** Validated on BigFlow-NIDS (NF-UQ-NIDS-v2); cross-domain validation on medical or financial fraud data remains future work.
  5. **Rigid Quota in Sequential Streaming:** Fixed quota of 150 reviews/batch prevents shifting capacity to surge periods.
- **Exact Viva Script:**  
  > *"To maintain complete scientific honesty, we identify four clear limitations in our Phase-I work: First, our evaluation is an offline benchmark on BigFlow-NIDS with simulated post-selection review rather than live human subjects. Second, we assume human review is error-free, whereas real analysts experience fatigue. Third, our static weights were validated on the test set, creating methodology exploration bias. And fourth, our sequential streaming imposes fixed per-batch staffing quotas. Addressing dynamic review capacity and multi-dataset generalization forms the core of our Phase-II roadmap."*
