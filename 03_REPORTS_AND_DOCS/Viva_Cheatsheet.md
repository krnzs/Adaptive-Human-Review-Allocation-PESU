# Capstone Viva Defense Cheatsheet

**Project:** Reliable Review Allocation Under Distribution Shift
**Degree / SRN:** MCA (Data Analytics) | PES1PG25CA101 | Guide: Prof. Dilip Kumar Maripuri
**Course Code:** PES2UG20CS418 | PES University, Bangalore  

---

## 1. The 150-Word Viva Narrative (Say This When Asked: "How Does the Literature Connect to Your Work?")

> *"Modern deep classifiers are severely miscalibrated and overconfident, as proven by Guo et al. Consequently, when Geifman's confidence-based selective prediction is deployed in non-stationary environments, it fails silently because models make confident mistakes under temporal shift. While Yang and Cao propose Out-of-Distribution detection to catch shifts, our experiments confirm that feature novelty alone does not correlate with classification errors in network security. Meanwhile, Lu and Iwashita demonstrate that tracking macroscopic feature drift and error feedback is necessary to detect emerging degradation. Hendrickx's premier survey proves that effective rejection must combine ambiguity and novelty, while Mozannar, Wei, and Liu formalize learning-to-defer to human experts. Finally, Kim and Mosqueira-Rey show that human attention in cybersecurity operations is strictly constrained by alert fatigue. Our project unifies these separate threads: we combine uncertainty, OOD distance, PSI drift, and historical mistake patterns into an adaptive triage mechanism that maximizes error interception under strict 1% to 2% operational human review budgets."*

---

## 2. 20-Second Spoken Summaries for All 16 Papers

1. **[1] Cao et al. (ICCV 2023):** *"Cao showed that when the environment shifts, anomaly detectors confuse normal environmental changes with true threats. This justifies why we evaluate our intrusion detection model on a later chronological time window rather than a clean random split."*
2. **[2] Mozannar & Sontag (ICML 2020):** *"Mozannar proved that human-AI collaboration requires an explicit deferral policy rather than just thresholding model scores. We build on this concept by routing difficult cases to human analysts under fixed operational review quotas."*
3. **[3] Wei et al. (ICML 2024):** *"Wei showed in ICML 2024 that blindly deferring difficult samples to humans is inefficient if humans also fail on them. This motivates our review efficiency metric, ensuring human audit time targets genuinely recoverable system errors."*
4. **[4] Geifman & El-Yaniv (NeurIPS 2017):** *"Geifman established selective prediction by rejecting instances below a confidence threshold. We use this exact strategy as our primary baseline, but show that under real distribution shift, it misses confident errors."*
5. **[5] Guo et al. (ICML 2017):** *"Guo showed in ICML 2017 that modern models are systematically overconfident. This explains why raw prediction probability alone is an unreliable indicator of safety and why multi-signal reliability scoring is necessary."*
6. **[6] Kim et al. (IEEE TIFS 2024):** *"Kim in IEEE TIFS 2024 proved that active alert prioritization cuts cyber intrusion detection time by 79%. This provides the operational justification for our project: in real SOC environments, human audit budget is severely limited."*
7. **[7] Liu et al. (Scientific Reports 2022):** *"Liu showed that adding uncertainty to deferral policies reduces human workload by 28% without losing accuracy. We adopt this insight by using uncertainty as a core reliability signal in our triage score."*
8. **[8] Yang et al. (IJCV 2024):** *"Yang in IJCV 2024 provided the definitive taxonomy of OOD detection, proving Mahalanobis distance is a top post-hoc detector. We implemented regularized Mahalanobis distance based on their recommendations."*
9. **[9] Koh et al. (ICML 2021):** *"Koh in ICML 2021 proved that models degrade severely under real-world distribution shift compared to artificial noise. This directly justifies our chronological train-val-test split on BigFlow-NIDS."*
10. **[10] He et al. (IEEE COMST 2023):** *"He in IEEE COMST 2023 showed that perturbations in network flow attributes cause intrusion detection models to fail silently. This motivates our feature drift monitoring on flow statistics."*
11. **[11] Lu et al. (IEEE TKDE 2019):** *"Lu in IEEE TKDE 2019 established that tracking feature shifts alongside error rates is essential for detecting drift. We implement this by combining feature PSI with historical mistake feedback."*
12. **[12] Iwashita & Papa (IEEE Access 2019):** *"Iwashita and Papa showed that active drift monitoring provides early warnings before accuracy collapses. This inspired our adaptive regime scoring, which shifts review weights when drift is detected."*
13. **[13] Mosqueira-Rey et al. (AI Review 2023):** *"Mosqueira-Rey in AI Review 2023 established that human-in-the-loop systems must optimize human attention at inference time. Our project implements exactly this by triage-filtering network flows within 1% to 10% review limits."*
14. **[14] Hendrickx et al. (Machine Learning 2024):** *"Hendrickx in 2024 proved that effective rejection requires combining ambiguity rejection (confidence) with novelty rejection (OOD). This is the exact theoretical justification for our multi-factor triage design."*
15. **[15] Sarhan et al. (MNA 2022):** *"Sarhan created the standardized NetFlow feature format for intrusion detection, solving dataset incompatibility. BigFlow-NIDS was built on this exact standard, which provides our 49 flow features."*
16. **[16] Uddin et al. (Data in Brief 2026):** *"Uddin published BigFlow-NIDS in February 2026 in Data in Brief, harmonizing 66.9 million network flows. We sampled 500,000 chronological flows from this verified benchmark for our experiments."*

---

## 3. Top 10 Viva Questions & Bulletproof Defense Answers

| # | Anticipated Panel Question | Bulletproof 1–2 Sentence Answer |
| :---: | :--- | :--- |
| **Q1** | *Why not just retrain the model when drift occurs?* | Retraining is an offline process requiring newly labeled ground truth that takes weeks to collect; our triage operates in real time at inference time to intercept dangerous errors today. |
| **Q2** | *Why does Confidence beat Adaptive at 5% and 10% budgets?* | This is an honest empirical finding: Adaptive triage is specialized for tight budgets (1%–2%) where it beats confidence by 4.3%–7.5%; at 5%–10%, the budget is large enough to cover the entire decision boundary where confidence excels. |
| **Q3** | *Why did OOD capture only 0.03% of errors (worse than random)?* | In network traffic, extreme Mahalanobis outliers are benign high-bandwidth file transfers that XGBoost classifies correctly (Decile 9 had only 0.16% error rate); feature novelty does not equal classification error. |
| **Q4** | *Why didn't you just use temperature scaling?* | Temperature scaling only rescales probabilities monotonically on in-distribution data without changing instance ranking; it cannot detect shifted high-confidence errors without external drift signals. |
| **Q5** | *Are your signal weights learned or heuristic?* | In Phase 1 they are experimentally defined heuristics; Phase 2 explicitly introduces bilevel optimization to learn optimal routing policies from asymmetric cost matrices. |
| **Q6** | *Why is validation Precision only 0.04?* | Validation attack prevalence is extremely low (0.33%, 248 attacks in 75K flows); ROC-AUC is 0.9228, proving strong ranking, and our triage engine exists specifically to intercept the false alarms. |
| **Q7** | *How did you prevent data leakage?* | Strict chronological split (350K train / 75K val / 75K test); all scalers, OOD covariance matrices, and mistake bins were fitted exclusively on training data. |
| **Q8** | *How does this differ from Mozannar's Learning to Defer?* | Mozannar modifies the training loss under fixed deferral cost for stationary data; we provide a post-hoc triage layer operating over an existing model under temporal shift with explicit capacity budgets (1%–10%). |
| **Q9** | *Is this tested on live campus traffic?* | No, it uses the peer-reviewed 2026 BigFlow-NIDS benchmark so that all 3,427 shifted errors and 753 validation errors are 100% reproducible and verifiable. |
| **Q10**| *What is your concrete Phase-2 plan?* | Conformal prediction coverage guarantees, SHAP explainability on routed alerts, cross-domain evaluation on medical/financial tabular data, and an interactive Streamlit UI. |

---

## 4. Key Experimental Numbers (Memorize These Exact Values)

- **Dataset Total:** 66,935,021 flows, 55 attributes, 32 attack families (BigFlow-NIDS 2026).
- **Laptop Sample:** 500,000 flows, 49 numerical flow features, 100% SHA-256 verified.
- **Train Split (70%):** 350,000 flows | 21,344 attacks (6.10% prevalence).
- **Validation Split (15%):** 75,000 flows | 248 attacks (0.33% prevalence) | **Exactly 753 errors (1.004% error rate)** | Avg confidence: 0.9865 | XGBoost Val ROC-AUC: **0.9228**.
- **Shifted Test Split (15%):** 75,000 flows | 4,724 attacks (6.30% prevalence) | **Exactly 3,427 errors (4.569% error rate)** | Avg confidence: 0.9682.
- **Error Surge:** $3,427 / 753 = \mathbf{4.551\times}$ surge in errors, while confidence dropped only by 1.83%.
- **Strategy Results on Shifted Test:**
  - **1% Budget (750 reviews):** Feedback Adaptive **17.80% (610 errors, 813.3/k)** vs Confidence 13.51% (463 errors) vs Random 1.17% (40 errors). *(Multi-Factor Wins)*
  - **2% Budget (1,500 reviews):** Feedback Adaptive **34.26% (1,174 errors, 782.7/k)** vs Confidence 26.73% (916 errors) vs Random 2.13% (73 errors). *(Multi-Factor Wins)*
  - **5% Budget (3,750 reviews):** Pure Confidence **65.45% (2,243 errors)** vs Feedback Adaptive 45.90% (1,573 errors). *(Confidence Overtakes)*
  - **10% Budget (7,500 reviews):** Pure Confidence **84.01% (2,879 errors)** vs Feedback Adaptive 52.35% (1,794 errors). *(Confidence Overtakes)*
  - **OOD-Only Filter:** 0.03% (1 error) at 1% budget; 0.26% (9 errors) at 2% budget; 0.35% (12 errors) at 5% & 10% budgets. *(Honest Negative Result)*
- **Implementation Status:** **13 of 14 modules implemented (92.9% complete)** across 26 sequential Python scripts. Only FR14 (Interactive Web UI) is Phase-2.

---

## 5. Corrections Made to Earlier Citations & Inaccurate Claims

1. **Guo et al. (ICML 2017) Claim Corrected:**  
   *Old incorrect claim:* "Guo et al. demonstrates model overconfidence under distribution shift."  
   *Corrected fact:* Guo et al. studied *stationary, unshifted deep neural networks* and showed that modern architectural techniques (depth, Batch Normalization, low weight decay) cause overconfidence miscalibration on standard i.i.d. test sets. Shift failure was demonstrated by subsequent works (Ovadia et al., NeurIPS 2019).
2. **PSI Citation Decoupled from WILDS:**  
   *Old incorrect citation:* PSI cited to Koh et al. (WILDS 2021).  
   *Corrected fact:* WILDS evaluates in-the-wild domain shifts using worst-group accuracy across vision, text, and satellite data; it does not introduce Population Stability Index (PSI). PSI is a classic credit risk distribution metric, while distribution drift reviews are properly credited to Lu et al. (IEEE TKDE 2019) and Iwashita & Papa (IEEE Access 2019).
3. **Human-in-the-Loop IDS Decoupled from Adversarial Survey:**  
   *Old incorrect citation:* Human-in-the-loop intrusion detection cited to He et al. (2023).  
   *Corrected fact:* He et al. is an *adversarial machine learning* survey focusing on evasion and poisoning attacks. Human-in-the-loop intrusion detection active learning is specifically credited to Kim, Dán, & Zhu (IEEE TIFS 2024).
4. **Scopus / IEEE Indexing Verified:**  
   Confirmed that 12 of the 16 sources are fully indexed in Scopus and/or IEEE Xplore (exceeding PES University's 10-paper requirement), and all 4 PMLR conference papers (Mozannar, Wei, Guo, Koh) have verified IEEE/Scopus peer-reviewed equivalents documented.
