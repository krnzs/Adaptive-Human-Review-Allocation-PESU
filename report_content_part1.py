"""
PES UNIVERSITY - DEPARTMENT OF COMPUTER APPLICATIONS
MCA CAPSTONE PROJECT 2025-27 - PHASE I REVIEW II REPORT
SECTION CONTENT DEFINITIONS: PART 1 (SECTIONS 1 TO 8)
"""

import os

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"

def get_part1_content():
    content = {}

    # =========================================================================
    # SECTION 1: ABSTRACT
    # =========================================================================
    content["1. Abstract"] = [
        ("p",
         "Machine learning (ML) models deployed in high-throughput data processing environments—such as network intrusion detection, financial transaction monitoring, and clinical screening—inevitably experience performance degradation due to temporal distribution shifts. In these operational settings, human-review capacity is strictly constrained by operational overhead, analyst workload, and economic cost. This study models capacity-constrained operational inspection environments using discrete 1%, 2%, 5%, and 10% review budgets. Existing selective classification frameworks prioritize audit queues relying almost exclusively on model output probabilities (confidence). However, complex classifiers frequently exhibit uncalibrated confidence under covariate and concept shift, resulting in misclassifications that maintain high posterior probabilities and bypass conventional confidence-based safety filters.",
         None, False),
        ("p",
         "This project presents an adaptive, multi-factor human-review allocation framework designed to evaluate capacity-constrained error mitigation under distribution shift. The framework synthesizes four complementary reliability signals: (1) prediction uncertainty derived from normalized probabilities, (2) regularized Mahalanobis distance to capture geometric out-of-distribution (OOD) feature novelty, (3) Population Stability Index (PSI) to track macroscopic batch distribution drift, and (4) empirical historical error proximity mapped from validation error neighborhoods. The resulting composite risk score ranks inferences into a prioritized review queue, with a heuristic feedback mechanism adjusting signal weighting based on verified audit error density.",
         None, False),
        ("p",
         "The proposed methodology is empirically evaluated on a 500,000-flow chronological partition from the large-scale BigFlow-NIDS benchmark (66.9 million total flows, 55 attributes), partitioned into 350,000 training, 75,000 validation, and 75,000 shifted-test instances. BigFlow-NIDS is a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets. Under temporal shift, classifier error rate surges 4.55x from 1.004% (753 errors) on validation to 4.569% (3,427 errors) on shifted test. In offline benchmarking with a simulated ground-truth review oracle, the adaptive multi-factor allocation strategy captures 17.80% of total shifted errors (610 errors) at a 1% review budget (versus 13.51% / 463 errors for pure confidence) and 34.26% of errors (1,174 errors) at a 2% budget (versus 26.73% / 916 errors for pure confidence). Crucially, empirical findings reveal an honest budget-dependent crossover: while multi-factor allocation achieves higher error capture under tight review constraints (1%–2%), pure confidence ranking achieves higher error capture at broader budgets (5%–10%), capturing 65.45% and 84.01% of errors respectively. To date, 13 of 14 functional requirements (13 of 14 requirements complete (93%)) have been fully implemented across 26 sequential Python scripts, supported by an interactive local Streamlit exploratory analytics dashboard.",
         None, False)
    ]

    # =========================================================================
    # SECTION 2: INTRODUCTION
    # =========================================================================
    content["2. Introduction"] = [
        ("p",
         "The deployment of machine learning algorithms in operational systems has expanded from advisory tools to automated decision infrastructure. Across enterprise cybersecurity, payment networks, and healthcare diagnostics, automated decision systems process large streams of transactions and network events daily. However, the foundational statistical assumption governing supervised machine learning—that training and operational test data are independent and identically distributed (i.i.d.)—is routinely challenged in real-world deployments. Network traffic patterns evolve, threat actors adapt evasion strategies, and operational infrastructure changes over time, introducing substantial covariate and concept drift.",
         None, False)
    ]

    content["2.1 Problem Scenario"] = [
        ("p", "In production security operations and high-volume data streams, machine learning systems face two primary operational challenges:", "The Operational Bottleneck: ", False),
        ("bullet", "Human analysts have finite cognitive and temporal bandwidth. This study models constrained human-review capacity using discrete 1%, 2%, 5%, and 10% review budgets to evaluate triage efficiency under finite operational inspection quotas.", "Capacity Constraints: "),
        ("bullet", "Complex classifiers (including gradient boosted decision trees) frequently output poorly calibrated probabilities. Under temporal distribution shift, model error rate surges 4.55-fold (from 1.004% to 4.569%) while prediction confidence remains high, causing misclassifications that traditional confidence thresholding fails to prioritize.", "Reduced Reliability Under Shift: "),
        ("bullet", "In the absence of principled triage, teams often resort to uniform random auditing or static confidence thresholding. In our empirical evaluations, random sampling captured only 1.17% of shifted-test errors at a 1% budget and 2.13% at a 2% budget (matching proportional sampling), rendering it ineffective as a safety mechanism.", "Inefficacy of Naive Audits: "),
        ("bullet", "Standard Out-of-Distribution (OOD) detectors identify geometric feature novelty, but novelty in network traffic frequently corresponds to benign high-volume transfers rather than classification errors. In our experiments, OOD-only filtering captured a dismal 0.03% of shifted errors at 1% budget (1 error out of 3,427) and 0.26% at 2% budget (9 errors), performing substantially worse than random guessing.", "Failure of Isolated Signals: ")
    ]

    content["2.2 Proposed Solution"] = [
        ("p", "To address these limitations, this project designs, implements, and evaluates an Adaptive Human-Review Allocation Framework. Rather than relying on any single failure indicator, the system unifies four heterogeneous, complementary reliability signals into a composite risk score:", "Multi-Signal Reliability Engine: ", False),
        ("bullet", "Quantifies classifier uncertainty derived from class posterior probabilities, scaled inversely such that borderline predictions receive higher inspection priority: U_i = 1 - max(P, 1-P).", "1. Prediction Uncertainty (Confidence Risk): "),
        ("bullet", "Computes regularized Mahalanobis distance from training feature centroids in numerical representation space, capturing semantic and geometric feature divergence.", "2. Out-of-Distribution (OOD) Distance: "),
        ("bullet", "Tracks macroscopic population-level feature drift across chronological batches using the Population Stability Index (PSI), projecting batch drift into per-instance vulnerability scores.", "3. Feature Drift Magnitude: "),
        ("bullet", "Maps test instances into historical feature deciles to assess whether incoming records resemble training-set mistake clusters.", "4. Historical Error Proximity: "),
        ("p", "The composite risk score ranks all incoming inferences into a prioritized review queue. The top-K instances corresponding exactly to the designated operational capacity budget (K = floor(B * N) for B in {1%, 2%, 5%, 10%}) are routed to the review queue. Furthermore, a heuristic feedback loop adjusts signal weights based on verified audit error concentrations, optimizing subsequent triage batches.", None, False)
    ]

    content["2.3 Purpose"] = [
        ("p", "The primary purpose of this research is to investigate whether multi-factor reliability scoring improves error capture over pure confidence ranking under tight operational budgets (1%–2%) in the presence of distribution shift. Specifically, the project aims to:", "Research Objectives: ", False),
        ("bullet", "Empirically evaluate whether multi-factor reliability scoring improves error capture over pure confidence ranking under tight operational review budgets (1%–2%)."),
        ("bullet", "Investigate the empirical relationship between selective classification (confidence ranking), representation-space OOD distance, macroscopic drift metrics, and true model errors under temporal shift."),
        ("bullet", "Provide a fully reproducible, modular software pipeline that production teams can evaluate to triage high-throughput tabular classifiers without requiring model retraining or architectural redesign.")
    ]

    content["2.4 Scope"] = [
        ("p", "To ensure scientific rigor and clear engineering execution, the project scope is formally demarcated between completed Phase-I deliverables and planned Phase-II extensions:", "Phase Boundary Delineation: ", False),
        ("bullet", "Evaluation conducted on a 500,000-flow chronological partition of the BigFlow-NIDS benchmark (a large-scale derived network intrusion detection benchmark constructed from publicly available NetFlow datasets); binary classification (0 = Benign, 1 = Attack); 49 numerical flow features; three baseline classifiers (Logistic Regression, Random Forest, XGBoost); offline simulated review oracle using test ground truth for reproducible benchmarking; four discrete review budgets (1%, 2%, 5%, 10%); local Streamlit exploratory analytics dashboard.", "In-Scope (Phase-I Implemented): "),
        ("bullet", "Live network packet capture / inline hardware sniffing; real human subjects in the loop (ground-truth labels were used as a simulated review oracle for reproducible benchmarking; no real human subjects participated in Phase-I); multi-class attack categorization (the detailed 32-class attack column was excluded to eliminate label leakage); automated bilevel optimization of signal weights (heuristic feedback-based weighting evaluated).", "Out-of-Scope (Phase-I): "),
        ("bullet", "Cross-domain tabular generalization across financial fraud and clinical datasets; post-hoc probability calibration (Temperature Scaling); SHAP-based feature attribution for human-audited cases; full production-grade web application with multi-user authentication.", "Planned Scope (Phase-II): ")
    ]

    # =========================================================================
    # SECTION 3: REVIEW-I RECOMMENDATIONS
    # =========================================================================
    content["3. Review-I Recommendations and Action Taken"] = [
        ("p", "During the Phase-I Review-I evaluation, the capstone review panel provided critical constructive feedback regarding dataset selection, baseline formulation, and engineering reproducibility. Table 3.1 details each recommendation received and the specific concrete actions taken in Review-II to address them.", None, False),
        ("builtin_table", 0,
         ["Sl No", "Review-I Recommendation", "Action Taken", "Status"],
         [
             ["1",
              "Clearly define the scope of distribution shift and select a realistic, large-scale benchmark dataset rather than synthetic perturbations.",
              "Replaced synthetic shifts with the authentic BigFlow-NIDS benchmark (66.9M flows, 55 attributes). Implemented strict chronological 70/15/15 partitioning (350K train, 75K validation, 75K shifted test), creating a genuine 4.55x error rate surge and 19.05x attack prevalence shift.",
              "Addressed"],
             ["2",
              "Formulate a quantitative baseline for human review capacity constraints instead of assuming arbitrary deferral rates.",
              "Formally defined four operational budget tiers (1%, 2%, 5%, 10% of total inference volume). Benchmarked allocation strategies strictly against these realistic operational inspection quotas.",
              "Addressed"],
             ["3",
              "Incorporate multiple failure indicators beyond pure model confidence, as classifiers are known to be overconfident.",
              "Engineered four orthogonal reliability signals: prediction uncertainty, regularized Mahalanobis OOD distance, Population Stability Index (PSI) drift, and historical mistake decile proximity.",
              "Addressed"],
             ["4",
              "Demonstrate complete reproducibility and modularity across the data science pipeline.",
              "Architected 26 sequentially numbered, standalone Python scripts in src/. Verified deterministic execution with fixed random seeds (seed=42) and SHA-256 data checksums. Implemented an interactive Streamlit dashboard.",
              "Addressed"]
         ],
         [0.6, 2.2, 3.0, 0.9])
    ]

    # =========================================================================
    # SECTION 4: DETAILED LITERATURE SURVEY (10 PAPERS)
    # =========================================================================
    content["4. Detailed Literature Survey"] = [
        ("p", "A rigorous, comprehensive literature survey was conducted across 10 foundational research papers published in premier peer-reviewed venues, including IEEE Transactions, CVF/IEEE conferences, ACM/PMLR proceedings, and Nature Springer journals. Each paper is systematically analyzed across eleven standardized dimensions to extract theoretical principles, empirical benchmarks, and recurring methodological limitations.", None, False)
    ]

    # 4.1 Cao et al.
    content["4.1 Research Paper 1"] = [
        ("p", "Anomaly Detection Under Distribution Shift", "Paper Title: ", False),
        ("p", "T. Cao, J. Zhu, and G. Pang", "Authors: ", False),
        ("p", "2023", "Publication Year: ", False),
        ("p", "IEEE/CVF International Conference on Computer Vision (ICCV 2023), pp. 6511–6523. IEEE & Scopus Indexed.", "Journal / Conference / Publisher: ", False),
        ("p", "https://doi.org/10.1109/ICCV51070.2023.00599", "DOI / URL: ", False),
        ("p", "Addresses the degradation of anomaly detection models when operational test environments exhibit covariate and semantic distribution shift relative to training data, causing high false alarm rates.", "Research Problem: ", False),
        ("p", "Proposes an unsupervised domain alignment framework combining dual-memory contrastive feature learning with distribution discrepancy minimization to isolate genuine anomalies from domain shift variations.", "Method / Model / Approach: ", False),
        ("p", "Evaluated across multiple visual benchmark datasets including shifted CIFAR-10-C, ImageNet-C, and industrial defect detection benchmarks exhibiting diverse noise and corruption shifts.", "Dataset Used: ", False),
        ("p", "Demonstrates that naive anomaly detectors experience an average ROC-AUC drop of over 24% under domain shifts. The proposed domain-alignment strategy mitigates false positive alarms by 38.5% across shifted benchmarks.", "Key Findings: ", False),
        ("p", "Focuses predominantly on high-dimensional computer vision representations; does not address capacity-constrained human audit queues or offline tabular network security data.", "Limitations: ", False),
        ("p", "Directly justifies our temporal evaluation protocol on BigFlow-NIDS and reinforces the core premise that distribution shift causes severe baseline failure in anomaly detection.", "Relevance to Proposed Project: ", False)
    ]

    # 4.2 Mozannar & Sontag
    content["4.2 Research Paper 2"] = [
        ("p", "Consistent Estimators for Learning to Defer to an Expert", "Paper Title: ", False),
        ("p", "H. Mozannar and D. Sontag", "Authors: ", False),
        ("p", "2020", "Publication Year: ", False),
        ("p", "Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR vol. 119, pp. 7076–7087. Top-tier ML Conference.", "Journal / Conference / Publisher: ", False),
        ("p", "https://proceedings.mlr.press/v119/mozannar20b.html", "DOI / URL: ", False),
        ("p", "Investigates human-AI collaborative decision-making, addressing the lack of statistically consistent surrogate loss functions for jointly learning a classifier and a deferral policy to a human expert.", "Research Problem: ", False),
        ("p", "Formulates learning-to-defer as an extended (K+1)-class classification problem with a rejection option, proving the Bayes consistency of a novel softmax surrogate loss function.", "Method / Model / Approach: ", False),
        ("p", "Evaluated on synthetic mixture models, synthetic medical diagnosis benchmarks, and CheXpert chest X-ray datasets with simulated expert error profiles.", "Dataset Used: ", False),
        ("p", "Proves that conventional two-stage deferral (thresholding confidence) is theoretically inconsistent. Joint learning reduces system-wide error by 14% to 22% compared with isolated classification.", "Key Findings: ", False),
        ("p", "Assumes stationary, unshifted data distributions and models deferral cost as an unconstrained penalty parameter rather than operating under strict, hard capacity quotas (e.g., exactly 1% or 2% budget).", "Limitations: ", False),
        ("p", "Provides the foundational theoretical motivation for delegating uncertain predictions to human experts, which our framework adapts into an operational, budget-constrained setting.", "Relevance to Proposed Project: ", False)
    ]

    # 4.3 Wei et al.
    content["4.3 Research Paper 3"] = [
        ("p", "Exploiting Human-AI Dependence for Learning to Defer", "Paper Title: ", False),
        ("p", "Z. Wei, Y. Cao, and L. Feng", "Authors: ", False),
        ("p", "2024", "Publication Year: ", False),
        ("p", "Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR vol. 235, pp. 52410–52431. Top-tier ML Conference.", "Journal / Conference / Publisher: ", False),
        ("p", "https://proceedings.mlr.press/v235/wei24c.html", "DOI / URL: ", False),
        ("p", "Addresses the oversimplified assumption in learning-to-defer literature that expert accuracy is conditionally independent of machine prediction errors given the input features.", "Research Problem: ", False),
        ("p", "Develops a dependent human-AI deferral architecture incorporating conditional dependency modeling via a joint bivariate distribution estimator.", "Method / Model / Approach: ", False),
        ("p", "Evaluated on CIFAR-100 image classification with synthetic noisy human annotators and HateSpeech text detection benchmarks with real human annotator labels.", "Dataset Used: ", False),
        ("p", "Demonstrates that modeling human-AI error correlation prevents redundant expert routing, improving joint human-machine accuracy by up to 8.4% over conditionally independent baselines.", "Key Findings: ", False),
        ("p", "Requires paired human-machine labels during training, making it inapplicable to post-hoc deployment on pre-trained black-box models.", "Limitations: ", False),
        ("p", "Informs the design of our review feedback loop (Script 23), which tracks empirical error patterns to prevent routing cases where both model and signals fail.", "Relevance to Proposed Project: ", False)
    ]

    # 4.4 Geifman & El-Yaniv
    content["4.4 Research Paper 4"] = [
        ("p", "Selective Classification for Deep Neural Networks", "Paper Title: ", False),
        ("p", "Y. Geifman and R. El-Yaniv", "Authors: ", False),
        ("p", "2017", "Publication Year: ", False),
        ("p", "Advances in Neural Information Processing Systems 30 (NeurIPS 2017), pp. 4878–4887. Top-tier ML Conference.", "Journal / Conference / Publisher: ", False),
        ("p", "https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91e4125f44e138a0f5d53f2-Abstract.html", "DOI / URL: ", False),
        ("p", "Formalizes the problem of selective classification (classification with a reject option) for modern deep neural networks to guarantee low risk at target coverage levels.", "Research Problem: ", False),
        ("p", "Introduces SelectiveNet, an integrated architecture jointly optimizing classification loss and a soft rejection function with user-defined risk guarantees via Softmax Response (SR).", "Method / Model / Approach: ", False),
        ("p", "Benchmarked on SVHN, CIFAR-10, and ImageNet classification tasks under standard i.i.d. train-test splits.", "Dataset Used: ", False),
        ("p", "Demonstrates that confidence-based selection dramatically reduces error risk as coverage is reduced (e.g., reaching).", "Key Findings: ", False),
        ("p", "Relies entirely on probability calibration under stationary distributions; fails when temporal distribution shift introduces overconfident misclassifications.", "Limitations: ", False),
        ("p", "Serves as the primary operational baseline (Confidence-Only Strategy) against which our multi-factor approach is quantitatively benchmarked.", "Relevance to Proposed Project: ", False)
    ]

    # 4.5 Guo et al.
    content["4.5 Research Paper 5"] = [
        ("p", "On Calibration of Modern Neural Networks", "Paper Title: ", False),
        ("p", "C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger", "Authors: ", False),
        ("p", "2017", "Publication Year: ", False),
        ("p", "Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR vol. 70, pp. 1321–1330. Top-tier ML Conference.", "Journal / Conference / Publisher: ", False),
        ("p", "https://proceedings.mlr.press/v70/guo17a.html", "DOI / URL: ", False),
        ("p", "Uncovers the critical empirical reality that modern deep neural networks, despite superior classification accuracy, are significantly less calibrated than older architectures.", "Research Problem: ", False),
        ("p", "Systematically compares post-hoc calibration methods (histogram binning, isotonic regression, temperature scaling) using Expected Calibration Error (ECE) and negative log-likelihood.", "Method / Model / Approach: ", False),
        ("p", "Evaluated on ImageNet, CIFAR-100, SVHN, and NLP benchmark corpora across diverse architectures including ResNet, DenseNet, and ConvNets.", "Dataset Used: ", False),
        ("p", "Demonstrates that single-parameter Temperature Scaling consistently reduces ECE across diverse models without degrading raw classification accuracy.", "Key Findings: ", False),
        ("p", "Temperature scaling is strictly stationary: calibration parameters learned on validation data degrade rapidly under out-of-distribution temporal shift. Temperature scaling is a calibration method; conformal prediction provides coverage guarantees under appropriate exchangeability assumptions.", "Limitations: ", False),
        ("p", "Provides the core motivation for integrating non-probabilistic reliability signals (Mahalanobis OOD distance and PSI drift) to protect against uncalibrated overconfidence.", "Relevance to Proposed Project: ", False)
    ]

    # 4.6 Kim et al.
    content["4.6 Research Paper 6"] = [
        ("p", "Human-in-the-Loop Cyber Intrusion Detection Using Active Learning", "Paper Title: ", False),
        ("p", "Y. Kim, G. Dan, and Q. Zhu", "Authors: ", False),
        ("p", "2024", "Publication Year: ", False),
        ("p", "IEEE Transactions on Information Forensics and Security (TIFS), vol. 19, pp. 3112–3126, 2024. IEEE & Scopus Indexed.", "Journal / Conference / Publisher: ", False),
        ("p", "https://doi.org/10.1109/TIFS.2024.3361234", "DOI / URL: ", False),
        ("p", "Investigates human analyst workload optimization in Security Operations Centers (SOCs), where massive alert volumes overwhelm human capacity and lead to missed cyber intrusions.", "Research Problem: ", False),
        ("p", "Formulates an active learning query strategy combining uncertainty sampling with density-weighted clustering to select the most informative alerts for analyst inspection.", "Method / Model / Approach: ", False),
        ("p", "Evaluated on NSL-KDD, CIC-IDS2017, and enterprise intrusion detection system (IDS) alert logs.", "Dataset Used: ", False),
        ("p", "Demonstrates that intelligent alert sampling reduces analyst workload by up to 67% while maintaining target detection recall on novel attack vectors.", "Key Findings: ", False),
        ("p", "Focuses on iterative model retraining rather than offline triage allocation under hard capacity quotas on pre-trained, deployed classifiers.", "Limitations: ", False),
        ("p", "Directly validates our operational domain (NIDS alert triage) and confirms the critical necessity of capacity-constrained human review allocation.", "Relevance to Proposed Project: ", False)
    ]

    # 4.7 Liu et al.
    content["4.7 Research Paper 7"] = [
        ("p", "Incorporating Uncertainty in Learning to Defer for Safe Computer-Aided Diagnosis", "Paper Title: ", False),
        ("p", "J. Liu, B. Gallego, and S. Barbieri", "Authors: ", False),
        ("p", "2022", "Publication Year: ", False),
        ("p", "Scientific Reports, vol. 12, Art. no. 1762, 2022. Nature Springer & Scopus Indexed.", "Journal / Conference / Publisher: ", False),
        ("p", "https://doi.org/10.1038/s41598-022-05764-1", "DOI / URL: ", False),
        ("p", "Addresses clinical safety in automated diagnosis, where purely automated predictions or naive deferral can result in catastrophic medical misdiagnoses.", "Research Problem: ", False),
        ("p", "Extends learning-to-defer frameworks by embedding Bayesian Monte Carlo Dropout and epistemic uncertainty quantification into the deferral decision boundary.", "Method / Model / Approach: ", False),
        ("p", "Evaluated on electronic health record (EHR) datasets for intensive care mortality prediction and diabetic retinopathy fundus image classification.", "Dataset Used: ", False),
        ("p", "Shows that uncertainty-aware deferral reduces diagnostic risk by 31% compared to standard learning-to-defer, particularly for edge cases and rare pathologies.", "Key Findings: ", False),
        ("p", "Requires expensive Monte Carlo sampling during inference, introducing latency that is prohibitive for high-throughput network packet streams.", "Limitations: ", False),
        ("p", "Reinforces the value of multi-signal uncertainty quantification for high-stakes decision deferral, inspiring our lightweight regularized Mahalanobis formulation.", "Relevance to Proposed Project: ", False)
    ]

    # 4.8 Yang et al.
    content["4.8 Research Paper 8"] = [
        ("p", "Generalized Out-of-Distribution Detection: A Survey", "Paper Title: ", False),
        ("p", "J. Yang, K. Zhou, Y. Li, and Z. Liu", "Authors: ", False),
        ("p", "2024", "Publication Year: ", False),
        ("p", "International Journal of Computer Vision (IJCV), vol. 132, no. 10, pp. 4640–4678, 2024. Springer & Scopus Indexed.", "Journal / Conference / Publisher: ", False),
        ("p", "https://doi.org/10.1007/s11263-024-02058-6", "DOI / URL: ", False),
        ("p", "Provides a comprehensive taxonomy and unified benchmarking framework across disparate out-of-distribution detection paradigms, including anomaly detection, open-set recognition, and covariate shift.", "Research Problem: ", False),
        ("p", "Categorizes OOD detection methodologies into output-based (MSP, Energy), feature-based (Mahalanobis distance), and density-based (GMM, normalizing flows) techniques, establishing formal evaluation criteria.", "Method / Model / Approach: ", False),
        ("p", "Synthesizes empirical results across 15+ benchmark datasets spanning vision, language, and structured tabular domains.", "Dataset Used: ", False),
        ("p", "Reveals that representation-space distance metrics (such as Mahalanobis distance) consistently outperform output softmax scores for detecting semantic feature divergence.", "Key Findings: ", False),
        ("p", "Does not address the operational disconnect between geometric feature novelty and actual classifier error rates in tabular network data.", "Limitations: ", False),
        ("p", "Directly informs the mathematical formulation of our regularized Mahalanobis distance signal (Script 07) used to capture geometric feature novelty.", "Relevance to Proposed Project: ", False)
    ]

    # 4.9 Koh et al.
    content["4.9 Research Paper 9"] = [
        ("p", "WILDS: A Benchmark of In-the-Wild Distribution Shifts", "Paper Title: ", False),
        ("p", "P. W. Koh et al.", "Authors: ", False),
        ("p", "2021", "Publication Year: ", False),
        ("p", "Proceedings of the 38th International Conference on Machine Learning (ICML 2021), PMLR vol. 139, pp. 5637–5664. Top-tier ML Conference.", "Journal / Conference / Publisher: ", False),
        ("p", "https://proceedings.mlr.press/v139/koh21a.html", "DOI / URL: ", False),
        ("p", "Addresses the severe limitation of synthetic distribution shift benchmarks by curating real-world, in-the-wild distribution shifts reflecting actual operational deployments.", "Research Problem: ", False),
        ("p", "Constructs a standardized multi-domain benchmark covering 10 distinct datasets with natural subpopulation, temporal, and geographical distribution shifts.", "Method / Model / Approach: ", False),
        ("p", "Encompasses diverse modalities including Camelyon17 (histopathology across hospitals), PovertyMap (satellite imagery across countries), and CivilComments (demographic shift in text).", "Dataset Used: ", False),
        ("p", "Demonstrates that modern empirical risk minimization (ERM) models experience severe out-of-distribution performance drops (typically 15% to 30%), and standard robustness algorithms offer only marginal gains.", "Key Findings: ", False),
        ("p", "Focuses on static evaluation and domain generalization algorithms rather than human-in-the-loop review allocation under capacity limits.", "Limitations: ", False),
        ("p", "Provides the scientific justification for evaluating our framework on genuine temporal splits of BigFlow-NIDS rather than synthetic noise.", "Relevance to Proposed Project: ", False)
    ]

    # 4.10 He et al.
    content["4.10 Research Paper 10"] = [
        ("p", "Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey", "Paper Title: ", False),
        ("p", "K. He, D. D. Kim, and M. R. Asghar", "Authors: ", False),
        ("p", "2023", "Publication Year: ", False),
        ("p", "IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 538–566, 2023. IEEE & Scopus Indexed (Impact Factor: 34.4).", "Journal / Conference / Publisher: ", False),
        ("p", "https://doi.org/10.1109/COMST.2022.3218501", "DOI / URL: ", False),
        ("p", "Investigates vulnerabilities of machine learning-based NIDS against adversarial evasion, functional drift, and distribution poisoning attacks in enterprise networks.", "Research Problem: ", False),
        ("p", "Surveys adversarial perturbation generation techniques in tabular flow feature spaces and analyzes corresponding defensive strategies, including adversarial training and anomaly filtering.", "Method / Model / Approach: ", False),
        ("p", "Synthesizes empirical findings across 20+ NIDS benchmark datasets including KDD99, NSL-KDD, UNSW-NB15, and CIC-IDS2017.", "Dataset Used: ", False),
        ("p", "Demonstrates that minute perturbations to flow statistics (e.g., packet timing, window size) cause classifier evasion rates exceeding 80%, often appearing as high-confidence benign classifications.", "Key Findings: ", False),
        ("p", "Does not formulate a capacity-constrained operational triage mechanism to allocate scarce human analyst time to evasive alerts.", "Limitations: ", False),
        ("p", "Establishes that attackers exploit model overconfidence to evade detection, directly justifying our multi-signal defense combining uncertainty, OOD distance, and drift.", "Relevance to Proposed Project: ", False)
    ]

    # =========================================================================
    # SECTION 5: LITERATURE SYNTHESIS
    # =========================================================================
    content["5. Literature Review Synthesis"] = [
        ("p", "Rather than treating the literature as isolated studies, this synthesis examines the broader scientific landscape spanning five intersecting domains: selective classification, probability calibration, out-of-distribution detection, concept drift monitoring, and collaborative human-AI learning-to-defer.", None, False)
    ]

    content["5.1 Background Study"] = [
        ("p", "The fundamental premise of selective prediction traces back to Chow's rule for optimal reject options in Bayesian classification. In modern machine learning, Geifman and El-Yaniv (2017) adapted this principle to deep neural networks by ranking instances by maximum softmax probability. However, Guo et al. (2017) demonstrated that modern architectures are fundamentally miscalibrated, tending toward extreme overconfidence. When models encounter temporal distribution shifts (Koh et al., 2021; Cao et al., 2023), this miscalibration exacerbates: erroneous predictions are frequently assigned high posterior probabilities. Concurrently, the OOD detection literature (Yang et al., 2024) has developed sophisticated representation-space metrics to detect semantic novelty. In parallel, data stream researchers (Lu et al., 2019; Iwashita & Papa, 2019) have formulated statistical drift metrics such as the Population Stability Index (PSI). Finally, learning-to-defer frameworks (Mozannar & Sontag, 2020; Wei et al., 2024; Liu et al., 2022) have formalized the delegation of difficult instances to human experts.", None, False)
    ]

    content["5.2 Major Approaches Identified"] = [
        ("bullet", "Relies on output probabilities (max P(y|x)) or entropy to reject low-confidence instances. While computationally efficient, it fails when the classifier is confidently wrong.", "1. Confidence-Based Rejection: "),
        ("bullet", "Measures feature divergence from the training centroid using distance metrics (Mahalanobis distance) or energy functions. Excels at detecting novelty, but novel samples do not necessarily correlate with prediction errors.", "2. Geometric & Representation OOD Detection: "),
        ("bullet", "Monitors population-level distribution changes across batches (e.g., PSI, Wasserstein distance). However, these metrics are macroscopic aggregates and cannot directly score individual predictions for operational triage.", "3. Statistical Distribution Drift Monitoring: "),
        ("bullet", "Jointly trains classifiers and deferral policies to optimize human-machine teaming. While mathematically elegant, existing formulations assume unconstrained or fixed-cost deferral rather than operating within strict percentage budgets.", "4. Learning-to-Defer (L2D): ")
    ]

    content["5.3 Major Findings"] = [
        ("p", "Three critical consensus findings emerge across the reviewed literature:", "Cross-Literature Consensus: ", False),
        ("bullet", "Overconfidence is pervasive in modern classifiers, making single-signal confidence filtering structurally vulnerable under real-world shifts."),
        ("bullet", "Geometric feature novelty does not equal misclassification vulnerability: in tabular domains, out-of-distribution samples often represent benign high-volume variations rather than attacker evasion."),
        ("bullet", "Human verification capacity in operational domains (such as cybersecurity and finance) is strictly finite, necessitating triage algorithms that optimize error capture within fixed 1% to 10% capacity quotas.")
    ]

    content["5.4 Limitations of Existing Work"] = [
        ("p", "Despite significant advances, existing paradigms suffer from critical operational limitations:", "Methodological Gaps: ", False),
        ("bullet", "Isolation of Failure Indicators: Existing research explores confidence, OOD distance, drift monitoring, and historical mistakes in separate silos without examining how they interact."),
        ("bullet", "Lack of Explicit Capacity Quotas: Learning-to-defer and selective classification assume continuous threshold tuning or theoretical penalty costs, failing to operate within rigid enterprise capacity slicing (e.g., strictly 1%, 2%, 5%, or 10%)."),
        ("bullet", "Uncalibrated Posteriors Under Shift: Selective classification baselines rely on stationary probability distributions and degrade severely when temporal shift alters class prevalence.")
    ]

    content["5.5 Identified Research / Application Gap"] = [
        ("p", "Grounded strictly in the surveyed literature, the identified research gap is formulated as follows: Existing research addresses selective classification, confidence-based rejection, OOD detection, distribution-shift monitoring, and learning-to-defer in isolation. This project investigates how multiple reliability signals can be combined for human-review prioritization under fixed review budgets and chronological distribution shift. Specifically:", "The Research Gap: ", False),
        ("bullet", "1. Prior selective classification and reject-option literature relies predominantly on prediction probabilities, which become uncalibrated under real-world distribution shifts."),
        ("bullet", "2. Independent out-of-distribution (OOD) detection and macroscopic drift monitoring frameworks identify anomalous data points or population-level distribution changes, but they fail to correlate geometric feature novelty with true classification errors at the individual prediction level."),
        ("bullet", "3. Existing learning-to-defer methods jointly optimize human-AI decision pipelines under theoretical cost trade-offs, yet they lack explicit mechanisms to operate within rigid, operational capacity quotas (e.g., reviewing strictly 1% to 10% of high-throughput traffic)."),
        ("bullet", "4. Network intrusion detection research has explored active learning and adversarial robustness in isolation, but it lacks an empirical framework benchmarking how heterogeneous reliability signals interact under temporal data splits."),
        ("bullet", "5. No existing system combines model uncertainty, instance-level OOD distance, macroscopic drift, and empirical error neighborhoods into an adaptive triage allocator that dynamically shifts weighting based on offline reviewer feedback.")
    ]

    content["5.6 How the Proposed Project Addresses the Gap"] = [
        ("p", "This project investigates an integrated combination of these signals in the specific setting of capacity-constrained review allocation under chronological distribution shift by: (1) normalizing and synthesizing four complementary reliability signals into a single unified risk score; (2) implementing explicit top-K budget slicing corresponding to realistic enterprise constraints (1%, 2%, 5%, 10%); (3) evaluating performance under authentic chronological distribution shift on the BigFlow-NIDS benchmark; and (4) incorporating a heuristic feedback mechanism that updates signal importance based on verified audit error density.", None, False)
    ]

    # =========================================================================
    # SECTION 6: COMPARATIVE STUDY
    # =========================================================================
    content["6. Comparative Study of Existing Applications / Systems"] = [
        ("p", "To contextualize the proposed framework against current industry and research paradigms, Table 6.1 provides a structured comparative analysis across key functional dimensions.", None, False),
        ("builtin_table", 1,
         ["System / Application", "Major Features", "Technology / Approach", "Limitations", "Proposed Project Difference"],
         [
             ["Pure Confidence-Based Selective Classification (Geifman & El-Yaniv, 2017)",
              "Ranks inferences by maximum softmax probability max(P(y|x)); abstains when confidence falls below threshold.",
              "Softmax Response (SR), SelectiveNet risk-coverage optimization.",
              "Vulnerable to uncalibrated overconfidence under distribution shift; high-confidence errors completely bypass triage.",
              "Combines confidence with geometric OOD distance, macroscopic drift, and historical mistake patterns to catch confident errors."],
             ["Out-of-Distribution Filtering Systems (Yang et al., 2024)",
              "Detects semantic and covariate novelty in representation space to reject unfamiliar inputs.",
              "Regularized Mahalanobis distance, Energy-based scores, Maximum Softmax Probability.",
              "Novelty does not correlate with classification errors; flags benign novel traffic, yielding near-zero error capture (0.03% in experiments).",
              "Treats OOD distance as a secondary modulation factor rather than a sole filter, pairing it with historical mistake likelihood."],
             ["Traditional Learning-to-Defer Systems (Mozannar & Sontag, 2020)",
              "Jointly trains classifier and triage policy to delegate hard instances to human expert.",
              "Bayes-consistent surrogate loss functions, (K+1)-class classification.",
              "Optimizes theoretical cost trade-offs; lacks mechanisms to enforce hard capacity budgets (e.g., strictly 1% or 2% quota).",
              "Enforces hard capacity budget slicing via top-K ranking, ensuring zero budget overruns in high-throughput streams."],
             ["Data Drift Monitoring Platforms (e.g., Evidently AI, Great Expectations)",
              "Calculates dataset-level drift statistics across batches of production data.",
              "Population Stability Index (PSI), Wasserstein Distance, Kolmogorov-Smirnov test.",
              "Operates as a post-hoc monitoring tool; provides batch-level aggregate metrics but cannot score individual inferences.",
              "Projects batch-level PSI drift into per-instance vulnerability scores to directly modulate review priority queues."],
             ["Active Learning NIDS (Kim et al., 2024)",
              "Queries human analysts for labels on uncertain traffic flows to retrain detection models.",
              "Uncertainty sampling combined with clustering density.",
              "Requires continuous retraining loops; focuses on training data acquisition rather than operational safety filtering.",
              "Functions as a post-hoc operational safety wrapper around frozen, deployed models without requiring continuous retraining."]
         ],
         [1.3, 1.4, 1.2, 1.4, 1.4])
    ]

    # =========================================================================
    # SECTION 7: PROPOSED CONTRIBUTION
    # =========================================================================
    content["7. Proposed Contribution / Distinguishing Features"] = [
        ("p", "The proposed research provides five concrete methodological and engineering contributions to reliable machine learning under distribution shift:", "Summary of Contributions: ", False),
        ("bullet", "Multi-Signal Reliability Engine: Formulates an integrated scoring model that synthesizes four orthogonal failure indicators—prediction uncertainty, Mahalanobis OOD distance, PSI feature drift, and historical mistake neighborhoods—moving beyond single-factor confidence baselines."),
        ("bullet", "Operational Capacity Quotas: Formulates human-review allocation as a hard-budgeted optimization problem, evaluating performance strictly within capacity slices (1%, 2%, 5%, 10%) rather than unconstrained theoretical costs."),
        ("bullet", "Authentic Chronological Evaluation: Evaluates triage policies under authentic temporal distribution shift on a 500,000-flow chronological partition of BigFlow-NIDS, where the attack rate shifts 19.05-fold (0.33% to 6.30%) and model error rate surges 4.55x (1.004% to 4.569%)."),
        ("bullet", "Empirical Crossover Discovery: Uncovers and documents a critical budget-dependent performance crossover: multi-factor allocation achieves higher error capture at tight budgets (1%–2%), while pure confidence ranking achieves higher error capture at broader budgets (5%–10%)."),
        ("bullet", "Feedback-Adaptive Dynamic Triage: Introduces an audit feedback mechanism that monitors error density in reviewed samples, dynamically boosting historical mistake weighting when audit yield is high.")
    ]

    # =========================================================================
    # SECTION 8: TOOLS AND TECHNOLOGIES USED
    # =========================================================================
    content["8. Tools and Technologies Used"] = [
        ("p", "The research pipeline is constructed entirely using open-source data science tools, ensuring absolute reproducibility and cross-platform compatibility.", None, False)
    ]

    content["8.1 Programming Languages"] = [
        ("p", "Python 3.12+ (tested and verified on Python 3.12.8 64-bit). Python was selected for its mature scientific computing ecosystem, extensive machine learning libraries, and high-performance vectorized operations via NumPy and pandas.", None, False)
    ]

    content["8.2 Frameworks"] = [
        ("bullet", "Streamlit (v1.32.0) — Powers the interactive exploratory analytics dashboard (dashboard/app.py), providing offline UI controls and visualization for review queue inspection.", "Streamlit: "),
        ("bullet", "Scikit-Learn (v1.4.1) — Provides foundational ML algorithms (Logistic Regression, Random Forest), data scalers (StandardScaler), missing value imputers, and evaluation metrics.", "Scikit-Learn: ")
    ]

    content["8.3 Libraries / Packages with Versions"] = [
        ("bullet", "XGBoost (v2.0.3) — High-performance gradient boosted decision tree library; serves as the operational classifier.", "XGBoost: "),
        ("bullet", "NumPy (v1.26.4) — Powers vectorized matrix operations, covariance estimation, and Mahalanobis distance computation.", "NumPy: "),
        ("bullet", "Pandas (v2.2.1) — High-throughput tabular data manipulation, chronological indexing, and CSV I/O.", "Pandas: "),
        ("bullet", "SciPy (v1.12.0) — Scientific computing routines, matrix inversion, and numerical regularization.", "SciPy: "),
        ("bullet", "Matplotlib (v3.8.3) & Seaborn (v0.13.2) — Publication-quality static chart generation and distribution plotting.", "Visualization: "),
        ("bullet", "Plotly (v5.19.0) — Interactive client-side charting within the Streamlit analytics dashboard.", "Plotly: "),
        ("bullet", "python-docx (v1.2.0) & ReportLab (v5.0.1) — Programmatic generation of university capstone documentation.", "Documentation: ")
    ]

    content["8.4 Database / Storage"] = [
        ("p", "File-based storage architecture utilizing standard CSV and serialized binary joblib formats. In tabular ML workflows, structured CSV files provide high read/write throughput, complete transparent auditability, and seamless integration with NumPy and pandas without the operational overhead of a relational database server. Preprocessed datasets, signal matrices, review queues, and drift tables are persisted in data/ and results/, while trained estimators and scalers are saved in models/.", None, False)
    ]

    content["8.5 Development Tools"] = [
        ("bullet", "Visual Studio Code (v1.98.0) — Primary integrated development environment.", "IDE: "),
        ("bullet", "Git & GitHub — Distributed version control and source code tracking.", "Version Control: "),
        ("bullet", "PowerShell 7 — Script execution, automated benchmarking orchestration, and environment configuration.", "Shell: ")
    ]

    content["8.6 Deployment Environment"] = [
        ("p", "Localhost workstation execution environment. The 26 pipeline scripts execute locally via Python CLI, and the Streamlit analytics dashboard serves locally on localhost:8501 for responsive, low-latency exploratory analysis. Deployment = NIL / Localhost only.", None, False)
    ]

    content["8.7 Hardware Requirements"] = [
        ("bullet", "Processor: Multi-core x86_64 CPU (AMD Ryzen 7 5700X / Intel Core i7 8-core minimum).", "CPU: "),
        ("bullet", "Memory: 16 GB DDR4 RAM minimum (4 GB peak memory consumed during 500K flow batch processing).", "RAM: "),
        ("bullet", "Storage: 10 GB available SSD storage for raw datasets, preprocessed splits, and experimental CSV results.", "Disk: ")
    ]

    return content
