from report_src.docx_helper import add_h1, add_h2, add_h3, add_p, add_bullet, add_image, create_table
import os
from docx.shared import Inches, Pt

BASE_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"

def build_section_15_ml_methodology(doc):
    add_h1(doc, "15. ML / DL / AI Methodology – Where Applicable")
    add_p(doc,
        "This section details the machine learning experimental design, benchmarking protocols, quantitative evaluation metrics, and empirical findings obtained on the BigFlow-NIDS dataset.")

    add_h2(doc, "15.1 Dataset and Source")
    add_p(doc,
        "The project evaluates models on the recently published BigFlow-NIDS benchmark (M. B. Uddin and M. S. Arefin, Data in Brief, vol. 65, Art. no. 112530, April 2026, doi: 10.1016/j.dib.2026.112530). BigFlow-NIDS is a comprehensive network flow dataset generated from large-scale synthetic and enterprise traffic traces.",
        bold_prefix="Benchmark Dataset: ")

    add_h2(doc, "15.2 Dataset Characteristics")
    add_bullet(doc, "The total corpus comprises 66,935,021 network flow records spanning 55 raw attributes and 32 fine-grained attack categories.", bold_prefix="Total Scale: ")
    add_bullet(doc, "A 500,000-flow chronological partition is utilized for experimental modeling, preserving authentic time-series dependencies.", bold_prefix="Experimental Partition: ")
    add_bullet(doc, "49 numerical flow features (durations, packet lengths, inter-arrival times, throughput metrics, TCP flags, window advertisements) are retained for modeling. The detailed multi-class Attack column is excluded to eliminate target leakage, framing the task as binary classification (0 = Benign, 1 = Attack).", bold_prefix="Feature Space: ")

    add_h2(doc, "15.3 Data Preprocessing")
    add_bullet(doc, "Infinite values resulting from division by zero in flow rate attributes are converted to nulls and imputed using median values computed strictly over the training split.")
    add_bullet(doc, "Missing numerical values are imputed using training-set feature medians.")
    add_bullet(doc, "StandardScaler is fitted exclusively on training data and applied to scale inputs for Logistic Regression. Tree-based models (Random Forest, XGBoost) operate directly on unscaled features.")
    add_bullet(doc, "All transformations strictly adhere to zero-leakage protocols; validation and test splits are transformed using parameters fitted on the training split.")

    add_h2(doc, "15.4 Data Augmentation / Feature Engineering")
    add_p(doc,
        "Synthetic data augmentation was deliberately avoided to preserve authentic temporal distribution drift characteristics. Feature engineering focused on constructing the four orthogonal reliability signals: normalized prediction uncertainty (1 - confidence), regularized Mahalanobis distance in numerical space, PSI feature drift mapping, and decile historical mistake density.",
        bold_prefix="Signal Engineering: ")

    add_h2(doc, "15.5 Train / Validation / Test Strategy")
    add_p(doc,
        "Data was partitioned chronologically (70% training, 15% validation, 15% shifted test):",
        bold_prefix="Temporal Partitioning: ")
    add_bullet(doc, "Training Split: First 350,000 chronological flows (Attack prevalence = 0.35%). Used for model training and baseline covariance fitting.")
    add_bullet(doc, "Validation Split: Next 75,000 chronological flows (Attack prevalence = 0.33%, 248 attacks, 753 model errors). Used for signal calibration and threshold tuning.")
    add_bullet(doc, "Shifted Test Split: Final 75,000 chronological flows (Attack prevalence = 6.30%, 4,724 attacks, 3,427 model errors). Used strictly for out-of-sample evaluation under temporal shift.")

    add_h2(doc, "15.6 Cross Validation Strategy")
    add_p(doc,
        "Standard k-fold cross-validation was explicitly avoided because uniform random shuffling shuffles past and future events, destroying the chronological temporal dependency required to evaluate real-world distribution shift. Instead, chronological out-of-time evaluation was enforced, mirroring genuine production deployment.",
        bold_prefix="Out-of-Time Protocol: ")

    add_h2(doc, "15.7 Benchmark Models")
    add_p(doc,
        "Three distinct classification algorithms were trained and benchmarked on the 350,000 training records: (1) Logistic Regression (linear baseline), (2) Random Forest (bagging ensemble), and (3) XGBoost (gradient boosting).")

    add_h2(doc, "15.8 Proposed / Modified / Optimised Model")
    add_p(doc,
        "The proposed operational architecture pairs the best-performing classifier (XGBoost) with the Adaptive Multi-Factor Review Allocation Engine. Rather than modifying model weights post-deployment, the framework acts as a dynamic reliability wrapper around the model, triaging predictions into human review queues.",
        bold_prefix="System Architecture: ")

    add_h2(doc, "15.9 Hyperparameter Optimisation")
    add_p(doc,
        "No formal automated hyperparameter optimization (such as Grid Search, Random Search, or Optuna) was performed. The models were evaluated using standard, robust fixed hyperparameter configurations established during baseline tuning:\n"
        "• Logistic Regression: max_iter=1000, class_weight='balanced', random_state=42.\n"
        "• Random Forest: n_estimators=150, max_depth=20, n_jobs=-1, class_weight='balanced', random_state=42.\n"
        "• XGBoost: n_estimators=150, max_depth=6, learning_rate=0.1, subsample=0.8, colsample_bytree=0.8, eval_metric='logloss', random_state=42, n_jobs=4.",
        bold_prefix="Hyperparameter Specification: ")

    add_h2(doc, "15.10 Evaluation Metrics")
    add_bullet(doc, "Model Performance: Accuracy, Precision, Recall, F1-Score, and ROC-AUC.", bold_prefix="Standard ML Metrics: ")
    add_bullet(doc, "Review Allocation Metrics: Errors Caught (absolute count), Error Capture Rate (percentage of total shifted errors caught), and Review Efficiency (errors captured per 1,000 manual reviews).", bold_prefix="Triage Metrics: ")

    add_h2(doc, "15.11 Preliminary Results")
    add_p(doc,
        "Table 15.1 summarizes the performance of the three benchmark classifiers evaluated on the 75,000 validation records.")

    headers_mod = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    rows_mod = [
        ["Logistic Regression", "0.9606", "0.0376", "0.4435", "0.0693", "0.7499"],
        ["Random Forest", "0.9801", "0.0708", "0.4153", "0.1210", "0.8526"],
        ["XGBoost", "0.9899", "0.0401", "0.0887", "0.0552", "0.9228"]
    ]
    col_w_mod = [2.0, 0.9, 0.9, 0.9, 0.9, 0.9]
    create_table(doc, headers_mod, rows_mod, col_w_mod)

    add_p(doc,
        "XGBoost achieved the highest ROC-AUC (0.9228) and overall accuracy (98.99%) on validation data, establishing it as the primary inference engine. When deployed on the shifted test split, the model encountered 3,427 total classification errors (error rate = 4.569%).")

    add_p(doc,
        "Table 15.2 provides the definitive empirical comparison across all five review allocation strategies evaluated on the 75,000 shifted test records across four operational review budgets (1%, 2%, 5%, 10%).")

    headers_strat = ["Review Budget", "Strategy", "Reviews Allocated", "Errors Caught", "Capture Rate (%)", "Errors / 1000 Reviews"]
    rows_strat = [
        ["1% (750 reviews)", "Uniform Random", "750", "40", "1.17%", "53.33"],
        ["1% (750 reviews)", "Pure Confidence", "750", "463", "13.51%", "617.33"],
        ["1% (750 reviews)", "Mahalanobis OOD", "750", "1", "0.03%", "1.33"],
        ["1% (750 reviews)", "Static Multi-Factor", "750", "600", "17.51%", "800.00"],
        ["1% (750 reviews)", "Feedback Adaptive", "750", "610", "17.80%", "813.33"],
        ["2% (1500 reviews)", "Uniform Random", "1500", "73", "2.13%", "48.67"],
        ["2% (1500 reviews)", "Pure Confidence", "1500", "916", "26.73%", "610.67"],
        ["2% (1500 reviews)", "Mahalanobis OOD", "1500", "9", "0.26%", "6.00"],
        ["2% (1500 reviews)", "Static Multi-Factor", "1500", "1165", "33.99%", "776.67"],
        ["2% (1500 reviews)", "Feedback Adaptive", "1500", "1174", "34.26%", "782.67"],
        ["5% (3750 reviews)", "Uniform Random", "3750", "189", "5.52%", "50.40"],
        ["5% (3750 reviews)", "Pure Confidence", "3750", "2243", "65.45%", "598.13"],
        ["5% (3750 reviews)", "Mahalanobis OOD", "3750", "12", "0.35%", "3.20"],
        ["5% (3750 reviews)", "Static Multi-Factor", "3750", "1870", "54.57%", "498.67"],
        ["5% (3750 reviews)", "Feedback Adaptive", "3750", "1573", "45.90%", "419.47"],
        ["10% (7500 reviews)", "Uniform Random", "7500", "340", "9.92%", "45.33"],
        ["10% (7500 reviews)", "Pure Confidence", "7500", "2879", "84.01%", "383.87"],
        ["10% (7500 reviews)", "Mahalanobis OOD", "7500", "12", "0.35%", "1.60"],
        ["10% (7500 reviews)", "Static Multi-Factor", "7500", "2242", "65.42%", "298.93"],
        ["10% (7500 reviews)", "Feedback Adaptive", "7500", "1794", "52.35%", "239.20"]
    ]
    col_w_strat = [1.3, 1.4, 1.1, 0.9, 1.0, 1.3]
    create_table(doc, headers_strat, rows_strat, col_w_strat)

    add_h2(doc, "15.12 Analysis of Results")
    add_p(doc,
        "The empirical findings yield critical, non-obvious insights regarding selective ML under distribution shift:",
        bold_prefix="Core Analytical Findings: ")
    add_bullet(doc, "At the 1% review budget (750 reviews), Feedback Adaptive captures 610 errors (17.80%) and Static Multi-Factor captures 600 errors (17.51%), significantly outperforming Pure Confidence, which captures only 463 errors (13.51%). Similarly, at the 2% budget (1,500 reviews), Feedback Adaptive captures 1,174 errors (34.26%) compared to 916 (26.73%) for Pure Confidence (+7.53% absolute improvement). In tight review regimes, multi-signal synthesis successfully detects high-risk confident errors.", bold_prefix="1. Multi-Factor Dominance at Low Budgets (1%–2%): ")
    add_bullet(doc, "At the 5% budget (3,750 reviews), Pure Confidence overtakes multi-factor strategies, capturing 2,243 errors (65.45%) versus 1,870 (54.57%) for Static Multi-Factor and 1,573 (45.90%) for Feedback Adaptive. At 10% budget, Confidence captures 2,879 errors (84.01%) versus 2,242 (65.42%) for Static Multi-Factor. When review capacity expands, model uncertainty sweeps through the broader pool of borderline mistakes more effectively than composite indicators.", bold_prefix="2. Confidence Crossover at Higher Budgets (5%–10%): ")
    add_bullet(doc, "Mahalanobis OOD filtering alone captured only 1 error at 1% budget (0.03%) and 12 errors at 10% budget (0.35%), performing substantially worse than Uniform Random sampling (which caught 40 and 340 errors respectively). This proves empirically that geometric feature rarity in tabular network traffic does not correspond to classification errors.", bold_prefix="3. Complete Failure of Isolated OOD Filtering: ")
    add_bullet(doc, "No single strategy universally dominates across all budgets. The optimal allocation strategy is strictly budget-dependent: multi-factor triage is optimal under severe resource constraints (1%–2%), whereas confidence ranking is optimal when auditing capacity reaches 5% or higher.", bold_prefix="4. Scientific Conclusion on Strategy Selection: ")

def build_section_16_testing(doc):
    add_h1(doc, "16. Testing / Evaluation")
    add_p(doc,
        "System testing was conducted across three formal layers: functional unit verification, UI/UX dashboard validation, and empirical model evaluation.")

    add_h2(doc, "16.1 Functional Testing")
    add_p(doc, "Table 16.1 presents the functional test cases executed across the data processing and triage pipeline.")

    headers_tc = ["Test Case ID", "Module Tested", "Test Description", "Input Data", "Expected Output", "Actual Output", "Status"]
    rows_tc = [
        ["TC-01", "M1: Ingestion", "Verify 55 attributes and SHA-256 data integrity.", "500K BigFlow records", "Schema match, verified hash", "Schema verified, hash logged", "Pass"],
        ["TC-02", "M1: Splitter", "Verify temporal monotonicity and split sizes.", "Raw chronological flows", "350K/75K/75K exact sizes", "Exact split sizes verified", "Pass"],
        ["TC-03", "M2: Training", "Verify model serialization and convergence.", "X_train, y_train", "Valid .pkl models, ROC-AUC > 0.85", "XGBoost val AUC = 0.9228", "Pass"],
        ["TC-04", "M3: Signals", "Verify mathematical bounds of extracted signals.", "X_validation (75K)", "All signals normalized in [0, 1]", "Signals strictly bounded in [0, 1]", "Pass"],
        ["TC-05", "M4: Allocator", "Verify top-K queue budget quota enforcement.", "75K test scores, B=0.01", "Exactly 750 unique reviews", "Exactly 750 reviews allocated", "Pass"],
        ["TC-06", "M5: Feedback", "Verify dynamic weight update based on audit.", "Audit error concentration", "Bounded historical weight <= 0.35", "Weight updated and bounded", "Pass"]
    ]
    col_w_tc = [0.8, 1.0, 1.4, 1.1, 1.2, 1.2, 0.5]
    create_table(doc, headers_tc, rows_tc, col_w_tc)

    add_h2(doc, "16.2 UI / UX Testing")
    add_p(doc,
        "The Streamlit dashboard (dashboard/app.py) was tested locally on Chrome and Edge browsers. All four budget sliders (1%, 2%, 5%, 10%) re-rendered Plotly charts within 250 milliseconds. Dataframe filtering and dark-mode CSS styling operated without layout overflows or visual clipping.",
        bold_prefix="Local Dashboard Verification: ")

    add_h2(doc, "16.3 Model Evaluation, where applicable")
    add_p(doc,
        "Under temporal shift, model performance degraded across the board: validation error rate rose from 1.004% (753 errors out of 75,000) to 4.569% (3,427 errors out of 75,000), representing an exact 4.55x surge. Despite this severe degradation, average model confidence declined by only 1.83 percentage points (from 98.65% to 96.82%), demonstrating the silent overconfidence failure mode in operational environments.",
        bold_prefix="Distribution Shift Evaluation: ")

def build_section_17_genai(doc):
    add_h1(doc, "17. External GenAI / API Usage Disclosure")
    add_p(doc,
        "In strict compliance with university academic integrity regulations, external Generative AI API disclosures are formally documented:")
    add_bullet(doc, "NIL. The system does not call or depend upon any commercial LLM or Generative AI APIs (e.g., OpenAI GPT-4, Google Gemini, Anthropic Claude) in its core execution pipeline.", bold_prefix="17.1 API / Service Used: ")
    add_bullet(doc, "NIL. No operational data, telemetry, or review routing decisions are processed via external generative APIs.", bold_prefix="17.2 Functionality Provided by API: ")
    add_bullet(doc, "0% contribution to core system functionality.", bold_prefix="17.3 Approximate Percentage Contribution: ")
    add_bullet(doc, "100% of data processing, machine learning modeling, signal extraction, triage allocation, and dashboard analytics are independently implemented using Python, pandas, NumPy, scikit-learn, XGBoost, SciPy, and Streamlit.", bold_prefix="17.4 Core Functionality Independently Implemented: ")

def build_section_18_challenges(doc):
    add_h1(doc, "18. Current Challenges")
    add_p(doc,
        "To maintain scientific honesty, four primary technical and operational challenges encountered during Phase-I are documented:",
        bold_prefix="Identified Challenges: ")
    add_bullet(doc, "Ground-truth labels from the test partition are utilized to simulate oracle review. In production SOC environments, human analysts exhibit cognitive fatigue, variable inspection latency, and non-zero diagnostic error rates, which are not currently modeled.", bold_prefix="1. Simulated Review Oracle: ")
    add_bullet(doc, "Current composite risk weights are defined via transparent heuristic weighting. While interpretable, heuristic weights are not mathematically guaranteed to be Pareto-optimal across all shifted distributions.", bold_prefix="2. Heuristic Signal Weights: ")
    add_bullet(doc, "Empirical evaluations are currently restricted to the BigFlow-NIDS benchmark. Validating whether the multi-factor advantage at 1%–2% budgets generalizes to financial transaction streams and healthcare tabular data remains an active requirement.", bold_prefix="3. Single-Domain Benchmark Scope: ")
    add_bullet(doc, "Historical error modeling currently utilizes training-set mistake clusters. While effective, out-of-fold cross-validated residual estimation on training data would provide cleaner, less overfitted error proximity maps.", bold_prefix="4. Historical Error Estimation Refinement: ")

def build_section_19_work_planned(doc):
    add_h1(doc, "19. Work Planned Before Review-III")
    add_p(doc,
        "Table 19.1 details the concrete engineering and scientific milestones scheduled for completion prior to the Phase-I Review-III evaluation.")

    headers_wp = ["Sl No", "Planned Activity", "Expected Outcome", "Target Completion Date"]
    rows_wp = [
        ["1", "Cross-Domain Tabular Generalization", "Benchmark the framework on CIC-IDS2017 and credit card fraud datasets to verify tabular domain agnosticism.", "November 15, 2026"],
        ["2", "Post-Hoc Probability Calibration", "Implement Temperature Scaling and evaluate Expected Calibration Error (ECE) under temporal shift.", "November 25, 2026"],
        ["3", "Explainable AI (XAI) Integration", "Integrate SHAP feature attribution to explain flagged review cases for human security analysts.", "December 10, 2026"],
        ["4", "Bilevel Optimization / Learned Weights", "Implement automated bilevel optimization or reinforcement learning to discover data-driven signal weights.", "December 20, 2026"],
        ["5", "Production Web Dashboard Portal", "Expand Streamlit app into a multi-dataset, production-grade review portal with live telemetry simulation.", "January 10, 2027"]
    ]
    col_w_wp = [0.6, 2.2, 2.8, 1.4]
    create_table(doc, headers_wp, rows_wp, col_w_wp)

def build_section_20_references(doc):
    add_h1(doc, "20. References")
    add_p(doc,
        "All references are formatted according to official IEEE bibliographic standards and verified directly against primary publisher publication records:")

    refs = [
        "[1] T. Cao, J. Zhu, and G. Pang, \"Anomaly Detection Under Distribution Shift,\" in IEEE/CVF International Conference on Computer Vision (ICCV), 2023, pp. 6511–6523, doi: 10.1109/ICCV51070.2023.00599.",
        "[2] H. Mozannar and D. Sontag, \"Consistent Estimators for Learning to Defer to an Expert,\" in Proceedings of the 37th International Conference on Machine Learning (ICML 2020), PMLR, vol. 119, pp. 7076–7087, 2020.",
        "[3] Z. Wei, Y. Cao, and L. Feng, \"Exploiting Human-AI Dependence for Learning to Defer,\" in Proceedings of the 41st International Conference on Machine Learning (ICML 2024), PMLR, vol. 235, pp. 52484–52499, 2024.",
        "[4] Y. Geifman and R. El-Yaniv, \"Selective Classification for Deep Neural Networks,\" in Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, pp. 4878–4887, 2017.",
        "[5] C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger, \"On Calibration of Modern Neural Networks,\" in Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR, vol. 70, pp. 1321–1330, 2017.",
        "[6] Y. Kim, G. Dán, and Q. Zhu, \"Human-in-the-Loop Cyber Intrusion Detection Using Active Learning,\" IEEE Transactions on Information Forensics and Security, vol. 19, pp. 8658–8672, 2024, doi: 10.1109/TIFS.2024.3434647.",
        "[7] J. Liu, B. Gallego, and S. Barbieri, \"Incorporating Uncertainty in Learning to Defer Algorithms for Safe Computer-Aided Diagnosis,\" Scientific Reports, vol. 12, no. 1, Art. no. 1762, pp. 1–11, 2022, doi: 10.1038/s41598-022-05725-7.",
        "[8] J. Yang, K. Zhou, Y. Li, and Z. Liu, \"Generalized Out-of-Distribution Detection: A Survey,\" International Journal of Computer Vision, vol. 132, no. 12, pp. 5635–5662, 2024, doi: 10.1007/s11263-024-02117-4.",
        "[9] P. W. Koh et al., \"WILDS: A Benchmark of In-the-Wild Distribution Shifts,\" in Proceedings of the 38th International Conference on Machine Learning (ICML 2021), PMLR, vol. 139, pp. 5637–5664, 2021.",
        "[10] K. He, D. D. Kim, and M. R. Asghar, \"Adversarial Machine Learning for Network Intrusion Detection Systems: A Comprehensive Survey,\" IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 538–566, 2023, doi: 10.1109/COMST.2022.3233793.",
        "[11] M. B. Uddin and M. S. Arefin, \"BigFlow-NIDS: A comprehensive flow-based dataset for network intrusion detection systems,\" Data in Brief, vol. 65, Art. no. 112530, Apr. 2026, doi: 10.1016/j.dib.2026.112530.",
        "[12] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, \"Learning under Concept Drift: A Review,\" IEEE Transactions on Knowledge and Data Engineering, vol. 31, no. 12, pp. 2346–2363, Dec. 2019, doi: 10.1109/TKDE.2018.2876857.",
        "[13] A. S. Iwashita and J. P. Papa, \"An Overview on Concept Drift Learning,\" IEEE Access, vol. 7, pp. 1532–1547, 2019, doi: 10.1109/ACCESS.2018.2886026.",
        "[14] E. Mosqueira-Rey et al., \"Human-in-the-loop machine learning: a state of the art,\" Artificial Intelligence Review, vol. 56, no. 4, pp. 3005–3054, 2023, doi: 10.1007/s10462-022-10246-w.",
        "[15] K. Hendrickx, L. Caelen, F. Delaere, and B. Baesens, \"Machine learning with a reject option: a survey,\" Machine Learning, vol. 113, pp. 1973–2010, 2024, doi: 10.1007/s10994-024-06534-8.",
        "[16] M. Sarhan, S. Layeghy, and M. Portmann, \"Towards a standard feature set for NIDS datasets,\" Mobile Networks and Applications, vol. 27, pp. 1060–1074, 2022, doi: 10.1007/s11036-021-01843-0.",
        "[17] T. Chen and C. Guestrin, \"XGBoost: A Scalable Tree Boosting System,\" in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016, pp. 785–794, doi: 10.1145/2939672.2939785.",
        "[18] F. Pedregosa et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011."
    ]

    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
