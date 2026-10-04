import pandas as pd
import numpy as np

FILE = "results/shifted_test_all_signals.csv"

OUTPUT = "results/dynamic_adaptive_results.csv"

df = pd.read_csv(FILE)

print("Loading shifted test signals...")
print("Rows:", len(df))


# ============================================
# SIGNALS
# ============================================

df["confidence_risk"] = (
    1 - df["confidence"]
)

df["ood_risk"] = (
    df["ood_percentile"]
)

df["drift_risk_signal"] = (
    df["drift_risk"]
)

df["historical_risk"] = (
    df["historical_error_percentile"]
)


# ============================================
# CURRENT ENVIRONMENT DRIFT
# ============================================

# This represents the current distribution
# observed by the allocation system.

environment_drift = (
    df["drift_risk_signal"].mean()
)

print(
    "\nCurrent environment drift:",
    round(environment_drift, 4)
)


# ============================================
# DYNAMIC REGIME
# ============================================

if environment_drift < 0.40:

    regime = "LOW"

elif environment_drift < 0.60:

    regime = "MODERATE"

else:

    regime = "HIGH"


print(
    "Detected drift regime:",
    regime
)


# ============================================
# ADAPTIVE WEIGHTS
# ============================================

if regime == "LOW":

    confidence_weight = 0.70
    ood_weight = 0.10
    drift_weight = 0.10
    historical_weight = 0.10


elif regime == "MODERATE":

    confidence_weight = 0.50
    ood_weight = 0.15
    drift_weight = 0.25
    historical_weight = 0.10


else:

    confidence_weight = 0.35
    ood_weight = 0.20
    drift_weight = 0.30
    historical_weight = 0.15


print("\n================================")
print("DYNAMIC ADAPTIVE WEIGHTS")
print("================================")

print(
    "Confidence:",
    confidence_weight
)

print(
    "OOD:",
    ood_weight
)

print(
    "Drift:",
    drift_weight
)

print(
    "Historical error:",
    historical_weight
)


# ============================================
# DYNAMIC RISK SCORE
# ============================================

df["dynamic_risk_score"] = (

    confidence_weight
    * df["confidence_risk"]

    +

    ood_weight
    * df["ood_risk"]

    +

    drift_weight
    * df["drift_risk_signal"]

    +

    historical_weight
    * df["historical_risk"]
)


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [
    0.01,
    0.02,
    0.05,
    0.10
]

total_errors = (
    df["actual_error"].sum()
)

results = []


print("\n================================")
print("DYNAMIC ADAPTIVE REVIEW")
print("================================")

print(
    "Total errors:",
    total_errors
)


for budget in budgets:

    review_count = int(
        len(df) * budget
    )

    review_df = (
        df
        .sort_values(
            by="dynamic_risk_score",
            ascending=False
        )
        .head(review_count)
    )

    errors_caught = (
        review_df["actual_error"].sum()
    )

    capture_rate = (
        errors_caught / total_errors
    )

    results.append({

        "regime": regime,

        "review_budget_percent":
            budget * 100,

        "predictions_reviewed":
            review_count,

        "errors_caught":
            int(errors_caught),

        "error_capture_percent":
            capture_rate * 100
    })


# ============================================
# RESULTS
# ============================================

result_df = pd.DataFrame(
    results
)

print("\nResults:")

print(
    result_df.to_string(
        index=False
    )
)


# ============================================
# SAVE
# ============================================

result_df.to_csv(
    OUTPUT,
    index=False
)

df.to_csv(
    "results/shifted_dynamic_signals.csv",
    index=False
)


print("\nSaved to:")
print(OUTPUT)