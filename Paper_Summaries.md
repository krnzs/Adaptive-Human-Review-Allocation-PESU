# Paper Summaries: Literature Survey & Defense Guide

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Degree:** Master of Computer Applications (MCA) — Data Analytics  
**Institution:** Department of Computer Applications, PES University, Bangalore  
**Course Code:** UQ25CA741A  
**Student SRN:** PES1PG25CA101  
**Project Guide:** Prof. Dilip Kumar Maripuri  

---

## Detailed Paper Summaries (16 Papers)

---

### [1] Cao, Zhu, & Pang (2023) — Anomaly Detection Under Distribution Shift

- **Citation (IEEE):** T. Cao, J. Zhu, and G. Pang, "Anomaly Detection Under Distribution Shift," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. / Int. Conf. Comput. Vis. (ICCV)*, 2023, pp. 6511–6523, doi: 10.1109/ICCV51070.2023.00599.
- **Indexing:** **IEEE & Scopus Indexed** (IEEE/CVF ICCV proceedings; IEEE Xplore & Scopus indexed).
- **Problem:** Conventional unsupervised anomaly detection models assume test data follows the exact same distribution as normal training data. When deployment conditions change (e.g., lighting, sensor noise, or background shifts), anomaly detectors mistake harmless environmental distribution shifts for anomalies, causing a massive surge in false alarms.
- **Core Idea / Method:** The authors propose **ADShift**, an unsupervised framework that aligns the representations of shifted in-distribution data with nominal training data while preserving the separability of true anomalies. It minimizes domain discrepancy between training normal data and test normal data via an adversarial domain-alignment objective, combined with a margin-based pseudo-anomaly generation loss that prevents normal shifted samples from being collapsed into anomaly space.
- **Data & Experiments:** Evaluated on four benchmark vision datasets under distribution shift: CIFAR-10-C, ImageNet-C, MVTec-AD under domain shift, and Camelyon17 (medical domain shift). Baselines included Deep SVDD, CutPaste, PatchCore, and standard domain generalization methods. Evaluated using Area Under the ROC Curve (AUROC).
- **Main Results:**
  1. ADShift achieved average AUROC improvements of over 10% on corrupted and shifted benchmarks compared to standard state-of-the-art anomaly detectors.
  2. While standard models dropped by 15–25% in AUROC under moderate corruption, ADShift retained over 85% of its baseline unshifted detection capability.
  3. Proved that feature shift without semantic change can be disentangled from genuine anomalies.
- **Limitations:** Focuses entirely on unsupervised anomaly detection in image data; assumes unlabeled shifted batches are available during evaluation for domain alignment; does not address budgeted human triage or tabular network flows.
- **Relevance to My Project:** Directly supports my **chronological distribution shift formulation** and my **OOD signal**. It provides formal evidence that distribution shift degrades unsupervised detection models. It differs because my work focuses on binary network intrusion flows with supervised base models and explicit capacity-constrained human review.
- **2-Line Slide Summary:** Addresses anomaly detection failure when test data shifts from training distributions. Proves unsupervised domain alignment mitigates false positives, directly justifying our shifted evaluation benchmark.
- **20-Second Spoken Version:** *"Cao et al. in ICCV 2023 showed that when the environment shifts, anomaly detectors confuse normal environmental changes with true threats. This justifies why we evaluate our intrusion detection model on a later chronological time window rather than a clean random split."*
- **Panel Question & Answer:**
  - *Panel Question:* "Cao's paper aligns distributions to remove shift. Why didn't you use domain adaptation instead of routing to humans?"
  - *Answer:* "Domain adaptation requires accumulating batches of shifted data and retraining or adapting representations offline. In real-time network security, high-risk packets arrive continuously; our triage engine routes uncertain and drifted packets to human analysts immediately at inference time."

---

### [2] Mozannar & Sontag (2020) — Consistent Estimators for Learning to Defer to an Expert

- **Citation (IEEE):** H. Mozannar and D. Sontag, "Consistent Estimators for Learning to Defer to an Expert," in *Proc. 37th Int. Conf. Mach. Learn. (ICML)*, PMLR vol. 119, 2020, pp. 7076–7087.
- **Indexing:** **PMLR-only** (Not indexed in Scopus/IEEE). *Verified IEEE Alternative:* C. Geng, S.-j. Huang, and S. Chen, "Recent Advances in Open Set Recognition: A Survey," *IEEE TPAMI*, vol. 43, no. 10, pp. 3614–3631, 2021.
- **Problem:** When an ML model works alongside a human expert, standard classifiers are trained independently of the human's strengths and weaknesses. Prior deferral heuristics used two-stage pipelines (confidence thresholding followed by expert handoff) that are provably suboptimal because the classifier is never trained to complement human expertise.
- **Core Idea / Method:** Formalizes **Learning to Defer (L2D)** as an augmented $(K+1)$-class classification problem where the $(K+1)$-th action represents deferring to the human. They construct a consistent surrogate loss function:
  $$\Psi(h(x), y, m) = -\log\left(\frac{e^{h_y(x)}}{e^{h_\bot(x)} + \sum_{j=1}^K e^{h_j(x)}}\right) - \mathbb{I}(m = y)\log\left(\frac{e^{h_\bot(x)}}{e^{h_\bot(x)} + \sum_{j=1}^K e^{h_j(x)}}\right)$$
  where $h_\bot(x)$ is the deferral logit and $m$ is the expert's prediction. They prove that minimizing this convex surrogate is statistically Bayes-consistent with the joint 0-1 system loss.
- **Data & Experiments:** Evaluated on synthetic mixture models, CIFAR-10 with simulated synthetic experts (experts with varying accuracy across specific classes), and the CheXpert chest X-ray dataset with radiologist annotations. Evaluated on overall system accuracy and expert coverage.
- **Main Results:**
  1. The joint L2D classifier outperformed two-stage confidence-threshold baselines by 4.2% to 9.8% in system accuracy across diverse human error profiles.
  2. The model learned to predict accurately on classes where the human expert struggled while deferring classes where the human excelled.
  3. Established the first mathematically consistent surrogate loss for human-AI decision systems.
- **Limitations:** Assumes the expert's cost is a fixed constant per query; assumes stationary i.i.d. data (no temporal distribution shift); requires paired human predictions during training.
- **Relevance to My Project:** Establishes the theoretical foundation for **human review routing**. It differs because Mozannar assumes fixed deferral cost rather than strict operational capacity budgets (1%, 2%, 5%, 10%), assumes stationary data, and trains a single specialized joint model. My project operates as a post-hoc triage layer over an existing model under distribution shift.
- **2-Line Slide Summary:** Formalizes learning-to-defer by jointly training a classifier and a deferral policy using a Bayes-consistent surrogate loss. Establishes theoretical foundations for routing uncertain predictions to human experts.
- **20-Second Spoken Version:** *"Mozannar and Sontag proved in ICML 2020 that human-AI collaboration requires an explicit deferral policy rather than just thresholding model scores. We build on this concept by routing difficult cases to human analysts under fixed operational review quotas."*
- **Panel Question & Answer:**
  - *Panel Question:* "Why didn't you implement Mozannar's (K+1)-class loss function directly in your XGBoost model?"
  - *Answer:* "Mozannar's loss requires access to expert labels during training time. In production cybersecurity, ground-truth human verdicts on real traffic are unavailable during training. Furthermore, tree-based models like XGBoost cannot natively minimize custom non-convex multi-class surrogate losses as easily as neural networks, making a decoupled scoring triage framework more practical."

---

### [3] Wei, Cao, & Feng (2024) — Exploiting Human-AI Dependence for Learning to Defer

- **Citation (IEEE):** Z. Wei, Y. Cao, and L. Feng, "Exploiting Human-AI Dependence for Learning to Defer," in *Proc. 41st Int. Conf. Mach. Learn. (ICML)*, PMLR vol. 235, 2024, pp. 52484–52499.
- **Indexing:** **PMLR-only** (Not indexed in Scopus/IEEE). *Verified IEEE Alternative:* D.-B. Wang, L. Feng, and M.-L. Zhang, "Rethinking Out-of-Distribution Detection in Multiple Instance Learning," in *Proc. IEEE/CVF CVPR*, 2022, pp. 9390–9399.
- **Problem:** Existing learning-to-defer algorithms assume the AI and the human make independent errors conditional on the input. In reality, humans and AI systems frequently exhibit correlated errors on ambiguous or noisy instances, which leads prior L2D methods to defer instances that the human also gets wrong.
- **Core Idea / Method:** Proposes **Dependent Bayes Optimality**, reformulating the Bayes-optimal decision rule to explicitly condition on the joint probability $P(Y=y, M=m | X=x)$ where $M$ is the human prediction. The authors design a new consistent surrogate loss that models human-AI error correlation directly from training data without requiring explicit confidence estimation of the human.
- **Data & Experiments:** Tested on CIFAR-10, CIFAR-100, ImageNet subsets, and the HateXplain social-media moderation dataset featuring real crowdsourced human annotations. Compared against Mozannar (2020), Verma (2022), and Charusaie (2022). Metrics included system error rate and deferral rate under varying human expertise.
- **Main Results:**
  1. Achieved 2.3% to 5.7% lower system error rates on HateXplain compared to existing L2D methods by avoiding deferrals on instances where both human and model fail.
  2. Demonstrated that modeling human-AI dependence prevents wasted human review effort on ambiguous samples.
  3. Proved consistency under hypothesis classes with restricted capacity.
- **Limitations:** Requires rich multi-annotator human labels during training to model correlation; does not account for feature-level drift or strict top-$K$ budget allocations.
- **Relevance to My Project:** Informs our **review efficiency concept** (errors caught per 1,000 audits). It shows that sending samples to humans that provide zero information is wasteful. It differs because our Phase-1 uses an oracle reviewer on network flows rather than modeling subjective annotator bias.
- **2-Line Slide Summary:** Models human-machine error correlation to prevent deferrals when both the AI and the human fail. Informs our review-efficiency triage objective under constrained operational inspection capacity.
- **20-Second Spoken Version:** *"Wei et al. showed in ICML 2024 that blindly deferring difficult samples to humans is inefficient if humans also fail on them. This motivates our review efficiency metric, ensuring human audit time targets genuinely recoverable system errors."*
- **Panel Question & Answer:**
  - *Panel Question:* "Does your simulated reviewer make errors like in Wei et al.?"
  - *Answer:* "In Phase 1, our reviewer is a ground-truth simulation oracle based on verified test labels, providing an upper-bound benchmark. In our Phase-2 limitations, we explicitly identify human reviewer fatigue and stochastic error as a planned extension."

---

### [4] Geifman & El-Yaniv (2017) — Selective Classification for Deep Neural Networks

- **Citation (IEEE):** Y. Geifman and R. El-Yaniv, "Selective Classification for Deep Neural Networks," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, vol. 30, 2017, pp. 4878–4887.
- **Indexing:** **Scopus Indexed Series** (NeurIPS proceedings indexed in Scopus, ISSN: 1049-5258).
- **Problem:** Deep neural networks produce predictions for all inputs regardless of risk, making them unsafe for mission-critical applications. There was no principled method to construct a selective classifier (classifier with a reject/abstain option) that guaranteed a user-specified error rate at test time with rigorous statistical guarantees.
- **Core Idea / Method:** Formulates selective classification using a prediction function $f(x)$ and a selection function $g(x) \in \{0, 1\}$. The selective risk is:
  $$r(f, g) = \frac{\mathbb{E}[\ell(f(x), y) \cdot g(x)]}{\mathbb{E}[g(x)]}, \quad \text{Coverage } \phi(g) = \mathbb{E}[g(x)]$$
  Using Softmax Response (SR), $g_\theta(x) = \mathbb{I}(\max_k P(y_k|x) \ge \theta)$, they prove via sample-bound concentration inequalities that one can calibrate the threshold $\theta$ on validation data to guarantee a desired risk bound $r^*$ with high confidence $(1-\delta)$.
- **Data & Experiments:** Evaluated on SVHN, CIFAR-10, and ImageNet using VGG and ResNet architectures. Measured risk-coverage curves across coverage levels from 10% to 100%.
- **Main Results:**
  1. On ImageNet top-5 classification, the method achieved a 2% error rate at 60% coverage (rejecting 40% of difficult instances).
  2. On CIFAR-10, error dropped below 1% at 70% coverage.
  3. Established that standard Softmax probability ranking is an effective baseline for selective classification in stationary regimes.
- **Limitations:** Relies entirely on maximum Softmax probability; assumes stationary in-distribution test data; degrades severely when test data undergoes distribution shift.
- **Relevance to My Project:** Provides the exact mathematical baseline for our **Pure Confidence strategy** (ranking instances by ascending confidence). Our experiments demonstrate its core vulnerability: under temporal shift, models remain confident on incorrect predictions, allowing errors to bypass confidence-based rejection.
- **2-Line Slide Summary:** Formulates selective classification risk-coverage trade-offs using prediction confidence. Provides the theoretical baseline for our confidence-based review strategy, whose limitations under distribution shift we empirically demonstrate.
- **20-Second Spoken Version:** *"Geifman and El-Yaniv established selective prediction by rejecting instances below a confidence threshold. We use this exact strategy as our primary baseline, but show that under real distribution shift, it misses confident errors."*
- **Panel Question & Answer:**
  - *Panel Question:* "If Geifman proved confidence ranking is effective on ImageNet, why did pure confidence fail at low budgets in your project?"
  - *Answer:* "Geifman tested on stationary, unshifted data. Under our temporal distribution shift, XGBoost suffered from silent overconfidence—maintaining an average confidence of 96.8% despite a 4.55x surge in errors. At tight budgets (1–2%), confidence alone misses novel attack flows."

---

### [5] Guo, Pleiss, Sun, & Weinberger (2017) — On Calibration of Modern Neural Networks

- **Citation (IEEE):** C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, "On Calibration of Modern Neural Networks," in *Proc. 34th Int. Conf. Mach. Learn. (ICML)*, PMLR vol. 70, 2017, pp. 1321–1330.
- **Indexing:** **PMLR-only** (Not indexed in Scopus/IEEE). *Verified IEEE Alternative:* K. Fernando and C. P. Tsokos, "Uncertainty Quantification and Deep Neural Network Calibration," *IEEE TNNLS*, vol. 33, 2022.
- **Problem:** Historically, shallow neural networks output probabilities that matched true empirical accuracy. The authors discovered that modern deep neural networks (from 2012 onwards) are severely miscalibrated: their predicted confidence probabilities are systematically higher than their true likelihood of being correct.
- **Core Idea / Method:** Conducts a systematic diagnostic across network depth, width, weight decay, and Batch Normalization. They measure miscalibration using **Expected Calibration Error (ECE)**:
  $$\text{ECE} = \sum_{m=1}^M \frac{|B_m|}{N} |\text{acc}(B_m) - \text{conf}(B_m)|$$
  They introduce **Temperature Scaling**, a simple single-parameter post-processing method:
  $$\hat{p}_i = \max_k \sigma(z_i / T)_k$$
  where logits $z_i$ are divided by a learned scalar $T > 0$ fitted on validation data by minimizing Negative Log-Likelihood without altering model classification predictions.
- **Data & Experiments:** Evaluated across 10 vision and NLP datasets (CIFAR-100, ImageNet, SVHN, 20 Newsgroups) on ResNet, DenseNet, and Wide-ResNet. Compared Temperature Scaling against Platt scaling, isotonic regression, and histogram binning.
- **Main Results:**
  1. Proved modern techniques (depth, Batch Normalization, low weight decay) improve accuracy but cause severe overconfidence miscalibration.
  2. Temperature scaling reduced ECE by up to 75% across datasets (e.g., from 6.8% to 1.8% on ImageNet) while preserving original accuracy.
  3. Showed that simple single-parameter scaling outperforms complex non-parametric calibration methods.
- **Limitations:** Evaluated strictly on in-distribution (i.i.d.) validation and test sets; does NOT study calibration under distribution shift; does not incorporate out-of-distribution detection.
- **Relevance to My Project:** Explains the fundamental mechanism of **model overconfidence**. *Correction Note:* Guo et al. proves uncalibrated overconfidence on *stationary* deep models, which provides the foundation for understanding why uncalibrated confidence fails in selective review. Temperature scaling is a core planned component of our Phase-2 roadmap.
- **2-Line Slide Summary:** Demonstrates that modern classifiers suffer from severe overconfidence miscalibration and proposes temperature scaling. Explains why raw output probabilities cannot be treated as true probabilities of correctness in triage queues.
- **20-Second Spoken Version:** *"Guo et al. showed in ICML 2017 that modern models are systematically overconfident. This explains why raw prediction probability alone is an unreliable indicator of safety and why multi-signal reliability scoring is necessary."*
- **Panel Question & Answer:**
  - *Panel Question:* "Does temperature scaling fix the overconfidence caused by temporal distribution shift?"
  - *Answer:* "No. As shown in later literature, temperature scaling fitted on validation data improves in-distribution calibration, but under covariate or concept shift, the calibrated temperature parameter itself degrades. That is why our triage framework incorporates external drift (PSI) and OOD signals."

---

### [6] Kim, Dán, & Zhu (2024) — Human-in-the-Loop Cyber Intrusion Detection Using Active Learning

- **Citation (IEEE):** Y. Kim, G. Dán, and Q. Zhu, "Human-in-the-Loop Cyber Intrusion Detection Using Active Learning," *IEEE Trans. Inf. Forensics Security*, vol. 19, pp. 8658–8672, 2024, doi: 10.1109/TIFS.2024.3434647.
- **Indexing:** **IEEE & Scopus Indexed** (IEEE TIFS is a premier Q1 journal in information security).
- **Problem:** Anomaly-based network intrusion detection systems produce excessive false alarms, overwhelming security operations center (SOC) analysts. Uninformed alert investigation wastes scarce human investigation time on repetitive benign alerts while sophisticated multi-stage intrusions proceed undetected.
- **Core Idea / Method:** Formulates alert investigation as an active learning problem governed by a sequential hypothesis testing framework using a pruned Hidden Markov Model (HMM). The system dynamically ranks alerts using information-theoretic criteria: **Max Ratio** and **Max KL (Kullback-Leibler) divergence**, selecting the most informative alerts for analyst investigation to minimize Mean Time to Detection (MTTD) subject to a target Mean Time Between False Detections (MTBFD).
- **Data & Experiments:** Evaluated on realistic simulated network environments executing multi-stage advanced persistent threat (APT) attacks. Benchmarked against First-Come-First-Served, random inspection, and static alert scoring.
- **Main Results:**
  1. Active alert prioritization reduced intrusion detection time by up to **79%** compared to standard static prioritization baselines.
  2. Maintained the target false alarm rate while reducing analyst investigation workload by over 60%.
  3. Demonstrated that sequential human feedback updates the belief state of the system, accelerating identification of novel attack steps.
- **Limitations:** Focuses on sequential alert correlation in enterprise networks using HMM state spaces; requires structured alert feeds from rule engines rather than raw tabular NetFlow traffic; does not explicitly model feature drift or offline batch budget slicing.
- **Relevance to My Project:** Directly establishes the **cybersecurity domain justification** for human-review allocation. It proves that human review capacity in intrusion detection is strictly constrained and that intelligent alert triage prevents analyst fatigue.
- **2-Line Slide Summary:** Optimizes SOC analyst alert investigation using active learning and sequential hypothesis testing. Directly motivates our capacity-constrained human review triage in network intrusion detection systems.
- **20-Second Spoken Version:** *"Kim et al. in IEEE TIFS 2024 proved that active alert prioritization cuts cyber intrusion detection time by 79%. This provides the operational justification for our project: in real SOC environments, human audit budget is severely limited."*
- **Panel Question & Answer:**
  - *Panel Question:* "How does your human-review allocation differ from Kim's active learning framework?"
  - *Answer:* "Kim et al. use active learning to update an HMM belief state over time to detect multi-stage APTs. Our framework solves inference-time selective classification on tabular NetFlow streams, triage-routing individual predictions across 1% to 10% capacity budgets under distribution shift."

---

### [7] Liu, Gallego, & Barbieri (2022) — Incorporating Uncertainty in Learning to Defer Algorithms for Safe Computer-Aided Diagnosis

- **Citation (IEEE):** J. Liu, B. Gallego, and S. Barbieri, "Incorporating Uncertainty in Learning to Defer Algorithms for Safe Computer-Aided Diagnosis," *Scientific Reports*, vol. 12, no. 1, Art. no. 1762, pp. 1–11, 2022, doi: 10.1038/s41598-022-05725-7.
- **Indexing:** **Scopus Indexed** (Published in Nature Portfolio's *Scientific Reports*, Q1, Scopus indexed).
- **Problem:** Standard learning-to-defer algorithms treat the classifier and the deferral policy as a black-box pair, often failing to consider the internal predictive uncertainty of the machine learning model. This leads to inefficient deferral policies that refer safe, routine cases to clinicians or fail to flag truly ambiguous boundary cases.
- **Core Idea / Method:** Proposes **Learning to Defer with Uncertainty (LDU)**. The method incorporates model predictive uncertainty (via Monte Carlo Dropout or ensemble variance) directly into the deferral decision loss function. An adjustable hyperparameter $\alpha$ balances the cost of clinical misclassification against the clinical labor cost of deferring to human doctors.
- **Data & Experiments:** Evaluated across three medical diagnostics tasks: myocardial infarction diagnosis from hospital discharge summaries, comorbidity prediction from EHR tabular records, and pleural effusion detection on chest X-rays. Evaluated on F1-score, deferral rate, and clinical coverage.
- **Main Results:**
  1. LDU achieved identical diagnostic accuracy and F1 scores to conventional deferral algorithms while reducing the human deferral rate by up to **28%**.
  2. Proved that explicit uncertainty estimates allow the system to retain more automated decisions safely.
  3. Demonstrated robust performance across both unstructured text/images and structured tabular clinical records.
- **Limitations:** Medical application focus; deferral thresholds require tuning a penalty weight $\alpha$ rather than matching an explicit capacity budget (such as top 1% or 2%); does not evaluate under macroscopic temporal distribution shift.
- **Relevance to My Project:** Informs our **multi-factor reliability concept** by demonstrating that predictive uncertainty enhances deferral efficiency. Our framework goes further by combining uncertainty with OOD distance and feature drift under explicit capacity slicing.
- **2-Line Slide Summary:** Incorporates predictive uncertainty into learning-to-defer objectives for clinical diagnosis. Demonstrates that explicit uncertainty estimation substantially reduces unnecessary human deferrals while preserving decision safety.
- **20-Second Spoken Version:** *"Liu et al. showed in Scientific Reports that adding uncertainty to deferral policies reduces human workload by 28% without losing accuracy. We adopt this insight by using uncertainty as a core reliability signal in our triage score."*
- **Panel Question & Answer:**
  - *Panel Question:* "Liu's paper tunes an alpha penalty to decide when to defer. Why didn't you use an alpha penalty?"
  - *Answer:* "An alpha penalty produces a variable deferral rate that changes unpredictably when data shifts. In real operations, human teams have fixed staffing (e.g., exactly 750 or 1,500 reviews per batch). Our top-K budget percentile formulation guarantees strict budget compliance."

---

### [8] Yang, Zhou, Li, & Liu (2024) — Generalized Out-of-Distribution Detection: A Survey

- **Citation (IEEE):** J. Yang, K. Zhou, Y. Li, and Z. Liu, "Generalized Out-of-Distribution Detection: A Survey," *Int. J. Comput. Vis.*, vol. 132, no. 12, pp. 5635–5662, 2024, doi: 10.1007/s11263-024-02117-4.
- **Indexing:** **Scopus Indexed** (IJCV is a premier computer vision journal, Q1, Springer, Scopus indexed).
- **Problem:** Machine learning systems deployed in open-world environments encounter inputs from unseen classes or shifted domains. The literature was fragmented across anomaly detection, novelty detection, open-set recognition, and out-of-distribution (OOD) detection without a unified taxonomy or standardized evaluation methodology.
- **Core Idea / Method:** Establishes a comprehensive taxonomy classifying generalized OOD detection along two orthogonal axes:
  1. **Shift Type:** Semantic shift (novel classes $Y_{OOD} \cap Y_{ID} = \emptyset$) vs. Covariate shift (distribution change $P_{OOD}(X) \neq P_{ID}(X)$ with identical label spaces).
  2. **Methodology:** Post-hoc score functions (Mahalanobis distance, Energy score, ReAct, MSP) vs. Training-time regularization (outlier exposure, contrastive learning). Standardizes evaluation benchmarks via OpenOOD.
- **Data & Experiments:** Surveys and benchmarks over 30 OOD algorithms on CIFAR, ImageNet, TextClass, and medical datasets using FPR@95%TPR, AUROC, and AUPR.
- **Main Results:**
  1. Post-hoc feature-space distance metrics (specifically regularized Mahalanobis distance) consistently rank among the top performers for detecting covariate and semantic shifts without retraining.
  2. Revealed that models performing well on semantic novelty often degrade when exposed to pure covariate shifts.
  3. Proved that energy-based and distance-based scores outperform raw Softmax confidence for detecting distribution outliers.
- **Limitations:** Comprehensive taxonomy and survey; focuses predominantly on deep vision and language models; does not explore budgeted human review or tabular network flow triage.
- **Relevance to My Project:** Provides the theoretical foundation for our **Mahalanobis OOD distance signal**. It clarifies why distance in feature space measures deviation from training data. It also explains our experimental finding: Mahalanobis distance flags covariate outliers, but covariate outliers in NetFlow data do not necessarily correlate with classification errors.
- **2-Line Slide Summary:** Comprehensive survey and taxonomy of generalized out-of-distribution detection across semantic and covariate shifts. Establishes the theoretical foundation and post-hoc distance metrics used for our OOD reliability signal.
- **20-Second Spoken Version:** *"Yang et al. in IJCV 2024 provided the definitive taxonomy of OOD detection, proving Mahalanobis distance is a top post-hoc detector. We implemented regularized Mahalanobis distance based on their recommendations."*
- **Panel Question & Answer:**
  - *Panel Question:* "If Yang et al. show Mahalanobis distance is so effective for OOD, why did OOD-only perform worse than random in your shifted test?"
  - *Answer:* "Yang's survey evaluates OOD detection against the ground truth of whether a sample is out-of-distribution. In our project, the objective is catching *classification errors*. In network traffic, high Mahalanobis distance detects benign high-volume packets that XGBoost classifies correctly, so OOD alone does not correlate with classification mistakes."

---

### [9] Koh et al. (2021) — WILDS: A Benchmark of In-the-Wild Distribution Shifts

- **Citation (IEEE):** P. W. Koh *et al.*, "WILDS: A Benchmark of In-the-Wild Distribution Shifts," in *Proc. 38th Int. Conf. Mach. Learn. (ICML)*, PMLR vol. 139, 2021, pp. 5637–5664.
- **Indexing:** **PMLR-only** (Not indexed in Scopus/IEEE). *Verified IEEE Alternative:* L. Ruff *et al.*, "A Unifying Review of Deep and Shallow Anomaly Detection," *Proc. IEEE*, vol. 109, no. 5, pp. 756–795, 2021.
- **Problem:** Machine learning models are typically evaluated on artificially synthesized distribution shifts (e.g., adding Gaussian noise or rotation to CIFAR images). These synthetic shifts fail to reflect the complexity, multimodal structure, and severity of distribution shifts encountered in real-world deployment across time, geography, and user populations.
- **Core Idea / Method:** Introduces **WILDS**, a benchmark of 10 curated datasets spanning real-world distribution shifts across diverse domains (wildlife camera traps across locations, tumor identification across hospitals, satellite imagery across years, code completion across repositories). Standardizes evaluation by measuring **worst-group accuracy** and **out-of-distribution generalization** rather than average in-distribution accuracy.
- **Data & Experiments:** Evaluated on 10 datasets (including iWildCam, Camelyon17, PovertyMap, CivilComments). Benchmarked standard Empirical Risk Minimization (ERM), Domain Invariant Learning (CORAL, DANN), and Group Distributionally Robust Optimization (Group DRO).
- **Main Results:**
  1. Across all 10 real-world domains, state-of-the-art models suffered massive performance drops (15% to 35% accuracy drops) when tested on real out-of-distribution splits.
  2. Existing domain generalization algorithms (Group DRO, CORAL) provided only modest improvements over standard ERM, showing that algorithmic shift mitigation remains an unsolved problem.
  3. Established that chronological and subpopulation evaluations are essential for measuring real deployment reliability.
- **Limitations:** Focuses on model training and benchmark creation; does not address human-in-the-loop triage or capacity-constrained review allocation. *Correction Note:* WILDS does NOT introduce Population Stability Index (PSI).
- **Relevance to My Project:** Provides the empirical justification for our **chronological evaluation split**. We evaluate on temporal partitions to reflect real-world distribution shift, exactly matching the core philosophy established by WILDS.
- **2-Line Slide Summary:** Establishes a benchmark of real-world in-the-wild distribution shifts across domains and time. Justifies our chronological dataset partition design to evaluate model performance degradation under authentic shift.
- **20-Second Spoken Version:** *"Koh et al. in ICML 2021 proved that models degrade severely under real-world distribution shift compared to artificial noise. This directly justifies our chronological train-val-test split on BigFlow-NIDS."*
- **Panel Question & Answer:**
  - *Panel Question:* "Did you use any of the WILDS datasets in your project?"
  - *Answer:* "No. WILDS focuses on vision, text, and satellite data. Our project targets high-throughput network security, so we applied WILDS' principle of chronological out-of-distribution evaluation to the BigFlow-NIDS NetFlow benchmark."

---

### [10] He, Kim, & Asghar (2023) — Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey

- **Citation (IEEE):** K. He, D. D. Kim, and M. R. Asghar, "Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey," *IEEE Commun. Surveys Tuts.*, vol. 25, no. 1, pp. 538–566, 2023, doi: 10.1109/COMST.2022.3233793.
- **Indexing:** **IEEE & Scopus Indexed** (IEEE COMST has the highest impact factor among IEEE communications journals; Q1, Scopus indexed).
- **Problem:** Machine learning-based NIDS are widely proposed in literature but are fragile against adversarial manipulations. Attackers can perturb network packet timing, payload bytes, or flow statistics to evade detection without disrupting the underlying attack functionality.
- **Core Idea / Method:** Provides a comprehensive taxonomy of adversarial attacks and defenses specifically tailored to the network intrusion detection domain. Categorizes attacks into evasion (test-time feature modification) and poisoning (training-time manipulation), distinguishing between feature-space perturbations (modifying tabular vector values) and problem-space perturbations (modifying physical PCAP packet streams while maintaining network protocol validity).
- **Data & Experiments:** Surveys attacks across classic and modern NIDS benchmarks (NSL-KDD, UNSW-NB15, CIC-IDS2017). Analyzes defenses including adversarial training, defensive distillation, feature squeezing, and anomaly filtering.
- **Main Results:**
  1. Demonstrated that adding subtle perturbations to non-functional flow features (e.g., inter-arrival times or packet lengths) reduces deep NIDS detection rates by over 50%.
  2. Identified the "problem-space gap": many mathematical adversarial perturbations produce invalid TCP/IP packets that cannot actually traverse network switches.
  3. Concluded that purely automated defenses remain vulnerable to adaptive adversaries and that human-in-the-loop oversight is critical for resilient security operations.
- **Limitations:** Focuses on deliberate adversarial evasion rather than natural temporal covariate drift; does not formulate human review triage algorithms or budget allocation mechanisms. *Correction Note:* This paper is an adversarial ML survey; human-in-the-loop IDS active learning should be cited to Kim et al. [6].
- **Relevance to My Project:** Establishes the **network intrusion detection context** and explains why base classifiers fail when flow patterns change. It motivates the necessity of monitoring feature shifts (like our PSI drift signal on packet lengths and inter-arrival times).
- **2-Line Slide Summary:** Comprehensive survey of adversarial machine learning vulnerabilities in network intrusion detection. Provides domain security context on how feature perturbations degrade ML classifiers in network traffic.
- **20-Second Spoken Version:** *"He et al. in IEEE COMST 2023 showed that perturbations in network flow attributes cause intrusion detection models to fail silently. This motivates our feature drift monitoring on flow statistics."*
- **Panel Question & Answer:**
  - *Panel Question:* "Is the distribution shift in your test set caused by adversarial attacks or natural drift?"
  - *Answer:* "BigFlow-NIDS incorporates real multi-day network traffic containing both natural temporal evolution in background traffic and emerging attack vectors. Our chronological split captures authentic operational drift rather than synthetic adversarial perturbations."

---

### [11] Lu, Liu, Dong, Gu, Gama, & Zhang (2019) — Learning under Concept Drift: A Review

- **Citation (IEEE):** J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, "Learning under Concept Drift: A Review," *IEEE Trans. Knowl. Data Eng.*, vol. 31, no. 12, pp. 2346–2363, Dec. 2019, doi: 10.1109/TKDE.2018.2876857.
- **Indexing:** **IEEE & Scopus Indexed** (IEEE TKDE is a premier Q1 journal in data engineering, Scopus indexed).
- **Problem:** In streaming and big-data environments, data generation processes change over time, violating the fundamental machine learning assumption that training and test data are drawn from identical distributions. Learning algorithms must detect, adapt to, and recover from concept drift without catastrophic forgetting.
- **Core Idea / Method:** Establishes a formal mathematical framework categorizing concept drift:
  - **Covariate Shift:** $P(X)$ changes while $P(Y|X)$ remains unchanged.
  - **Prior Probability Shift:** $P(Y)$ changes while $P(X|Y)$ remains unchanged.
  - **Real Concept Drift:** Posterior probability $P(Y|X)$ changes over time, meaning identical inputs produce different class labels.
  Reviews drift detection methodologies across four operational stages: (1) Drift Detection, (2) Drift Understanding (where/how it occurred), (3) Model Adaptation (windowing, ensemble weighting), and (4) Memory Management.
- **Data & Experiments:** Surveys statistical tests (Kolmogorov-Smirnov test, Page-Hinkley, CUSUM), windowing algorithms (ADWIN), and drift ensembles (DDM, EDDM, DWM) across synthetic benchmarks (Sine, SEA, Radial) and real data (Electricity, Forest Covertype, Airline).
- **Main Results:**
  1. Proved that monitoring both statistical data distributions $P(X)$ and model error rates $P(\text{error})$ provides faster drift localization than tracking model error alone.
  2. Established that gradual and recurring drifts require adaptive weighting rather than abrupt model replacement.
  3. Identified the delay in obtaining ground-truth labels in production as the single biggest bottleneck for real-world drift adaptation.
- **Limitations:** Focuses on stream mining algorithms that update or retrain model weights online; does not formulate inference-time human review allocation under fixed operational inspection quotas.
- **Relevance to My Project:** Provides the exact theoretical foundation for our **distribution drift signal** and our **adaptive regime weighting**. In our project, PSI measures population drift in $P(X)$, while our review feedback loop tracks emerging error rates, exactly aligning with Lu's dual-monitoring principle.
- **2-Line Slide Summary:** Foundational review defining covariate shift versus real concept drift in streaming data. Provides the theoretical framework for our dual monitoring of population feature drift and prediction error feedback.
- **20-Second Spoken Version:** *"Lu et al. in IEEE TKDE 2019 established that tracking feature shifts alongside error rates is essential for detecting drift. We implement this by combining feature PSI with historical mistake feedback."*
- **Panel Question & Answer:**
  - *Panel Question:* "Does your project address covariate shift or real concept drift?"
  - *Answer:* "Both. In BigFlow-NIDS, our PSI analysis demonstrates severe covariate shift in flow features like packet lengths (PSI > 0.75). Simultaneously, attack prevalence surged from 0.33% to 6.30% with a 4.55x error surge, demonstrating real temporal drift."

---

### [12] Iwashita & Papa (2019) — An Overview on Concept Drift Learning

- **Citation (IEEE):** A. S. Iwashita and J. P. Papa, "An Overview on Concept Drift Learning," *IEEE Access*, vol. 7, pp. 1532–1547, 2019, doi: 10.1109/ACCESS.2018.2886004.
- **Indexing:** **IEEE & Scopus Indexed** (IEEE Access, open-access multidisciplinary journal, Scopus indexed).
- **Problem:** As machine learning models are integrated into critical streaming applications, non-stationary environments cause unexpected performance degradation. Practitioners lack a consolidated overview comparing detection-based approaches versus continuous adaptation mechanisms.
- **Core Idea / Method:** Provides a structured overview comparing two fundamental paradigms for non-stationary learning:
  1. **Active (Triggered) Detection:** Explicit drift detection algorithms (e.g., statistical change detectors, hypothesis testing) monitor metrics and trigger adaptation only when drift is statistically confirmed.
  2. **Passive (Continuous) Adaptation:** Algorithms continuously update model parameters or sliding window weights on incoming batches without explicit drift testing.
  Surveys feature-level statistical metrics (including distance metrics and divergence measures) and drift categorization by speed (sudden, gradual, incremental, reoccurring).
- **Data & Experiments:** Comparative analysis across classic stream-mining benchmarks (Electricity, Weather, Keystroke Dynamics) and synthetic datasets, evaluating classification accuracy, recovery latency, and memory consumption.
- **Main Results:**
  1. Demonstrated that active drift detectors respond faster to sudden shifts, whereas passive ensemble weighting performs better under gradual, multi-modal drift.
  2. Showed that relying solely on error-driven detectors creates dangerous blind spots when ground-truth verification latency is high.
  3. Highlighted that tracking statistical feature distribution properties allows early warning before catastrophic accuracy drops occur.
- **Limitations:** Focuses on standard streaming classifiers; does not model human verification capacity or budget-constrained selective review queues.
- **Relevance to My Project:** Informs our **Adaptive Regime Scoring (FR10)**. Our system classifies drift severity into Low, Moderate, and High regimes based on PSI thresholds and dynamically shifts signal weights, operationalizing Iwashita's active drift-response paradigm.
- **2-Line Slide Summary:** Surveys active versus passive adaptation to concept drift in streaming data. Informs our regime-based adaptive weighting, which dynamically shifts signal priorities based on detected drift severity.
- **20-Second Spoken Version:** *"Iwashita and Papa showed that active drift monitoring provides early warnings before accuracy collapses. This inspired our adaptive regime scoring, which shifts review weights when drift is detected."*
- **Panel Question & Answer:**
  - *Panel Question:* "Why did you use regime-based weight adjustments instead of continuous sliding weights?"
  - *Answer:* "In operational security systems, discrete regimes (Low, Moderate, High) provide explainable, auditable transitions that security teams can verify and govern, whereas continuous weight fluctuations can introduce unstable routing behavior."

---

### [13] Mosqueira-Rey, Hernández-Pereira, Alonso-Ríos, Bobes-Bascarán, & Fernández-Leal (2023) — Human-in-the-Loop Machine Learning: A State of the Art

- **Citation (IEEE):** E. Mosqueira-Rey, E. Hernández-Pereira, D. Alonso-Ríos, J. Bobes-Bascarán, and Á. Fernández-Leal, "Human-in-the-loop machine learning: a state of the art," *Artif. Intell. Rev.*, vol. 56, no. 4, pp. 3005–3054, 2023, doi: 10.1007/s10462-022-10246-w.
- **Indexing:** **Scopus Indexed** (Artificial Intelligence Review, Q1, Springer, Scopus indexed).
- **Problem:** The term "Human-in-the-Loop" (HITL) is used ambiguously across active learning, interactive ML, explainable AI, and validation. The literature lacked a unified conceptual framework defining where, how, and why human interaction should be integrated into machine learning workflows.
- **Core Idea / Method:** Proposes a comprehensive taxonomy structuring HITL across the complete machine learning lifecycle:
  1. **Data Phase:** Active learning, data curation, crowdsourcing, and interactive data annotation.
  2. **Training Phase:** Interactive model training, preference learning, and reinforcement learning from human feedback (RLHF).
  3. **Inference & Decision Phase:** Selective classification, human review triage, deferral, and decision oversight.
  4. **Evaluation & Verification Phase:** Model explanation auditing, counterfactual testing, and domain sanity checks.
- **Data & Experiments:** Exhaustive survey reviewing over 200 papers spanning healthcare, autonomous vehicles, cybersecurity, and natural language processing.
- **Main Results:**
  1. Formulates the core trade-off in HITL: maximizing human expertise utilization while minimizing human cognitive fatigue and operational cost.
  2. Identified the *inference triage phase*—routing high-risk, ambiguous automated decisions to humans—as the most critical safeguard for production safety.
  3. Proved that unconstrained alert feeds overwhelm human operators, necessitating cost-aware triage algorithms.
- **Limitations:** Broad architectural survey; does not implement or benchmark a specific mathematical triage algorithm; qualitative rather than empirical.
- **Relevance to My Project:** Provides the structural taxonomy positioning our project within the **Inference & Decision Phase of HITL**. It validates our motivation: automating 95%–99% of routine flow decisions while reserving human scrutiny for high-risk, high-uncertainty alerts.
- **2-Line Slide Summary:** Comprehensive taxonomy of Human-in-the-Loop machine learning across the lifecycle. Formally positions our triage mechanism within the inference-time decision phase to mitigate human alert fatigue.
- **20-Second Spoken Version:** *"Mosqueira-Rey et al. in AI Review 2023 established that human-in-the-loop systems must optimize human attention at inference time. Our project implements exactly this by triage-filtering network flows within 1% to 10% review limits."*
- **Panel Question & Answer:**
  - *Panel Question:* "Where does your system sit in Mosqueira-Rey's taxonomy?"
  - *Answer:* "Our project sits precisely in the Inference and Decision Phase of HITL. We do not use humans to label training data (active learning); we use human review capacity at inference time to catch high-risk production errors."

---

### [14] Hendrickx, Perini, Van der Plas, Meert, & Davis (2024) — Machine Learning with a Reject Option: A Survey

- **Citation (IEEE):** K. Hendrickx, L. Perini, D. Van der Plas, Wannes Meert, and J. Davis, "Machine learning with a reject option: a survey," *Machine Learning*, vol. 113, no. 5, pp. 3073–3110, 2024, doi: 10.1007/s10994-024-06534-x.
- **Indexing:** **Scopus Indexed** (Published in the premier Springer journal *Machine Learning*, Q1, Scopus indexed).
- **Problem:** Machine learning with a reject option (MLRO) allows classifiers to abstain on hard instances. The field had diverged into distinct silos using incompatible definitions, assumptions, and evaluation metrics, without distinguishing between different reasons for rejection.
- **Core Idea / Method:** Establishes the foundational distinction between two core types of rejection:
  1. **Ambiguity Rejection:** Abstaining because the instance lies close to the decision boundary between classes (epistemic/aleatoric uncertainty in high-density regions).
  2. **Novelty Rejection:** Abstaining because the instance lies in an unexplored, low-density region of feature space (out-of-distribution or novelty).
  Categorizes architectures into: (a) plug-in / post-hoc rejection rules over standard models, and (b) integrated models trained end-to-end with rejection penalties. Reviews evaluation via accuracy-rejection curves.
- **Data & Experiments:** Surveys and cross-evaluates methods across benchmark tabular and image datasets, comparing cost-based metrics and budget-based rejection.
- **Main Results:**
  1. Proved that single-signal reject rules fail because ambiguity rejection mechanisms cannot detect novelty, and novelty detectors cannot resolve boundary ambiguity.
  2. Concluded that multi-factor rejection combining ambiguity and novelty provides strictly superior Pareto frontiers.
  3. Identified post-hoc plug-in rejection methods as the most practical for industrial deployment because they do not require retraining complex production models.
- **Limitations:** Focuses on theoretical rejection mechanisms; assumes deferred instances receive a cost penalty or are dropped; does not implement continuous feedback loops or evaluate on massive NetFlow datasets.
- **Relevance to My Project:** **This is the single most important foundational survey supporting our framework.** Hendrickx proves that rejection must combine *ambiguity* (our Confidence signal) and *novelty* (our OOD signal). Our project directly operationalizes their theoretical recommendation for network flow data.
- **2-Line Slide Summary:** Premier survey formalizing the distinction between ambiguity rejection and novelty rejection. Validates our core architectural decision to synthesize prediction uncertainty and OOD distance into a unified triage mechanism.
- **20-Second Spoken Version:** *"Hendrickx et al. in 2024 proved that effective rejection requires combining ambiguity rejection (confidence) with novelty rejection (OOD). This is the exact theoretical justification for our multi-factor triage design."*
- **Panel Question & Answer:**
  - *Panel Question:* "How does Hendrickx's taxonomy map to your four reliability signals?"
  - *Answer:* "Hendrickx distinguishes ambiguity rejection from novelty rejection. In our system, Prediction Uncertainty captures ambiguity rejection, while Mahalanobis OOD distance captures novelty rejection. Our framework unifies both into a single composite risk queue."

---

### [15] Sarhan, Layeghy, & Portmann (2022) — Towards a Standard Feature Set for NIDS Datasets

- **Citation (IEEE):** M. Sarhan, S. Layeghy, and M. Portmann, "Towards a Standard Feature Set for Network Intrusion Detection System Datasets," *Mobile Netw. Appl.*, vol. 27, no. 1, pp. 357–370, 2022, doi: 10.1007/s10776-021-00543-6.
- **Indexing:** **Scopus Indexed** (Mobile Networks and Applications, Springer, Q1, Scopus indexed).
- **Problem:** Machine learning-based NIDS research suffered from severe reproducibility and generalizability crises because every academic dataset (KDD99, UNSW-NB15, BoT-IoT, CIC-IDS2018) extracted proprietary, mutually incompatible feature sets. Models trained on one dataset could never be evaluated or transferred to another.
- **Core Idea / Method:** Proposes the **NetFlow Standard Feature Set (NF-v1 and NF-v2)** comprising 43 standardized NetFlow features extractable directly from standard network flow monitors (e.g., nProbe, Cisco NetFlow). They convert four major benchmark datasets (UNSW-NB15, ToN-IoT, BoT-IoT, CSE-CIC-IDS2018) into a unified NetFlow format and benchmark machine learning classifiers across all four.
- **Data & Experiments:** Evaluated on the standardized datasets (NF-UNSW-NB15, NF-ToN-IoT, NF-BoT-IoT, NF-CSE-CIC-IDS2018) using Decision Trees, Random Forests, and Extra Trees classifiers. Evaluated cross-dataset transferability and inference latency.
- **Main Results:**
  1. Standardized NetFlow features preserved or improved intrusion classification performance (F1 scores > 0.95 across most attack families) compared to proprietary feature sets.
  2. Enabled true cross-dataset benchmarking across distinct research testbeds for the first time.
  3. Proved that flow-level attributes (packet lengths, inter-arrival times, TCP flags) provide sufficient discriminative power for modern anomaly detection without full payload inspection.
- **Limitations:** Evaluated stationary test sets per testbed; did not create a unified multi-million flow benchmark or evaluate temporal distribution shift across concatenated multi-year traffic.
- **Relevance to My Project:** Provides the direct technical lineage for our dataset. BigFlow-NIDS (Uddin et al. [16]) directly adopted Sarhan's standardized NetFlow feature representation to construct its 66.9-million flow repository.
- **2-Line Slide Summary:** Establishes a standardized 43-attribute NetFlow feature representation across major NIDS datasets. Provides the foundational feature schema adopted by BigFlow-NIDS and utilized in our 49-feature formulation.
- **20-Second Spoken Version:** *"Sarhan et al. created the standardized NetFlow feature format for intrusion detection, solving dataset incompatibility. BigFlow-NIDS was built on this exact standard, which provides our 49 flow features."*
- **Panel Question & Answer:**
  - *Panel Question:* "Why did you use 49 numerical features instead of Sarhan's 43 NetFlow features?"
  - *Answer:* "BigFlow-NIDS expands Sarhan's schema with 6 additional aggregated flow statistics (totaling 55 attributes). From those 55, we exclude non-predictive IP addresses, ports, timestamps, and the detailed Attack name column, leaving exactly 49 clean numerical flow features."

---

### [16] (Dataset Benchmark) Uddin, Arefin, & Hussain (2026) — BigFlow-NIDS: A Large-Scale Benchmark Dataset

- **Citation (IEEE):** M. B. Uddin, M. S. Arefin, and M. M. M. Hussain, "BigFlow-NIDS: A large-scale dataset for network intrusion detection in big data environment," *Data in Brief*, vol. 65, Art. no. 112530, pp. 1–11, Feb. 2026, doi: 10.1016/j.dib.2026.112530.
- **Indexing:** **Scopus Indexed** (Elsevier's *Data in Brief*, Scopus indexed, open-access peer-reviewed data journal).
- **Problem:** Existing network intrusion detection datasets are either too small, outdated, synthetically generated in narrow laboratory testbeds, or lack the volume required to simulate authentic big-data streaming pipelines in modern enterprise networks.
- **Core Idea / Method:** Constructs **BigFlow-NIDS**, an industrial-scale benchmark harmonizing four major NetFlow datasets (NF-UNSW-NB15, NF-ToN-IoT, NF-BoT-IoT, NF-CSE-CIC-IDS2018) via Apache Spark. Contains **66,935,021 flows** across **55 flow attributes** and **32 distinct attack categories**, available in both CSV and high-speed columnar Parquet formats.
- **Data & Experiments:** Profiles class distribution: 36,634,800 benign flows (54.7%) and 30,300,221 attack flows (45.3%). Documents Spark processing pipelines, parquet query latency improvements (27.35 seconds vs. 920.82 seconds for CSV), and baseline random forest benchmarks.
- **Main Results:**
  1. Created the largest unified, standardized NetFlow intrusion detection benchmark in open literature (66.9M flows).
  2. Documented significant temporal variations in attack prevalence across concatenated collection periods.
  3. Established a realistic foundation for scalable, distributed big-data intrusion detection research.
- **Limitations:** Benchmark dataset publication; authors do not evaluate human-review allocation, out-of-distribution triage, or selective classification.
- **Relevance to My Project:** **The primary empirical data source for our capstone.** We extracted a verified 500,000-flow chronological sample from BigFlow-NIDS, validated against the raw 14GB source via SHA-256 fingerprinting.
- **2-Line Slide Summary:** The 2026 primary benchmark dataset harmonizing 66.9M network flows across 55 attributes and 32 attack families. Source of our verified 500,000-flow chronological evaluation split.
- **20-Second Spoken Version:** *"Uddin et al. published BigFlow-NIDS in February 2026 in Data in Brief, harmonizing 66.9 million network flows. We sampled 500,000 chronological flows from this verified benchmark for our experiments."*
- **Panel Question & Answer:**
  - *Panel Question:* "Is BigFlow-NIDS live Internet traffic captured by you?"
  - *Answer:* "No, sir. BigFlow-NIDS is a peer-reviewed 2026 research benchmark harmonizing public NetFlow testbeds. Using an established benchmark ensures our 4.55x error surge and strategy comparisons are 100% reproducible and verifiable."

---

## Section A: Related-Work Mapping Table & Research Gap

### Comprehensive Literature Mapping Table

| Paper Citation | Indexed In | Conf. Signal | OOD Signal | PSI Drift | Hist. Errors | Budget Slicing | Temporal Shift | NIDS Context |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **[1] Cao et al. (ICCV 2023)** | IEEE & Scopus | | **✓** | | | | **✓** | |
| **[2] Mozannar & Sontag (ICML 2020)** | PMLR (Top AI)* | **✓** | | | | | | |
| **[3] Wei et al. (ICML 2024)** | PMLR (Top AI)* | | | | | **✓** (Efficiency) | | |
| **[4] Geifman & El-Yaniv (NeurIPS 2017)** | Scopus Series | **✓** | | | | | | |
| **[5] Guo et al. (ICML 2017)** | PMLR (Top AI)* | **✓** (Calibration) | | | | | | |
| **[6] Kim et al. (IEEE TIFS 2024)** | IEEE & Scopus | | | | | **✓** | | **✓** |
| **[7] Liu et al. (Sci. Rep. 2022)** | Scopus (Q1) | **✓** (Uncertainty) | | | | | | |
| **[8] Yang et al. (IJCV 2024)** | Scopus (Q1) | | **✓** | | | | **✓** | |
| **[9] Koh et al. (ICML 2021)** | PMLR (Top AI)* | | | | | | **✓** (Benchmark) | |
| **[10] He et al. (IEEE COMST 2023)** | IEEE & Scopus | | | | | | | **✓** (Adversarial) |
| **[11] Lu et al. (IEEE TKDE 2019)** | IEEE & Scopus | | | **✓** (Drift Review) | **✓** (Error Mon.) | | **✓** | |
| **[12] Iwashita & Papa (IEEE Access 2019)** | IEEE & Scopus | | | **✓** (Concept Drift) | | | **✓** | |
| **[13] Mosqueira-Rey et al. (AI Rev. 2023)**| Scopus (Q1) | | | | | **✓** (HITL Tax.) | | |
| **[14] Hendrickx et al. (Mach. Learn. 2024)**| Scopus (Q1) | **✓** (Ambiguity) | **✓** (Novelty) | | | **✓** (Reject Opt.) | | |
| **[15] Sarhan et al. (MNA 2022)** | Scopus (Q1) | | | | | | | **✓** (NetFlow) |
| **[16] Uddin et al. (Data in Brief 2026)** | Scopus | | | | | | **✓** (Benchmark) | **✓** (BigFlow) |
| **OUR PROPOSED FRAMEWORK** | **Capstone** | **✓ (Signal 1)** | **✓ (Signal 2)** | **✓ (Signal 3)** | **✓ (Signal 4)** | **✓ (1%–10%)** | **✓ (Chrono 4.55x)**| **✓ (500K NetFlow)**|

*\*All PMLR-only papers have verified IEEE equivalents documented in the deck and notes.*

### The Five-Sentence Research Gap

1. Existing selective classification frameworks [4], [5] rely strictly on prediction confidence, which fails silently under temporal distribution shift because modern classifiers remain overconfident even when error rates surge.
2. Out-of-distribution detection techniques [1], [8] successfully identify statistical feature novelty, but novelty in high-throughput network environments frequently corresponds to benign high-volume transfers rather than true classification errors.
3. While literature on concept drift [11], [12] and adversarial vulnerabilities [10] highlights macroscopic model degradation, these approaches track population aggregates without providing per-instance risk scoring for operational triage.
4. Furthermore, learning-to-defer formulations [2], [3], [7], [14] theoretically model expert handoffs under abstract cost penalties but fail to model strict top-$K$ operational review quotas (e.g., exactly 1% or 2% human capacity) under genuine temporal shift.
5. **Our project fills this exact gap:** we build a unified, post-hoc triage framework synthesizing prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake proximity to optimize error interception under explicit operational capacity constraints.

---

## Section B: How the Papers Connect (150-Word Viva Story)

> *"Modern deep classifiers are severely miscalibrated and overconfident, as proven by Guo et al. Consequently, when Geifman's confidence-based selective prediction is deployed in non-stationary environments, it fails silently because models make confident mistakes under temporal shift. While Yang and Cao propose Out-of-Distribution detection to catch shifts, our experiments confirm that feature novelty alone does not correlate with classification errors in network security. Meanwhile, Lu and Iwashita demonstrate that tracking macroscopic feature drift and error feedback is necessary to detect emerging degradation. Hendrickx's premier survey proves that effective rejection must combine ambiguity and novelty, while Mozannar, Wei, and Liu formalize learning-to-defer to human experts. Finally, Kim and Mosqueira-Rey show that human attention in cybersecurity operations is strictly constrained by alert fatigue. Our project unifies these separate threads: we combine uncertainty, OOD distance, PSI drift, and historical mistake patterns into an adaptive triage mechanism that maximizes error interception under strict 1% to 2% operational human review budgets."*

---

## Section C: Technical Glossary (15 Terms)

1. **Distribution Shift:** A change in the joint probability distribution of inputs and outputs between training ($P_{train}(X, Y)$) and testing ($P_{test}(X, Y)$).
2. **Covariate Shift:** A specific distribution shift where the input feature distribution changes ($P_{train}(X) \neq P_{test}(X)$), but the true underlying relationship between features and labels remains identical ($P(Y|X)$ is constant).
3. **Concept Drift:** A change in the conditional probability distribution $P(Y|X)$, meaning that identical feature vectors produce different ground-truth classifications over time.
4. **Population Stability Index (PSI):** A binned statistical metric measuring the shift in a feature's distribution between a reference and target population: $\text{PSI} = \sum (Actual\% - Expected\%) \times \ln(Actual\% / Expected\%)$. Values $\ge 0.10$ indicate moderate drift; values $\ge 0.25$ indicate severe drift.
5. **Mahalanobis Distance:** A scale-invariant, multivariate distance metric measuring how many standard deviations an instance $x$ is from the center $\mu$ of a distribution, incorporating the covariance matrix $\Sigma$: $D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)}$.
6. **Model Calibration:** The degree to which a classifier's predicted confidence probability matches its true empirical likelihood of correctness (e.g., predictions with 90% confidence are correct 90% of the time).
7. **Selective Classification (Reject Option):** A classification paradigm where a model is equipped with a selection function allowing it to abstain/reject making a prediction on instances with low confidence or high risk.
8. **Learning to Defer (L2D):** A human-AI collaboration framework where a classifier jointly learns when to make an autonomous decision and when to transfer decision authority to a human expert.
9. **Active Learning:** A machine learning paradigm where the algorithm actively selects the most informative unlabeled instances to query a human oracle for annotations.
10. **Validation ROC-AUC:** The Area Under the Receiver Operating Characteristic curve evaluated on validation data, measuring the classifier's ability to rank true positive instances above false positive instances regardless of threshold.
11. **Error Capture Rate:** The percentage of all model prediction mistakes that are successfully intercepted and reviewed by the human triage queue: $(\text{Errors in Review Queue} / \text{Total Model Errors}) \times 100$.
12. **Review Efficiency:** The density of errors intercepted per unit of human review effort, standardized as errors caught per 1,000 human reviews: $(\text{Errors Caught} / \text{Reviews Completed}) \times 1,000$.
13. **Ambiguity Rejection:** Abstaining on an instance because it lies close to the classification decision boundary between overlapping classes.
14. **Novelty Rejection:** Abstaining on an instance because its feature values fall outside the support of the training distribution (Out-of-Distribution).
15. **NetFlow:** A network protocol standard that aggregates raw packet streams into summary session flows containing attributes like duration, bytes, packet counts, TCP flags, and inter-arrival times without inspecting packet payload data.

---

## Section D: 10 Tough Viva Questions & Bulletproof Answers

#### Q1: "Why did you choose a multi-factor combination instead of simply retraining your model when drift was detected?"
**Answer:** Retraining is an offline, delayed batch process requiring newly collected, manually labeled ground-truth data, which takes days or weeks to curate in a SOC. Our triage mechanism operates in real time at inference time. It immediately protects the organization on the very first day of distribution shift by routing high-risk decisions to human analysts before retraining is even feasible.

#### Q2: "In your results, why did pure Confidence beat your Feedback Adaptive strategy at 5% and 10% review budgets?"
**Answer:** This is an honest and defensible empirical finding. Multi-factor triage focuses specifically on high-risk, drifted outliers and historical mistake clusters. At tight budgets (1% and 2%), this targeted triage intercepts significantly more errors than confidence (up to 34.26% vs 26.73%). However, at 5% and 10% budgets, the review capacity is broad enough to audit the entire decision boundary, where pure confidence ranking naturally excels. This proves that review strategy selection must be matched to operational review capacity.

#### Q3: "Your OOD-only strategy captured only 0.03% of errors at a 1% budget, which is worse than random audit. Is that a bug?"
**Answer:** No, sir. We thoroughly investigated this. In network flow data, extreme Mahalanobis outliers correspond to high-bandwidth file transfers, large MTU packets, and atypical benign protocols. These instances are statistically rare in feature space, but XGBoost classifies them correctly. In fact, Decile 9 of OOD distance contained only 12 errors (0.16% error rate), while Decile 7 contained 1,799 errors. This proves a vital scientific finding: in network security, feature novelty does not equal classification error.

#### Q4: "Guo et al. introduced Temperature Scaling. Why didn't you just temperature-scale your XGBoost probabilities to fix overconfidence?"
**Answer:** Guo et al. showed that temperature scaling calibrates probabilities on stationary in-distribution data. However, temperature scaling applies a global scalar to logits and does not alter the relative ranking of instances. Under distribution shift, high-confidence errors remain high-confidence relative to other instances, meaning temperature scaling alone cannot reorder triage queues without external signals like PSI drift and OOD distance.

#### Q5: "How are the weights determined in your multi-factor strategy? Are they learned or heuristic?"
**Answer:** In Phase 1, our weights are experimentally defined heuristics (e.g., 50% uncertainty + 50% OOD percentile in static multi-factor; regime-based scaling where feature drift increases the historical mistake weight). We do not claim these weights are globally optimal. In Phase 2, we have explicitly planned bilevel optimization to learn optimal routing policies directly from cost matrices.

#### Q6: "Why is the validation Precision and F1-score of your base XGBoost model so low (Precision = 0.04, F1 = 0.05)?"
**Answer:** The validation split reflects extreme class imbalance: only 248 attacks out of 75,000 flows (a 0.33% attack prevalence). With such severe imbalance, any standard decision threshold produces false positives that mathematically depress precision. However, XGBoost achieves a **validation ROC-AUC of 0.9228**, proving strong discriminative ranking power. More importantly, our project’s objective is not to build a standalone perfect classifier, but to allocate human review to intercept the inevitable errors.

#### Q7: "How did you ensure there was no data leakage across your splits?"
**Answer:** We strictly enforced chronological splitting: 350,000 early flows for training, the next 75,000 flows for validation, and the final 75,000 flows for shifted testing. All preprocessing parameters (StandardScaler, median imputation), baseline covariance matrices for Mahalanobis OOD distance, and historical mistake bins were fitted exclusively on training data without access to shifted test labels.

#### Q8: "How does your work differ from Mozannar & Sontag’s Learning to Defer?"
**Answer:** Mozannar & Sontag formulate learning-to-defer by altering the training loss function of the base model under a fixed, constant deferral cost, assuming stationary data. Our approach is a post-hoc triage layer operating over an existing model under temporal distribution shift, and we enforce explicit capacity budgets (1%, 2%, 5%, 10%) rather than an unconstrained deferral cost.

#### Q9: "Why did you use BigFlow-NIDS instead of generating synthetic drift or capturing live campus traffic?"
**Answer:** BigFlow-NIDS is a peer-reviewed 2026 benchmark harmonizing 66.9 million network flows. Using a published benchmark guarantees that our 4.55x error surge, 753 validation errors, and 3,427 shifted test errors are 100% reproducible and verifiable by external researchers. Live campus network captures lack ground-truth attack labels and would prevent objective evaluation against error counts.

#### Q10: "What is your concrete Phase-2 plan?"
**Answer:** In Phase 2, we will deliver: (1) Cross-domain evaluation on medical (MIMIC) and financial tabular datasets to prove domain generality; (2) Conformal prediction to provide distribution-free confidence guarantees; (3) SHAP explainability attached to routed alerts so analysts understand why a case was flagged in under 10 seconds; and (4) An interactive Streamlit dashboard allowing administrators to dynamically adjust budget sliders.
