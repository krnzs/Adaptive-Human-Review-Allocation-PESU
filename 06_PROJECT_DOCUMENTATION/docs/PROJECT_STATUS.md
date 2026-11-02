# Project Status Report

**Project Title:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty  
**SRN:** `PES1PG25CA101`  
**Degree Programme:** Master of Computer Applications (Data Analytics)  
**Institution:** Department of Computer Applications, PES University, Bengaluru  
**Faculty Guide:** Dilip Kumar Maripuri  
**Review Milestone:** Phase-I Review-II Final Status  

---

## 1. Mandatory Implementation Status Statement

> **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**

---

## 2. Functional Requirements Status Matrix

| ID | Functional Requirement | Status | Implementation Evidence |
| :---: | :--- | :---: | :--- |
| **FR01** | Chronological Data Partitioning (70/15/15) | **Completed** | `src/02_create_splits.py`, `src/27_split_audit.py`, `tests/test_splits_and_leakage.py` |
| **FR02** | Training-Only Feature Preprocessing | **Completed** | `src/03_preprocess.py`, `models/preprocessor.joblib` |
| **FR03** | Supervised Base Model Suite (XGBoost, RF, LR) | **Completed** | `src/04_train_models.py`, `models/xgb_model.joblib`, `results/model_comparison.csv` |
| **FR04** | Prediction Uncertainty Signal Generation | **Completed** | `src/05_generate_prediction_signals.py` ($u = 1 - \max(P_0, P_1) \in [0, 0.50]$) |
| **FR05** | Confidence-Only Review Strategy Implementation | **Completed** | `src/06_confidence_review_strategy.py`, `results/confidence_review_results.csv` |
| **FR06** | Mahalanobis Out-of-Distribution Signal | **Completed** | `src/07_ood_detection.py`, `results/shifted_test_all_signals.csv` |
| **FR07** | OOD-Only Review Strategy Implementation | **Completed** | `src/08_ood_review_strategy.py`, `results/ood_review_results.csv` |
| **FR08** | Feature-Level PSI Drift Measurement | **Completed** | `src/10_measure_drift.py`, `results/drift_results.csv` |
| **FR09** | Instance-Level Drift-Risk Mapping | **Completed** | `src/11_create_drift_risk.py`, `results/shifted_test_all_signals.csv` |
| **FR10** | Historical Error Proximity Memory Signal | **Completed** | `src/14_historical_error_risk.py`, `src/28_historical_variants.py` |
| **FR11** | Four-Factor Static Multi-Factor Strategy | **Completed** | `src/15_four_factor_risk.py`, `results/static_multifactor_results.csv` |
| **FR12** | Multi-Budget Shifted Test Evaluation (1%, 2%, 5%, 10%) | **Completed** | `src/25_final_strategy_comparison.py`, `results/final_shifted_strategy_comparison.csv` |
| **FR13** | Sequential Simulated Human Feedback & Adaptation | **Completed** | `src/28_sequential_feedback_eval.py`, `results/sequential_feedback.csv` |
| **FR14** | Multi-Dataset Web Portal & Cross-Domain Deployment | **Partially Implemented** | Implemented as local Streamlit interactive dashboard (`dashboard/app.py`) for NF-UQ-NIDS-v2; multi-tenant cloud ingestion & medical/financial cross-domain deployment formally deferred to Phase-II. |

---

## 3. Verified Experimental Benchmark Summary

- **Total Shifted Test Flows:** 75,000  
- **Total Shifted Test Prediction Errors:** 3,427 (Error rate: 4.569%)  
- **Total Validation Prediction Errors:** 753 (Error rate: 1.004%)  
- **Distribution Shift Impact Ratio:** Test error rate is $4.55\times$ higher than validation.  

### Five-Strategy Review Allocation Table

```
+-------------------------------------------------------------------------------------------------+
| Strategy                 | 1% Budget (750)  | 2% Budget (1500) | 5% Budget (3750) | 10% (7500)  |
+-------------------------------------------------------------------------------------------------+
| Random Baseline          |   40 ( 1.17%)    |   73 ( 2.13%)    |  189 ( 5.52%)    |  340 ( 9.92%)|
| Mahalanobis OOD-Only     |    1 ( 0.03%)    |    9 ( 0.26%)    |   12 ( 0.35%)    |   12 ( 0.35%)|
| Confidence-Only          |  463 (13.51%)    |  916 (26.73%)    | 2243 (65.45%)*   | 2879 (84.01%)*|
| Static Multi-Factor      |  600 (17.51%)    | 1165 (33.99%)    | 1870 (54.57%)    | 2242 (65.42%)|
| Feedback-Adaptive        |  610 (17.80%)*   | 1174 (34.26%)*   | 1573 (45.90%)    | 1794 (52.35%)|
+-------------------------------------------------------------------------------------------------+
* Winning strategy at each budget.
```

### Key Analytical Findings
1. **Adaptive Advantage at Restricted Budgets:** At 1% budget, Feedback-Adaptive captures 610 errors vs. 463 for Confidence-Only (**+31.7% relative gain**, 95% Bootstrap CI: [+3.45%, +5.28%]).
2. **The Honest Crossover:** Confidence-Only overtakes Adaptive allocation at 5% (2,243 vs. 1,573) and 10% (2,879 vs. 1,794) because broad inspection budgets sweep borderline classifications directly.
3. **Signal Redundancy:** OOD and Drift are strongly rank-correlated ($\rho = 0.8414$, shared variance $>70\%$), forming a *Distribution Shift Detector* cluster.
4. **Ablation Criticality:** Removing Historical Error proximity collapses 1% error capture from 17.80% down to 0.73% (25 errors), confirming its role as an error-targeting spatial filter.

---

## 4. Phase-II Planned Extensions (Not Part of Current Review)
The following features are formally designated as future research:
1. Streaming post-hoc probability recalibration (adaptive Platt scaling under active concept drift).
2. Local Tree-SHAP feature attributions integrated into the analyst review UI.
3. Bilevel meta-learning for online dynamic weight optimization.
4. Enterprise cloud multi-tenant deployment across non-network datasets (healthcare, finance).
