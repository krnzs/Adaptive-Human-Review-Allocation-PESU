# Extended Evaluation Summary

## 1. Model Metrics
Generated in \esults/extended_model_metrics.csv\. Included ROC-AUC, PR-AUC, Balanced Accuracy, Precision, Recall, F1, and ECE (Expected Calibration Error).
The XGBoost model demonstrates stable but imperfect calibration across the shift, motivating the use of multiple signals.

## 2. Strategy & Budget Evaluations
Generated in \esults/extended_strategy_eval.csv\. We evaluated the following strategies:
- Random, Confidence, OOD, Drift, History
- Static (equal weight)
- Adaptive (feedback-informed weights)
- Ablation variants (leave-one-out for all signals)
- Rank-normalised adaptive combination

Metrics included:
- Errors caught and error capture %
- FN/FP captured
- Attack-class rows captured
- Review efficiency

## 3. Bootstrap 95% CIs
Bootstrapped (N=1000) 95% Confidence Intervals are generated in \esults/extended_bootstrap_cis.csv\ comparing the Adaptive strategy against Static and Confidence baselines.
