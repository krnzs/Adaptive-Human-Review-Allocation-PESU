import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier


# ============================================================
# LOAD DATA
# ============================================================

print("Loading preprocessed data...")

X_train = pd.read_csv("results/X_train.csv")
y_train = pd.read_csv("results/y_train.csv").squeeze()

X_validation = pd.read_csv("results/X_validation.csv")
y_validation = pd.read_csv("results/y_validation.csv").squeeze()


print("Training:", X_train.shape)
print("Validation:", X_validation.shape)


# ============================================================
# SCALE DATA FOR LOGISTIC REGRESSION
# ============================================================

print("\nScaling data for Logistic Regression...")

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_validation_scaled = scaler.transform(X_validation)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)


# ============================================================
# MODEL 1 — LOGISTIC REGRESSION
# ============================================================

print("\n================================")
print("MODEL 1: LOGISTIC REGRESSION")
print("================================")

logistic = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

logistic.fit(
    X_train_scaled,
    y_train
)

logistic_pred = logistic.predict(
    X_validation_scaled
)

logistic_prob = logistic.predict_proba(
    X_validation_scaled
)[:, 1]


# ============================================================
# MODEL 2 — RANDOM FOREST
# ============================================================

print("\n================================")
print("MODEL 2: RANDOM FOREST")
print("================================")

random_forest = RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    n_jobs=-1,
    class_weight="balanced",
    random_state=42
)

random_forest.fit(
    X_train,
    y_train
)

rf_pred = random_forest.predict(
    X_validation
)

rf_prob = random_forest.predict_proba(
    X_validation
)[:, 1]


# ============================================================
# MODEL 3 — XGBOOST
# ============================================================

print("\n================================")
print("MODEL 3: XGBOOST")
print("================================")

xgb = XGBClassifier(
    n_estimators=150,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42,
    n_jobs=4
)

xgb.fit(
    X_train,
    y_train
)

xgb_pred = xgb.predict(
    X_validation
)

xgb_prob = xgb.predict_proba(
    X_validation
)[:, 1]


# ============================================================
# EVALUATION FUNCTION
# ============================================================

def evaluate_model(name, y_true, predictions, probabilities):

    results = {
        "Model": name,
        "Accuracy": accuracy_score(
            y_true,
            predictions
        ),
        "Precision": precision_score(
            y_true,
            predictions,
            zero_division=0
        ),
        "Recall": recall_score(
            y_true,
            predictions,
            zero_division=0
        ),
        "F1": f1_score(
            y_true,
            predictions,
            zero_division=0
        ),
        "ROC_AUC": roc_auc_score(
            y_true,
            probabilities
        )
    }

    return results


# ============================================================
# COMPARE MODELS
# ============================================================

results = []

results.append(
    evaluate_model(
        "Logistic Regression",
        y_validation,
        logistic_pred,
        logistic_prob
    )
)

results.append(
    evaluate_model(
        "Random Forest",
        y_validation,
        rf_pred,
        rf_prob
    )
)

results.append(
    evaluate_model(
        "XGBoost",
        y_validation,
        xgb_pred,
        xgb_prob
    )
)


results_df = pd.DataFrame(results)


# ============================================================
# SAVE MODELS
# ============================================================

joblib.dump(
    logistic,
    "models/logistic_regression.pkl"
)

joblib.dump(
    random_forest,
    "models/random_forest.pkl"
)

joblib.dump(
    xgb,
    "models/xgboost.pkl"
)


# ============================================================
# SAVE RESULTS
# ============================================================

results_df.to_csv(
    "results/model_comparison.csv",
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("\n================================")
print("MODEL COMPARISON")
print("================================")

print(
    results_df.to_string(
        index=False
    )
)

print("\nModels saved in models/")
print("Results saved in results/model_comparison.csv")