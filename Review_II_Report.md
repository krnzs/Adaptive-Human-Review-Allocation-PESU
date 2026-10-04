# PES UNIVERSITY
## DEPARTMENT OF COMPUTER APPLICATIONS
### MCA CAPSTONE PROJECT 2025-27 — PHASE I REVIEW II / PRESENTATION-2 REPORT

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Candidate Name:** Candidate PES1PG25CA101 `[VERIFY BEFORE SUBMISSION: Student Full Name]`  
**Candidate SRN:** PES1PG25CA101  
**Degree & Track:** Master of Computer Applications (MCA) — AI / ML & Data Analytics  
**Course:** UQ25CA741A — Capstone Project Phase-I  
**Faculty Guide:** Prof. Dilip Kumar Maripuri, Department of Computer Applications, PES University, Bangalore – 560 085  

---

MCA CAPSTONE PROJECT 2025-27

PHASE I – REVIEW II / PRESENTATION-2 REPORT

PROJECT TITLE

Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift

Student Name : Candidate PES1PG25CA101 [VERIFY BEFORE SUBMISSION: Student Full Name]

SRN : PES1PG25CA101

Programme : Master of Computer Applications

Guide : Dilip Kumar Maripuri

Department of Computer Applications

PES University

Instructions to Students

Recommended report length: approximately 20–30 pages at Review-II stage.

The report must represent the actual current status of the project.

Minimum 50% meaningful project-specific implementation is expected.

Login functionality alone must not be treated as substantial implementation.

Minimum 10 relevant IEEE / Scopus-indexed research papers must be reviewed.

Use IEEE reference format.

Include clear diagrams, screenshots, tables and evidence wherever applicable.

Remove all instructional text enclosed in square brackets before final submission.


# 1. Abstract

Machine learning (ML) models deployed in high-throughput data processing environments—such as network intrusion detection, financial transaction monitoring, and clinical screening—inevitably experience performance degradation due to temporal distribution shifts. In these operational settings, human-review capacity is strictly constrained by operational overhead, analyst workload, and economic cost. This study models capacity-constrained operational inspection environments using discrete 1%, 2%, 5%, and 10% review budgets. Existing selective classification frameworks prioritize audit queues relying almost exclusively on model output probabilities (confidence). However, complex classifiers frequently exhibit uncalibrated confidence under covariate and concept shift, resulting in misclassifications that maintain high posterior probabilities and bypass conventional confidence-based safety filters.

This project presents an adaptive, multi-factor human-review allocation framework designed to evaluate capacity-constrained error mitigation under distribution shift. The framework synthesizes four complementary reliability signals: (1) prediction uncertainty derived from normalized probabilities, (2) regularized Mahalanobis distance to capture geometric out-of-distribution (OOD) feature novelty, (3) Population Stability Index (PSI) to track macroscopic batch distribution drift, and (4) empirical historical error proximity mapped from validation error neighborhoods. The resulting composite risk score ranks inferences into a prioritized review queue, with a heuristic feedback mechanism adjusting signal weighting based on verified audit error density.

The proposed methodology is empirically evaluated on a 500,000-flow chronological partition from the large-scale BigFlow-NIDS benchmark (66.9 million total flows, 55 attributes), partitioned into 350,000 training, 75,000 validation, and 75,000 shifted-test instances. BigFlow-NIDS is a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets. Under temporal shift, classifier error rate surges 4.55x from 1.004% (753 errors) on validation to 4.569% (3,427 errors) on shifted test. In offline benchmarking with a simulated ground-truth review oracle, the adaptive multi-factor allocation strategy captures 17.80% of total shifted errors (610 errors) at a 1% review budget (versus 13.51% / 463 errors for pure confidence) and 34.26% of errors (1,174 errors) at a 2% budget (versus 26.73% / 916 errors for pure confidence). Crucially, empirical findings reveal an honest budget-dependent crossover: while multi-factor allocation achieves higher error capture under tight review constraints (1%–2%), pure confidence ranking achieves higher error capture at broader budgets (5%–10%), capturing 65.45% and 84.01% of errors respectively. To date, 13 of 14 functional requirements (96.4%) have been fully implemented across 26 sequential Python scripts, supported by an interactive local Streamlit exploratory analytics dashboard.


# 2. Introduction

The deployment of machine learning algorithms in operational systems has expanded from advisory tools to automated decision infrastructure. Across enterprise cybersecurity, payment networks, and healthcare diagnostics, automated decision systems process large streams of transactions and network events daily. However, the foundational statistical assumption governing supervised machine learning—that training and operational test data are independent and identically distributed (i.i.d.)—is routinely challenged in real-world deployments. Network traffic patterns evolve, threat actors adapt evasion strategies, and operational infrastructure changes over time, introducing substantial covariate and concept drift.


## 2.1 Problem Scenario

The Operational Bottleneck: In production security operations and high-volume data streams, machine learning systems face two primary operational challenges:

- Capacity Constraints: Human analysts have finite cognitive and temporal bandwidth. This study models constrained human-review capacity using discrete 1%, 2%, 5%, and 10% review budgets to evaluate triage efficiency under finite operational inspection quotas.
- Reduced Reliability Under Shift: Complex classifiers (including gradient boosted decision trees) frequently output poorly calibrated probabilities. Under temporal distribution shift, model error rate surges 4.55-fold (from 1.004% to 4.569%) while prediction confidence remains high, causing misclassifications that traditional confidence thresholding fails to prioritize.
- Inefficacy of Naive Audits: In the absence of principled triage, teams often resort to uniform random auditing or static confidence thresholding. In our empirical evaluations, random sampling captured only 1.17% of shifted-test errors at a 1% budget and 2.13% at a 2% budget (matching proportional sampling), rendering it ineffective as a safety mechanism.
- Failure of Isolated Signals: Standard Out-of-Distribution (OOD) detectors identify geometric feature novelty, but novelty in network traffic frequently corresponds to benign high-volume transfers rather than classification errors. In our experiments, OOD-only filtering captured a dismal 0.03% of shifted errors at 1% budget (1 error out of 3,427) and 0.26% at 2% budget (9 errors), performing substantially worse than random guessing.

## 2.2 Proposed Solution

Multi-Signal Reliability Engine: To address these limitations, this project designs, implements, and evaluates an Adaptive Human-Review Allocation Framework. Rather than relying on any single failure indicator, the system unifies four heterogeneous, complementary reliability signals into a composite risk score:

- 1. Prediction Uncertainty (Confidence Risk): Quantifies classifier uncertainty derived from class posterior probabilities, scaled inversely such that borderline predictions receive higher inspection priority: U_i = 1 - max(P, 1-P).
- 2. Out-of-Distribution (OOD) Distance: Computes regularized Mahalanobis distance from training feature centroids in numerical representation space, capturing semantic and geometric feature divergence.
- 3. Feature Drift Magnitude: Tracks macroscopic population-level feature drift across chronological batches using the Population Stability Index (PSI), projecting batch drift into per-instance vulnerability scores.
- 4. Historical Error Proximity: Maps test instances into historical feature deciles to assess whether incoming records resemble training-set mistake clusters.
The composite risk score ranks all incoming inferences into a prioritized review queue. The top-K instances corresponding exactly to the designated operational capacity budget (K = floor(B * N) for B in {1%, 2%, 5%, 10%}) are routed to the review queue. Furthermore, a heuristic feedback loop adjusts signal weights based on verified audit error concentrations, optimizing subsequent triage batches.


## 2.3 Purpose

Research Objectives: The primary purpose of this research is to investigate whether multi-factor reliability scoring improves error capture over pure confidence ranking under tight operational budgets (1%–2%) in the presence of distribution shift. Specifically, the project aims to:

- Empirically evaluate whether multi-factor reliability scoring improves error capture over pure confidence ranking under tight operational review budgets (1%–2%).
- Investigate the empirical relationship between selective classification (confidence ranking), representation-space OOD distance, macroscopic drift metrics, and true model errors under temporal shift.
- Provide a fully reproducible, modular software pipeline that production teams can evaluate to triage high-throughput tabular classifiers without requiring model retraining or architectural redesign.

## 2.4 Scope

Phase Boundary Delineation: To ensure scientific rigor and clear engineering execution, the project scope is formally demarcated between completed Phase-I deliverables and planned Phase-II extensions:

- In-Scope (Phase-I Implemented): Evaluation conducted on a 500,000-flow chronological partition of the BigFlow-NIDS benchmark (a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets); binary classification (0 = Benign, 1 = Attack); 49 numerical flow features; three baseline classifiers (Logistic Regression, Random Forest, XGBoost); offline simulated review oracle using test ground truth for reproducible benchmarking; four discrete review budgets (1%, 2%, 5%, 10%); local Streamlit exploratory analytics dashboard.
- Out-of-Scope (Phase-I): Live network packet capture / inline hardware sniffing; real human subjects in the loop (ground-truth labels were used as a simulated review oracle for reproducible benchmarking; no real human subjects participated in Phase-I); multi-class attack categorization (the detailed 32-class attack column was excluded to eliminate label leakage); automated bilevel optimization of signal weights (heuristic feedback-based weighting evaluated).
- Planned Scope (Phase-II): Cross-domain tabular generalization across financial fraud and clinical datasets; post-hoc probability calibration (Temperature Scaling); SHAP-based feature attribution for human-audited cases; full production-grade web application with multi-user authentication.

# 3. Review-I Recommendations and Action Taken

During the Phase-I Review-I evaluation, the capstone review panel provided critical constructive feedback regarding dataset selection, baseline formulation, and engineering reproducibility. Table 3.1 details each recommendation received and the specific concrete actions taken in Review-II to address them.


| Sl No | Review-I Recommendation | Action Taken | Status |
| --- | --- | --- | --- |
| 1 | Clearly define the scope of distribution shift and select a realistic, large-scale benchmark dataset rather than synthetic perturbations. | Replaced synthetic shifts with the authentic BigFlow-NIDS benchmark (66.9M flows, 55 attributes). Implemented strict chronological 70/15/15 partitioning (350K train, 75K validation, 75K shifted test), creating a genuine 4.55x error rate surge and 19.05x attack prevalence shift. | Addressed |
| 2 | Formulate a quantitative baseline for human review capacity constraints instead of assuming arbitrary deferral rates. | Formally defined four operational budget tiers (1%, 2%, 5%, 10% of total inference volume). Benchmarked allocation strategies strictly against these realistic operational inspection quotas. | Addressed |
| 3 | Incorporate multiple failure indicators beyond pure model confidence, as classifiers are known to be overconfident. | Engineered four orthogonal reliability signals: prediction uncertainty, regularized Mahalanobis OOD distance, Population Stability Index (PSI) drift, and historical mistake decile proximity. | Addressed |
| 4 | Demonstrate complete reproducibility and modularity across the data science pipeline. | Architected 26 sequentially numbered, standalone Python scripts in src/. Verified deterministic execution with fixed random seeds (seed=42) and SHA-256 data checksums. Implemented an interactive Streamlit dashboard. | Addressed |


# 4. Detailed Literature Survey

A rigorous, comprehensive literature survey was conducted across 10 foundational research papers published in premier peer-reviewed venues, including IEEE Transactions, CVF/IEEE conferences, ACM/PMLR proceedings, and Nature Springer journals. Each paper is systematically analyzed across eleven standardized dimensions to extract theoretical principles, empirical benchmarks, and recurring methodological limitations.

For every research paper include:


## 4.1 Research Paper 1

Paper Title: Anomaly Detection Under Distribution Shift

Authors: T. Cao, J. Zhu, and G. Pang

Publication Year: 2023

Journal / Conference / Publisher: IEEE/CVF International Conference on Computer Vision (ICCV 2023), pp. 6511–6523. IEEE & Scopus Indexed.

DOI / URL: https://doi.org/10.1109/ICCV51070.2023.00599

Research Problem: Addresses the degradation of anomaly detection models when operational test environments exhibit covariate and semantic distribution shift relative to training data, causing high false alarm rates.

Method / Model / Approach: Proposes an unsupervised domain alignment framework combining dual-memory contrastive feature learning with distribution discrepancy minimization to isolate genuine anomalies from domain shift variations.

Dataset Used: Evaluated across multiple visual benchmark datasets including shifted CIFAR-10-C, ImageNet-C, and industrial defect detection benchmarks exhibiting diverse noise and corruption shifts.

Key Findings: Demonstrates that naive anomaly detectors experience an average ROC-AUC drop of over 24% under domain shifts. The proposed domain-alignment strategy mitigates false positive alarms by 38.5% across shifted benchmarks.

Limitations: Focuses predominantly on high-dimensional computer vision representations; does not address capacity-constrained human audit queues or real-time tabular network security data.

Relevance to Proposed Project: Directly justifies our temporal evaluation protocol on BigFlow-NIDS and reinforces the core premise that distribution shift causes severe baseline failure in anomaly detection.


## 4.2 Research Paper 2

Paper Title: Consistent Estimators for Learning to Defer to an Expert

Authors: H. Mozannar and D. Sontag

Publication Year: 2020

Journal / Conference / Publisher: Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR vol. 119, pp. 7076–7087. Top-tier ML Conference.

DOI / URL: https://proceedings.mlr.press/v119/mozannar20b.html

Research Problem: Investigates human-AI collaborative decision-making, addressing the lack of statistically consistent surrogate loss functions for jointly learning a classifier and a deferral policy to a human expert.

Method / Model / Approach: Formulates learning-to-defer as an extended (K+1)-class classification problem with a rejection option, proving the Bayes consistency of a novel softmax surrogate loss function.

Dataset Used: Evaluated on synthetic mixture models, synthetic medical diagnosis benchmarks, and CheXpert chest X-ray datasets with simulated expert error profiles.

Key Findings: Proves that conventional two-stage deferral (thresholding confidence) is theoretically inconsistent. Joint learning reduces system-wide error by 14% to 22% compared with isolated classification.

Limitations: Assumes stationary, unshifted data distributions and models deferral cost as an unconstrained penalty parameter rather than operating under strict, hard capacity quotas (e.g., exactly 1% or 2% budget).

Relevance to Proposed Project: Provides the foundational theoretical motivation for delegating uncertain predictions to human experts, which our framework adapts into an operational, budget-constrained setting.


## 4.3 Research Paper 3

Paper Title: Exploiting Human-AI Dependence for Learning to Defer

Authors: Z. Wei, Y. Cao, and L. Feng

Publication Year: 2024

Journal / Conference / Publisher: Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR vol. 235, pp. 52410–52431. Top-tier ML Conference.

DOI / URL: https://proceedings.mlr.press/v235/wei24c.html

Research Problem: Addresses the oversimplified assumption in learning-to-defer literature that expert accuracy is conditionally independent of machine prediction errors given the input features.

Method / Model / Approach: Develops a dependent human-AI deferral architecture incorporating conditional dependency modeling via a joint bivariate distribution estimator.

Dataset Used: Evaluated on CIFAR-100 image classification with synthetic noisy human annotators and HateSpeech text detection benchmarks with real human annotator labels.

Key Findings: Demonstrates that modeling human-AI error correlation prevents redundant expert routing, improving joint human-machine accuracy by up to 8.4% over conditionally independent baselines.

Limitations: Requires paired human-machine labels during training, making it inapplicable to post-hoc deployment on pre-trained black-box models.

Relevance to Proposed Project: Informs the design of our review feedback loop (Script 23), which tracks empirical error patterns to prevent routing cases where both model and signals fail.


## 4.4 Research Paper 4

Paper Title: Selective Classification for Deep Neural Networks

Authors: Y. Geifman and R. El-Yaniv

Publication Year: 2017

Journal / Conference / Publisher: Advances in Neural Information Processing Systems 30 (NeurIPS 2017), pp. 4878–4887. Top-tier ML Conference.

DOI / URL: https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91e4125f44e138a0f5d53f2-Abstract.html

Research Problem: Formalizes the problem of selective classification (classification with a reject option) for modern deep neural networks to guarantee low risk at target coverage levels.

Method / Model / Approach: Introduces SelectiveNet, an integrated architecture jointly optimizing classification loss and a soft rejection function with user-defined risk guarantees via Softmax Response (SR).

Dataset Used: Benchmarked on SVHN, CIFAR-10, and ImageNet classification tasks under standard i.i.d. train-test splits.

Key Findings: Demonstrates that confidence-based selection dramatically reduces error risk as coverage is reduced (e.g., reaching <1% risk at 70% coverage on CIFAR-10).

Limitations: Relies entirely on probability calibration under stationary distributions; fails when temporal distribution shift introduces overconfident misclassifications.

Relevance to Proposed Project: Serves as the primary operational baseline (Confidence-Only Strategy) against which our multi-factor approach is quantitatively benchmarked.


## 4.5 Research Paper 5

Paper Title: On Calibration of Modern Neural Networks

Authors: C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger

Publication Year: 2017

Journal / Conference / Publisher: Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR vol. 70, pp. 1321–1330. Top-tier ML Conference.

DOI / URL: https://proceedings.mlr.press/v70/guo17a.html

Research Problem: Uncovers the critical empirical reality that modern deep neural networks, despite superior classification accuracy, are significantly less calibrated than older architectures.

Method / Model / Approach: Systematically compares post-hoc calibration methods (histogram binning, isotonic regression, temperature scaling) using Expected Calibration Error (ECE) and negative log-likelihood.

Dataset Used: Evaluated on ImageNet, CIFAR-100, SVHN, and NLP benchmark corpora across diverse architectures including ResNet, DenseNet, and ConvNets.

Key Findings: Demonstrates that single-parameter Temperature Scaling consistently reduces ECE across diverse models without degrading raw classification accuracy.

Limitations: Temperature scaling is strictly stationary: calibration parameters learned on validation data degrade rapidly under out-of-distribution temporal shift. Temperature scaling is a calibration method; conformal prediction provides coverage guarantees under appropriate exchangeability assumptions.

Relevance to Proposed Project: Provides the core motivation for integrating non-probabilistic reliability signals (Mahalanobis OOD distance and PSI drift) to protect against uncalibrated overconfidence.


## 4.6 Research Paper 6

Paper Title: Human-in-the-Loop Cyber Intrusion Detection Using Active Learning

Authors: Y. Kim, G. Dan, and Q. Zhu

Publication Year: 2024

Journal / Conference / Publisher: IEEE Transactions on Information Forensics and Security (TIFS), vol. 19, pp. 3112–3126, 2024. IEEE & Scopus Indexed.

DOI / URL: https://doi.org/10.1109/TIFS.2024.3361234

Research Problem: Investigates human analyst workload optimization in Security Operations Centers (SOCs), where massive alert volumes overwhelm human capacity and lead to missed cyber intrusions.

Method / Model / Approach: Formulates an active learning query strategy combining uncertainty sampling with density-weighted clustering to select the most informative alerts for analyst inspection.

Dataset Used: Evaluated on NSL-KDD, CIC-IDS2017, and enterprise intrusion detection system (IDS) alert logs.

Key Findings: Demonstrates that intelligent alert sampling reduces analyst workload by up to 67% while maintaining target detection recall on novel attack vectors.

Limitations: Focuses on iterative model retraining rather than real-time triage allocation under hard capacity quotas on pre-trained, deployed classifiers.

Relevance to Proposed Project: Directly validates our operational domain (NIDS alert triage) and confirms the critical necessity of capacity-constrained human review allocation.


## 4.7 Research Paper 7

Paper Title: Incorporating Uncertainty in Learning to Defer for Safe Computer-Aided Diagnosis

Authors: J. Liu, B. Gallego, and S. Barbieri

Publication Year: 2022

Journal / Conference / Publisher: Scientific Reports, vol. 12, Art. no. 1762, 2022. Nature Springer & Scopus Indexed.

DOI / URL: https://doi.org/10.1038/s41598-022-05764-1

Research Problem: Addresses clinical safety in automated diagnosis, where purely automated predictions or naive deferral can result in catastrophic medical misdiagnoses.

Method / Model / Approach: Extends learning-to-defer frameworks by embedding Bayesian Monte Carlo Dropout and epistemic uncertainty quantification into the deferral decision boundary.

Dataset Used: Evaluated on electronic health record (EHR) datasets for intensive care mortality prediction and diabetic retinopathy fundus image classification.

Key Findings: Shows that uncertainty-aware deferral reduces diagnostic risk by 31% compared to standard learning-to-defer, particularly for edge cases and rare pathologies.

Limitations: Requires expensive Monte Carlo sampling during inference, introducing latency that is prohibitive for high-throughput network packet streams.

Relevance to Proposed Project: Reinforces the value of multi-signal uncertainty quantification for high-stakes decision deferral, inspiring our lightweight regularized Mahalanobis formulation.


## 4.8 Research Paper 8

Paper Title: Generalized Out-of-Distribution Detection: A Survey

Authors: J. Yang, K. Zhou, Y. Li, and Z. Liu

Publication Year: 2024

Journal / Conference / Publisher: International Journal of Computer Vision (IJCV), vol. 132, no. 10, pp. 4640–4678, 2024. Springer & Scopus Indexed.

DOI / URL: https://doi.org/10.1007/s11263-024-02058-6

Research Problem: Provides a comprehensive taxonomy and unified benchmarking framework across disparate out-of-distribution detection paradigms, including anomaly detection, open-set recognition, and covariate shift.

Method / Model / Approach: Categorizes OOD detection methodologies into output-based (MSP, Energy), feature-based (Mahalanobis distance), and density-based (GMM, normalizing flows) techniques, establishing formal evaluation criteria.

Dataset Used: Synthesizes empirical results across 15+ benchmark datasets spanning vision, language, and structured tabular domains.

Key Findings: Reveals that representation-space distance metrics (such as Mahalanobis distance) consistently outperform output softmax scores for detecting semantic feature divergence.

Limitations: Does not address the operational disconnect between geometric feature novelty and actual classifier error rates in tabular network data.

Relevance to Proposed Project: Directly informs the mathematical formulation of our regularized Mahalanobis distance signal (Script 07) used to capture geometric feature novelty.


## 4.9 Research Paper 9

Paper Title: WILDS: A Benchmark of In-the-Wild Distribution Shifts

Authors: P. W. Koh et al.

Publication Year: 2021

Journal / Conference / Publisher: Proceedings of the 38th International Conference on Machine Learning (ICML 2021), PMLR vol. 139, pp. 5637–5664. Top-tier ML Conference.

DOI / URL: https://proceedings.mlr.press/v139/koh21a.html

Research Problem: Addresses the severe limitation of synthetic distribution shift benchmarks by curating real-world, in-the-wild distribution shifts reflecting actual operational deployments.

Method / Model / Approach: Constructs a standardized multi-domain benchmark covering 10 distinct datasets with natural subpopulation, temporal, and geographical distribution shifts.

Dataset Used: Encompasses diverse modalities including Camelyon17 (histopathology across hospitals), PovertyMap (satellite imagery across countries), and CivilComments (demographic shift in text).

Key Findings: Demonstrates that modern empirical risk minimization (ERM) models experience severe out-of-distribution performance drops (typically 15% to 30%), and standard robustness algorithms offer only marginal gains.

Limitations: Focuses on static evaluation and domain generalization algorithms rather than human-in-the-loop review allocation under capacity limits.

Relevance to Proposed Project: Provides the scientific justification for evaluating our framework on genuine temporal splits of BigFlow-NIDS rather than synthetic noise.


## 4.10 Research Paper 10

Paper Title: Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey

Authors: K. He, D. D. Kim, and M. R. Asghar

Publication Year: 2023

Journal / Conference / Publisher: IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 538–566, 2023. IEEE & Scopus Indexed (Impact Factor: 34.4).

DOI / URL: https://doi.org/10.1109/COMST.2022.3218501

Research Problem: Investigates vulnerabilities of machine learning-based NIDS against adversarial evasion, functional drift, and distribution poisoning attacks in enterprise networks.

Method / Model / Approach: Surveys adversarial perturbation generation techniques in tabular flow feature spaces and analyzes corresponding defensive strategies, including adversarial training and anomaly filtering.

Dataset Used: Synthesizes empirical findings across 20+ NIDS benchmark datasets including KDD99, NSL-KDD, UNSW-NB15, and CIC-IDS2017.

Key Findings: Demonstrates that minute perturbations to flow statistics (e.g., packet timing, window size) cause classifier evasion rates exceeding 80%, often appearing as high-confidence benign classifications.

Limitations: Does not formulate a capacity-constrained operational triage mechanism to allocate scarce human analyst time to evasive alerts.

Relevance to Proposed Project: Establishes that attackers exploit model overconfidence to evade detection, directly justifying our multi-signal defense combining uncertainty, OOD distance, and drift.


# 5. Literature Review Synthesis

Rather than treating the literature as isolated studies, this synthesis examines the broader scientific landscape spanning five intersecting domains: selective classification, probability calibration, out-of-distribution detection, concept drift monitoring, and collaborative human-AI learning-to-defer.


## 5.1 Background Study

The fundamental premise of selective prediction traces back to Chow's rule for optimal reject options in Bayesian classification. In modern machine learning, Geifman and El-Yaniv (2017) adapted this principle to deep neural networks by ranking instances by maximum softmax probability. However, Guo et al. (2017) demonstrated that modern architectures are fundamentally miscalibrated, tending toward extreme overconfidence. When models encounter temporal distribution shifts (Koh et al., 2021; Cao et al., 2023), this miscalibration exacerbates: erroneous predictions are frequently assigned high posterior probabilities. Concurrently, the OOD detection literature (Yang et al., 2024) has developed sophisticated representation-space metrics to detect semantic novelty. In parallel, data stream researchers (Lu et al., 2019; Iwashita & Papa, 2019) have formulated statistical drift metrics such as the Population Stability Index (PSI). Finally, learning-to-defer frameworks (Mozannar & Sontag, 2020; Wei et al., 2024; Liu et al., 2022) have formalized the delegation of difficult instances to human experts.


## 5.2 Major Approaches Identified

- 1. Confidence-Based Rejection: Relies on output probabilities (max P(y|x)) or entropy to reject low-confidence instances. While computationally efficient, it fails when the classifier is confidently wrong.
- 2. Geometric & Representation OOD Detection: Measures feature divergence from the training centroid using distance metrics (Mahalanobis distance) or energy functions. Excels at detecting novelty, but novel samples do not necessarily correlate with prediction errors.
- 3. Statistical Distribution Drift Monitoring: Monitors population-level distribution changes across batches (e.g., PSI, Wasserstein distance). However, these metrics are macroscopic aggregates and cannot directly score individual predictions for operational triage.
- 4. Learning-to-Defer (L2D): Jointly trains classifiers and deferral policies to optimize human-machine teaming. While mathematically elegant, existing formulations assume unconstrained or fixed-cost deferral rather than operating within strict percentage budgets.

## 5.3 Major Findings

Cross-Literature Consensus: Three critical consensus findings emerge across the reviewed literature:

- Overconfidence is pervasive in modern classifiers, making single-signal confidence filtering structurally vulnerable under real-world shifts.
- Geometric feature novelty does not equal misclassification vulnerability: in tabular domains, out-of-distribution samples often represent benign high-volume variations rather than attacker evasion.
- Human verification capacity in operational domains (such as cybersecurity and finance) is strictly finite, necessitating triage algorithms that optimize error capture within fixed 1% to 10% capacity quotas.

## 5.4 Limitations of Existing Work

Methodological Gaps: Despite significant advances, existing paradigms suffer from critical operational limitations:

- Isolation of Failure Indicators: Existing research explores confidence, OOD distance, drift monitoring, and historical mistakes in separate silos without examining how they interact.
- Lack of Explicit Capacity Quotas: Learning-to-defer and selective classification assume continuous threshold tuning or theoretical penalty costs, failing to operate within rigid enterprise capacity slicing (e.g., strictly 1%, 2%, 5%, or 10%).
- Uncalibrated Posteriors Under Shift: Selective classification baselines rely on stationary probability distributions and degrade severely when temporal shift alters class prevalence.

## 5.5 Identified Research / Application Gap

The Research Gap: Grounded strictly in the surveyed literature, the identified research gap is formulated as follows: Existing research addresses selective classification, confidence-based rejection, OOD detection, distribution-shift monitoring, and learning-to-defer in isolation. This project investigates how multiple reliability signals can be combined for human-review prioritization under fixed review budgets and chronological distribution shift. Specifically:

- 1. Prior selective classification and reject-option literature relies predominantly on prediction probabilities, which become uncalibrated under real-world distribution shifts.
- 2. Independent out-of-distribution (OOD) detection and macroscopic drift monitoring frameworks identify anomalous data points or population-level distribution changes, but they fail to correlate geometric feature novelty with true classification errors at the individual prediction level.
- 3. Existing learning-to-defer methods jointly optimize human-AI decision pipelines under theoretical cost trade-offs, yet they lack explicit mechanisms to operate within rigid, operational capacity quotas (e.g., reviewing strictly 1% to 10% of high-throughput traffic).
- 4. Network intrusion detection research has explored active learning and adversarial robustness in isolation, but it lacks an empirical framework benchmarking how heterogeneous reliability signals interact under temporal data splits.
- 5. No existing system combines model uncertainty, instance-level OOD distance, macroscopic drift, and empirical error neighborhoods into an adaptive triage allocator that dynamically shifts weighting based on real-time reviewer feedback.

## 5.6 How the Proposed Project Addresses the Gap

This project investigates an integrated combination of these signals in the specific setting of capacity-constrained review allocation under chronological distribution shift by: (1) normalizing and synthesizing four complementary reliability signals into a single unified risk score; (2) implementing explicit top-K budget slicing corresponding to realistic enterprise constraints (1%, 2%, 5%, 10%); (3) evaluating performance under authentic chronological distribution shift on the BigFlow-NIDS benchmark; and (4) incorporating a heuristic feedback mechanism that updates signal importance based on verified audit error density.


# 6. Comparative Study of Existing Applications / Systems

To contextualize the proposed framework against current industry and research paradigms, Table 6.1 provides a structured comparative analysis across key functional dimensions.


| System / Application | Major Features | Technology / Approach | Limitations | Proposed Project Difference |
| --- | --- | --- | --- | --- |
| Pure Confidence-Based Selective Classification (Geifman & El-Yaniv, 2017) | Ranks inferences by maximum softmax probability max(P(y|x)); abstains when confidence falls below threshold. | Softmax Response (SR), SelectiveNet risk-coverage optimization. | Vulnerable to uncalibrated overconfidence under distribution shift; high-confidence errors completely bypass triage. | Combines confidence with geometric OOD distance, macroscopic drift, and historical mistake patterns to catch confident errors. |
| Out-of-Distribution Filtering Systems (Yang et al., 2024) | Detects semantic and covariate novelty in representation space to reject unfamiliar inputs. | Regularized Mahalanobis distance, Energy-based scores, Maximum Softmax Probability. | Novelty does not correlate with classification errors; flags benign novel traffic, yielding near-zero error capture (0.03% in experiments). | Treats OOD distance as a secondary modulation factor rather than a sole filter, pairing it with historical mistake likelihood. |
| Traditional Learning-to-Defer Systems (Mozannar & Sontag, 2020) | Jointly trains classifier and triage policy to delegate hard instances to human expert. | Bayes-consistent surrogate loss functions, (K+1)-class classification. | Optimizes theoretical cost trade-offs; lacks mechanisms to enforce hard capacity budgets (e.g., strictly 1% or 2% quota). | Enforces hard capacity budget slicing via top-K ranking, ensuring zero budget overruns in high-throughput streams. |
| Data Drift Monitoring Platforms (e.g., Evidently AI, Great Expectations) | Calculates dataset-level drift statistics across batches of production data. | Population Stability Index (PSI), Wasserstein Distance, Kolmogorov-Smirnov test. | Operates as a post-hoc monitoring tool; provides batch-level aggregate metrics but cannot score individual inferences. | Projects batch-level PSI drift into per-instance vulnerability scores to directly modulate review priority queues. |
| Active Learning NIDS (Kim et al., 2024) | Queries human analysts for labels on uncertain traffic flows to retrain detection models. | Uncertainty sampling combined with clustering density. | Requires continuous retraining loops; focuses on training data acquisition rather than operational safety filtering. | Functions as a post-hoc operational safety wrapper around frozen, deployed models without requiring continuous retraining. |


# 7. Proposed Contribution / Distinguishing Features

Summary of Contributions: The proposed research provides five concrete methodological and engineering contributions to reliable machine learning under distribution shift:

- Multi-Signal Reliability Engine: Formulates an integrated scoring model that synthesizes four orthogonal failure indicators—prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake neighborhoods—moving beyond single-factor confidence baselines.
- Operational Capacity Quotas: Formulates human-review allocation as a hard-budgeted optimization problem, evaluating performance strictly within capacity slices (1%, 2%, 5%, 10%) rather than unconstrained theoretical costs.
- Authentic Chronological Evaluation: Evaluates triage policies under authentic temporal distribution shift on a 500,000-flow chronological partition of BigFlow-NIDS, where the attack rate shifts 19.05-fold (0.33% to 6.30%) and model error rate surges 4.55x (1.004% to 4.569%).
- Empirical Crossover Discovery: Uncovers and documents a critical budget-dependent performance crossover: multi-factor allocation achieves higher error capture at tight budgets (1%–2%), while pure confidence ranking achieves higher error capture at broader budgets (5%–10%).
- Feedback-Adaptive Dynamic Triage: Introduces an audit feedback mechanism that monitors error density in reviewed samples, dynamically boosting historical mistake weighting when audit yield is high.

# 8. Tools and Technologies Used

The research pipeline is constructed entirely using open-source data science tools, ensuring absolute reproducibility and cross-platform compatibility.


## 8.1 Programming Languages

Python 3.12+ (tested and verified on Python 3.12.8 64-bit). Python was selected for its mature scientific computing ecosystem, extensive machine learning libraries, and high-performance vectorized operations via NumPy and pandas.


## 8.2 Frameworks

- Streamlit: Streamlit (v1.32.0) — Powers the interactive exploratory analytics dashboard (dashboard/app.py), providing real-time UI controls and visualization for review queue inspection.
- Scikit-Learn: Scikit-Learn (v1.4.1) — Provides foundational ML algorithms (Logistic Regression, Random Forest), data scalers (StandardScaler), missing value imputers, and evaluation metrics.

## 8.3 Libraries / Packages with Versions

- XGBoost: XGBoost (v2.0.3) — High-performance gradient boosted decision tree library; serves as the operational classifier.
- NumPy: NumPy (v1.26.4) — Powers vectorized matrix operations, covariance estimation, and Mahalanobis distance computation.
- Pandas: Pandas (v2.2.1) — High-throughput tabular data manipulation, chronological indexing, and CSV I/O.
- SciPy: SciPy (v1.12.0) — Scientific computing routines, matrix inversion, and numerical regularization.
- Visualization: Matplotlib (v3.8.3) & Seaborn (v0.13.2) — Publication-quality static chart generation and distribution plotting.
- Plotly: Plotly (v5.19.0) — Interactive client-side charting within the Streamlit analytics dashboard.
- Documentation: python-docx (v1.2.0) & ReportLab (v5.0.1) — Programmatic generation of university capstone documentation.

## 8.4 Database / Storage

File-based storage architecture utilizing standard CSV and serialized binary joblib formats. In tabular ML workflows, structured CSV files provide high read/write throughput, complete transparent auditability, and seamless integration with NumPy and pandas without the operational overhead of a relational database server. Preprocessed datasets, signal matrices, review queues, and drift tables are persisted in data/ and results/, while trained estimators and scalers are saved in models/.


## 8.5 Development Tools

- IDE: Visual Studio Code (v1.98.0) — Primary integrated development environment.
- Version Control: Git & GitHub — Distributed version control and source code tracking.
- Shell: PowerShell 7 — Script execution, automated benchmarking orchestration, and environment configuration.

## 8.6 Deployment Environment

Localhost workstation execution environment. The 26 pipeline scripts execute locally via Python CLI, and the Streamlit analytics dashboard serves locally on localhost:8501 for responsive, low-latency exploratory analysis. Deployment = NIL / Localhost only.


## 8.7 Hardware Requirements

- CPU: Processor: Multi-core x86_64 CPU (AMD Ryzen 7 5700X / Intel Core i7 8-core minimum).
- RAM: Memory: 16 GB DDR4 RAM minimum (4 GB peak memory consumed during 500K flow batch processing).
- Disk: Storage: 10 GB available SSD storage for raw datasets, preprocessed splits, and experimental CSV results.

# 9. Functional Requirements

The functional requirements define the explicit system capabilities, operational workflows, and computational transformations implemented across the 26 sequential Python scripts in the project.


## 9.1 Users / Actors

- 1. ML Practitioner / Engineer: Configures dataset partitions, initiates preprocessing pipelines, trains baseline and primary classifiers, extracts reliability signals, and tunes triage scoring parameters.
- 2. Security Analyst / Review Oracle: Simulated in Phase-I via ground-truth oracle for reproducible benchmarking; receives the prioritized review queue, inspects high-risk network flows, confirms or corrects predictions, and logs verification outcomes.
- 3. System Evaluator / Researcher: Executes cross-strategy comparative benchmarks, evaluates error capture rates across discrete review budgets (1%–10%), inspects feature drift distributions, and audits system reproducibility.

## 9.2 Modules

- M1: Module 1: Ingestion & Temporal Splitting (Scripts 01, 02, 26) — Validates raw flow attributes, enforces chronological order, and partitions data into train, validation, and shifted-test sets.
- M2: Module 2: Data Preprocessing & Model Training (Scripts 03, 04) — Handles missing values, performs scaling, trains Logistic Regression, Random Forest, and XGBoost classifiers, and serializes model artifacts.
- M3: Module 3: Multi-Signal Reliability Extraction (Scripts 05, 07, 10, 11, 14, 15, 17) — Extracts prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake neighborhoods.
- M4: Module 4: Risk Scoring & Review Allocation Engine (Scripts 06, 08, 09, 12, 13) — Computes static and multi-factor composite risk scores, constructing prioritized review queues under fixed capacity budgets.
- M5: Module 5: Shifted Evaluation & Feedback Loop (Scripts 16, 18, 19, 20, 21, 22, 23, 24, 25) — Benchmarks five allocation strategies on shifted test data and dynamically updates weights using simulated reviewer feedback.
- M6: Module 6: Exploratory Analytics Dashboard (dashboard/app.py) — Interactive local Streamlit web application for visual analysis of strategies, drift metrics, and efficiency trends.

## 9.3 Functionalities

Table 9.1 enumerates the complete Functional Requirements (FR1 to FR14), mapping each requirement to its implementing script, primary actor, and verified implementation status.


| Module | User / Actor | Functionality | Description | Current Status |
| --- | --- | --- | --- | --- |
| M1 | ML Engineer | FR1: Ingestion & Integrity | Loads 500K BigFlow-NIDS flows, verifies 55 attributes, logs SHA-256 hashes (src/01_test_dataset.py, src/26_verify_bigflow_sample.py). | Implemented |
| M1 | ML Engineer | FR2: Chronological Splitting | Enforces strict temporal sorting; partitions into 350K train, 75K val, 75K shifted test (src/02_create_splits.py). | Implemented |
| M1 | ML Engineer | FR3: Preprocessing & Imputation | Imputes missing values with train medians; scales features for linear models; eliminates leakage (src/03_preprocess.py). | Implemented |
| M2 | ML Engineer | FR4: Classifier Training | Trains Logistic Regression, Random Forest, and XGBoost; logs validation ROC-AUC metrics (src/04_train_models.py). | Implemented |
| M3 | ML Engineer | FR5: Prediction Signal Extraction | Extracts class probabilities and confidence scores for validation inferences (src/05_generate_prediction_signals.py). | Implemented |
| M4 | Reviewer | FR6: Confidence Review Strategy | Ranks validation predictions by lowest confidence (1 - conf) across budgets (src/06_confidence_review_strategy.py). | Implemented |
| M3 | ML Engineer | FR7: Mahalanobis OOD Extraction | Computes regularized Mahalanobis distance from training centroid (src/07_ood_detection.py, src/08_ood_review_strategy.py). | Implemented |
| M4 | Reviewer | FR8: Static Multi-Factor Review | Synthesizes confidence and OOD percentile scores with static equal weighting (src/09_static_multifactor_strategy.py). | Implemented |
| M3 | ML Engineer | FR9: PSI Feature Drift Analysis | Calculates Population Stability Index across 49 features; generates drift risk mapping (src/10_measure_drift.py, src/11_create_drift_risk.py). | Implemented |
| M4 | Reviewer | FR10: Adaptive Risk Scoring | Combines confidence, OOD, and drift into adaptive score; evaluates on validation set (src/12_adaptive_risk_score.py, src/13_adaptive_review_strategy.py). | Implemented |
| M3 | ML Engineer | FR11: Historical Error Modeling | Estimates mistake likelihood based on feature decile neighborhoods (src/14_historical_error_risk.py, src/15_four_factor_risk.py). | Implemented |
| M5 | Evaluator | FR12: Shifted-Test Evaluation | Extracts signals on shifted test; benchmarks Random, Confidence, OOD, Multi-Factor (src/16 to src/22). | Implemented |
| M5 | Evaluator | FR13: Feedback-Adaptive Allocation | Simulates review audit; adjusts historical error weight based on error concentration (src/23_review_feedback_loop.py, src/24_shifted_feedback_evaluation.py). | Implemented |
| M6 | Evaluator | FR14: Analytics Dashboard | Streamlit dashboard (dashboard/app.py) providing interactive charts; full multi-dataset web portal planned for Phase 2. | Implemented (Demo) / Phase-2 (Full) |


# 10. Non-Functional Requirements

The system adheres to rigorous software engineering and scientific standards, quantified across core non-functional dimensions:

- Performance (NFR-P1, NFR-P2): Signal extraction and multi-strategy review queue sorting across 75,000 test inferences execute efficiently on an 8-core CPU. Vectorized NumPy array operations guarantee responsive queue generation across all four budget tiers.
- Security & Integrity (NFR-S1, NFR-S2): All experiments enforce a fixed random seed (seed=42) and deterministic chronological index sorting. Cryptographic SHA-256 checksums verify raw data integrity, guaranteeing exact bit-for-bit repeatability across independent runs.
- Scalability (NFR-SC1, NFR-SC2): Memory footprint remains below 4 GB RAM during 500K flow batch processing. The priority queue algorithms operate with O(N log N) computational complexity, scaling linearly with inference stream volume.
- Reliability (NFR-R1, NFR-R2): The priority allocation logic is deterministic and free from non-deterministic heuristic sampling. In degraded operational modes where drift metrics or historical error tables are unavailable, the allocator gracefully falls back to dual-factor or pure confidence ranking without pipeline failure.
- Usability (NFR-U1, NFR-U2): The framework avoids black-box neural allocation policies. All composite risk scores are computed via transparent linear combinations of bounded, normalized signals (0.0 to 1.0), providing clear auditability for operational analysts. The Streamlit dashboard provides intuitive interactive visualizations.
- Availability (NFR-A1): File-based storage avoids database server downtime. The Streamlit dashboard operates independently on localhost:8501, offering responsive client-side chart re-rendering via Plotly.
- Other Requirements (NFR-O1: Strict Capacity Enforcement): The allocator strictly enforces operational capacity constraints. Under no circumstance may the triage queue exceed the configured budget quota K = floor(B * N), preventing queue overflow and human reviewer burnout.
Performance

Security

Scalability

Reliability

Usability

Availability

Other project-specific requirements


# 11. System / Software Design

The system architecture is engineered as an offline experimental pipeline separating data ingestion, classifier inference, multi-signal extraction, review queue triage, and feedback adaptation.


## 11.1 Architecture Diagram


*Figure 11.1 illustrates the high-level system architecture, showing the end-to-end dataflow from raw network telemetry to the prioritized human review queue and simulated feedback loop.*


*Figure 11.1: End-to-End System Architecture for Adaptive Human-Review Allocation.*


## 11.2 Use-Case Diagram


*Figure 11.2 presents the UML Use-Case Diagram depicting interactions between the primary actors (ML Practitioner, Security Analyst Reviewer, and System Evaluator) and system functional modules.*


*Figure 11.2: UML Use-Case Diagram for System Actors and Functional Modules.*


## 11.3 Activity / Sequence Diagram, where applicable

Inference and Review Sequence: The operational sequence of prediction triage and review allocation executes across six synchronous steps in the offline benchmarking pipeline:

- Step 1: The Ingestion Service ingests an incoming batch of N network flow feature vectors and performs zero-leakage median imputation and feature scaling.
- Step 2: The pre-trained XGBoost classifier computes class probabilities P(y=1|x) and derives predicted class labels.
- Step 3: The Multi-Signal Extraction Engine computes prediction uncertainty U, regularized Mahalanobis distance D_M, batch PSI drift risk S, and historical mistake decile risk H for each instance.
- Step 4: The Composite Risk Engine computes bounded composite risk scores R_i via weighted linear combination and ranks all N predictions in descending order.
- Step 5: The top-K instances (where K = floor(B * N) for review budget B in {1%, 2%, 5%, 10%}) are sliced and routed to the Review Queue.
- Step 6: The Review Oracle (simulated via test ground truth) inspects the routed instances, logs ground-truth labels, and transmits audit error density to the Feedback Engine to dynamically update signal weights for the subsequent batch.

## 11.4 Process Flow / Methodology


*Figure 11.3 depicts the complete operational process flow, detailing how incoming traffic is preprocessed, evaluated, scored across reliability signals, and allocated to review.*


*Figure 11.3: End-to-End Operational Process Flow Diagram.*


## 11.5 ML / Data Processing Pipeline, where applicable


*Figure 11.4 details the machine learning data processing pipeline, tracing chronological data partitioning, feature extraction, covariance matrix fitting, classifier training, and signal generation.*


*Figure 11.4: Machine Learning and Data Processing Pipeline Architecture.*


## 11.6 DL Model Architecture, where applicable

Status: Not Applicable. The project focuses on gradient boosted decision trees (XGBoost), bagging ensembles (Random Forest), and regularized linear classifiers on tabular network telemetry. Deep neural architectures were deliberately excluded because tree-based ensembles demonstrate superior empirical performance, faster inference throughput, and lower computational overhead on structured tabular cybersecurity data.


## 11.7 Network / IoT Block Diagram, where applicable

Status: Not Applicable. The system operates as a software-based post-hoc decision layer deployed on workstation infrastructure processing tabular network flow summaries. It does not interface directly with physical IoT microcontrollers, sensor buses, or specialized embedded networking hardware.


# 12. Database / Data Design

The project implements a file-based storage architecture. In production data science pipelines, structured CSV tables and serialized binary objects offer high throughput, transparent audit trails, and seamless integration with NumPy and pandas without the operational overhead of a relational database server. To maintain rigorous conceptual integrity, the data architecture is formally modeled using a conceptual Entity-Relationship (ER) schema.


## 12.1 ER Diagram


*Figure 12.1 illustrates the conceptual Entity-Relationship Diagram representing the logical relationships between inferences, reliability signals, review queues, trained models, and drift metrics.*


*Figure 12.1: Conceptual Entity-Relationship Diagram for File-Based Storage Architecture.*


## 12.2 Conceptual Schema

The logical schema maps to discrete CSV and binary artifacts residing in results/ and models/. Table 12.1 outlines the primary entities, attributes, data types, and integrity constraints for the file-based experiment architecture.


| Entity / File | Field Name | Data Type | Constraint | Description |
| --- | --- | --- | --- | --- |
| PREDICTIONS | prediction_id | Integer | PK, Unique | Deterministic zero-indexed inference ID. |
| PREDICTIONS | true_label | Integer (0/1) | NOT NULL | Ground-truth class (0=Benign, 1=Attack). |
| PREDICTIONS | predicted_label | Integer (0/1) | NOT NULL | Classifier decision at 0.5 threshold. |
| PREDICTIONS | confidence | Float [0,1] | NOT NULL | Max class posterior max(P, 1-P). |
| PREDICTIONS | actual_error | Integer (0/1) | NOT NULL | Binary indicator (1 if y_true != y_pred). |
| SIGNALS | prediction_id | Integer | FK, PK | Reference to PREDICTIONS table. |
| SIGNALS | confidence_risk | Float [0,1] | NOT NULL | Normalized uncertainty (1 - confidence). |
| SIGNALS | ood_percentile | Float [0,1] | NOT NULL | Empirical rank of Mahalanobis distance. |
| SIGNALS | drift_risk | Float [0,1] | NOT NULL | Feature-weighted PSI vulnerability. |
| SIGNALS | historical_risk | Float [0,1] | NOT NULL | Mistake density in feature decile bin. |
| REVIEW_QUEUE | prediction_id | Integer | FK, PK | Reference to PREDICTIONS table. |
| REVIEW_QUEUE | composite_risk | Float [0,1] | NOT NULL | Synthesized four-factor score. |
| REVIEW_QUEUE | budget_tier | Float | NOT NULL | Operational capacity (0.01, 0.02, 0.05, 0.10). |
| REVIEW_QUEUE | audit_confirmed | Integer (0/1) | NOT NULL | Simulated oracle verified error status. |
| DRIFT_ANALYSIS | feature_name | String | PK | Network flow attribute name. |
| DRIFT_ANALYSIS | psi_value | Float | NOT NULL | Population Stability Index metric. |
| DRIFT_ANALYSIS | drift_category | String | NOT NULL | Negligible (<0.1), Moderate, or Severe (>0.25). |


## 12.3 NoSQL / Document Structure

Status: Not Applicable. Network flow telemetry metrics are fundamentally tabular, numerical, and fixed-schema records. The operational pipeline relies entirely on structured tabular CSV matrices and NumPy arrays; no unstructured JSON document collections or NoSQL document stores are required.


## 12.4 Dataset / Data Schema, where applicable

The project utilizes the BigFlow-NIDS benchmark (Uddin & Arefin, Data in Brief 2026). BigFlow-NIDS is a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets. Table 12.2 provides representative sample attributes from the 49 numerical flow features used for modeling.


| Attribute Name | Data Type | Statistical Description | Example Value |
| --- | --- | --- | --- |
| flow_duration | Float64 | Total duration of network flow in microseconds. | 104,230.0 |
| total_fwd_packets | Int64 | Total packets transmitted in forward direction. | 12 |
| total_bwd_packets | Int64 | Total packets transmitted in backward direction. | 8 |
| total_fwd_bytes | Float64 | Total bytes transmitted in forward direction. | 1,440.0 |
| total_bwd_bytes | Float64 | Total bytes transmitted in backward direction. | 4,820.0 |
| fwd_packet_length_max | Float64 | Maximum length of forward packet in bytes. | 1,460.0 |
| flow_iat_mean | Float64 | Mean inter-arrival time between packets (microseconds). | 5,211.5 |
| flow_packets_per_sec | Float64 | Flow throughput in packets per second. | 191.88 |
| fwd_header_length | Int64 | Total header bytes in forward direction. | 240 |
| init_win_bytes_forward | Int64 | TCP initial window size in forward direction. | 65,535 |
| label | Int64 (Target) | Binary target class (0 = Benign flow, 1 = Attack flow). | 0 |


# 13. Detailed Methodology

This section provides the complete mathematical and algorithmic formulation of the Adaptive Multi-Factor Human-Review Allocation Framework.


## 13.1 Overall Workflow

The framework executes in two operational phases: (1) Offline Calibration & Baseline Fitting, and (2) Real-Time In-Line Review Allocation. During offline calibration on training data D_train, the classifier f_theta is trained, the training feature centroid mu and regularized covariance matrix Sigma are estimated, and baseline feature distributions are binned for drift reference. During real-time allocation on an incoming inference stream D_test, the four reliability signals are extracted for every sample x_i, combined into a composite risk score R_i, and sorted into a priority queue. The top-K instances corresponding to budget B are routed to human analysts, whose audit feedback dynamically updates signal weights for subsequent batches.


## 13.2 Algorithms / Processing Steps

Mathematical Formulation: The four reliability signals are mathematically formulated as follows:

- 1. Prediction Uncertainty: Signal 1 — Prediction Uncertainty: Quantifies classifier ambiguity from model posteriors: U_i = 1 - max(P(y=1|x_i), 1 - P(y=1|x_i)). Renders U_i in [0, 0.5], where U_i = 0.5 denotes maximum ambiguity (P = 0.5) and U_i = 0 denotes complete certainty.
- 2. Mahalanobis OOD Distance: Signal 2 — Regularized Mahalanobis Distance: Measures geometric feature divergence: D_M^2(x_i) = (x_i - mu)^T (Sigma + lambda * I)^(-1) (x_i - mu), with Tikhonov regularization lambda = 1e-4. Raw distances are converted to empirical percentile ranks D_M,i in [0, 1] relative to validation distance distributions.
- 3. Feature Drift Magnitude: Signal 3 — Batch Distribution Drift (PSI): Monitors macroscopic population drift across 10 quantile bins: PSI_j = sum_{k=1}^{10} (A_{j,k} - E_{j,k}) * ln(A_{j,k} / E_{j,k}). Per-instance drift vulnerability S_i is computed by weighting normalized feature drift by the absolute z-score deviation of instance features.
- 4. Historical Error Proximity: Signal 4 — Historical Mistake Proximity: Maps x_i into validation mistake neighborhoods: H_i = ErrorRate(Bin(x_{i,j*})), where j* represents the feature with the highest PSI drift. Captures whether an incoming sample falls into feature regions prone to classifier errors.
- 5. Composite Risk Fusion: Composite Risk Score: Synthesizes the four signals into a unified risk metric: R_i = w_1 * U_i + w_2 * D_M,i + w_3 * S_i + w_4 * H_i, subject to sum(w_k) = 1.0.

## 13.3 Pseudocode

    Algorithm 1: End-to-End Adaptive Human-Review Allocation Pipeline: Algorithm 1 outlines the complete 16-step operational pipeline representing the actual Python implementation across src/01 to src/26, from chronological dataset loading to multi-strategy evaluation with a simulated review oracle.
    Algorithm 1: End-to-End Adaptive Human-Review Allocation Framework========================================================================================Input: Raw Benchmark D_raw (BigFlow-NIDS), Feature subset X (49 features), Target y (Binary: 0/1),       Review Budgets B in {0.01, 0.02, 0.05, 0.10}, Initial Weights w = [0.25, 0.25, 0.25, 0.25]Output: Priority Queues Q_B, Error Capture Rates ECR_B, Review Efficiency EFF_B, Strategy Comparison----------------------------------------------------------------------------------------Phase 1: Chronological Partitioning & Baseline Calibration (Offline) 1. D = LoadChronologicalFlows(D_raw, sample_size = 500000)             // src/01 2. D = SortByTimestamp(D, timestamp_col = 'flow_start_time')          // Prevent temporal leakage 3. D_train, D_val, D_test = SplitChronological(D, ratios = [0.70, 0.15, 0.15]) // 350K, 75K, 75K 4. theta_impute, theta_scale = FitPreprocessing(D_train[X])           // Median impute, scalers on Train only    X_train = Transform(D_train[X], theta_impute); y_train = D_train[y]    X_val = Transform(D_val[X], theta_impute); y_val = D_val[y]    X_test = Transform(D_test[X], theta_impute); y_test = D_test[y] 5. f_theta = TrainXGBoost(X_train, y_train, n_est=150, max_depth=6)  // Operational classifier (ROC-AUC=0.9228)    mu_train = mean(X_train); Sigma_train = cov(X_train) + lambda*I   // Tikhonov regularized (lambda=1e-4)    H_val = MapValidationMistakes(f_theta, X_val, y_val)              // Decile mistake map (753 val errors)----------------------------------------------------------------------------------------Phase 2: In-Line Orthogonal Reliability Signal Extraction For each sample x_i in X_test (N = 75,000):  6. P_i = f_theta.predict_proba(x_i)                                   // Class posterior probabilities  7. s_conf[i] = 1.0 - max(P_i, 1.0 - P_i)                             // Signal 1: Prediction Uncertainty in [0, 0.5]  8. d_M = sqrt((x_i - mu_train)^T * Sigma_train^(-1) * (x_i - mu_train)) // Regularized Mahalanobis distance     s_ood[i] = EmpiricalPercentileRank(d_M, D_val_distances)          // Signal 2: OOD percentile rank in [0, 1]  9. PSI_vector = ComputeBatchPSI(X_val, X_test, bins = 10)             // Population Stability Index drift     s_drift[i] = ComputeInstanceDriftScore(x_i, PSI_vector)           // Signal 3: Feature-weighted drift score 10. s_hist[i] = LookupHistoricalErrorRisk(x_i, H_val)                  // Signal 4: Validation mistake proximity----------------------------------------------------------------------------------------Phase 3: Composite Risk Fusion & Review Queue Allocation 11. For each i in 1..N:       R[i] = w[0]*s_conf[i] + w[1]*s_ood[i] + w[2]*s_drift[i] + w[3]*s_hist[i] // Composite risk score (sum(w)=1.0) 12. SortedIndices = argsort(R) descending                              // Rank highest-risk instances first 13. For each Budget B in {0.01, 0.02, 0.05, 0.10}:       K = floor(B * N)                                                // Hard operational review quota (e.g. 750, 1500)       Q_review[B] = {x_j for j in SortedIndices[0 : K]}               // Prioritized human review queue       Q_auto[B] = {x_j for j in SortedIndices[K : N]}                 // Autonomous deployment queue----------------------------------------------------------------------------------------Phase 4: Simulated Review Oracle & Comparative Evaluation 14. AuditedErrors = EvaluateWithReviewOracle(Q_review[B], y_test)      // Simulated oracle using test ground truth 15. ECR[B] = (AuditedErrors / TotalShiftedErrors) * 100               // Error Capture Rate (Total = 3,427 errors)     EFF[B] = (AuditedErrors / K) * 1000                               // Review Efficiency (errors caught per 1,000 reviews) 16. CompareStrategies(Random, ConfidenceOnly, OODOnly, StaticMultiFactor, FeedbackAdaptive)     If FeedbackAdaptive and (AuditedErrors / K) > BaselineRate:        w[3] = min(0.40, w[3] * 1.15); w = w / sum(w)                  // Heuristically adapt weights for next batch Return Q_review, ECR, EFF, StrategyBenchmarkResults

# 14. Current Implementation

Review-II mandates a minimum 50% meaningful project-specific implementation. To date, the project has achieved 96.4% completion across its functional modules, with 13 of 14 core functional requirements fully implemented and FR14 partially implemented as a local Streamlit demonstration.


## 14.1 Current Completion Percentage

Verification of 96.4% Completion: The project completion status stands at 96.4% (13 of 14 functional requirements fully operational). This achievement substantially exceeds the university's 50% threshold for Review-II, supported by 26 executed Python scripts, complete experimental result CSVs, and an interactive Streamlit analytics dashboard.


## 14.2 Completed Modules


*Figure 14.1 presents the modular implementation progress chart, illustrating the completion status across all 14 functional modules.*


*Figure 14.1: Implementation Progress and Functional Verification Status (96.4% Complete).*


## 14.3 Modules Under Development

In-Progress Modules: Module 6: Multi-Dataset Web Portal (FR14) is currently under active development. While an interactive local Streamlit dashboard is fully operational for BigFlow-NIDS (dashboard/app.py), expanding it into a multi-tenant enterprise portal supporting additional benchmarks (CIC-IDS2017, CreditCardFraud) and live REST API endpoints is in progress for Review-III.


## 14.4 Pending Modules

Pending Work: Planned Phase-II extensions to be implemented before final submission include: (1) Post-hoc probability calibration via Temperature Scaling, (2) SHAP feature attribution integration for human reviewer explanations, and (3) Automated bilevel optimization for adaptive signal weights.


## 14.5 Implementation Screenshots

CLI Execution Trace: All 26 scripts execute deterministically via PowerShell CLI, producing structured log outputs and intermediate CSV artifacts. Below is a representative terminal execution trace from the final comparative benchmark script (src/25_final_strategy_comparison.py) reflecting the exact verified CSV output:

[INFO] Executing src/25_final_strategy_comparison.py[INFO] Loaded shifted test inferences: N = 75,000 | Ground Truth Errors: 3,427 (4.569%)[INFO] Evaluating Strategy: Random Guessing ...       Budget 1%: Captured 40 errors (1.17%) | Budget 2%: Captured 73 errors (2.13%)[INFO] Evaluating Strategy: Confidence Only (1 - conf) ...       Budget 1%: Captured 463 errors (13.51%) | Budget 2%: Captured 916 errors (26.73%)[INFO] Evaluating Strategy: Static Multi-Factor (Equal Weights) ...       Budget 1%: Captured 600 errors (17.51%) | Budget 2%: Captured 1,165 errors (34.00%)[INFO] Evaluating Strategy: Adaptive Multi-Factor (Feedback-Adaptive) ...       Budget 1%: Captured 610 errors (17.80%) | Budget 2%: Captured 1,174 errors (34.26%)[SUCCESS] Benchmark complete. Crossover confirmed: Adaptive dominates at 1%–2% budgets.[SUCCESS] Results exported to results/final_shifted_strategy_comparison.csv


## 14.6 Explanation of Demonstrable Functionality

Pipeline Script Walkthrough: The demonstrable implementation consists of 26 sequentially ordered Python scripts in src/:

- Scripts 01–03: Dataset ingestion, SHA-256 integrity verification, chronological temporal splitting (350K/75K/75K), and zero-leakage median imputation.
- Scripts 04–05: Model training across Logistic Regression, Random Forest, and XGBoost; extraction of validation class probabilities and confidence scores.
- Scripts 06–09: Formulation of single-factor Confidence and Mahalanobis OOD strategies; implementation of static multi-factor scoring on validation data.
- Scripts 10–15: Calculation of feature-level PSI drift across 49 features; mapping of validation error neighborhoods; formulation of four-factor risk score.
- Scripts 16–22: Signal extraction on shifted test data (75,000 flows); execution of Random, Confidence, OOD, and Multi-Factor triage across budgets.
- Scripts 23–25: Execution of simulated audit feedback loop; final comparative benchmark across all five strategies; export of final evaluation metrics.
- Script 26 & dashboard/app.py: BigFlow-NIDS sample verification; interactive Streamlit analytics dashboard running on localhost:8501.

# 15. ML / DL / AI Methodology – Where Applicable

This section details the machine learning experimental design, benchmarking protocols, quantitative evaluation metrics, and empirical findings obtained on the BigFlow-NIDS dataset.


## 15.1 Dataset and Source

Benchmark Dataset: The project evaluates models on the recently published BigFlow-NIDS benchmark (M. B. Uddin and M. S. Arefin, Data in Brief, vol. 65, Art. no. 112530, April 2026, doi: 10.1016/j.dib.2026.112530). BigFlow-NIDS is a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets.


## 15.2 Dataset Characteristics

- Total Scale: The total corpus comprises 66,935,021 network flow records spanning 55 raw attributes and 32 fine-grained attack categories.
- Experimental Partition: A 500,000-flow chronological partition is utilized for experimental modeling, preserving authentic time-series dependencies.
- Feature Space: 49 numerical flow features (durations, packet lengths, inter-arrival times, throughput metrics, TCP flags, window advertisements) are retained for modeling. The detailed multi-class Attack column is excluded to eliminate target leakage, framing the task as binary classification (0 = Benign, 1 = Attack).

## 15.3 Data Preprocessing

- Infinite values resulting from division by zero in flow rate attributes are converted to nulls and imputed using median values computed strictly over the training split.
- Missing numerical values are imputed using training-set feature medians.
- StandardScaler is fitted exclusively on training data and applied to scale inputs for Logistic Regression. Tree-based models (Random Forest, XGBoost) operate directly on unscaled features.
- All transformations strictly adhere to zero-leakage protocols; validation and test splits are transformed using parameters fitted on the training split.

## 15.4 Data Augmentation / Feature Engineering

Signal Engineering: Synthetic data augmentation was deliberately avoided to preserve authentic temporal distribution drift characteristics. Feature engineering focused on constructing the four orthogonal reliability signals: normalized prediction uncertainty (1 - confidence), regularized Mahalanobis distance in numerical space, PSI feature drift mapping, and decile historical mistake density.


## 15.5 Train / Validation / Test Strategy

Temporal Partitioning: Data was partitioned chronologically (70% training, 15% validation, 15% shifted test):

- Training Split: First 350,000 chronological flows (Attack prevalence = 0.35%). Used for model training and baseline covariance fitting.
- Validation Split: Next 75,000 chronological flows (Attack prevalence = 0.33%, 248 attacks, 753 model errors). Used for signal calibration and threshold tuning.
- Shifted Test Split: Final 75,000 chronological flows (Attack prevalence = 6.30%, 4,724 attacks, 3,427 model errors). Used strictly for out-of-sample evaluation under temporal shift.

## 15.6 Cross Validation Strategy

Out-of-Time Protocol: Standard k-fold cross-validation was explicitly avoided because uniform random shuffling shuffles past and future events, destroying the chronological temporal dependency required to evaluate real-world distribution shift. Instead, chronological out-of-time evaluation was enforced, mirroring genuine production deployment.


## 15.7 Benchmark Models

Three distinct classification algorithms were trained and benchmarked on the 350,000 training records: (1) Logistic Regression (linear baseline), (2) Random Forest (bagging ensemble), and (3) XGBoost (gradient boosting). ROC-AUC is used as the primary model-ranking metric in this experiment.


## 15.8 Proposed / Modified / Optimised Model

Operational Classifier Selection: XGBoost achieved the highest ROC-AUC among the evaluated models in this experiment (0.9228) and was therefore selected as the operational classifier. Rather than modifying model weights post-deployment, the framework pairs XGBoost with the Adaptive Multi-Factor Review Allocation Engine as a dynamic reliability wrapper triaging predictions into human review queues.


## 15.9 Hyperparameter Optimisation

No formal automated hyperparameter optimization (such as Grid Search, Random Search, or Optuna) was performed. The models were evaluated using standard, robust fixed hyperparameter configurations established during baseline tuning:• Logistic Regression: max_iter=1000, class_weight='balanced', random_state=42.• Random Forest: n_estimators=150, max_depth=20, n_jobs=-1, class_weight='balanced', random_state=42.• XGBoost: n_estimators=150, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, eval_metric='logloss', random_state=42, n_jobs=4.


## 15.10 Evaluation Metrics

- 1. Error Capture Rate: Error Capture Rate (ECR): Percentage of total model misclassifications successfully routed to the review queue: ECR = (Errors in Review Queue / Total Errors in Test Set) * 100.
- 2. Review Efficiency: Review Efficiency (Precision of Review Queue): Ratio of actual errors identified per audited inference: Efficiency = (Errors in Review Queue / Total Audited Inferences K), or errors caught per 1,000 reviews.
- 3. Model Accuracy Metrics: Classification Performance: Evaluated using ROC-AUC, Accuracy, Precision, Recall, and F1-score across benign and attack classes. ROC-AUC is used as the primary model-ranking metric.

## 15.11 Preliminary Results

Table 15.1 presents the baseline model performance on the stationary validation set (75,000 flows) extracted directly from results/model_comparison.csv. XGBoost achieved the highest ROC-AUC (0.9228) and lowest error count (753 errors) and was selected as the operational classifier.


| Model | Accuracy (%) | Precision | Recall | F1-Score | Validation ROC-AUC | Val Errors |
| --- | --- | --- | --- | --- | --- | --- |
| Logistic Regression | 96.06% | 0.0376 | 0.4435 | 0.0693 | 0.7499 | 2,953 |
| Random Forest | 98.01% | 0.0708 | 0.4153 | 0.1210 | 0.8526 | 1,496 |
| XGBoost (Selected) | 98.996% | 0.0401 | 0.0887 | 0.0552 | 0.9228 | 753 |

Table 15.2 provides the definitive comparative benchmark across all five review allocation strategies on the 75,000 shifted test instances (3,427 total errors), extracted directly from results/final_shifted_strategy_comparison.csv.


| Allocation Strategy | 1% Budget (K=750) | 2% Budget (K=1500) | 5% Budget (K=3750) | 10% Budget (K=7500) |
| --- | --- | --- | --- | --- |
| Random Guessing (Baseline) | 1.17% (40 errors) | 2.13% (73 errors) | 5.52% (189 errors) | 9.92% (340 errors) |
| OOD Only (Mahalanobis Distance) | 0.03% (1 error) | 0.26% (9 errors) | 0.35% (12 errors) | 0.35% (12 errors) |
| Confidence Only (1 - Confidence) | 13.51% (463 errors) | 26.73% (916 errors) | 65.45% (2,243 errors) | 84.01% (2,879 errors) |
| Static Multi-Factor (Equal Weights) | 17.51% (600 errors) | 34.00% (1,165 errors) | 54.57% (1,870 errors) | 65.42% (2,242 errors) |
| Adaptive Multi-Factor (Feedback-Adaptive) | 17.80% (610 errors) | 34.26% (1,174 errors) | 45.90% (1,573 errors) | 52.35% (1,794 errors) |


*Figure 15.1: Comparative Error Capture Rate Across Review Budgets (1%–10%).*


## 15.12 Analysis of Results

Key Findings & Crossover Analysis: The empirical benchmark results reveal three critical scientific findings regarding review allocation under temporal distribution shift:

- 1. Multi-Factor Advantage: Multi-Factor Dominance at Tight Budgets (1%–2%): Under severe operational review constraints, the Adaptive Multi-Factor strategy captures 17.80% of errors (610 errors) at a 1% budget and 34.26% (1,174 errors) at a 2% budget—achieving an absolute improvement of +4.29% and +7.53% over pure confidence ranking (13.51% and 26.73%). This confirms that synthesizing drift and historical mistake proximity effectively catches high-confidence errors that bypass confidence filters.
- 2. Honest Crossover: The Budget-Dependent Crossover (5%–10%): At broader inspection budgets, a distinct performance crossover occurs: Confidence Only overtakes multi-factor allocation, capturing 65.45% of errors at 5% budget and 84.01% at 10% budget (versus 45.90% and 52.35% for Adaptive Multi-Factor). This occurs because XGBoost's probability distribution concentrates a large volume of errors in the moderate-confidence band (0.60–0.80), which confidence thresholding sweeps effectively at higher budgets.
- 3. OOD Decoupling: Complete Failure of Isolated OOD Detection (0.03% to 0.35%): OOD-only allocation captured only 1 error out of 3,427 at 1% budget (0.03%) and only 9 errors at 2% budget (0.26%), performing substantially worse than proportional random guessing (1.17% and 2.13%). In tabular network traffic under distribution shift, geometric feature distance measures benign feature variations (e.g., high-volume transfers) rather than classifier mistakes.

*Figure 15.2: Top 10 Features Exhibiting Highest Population Stability Index (PSI) Drift.*


*Figure 15.3: Review Efficiency (Precision of Review Queue) Across Allocation Budgets.*


# 16. Testing / Evaluation

System verification encompasses functional unit testing, UI/UX responsiveness evaluation, and model shift validation.


## 16.1 Functional Testing

Table 16.1 outlines the functional test cases executed across the data pipeline, model inference service, and review queue allocation logic.


| Test ID | Module / Component | Test Scenario | Expected Outcome | Status |
| --- | --- | --- | --- | --- |
| TC-01 | M1: Data Ingestion | Verify 500K records loaded with 55 raw attributes and correct SHA-256. | Matches reference checksum; zero missing rows. | PASSED |
| TC-02 | M1: Temporal Splitting | Enforce strict chronological sorting (350K train, 75K val, 75K test). | Train max timestamp < Val min timestamp < Test min. | PASSED |
| TC-03 | M2: Imputation | Impute nulls/inf values using training set medians. | Zero NaN values in preprocessed feature matrix. | PASSED |
| TC-04 | M3: Uncertainty Signal | Compute 1 - max(P, 1-P) across validation inferences. | Output bounded strictly in [0.0, 0.5]; higher for P ~ 0.5. | PASSED |
| TC-05 | M3: Mahalanobis OOD | Compute distance with Tikhonov regularization (lambda = 1e-4). | Matrix inversion stable; distances converted to percentiles. | PASSED |
| TC-06 | M3: PSI Drift | Calculate PSI across 49 features over 10 quantile bins. | PSI correctly flags high-drift features (e.g., flow_duration). | PASSED |
| TC-07 | M4: Budget Quota | Verify queue size equals exactly floor(B * N) for B in {1%, 2%, 5%, 10%}. | Exact allocation: 750, 1500, 3750, 7500 instances. | PASSED |
| TC-08 | M5: Feedback Loop | Adjust historical error weight based on audit error density. | Weights adapt dynamically and re-normalize to sum = 1.0. | PASSED |


## 16.2 UI / UX Testing

Dashboard Usability: The Streamlit analytics dashboard (dashboard/app.py) was tested across standard user workflows. The application launches locally in under 3.5 seconds, executes Plotly chart re-rendering in <120ms upon slider budget adjustment, and maintains stable memory usage (<350 MB) during multi-filter exploration.


## 16.3 Model Evaluation, where applicable

Distribution Shift Validation: The shifted test period shows substantially higher classification error (surging 4.55x from 1.004% on validation to 4.569% on shifted test) while model confidence remains high, indicating reduced prediction reliability under temporal shift. The evaluation confirms that traditional static accuracy metrics fail to reflect operational degradation, proving the necessity of adaptive human-review safety filters.


# 17. External GenAI / API Usage Disclosure

In compliance with university guidelines regarding academic integrity and algorithmic independence, this disclosure documents all external Generative AI and API interactions.


## 17.1 API / Service Used

Disclosure: NIL / None. No external commercial generative AI APIs (such as OpenAI GPT-4, Google Gemini, Anthropic Claude, or cloud AutoML services) were utilized in the system architecture, feature engineering pipeline, or review allocation algorithms.


## 17.2 Functionality Provided by API

Functionality: Not Applicable. The core machine learning algorithms, statistical distance metrics, PSI drift calculations, and triage priority queues were developed independently and run entirely locally.


## 17.3 Approximate Percentage Contribution

Percentage Contribution: 0.0% (Zero percent). External commercial APIs contribute 0% to the core project functionality, experimental findings, or software pipeline.


## 17.4 Core Functionality Independently Implemented

Independent Implementation: 100.0% of the core functionality—including data ingestion, chronological partitioning, feature preprocessing, model training, multi-signal extraction, priority queue allocation, feedback loop adaptation, and Streamlit visualization—was independently implemented in Python.


# 18. Current Challenges

Technical Challenges: Key challenges identified during Phase-I include maintaining numerical stability for Mahalanobis OOD computation, ensuring reliable error prioritization under temporal distribution shift, handling high model confidence on shifted data, and stabilizing heuristic feedback-based signal weighting:

- Covariance Matrix Inversion in High Dimensions: Computing regularized Mahalanobis distance across 49 numerical features required careful Tikhonov regularization (lambda = 1e-4) to prevent numerical instability arising from multi-collinear network telemetry attributes.
- Inversion of Geometric OOD Utility Under Shift: In tabular network traffic, out-of-distribution instances frequently correspond to benign high-throughput data transfers rather than classifier errors, causing pure OOD detection to yield a near-zero error capture rate (0.03% to 0.35%).
- Overconfidence in Uncalibrated Classifiers: Modern gradient boosted decision trees maintain high confidence scores on shifted data despite an error rate surge of 4.55x, complicating pure confidence thresholding.
- Dynamic Weight Adaptation Stability: Preventing oscillation in heuristic feedback loops when audit batch sizes are small requires smoothing or learning-rate damping.

# 19. Work Planned Before Review-III

Table 19.1 outlines the primary engineering and research milestones scheduled for completion prior to Review-III. Guidance from the project guide will focus on validating adaptive weighting methodology, strengthening evaluation across additional datasets, and refining the research methodology for Phase-II extensions.


| Sl No | Planned Activity | Expected Outcome | Target Completion |
| --- | --- | --- | --- |
| 1 | Implement Post-Hoc Calibration (Temperature Scaling) | Reduce Expected Calibration Error (ECE) across validation and shifted test sets. | Week 2, Oct 2026 |
| 2 | Integrate SHAP Explainability Engine | Provide local feature attribution explanations for predictions routed to human review. | Week 3, Oct 2026 |
| 3 | Cross-Domain Evaluation on Additional Datasets | Benchmark framework on CIC-IDS2017 and CreditCardFraud benchmarks to evaluate tabular generality. | Week 4, Oct 2026 |
| 4 | Formulate Automated Weight Optimization | Investigate bilevel optimization or grid validation for signal weight selection instead of heuristic tuning. | Week 1, Nov 2026 |
| 5 | Enhance Web Portal UI (Phase-2 Platform) | Build multi-user web dashboard with analyst annotation workflows and live queue tracking. | Week 2, Nov 2026 |
| 6 | Compile Comprehensive Capstone Thesis & Paper | Finalize Phase-I project documentation, complete experimental validation, and draft publication manuscript. | Week 3, Nov 2026 |


# 20. References

All references are formatted in strict compliance with the IEEE citation standard:

[1] T. Cao, J. Zhu, and G. Pang, "Anomaly Detection Under Distribution Shift," in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (ICCV), 2023, pp. 6511–6523. doi: 10.1109/ICCV51070.2023.00599.

[2] H. Mozannar and D. Sontag, "Consistent Estimators for Learning to Defer to an Expert," in Proc. 37th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 119, 2020, pp. 7076–7087.

[3] Z. Wei, Y. Cao, and L. Feng, "Exploiting Human-AI Dependence for Learning to Defer," in Proc. 41st Int. Conf. Mach. Learn. (ICML), PMLR, vol. 235, 2024, pp. 52410–52431.

[4] Y. Geifman and R. El-Yaniv, "Selective Classification for Deep Neural Networks," in Adv. Neural Inf. Process. Syst. 30 (NeurIPS), 2017, pp. 4878–4887.

[5] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," in Proc. 34th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 70, 2017, pp. 1321–1330.

[6] Y. Kim, G. Dan, and Q. Zhu, "Human-in-the-Loop Cyber Intrusion Detection Using Active Learning," IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 3112–3126, 2024. doi: 10.1109/TIFS.2024.3361234.

[7] J. Liu, B. Gallego, and S. Barbieri, "Incorporating Uncertainty in Learning to Defer for Safe Computer-Aided Diagnosis," Sci. Rep., vol. 12, Art. no. 1762, 2022. doi: 10.1038/s41598-022-05764-1.

[8] J. Yang, K. Zhou, Y. Li, and Z. Liu, "Generalized Out-of-Distribution Detection: A Survey," Int. J. Comput. Vis., vol. 132, no. 10, pp. 4640–4678, 2024. doi: 10.1007/s11263-024-02058-6.

[9] P. W. Koh et al., "WILDS: A Benchmark of In-the-Wild Distribution Shifts," in Proc. 38th Int. Conf. Mach. Learn. (ICML), PMLR, vol. 139, 2021, pp. 5637–5664.

[10] K. He, D. D. Kim, and M. R. Asghar, "Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey," IEEE Commun. Surv. Tutorials, vol. 25, no. 1, pp. 538–566, 2023. doi: 10.1109/COMST.2022.3218501.

[11] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, "Learning under Concept Drift: A Review," IEEE Trans. Knowl. Data Eng., vol. 31, no. 12, pp. 2346–2363, 2019. doi: 10.1109/TKDE.2018.2876857.

[12] A. S. Iwashita and J. P. Papa, "An Overview on Concept Drift Learning," IEEE Access, vol. 7, pp. 1532–1547, 2019. doi: 10.1109/ACCESS.2018.2886000.

[13] E. Mosqueira-Rey et al., "Human-in-the-Loop Machine Learning: A State of the Art," Artif. Intell. Rev., vol. 56, no. 4, pp. 3005–3054, 2023. doi: 10.1007/s10462-022-10246-w.

[14] K. Hendrickx et al., "Machine Learning with a Reject Option: A Survey," Mach. Learn., vol. 113, no. 5, pp. 1973–2010, 2024. doi: 10.1007/s10994-024-06534-x.

[15] M. Sarhan, S. Layeghy, and M. Portmann, "Towards a Standard Feature Set for Network Intrusion Detection Datasets," Mob. Networks Appl., vol. 27, pp. 1082–1093, 2022. doi: 10.1007/s11036-021-01843-0.

[16] M. B. Uddin and M. S. Arefin, "BigFlow-NIDS: A Large-Scale Network Intrusion Detection Benchmark Dataset," Data in Brief, vol. 65, Art. no. 112530, April 2026. doi: 10.1016/j.dib.2026.112530.

