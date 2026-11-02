# End-to-End Pipeline Architecture & Workflow

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  

---

## 1. Visual Pipeline Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
| 1. RAW DATA INGESTION                                                                             |
|    Dataset: NF-UQ-NIDS-v2 / BigFlow-NIDS Benchmark (500,000 flows total)                           |
|    File: BigFlow_sample.csv | 49 NetFlow features | Target: Binary 'Attack'                       |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 2. CHRONOLOGICAL DATA SPLIT (Strictly Ordered by 'Timestamp' -- Zero Leakage)                      |
|    Script: src/02_create_splits.py & src/27_split_audit.py                                        |
|    ├── Train Set:        350,000 flows (70.0%) | 6.10% attacks (21,350) | Timestamps 08:34-13:30  |
|    ├── Validation Set:    75,000 flows (15.0%) | 0.33% attacks (   248) | Timestamps 13:30-14:32  |
|    └── Shifted Test Set:  75,000 flows (15.0%) | 6.30% attacks ( 4,725) | Timestamps 14:32-15:35  |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 3. TRAINING-ONLY FEATURE PREPROCESSING                                                            |
|    Script: src/03_preprocess.py                                                                   |
|    ├── SimpleImputer(strategy='median')  -> Fitted EXCLUSIVELY on X_train                         |
|    ├── StandardScaler()                  -> Fitted EXCLUSIVELY on X_train                         |
|    └── Save Artifact: models/preprocessor.joblib (Transform X_val & X_shifted_test)               |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 4. SUPERVISED MODEL TRAINING & SELECTION                                                          |
|    Script: src/04_train_models.py                                                                 |
|    ├── Train: XGBoost, Random Forest, Logistic Regression on (X_train, y_train)                   |
|    ├── Select Champion Model: XGBoost (Val F1=0.912, Recall=0.871, ECE=0.012)                     |
|    └── Save Artifact: models/xgb_model.joblib                                                     |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 5. FOUR RELIABILITY SIGNAL GENERATION (Shifted Test Set: 75,000 flows)                             |
|    Script: src/17_shifted_test_signals.py -> results/shifted_test_all_signals.csv                 |
|    ├── Signal 1 (u):     Prediction Uncertainty: u = 1 - max(P0, P1) in [0, 0.50]                 |
|    ├── Signal 2 (OOD):   Mahalanobis OOD Percentile in [0, 1.00] (fitted on X_train)              |
|    ├── Signal 3 (Drift): Feature PSI Drift Risk in [0, 1.00] (L4_SRC_PORT, IN_BYTES)              |
|    └── Signal 4 (Hist):  k-NN Historical Error Proximity in [0, 1.00] (distance to E_train)       |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 6. COMPOSITE RISK SCORING & REVIEW ALLOCATION                                                     |
|    Scripts: src/15_four_factor_risk.py, src/25_final_strategy_comparison.py                       |
|    Formula: R = 0.35*u + 0.15*OOD + 0.25*Drift + 0.25*Hist  (Theoretical Max R = 0.825)           |
|    Strategies Evaluated: Random, Confidence-Only, OOD-Only, Static MultiFactor, Feedback-Adaptive |
|    Review Budgets: 1% (750 flows), 2% (1500 flows), 5% (3750 flows), 10% (7500 flows)             |
|    Key Phenomenon: Adaptive wins at 1% and 2%; Honest Crossover to Confidence at 5% and 10%       |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 7. SEQUENTIAL SIMULATED HUMAN FEEDBACK LOOP                                                       |
|    Script: src/28_sequential_feedback_eval.py -> results/sequential_feedback.csv                  |
|    ├── Partition Shifted Test into 5 Chronological Batches (15,000 flows each)                    |
|    ├── Rank by current weights & select top 150 flows (1% budget)                                 |
|    ├── REVEAL LABELS ONLY FOR REVIEWED FLOWS (Zero batch label leakage)                           |
|    ├── Calculate review precision: P_t = Errors_Found / 150                                       |
|    ├── Adapt weights for Batch t+1: w_hist <- min(0.40, w_hist * 1.15) if P_t > 0.40            |
|    └── Expand Error Memory with newly verified analyst corrections                                |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 8. EXTENDED STATISTICAL EVALUATION & VERIFICATION                                                 |
|    Scripts: src/29_extended_evaluation.py, src/30_verify_results.py                                |
|    ├── Benchmark: PR-AUC (0.7444), Balanced Acc (0.7321), ECE (0.0200)                            |
|    ├── Bootstrap: 1,000-resample 95% CI for Adaptive vs Confidence at 1%: [+3.45%, +5.28%]        |
|    ├── Signal Correlations: Spearman rho(OOD, Drift) = 0.8414; Pearson r(u, Hist) = 0.5531       |
|    └── Ablations: Dropping HistError collapses 1% error capture from 17.80% to 0.73%              |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 9. OPERATIONAL RESEARCH DASHBOARD (Streamlit Web UI)                                              |
|    Script: dashboard/app.py                                                                       |
|    ├── Interactive review budget slider (1%, 2%, 5%, 10%) & strategy filters                      |
|    ├── Real-time error capture comparisons & yield curves (errors per 1,000 reviews)              |
|    ├── Four signals diagnostic cards with explicit [0, 0.50] scaling rationale                     |
|    ├── Sequential 5-batch adaptation trace & weight progression chart                             |
|    └── Direct CSV data export for evaluators                                                      |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Distinguishing Implemented Stages vs. Phase-II Planned Extensions

### Implemented & Verified in Current Codebase (92.9% Progress)
- [x] Chronological data partitioning with zero temporal overlap.
- [x] Preprocessing pipelines fitted strictly on training data.
- [x] Supervised base model suite (XGBoost champion).
- [x] Four reliability signals ($u$, OOD, Drift, HistError) with empirical percentile bounds.
- [x] Composite risk scoring engine and deterministic tie-breaking.
- [x] Five-strategy comparative benchmark across 1%, 2%, 5%, and 10% budgets.
- [x] Sequential 5-batch online adaptation with post-selection label revelation.
- [x] Statistical validation: PR-AUC, Balanced Accuracy, ECE, and 1,000-sample bootstrap CIs.
- [x] Leave-one-out ablation studies proving necessity of historical error memory.
- [x] Interactive Streamlit research dashboard (`dashboard/app.py`).
- [x] Pytest automated test suite (13/13 passing assertions).

### Formally Scoped Phase-II Future Work
- [ ] **Streaming Probability Recalibration:** Online dynamic temperature scaling under non-stationary concept drift.
- [ ] **Explainable AI (XAI) UI Integration:** Local Tree-SHAP force plots for individual human review recommendations.
- [ ] **Automated Bilevel Meta-Optimization:** Online gradient-based signal weight adaptation.
- [ ] **Enterprise Multi-Tenant Cloud Deployment:** Cloud microservices architecture for multi-dataset ingestion across healthcare and finance.
