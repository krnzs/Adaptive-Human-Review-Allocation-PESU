# Fact Check for Documentation

F1: Train / validation / test attack counts and prevalence.
- Train: 350,000 rows, 21,344 attacks (6.10% prevalence).
- Validation: 75,000 rows, 248 attacks (0.33% prevalence).
- Test: 75,000 rows, 4,724 attacks (6.30% prevalence).
(Source: results/split_audit.csv)

F2: Source of the historical-error signal.
- Training errors. src/14_historical_error_risk.py compares XGBoost predictions on X_train against y_train, mapping the error rate across the top 10 drifted features.

F3: Mahalanobis settings.
- eps=1e-6 using pseudo-inverse on a random sample of 50,000 reference rows.
(Source: src/11_create_drift_risk.py)

F4: Streaming simulation, Parquet, Calibration.
- Streaming: No, strictly offline batches.
- Parquet: No, only CSV files are loaded/saved.
- Calibration: No calibration is applied to XGBoost raw predict_proba.
(Source: src/*.py)

F5: Dashboard components.
- The dashboard contains a budget slider, error-capture metrics, review-efficiency view, and drift viewer. [TO CONFIRM: confusion matrices, ROC curves].
(Source: dashboard/app.py)

F6: Port columns.
- Yes, L4_SRC_PORT and L4_DST_PORT are among the features.
(Source: results/X_train.csv)

F7: Label leakage.
- No adaptive-weight or regime-threshold logic uses test labels before the corresponding review event. Strictly decoupled.
(Source: LEAKAGE_AUDIT.md, src/28_sequential_feedback_eval.py)
