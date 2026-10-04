import pandas as pd
import numpy as np

FILE = "results/validation_signals_ood.csv"

df = pd.read_csv(FILE)

print("Loading prediction signals...")
print("Rows:", len(df))


# ============================================
# NORMALIZE SIGNALS
# ============================================

# Confidence risk:
# Low confidence = higher risk

df["confidence_risk"] = 1 - df["confidence"]


# OOD risk is already represented as a percentile
df["ood_risk"] = df["ood_percentile"]


# ============================================
# STATIC MULTI-FACTOR SCORE
# ============================================

# Equal weighting for the first baseline

df["risk_score"] = (
    0.50 * df["confidence_risk"]
    + 0.50 * df["ood_risk"]
)


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [0.01, 0.02, 0.05, 0.10]

results = []

total_errors = df["actual_error"].sum()

print("\n================================")
print("STATIC MULTI-FACTOR REVIEW")
print("================================")

print("Total actual errors:", total_errors)


for budget in budgets:

    review_count = int(len(df) * budget)

    # Highest risk reviewed first
    review_df = df.sort_values(
        by="risk_score",
        ascending=False
    ).head(review_count)

    errors_caught = review_df["actual_error"].sum()

    error_capture_rate = (
        errors_caught / total_errors
        if total_errors > 0
        else 0
    )

    results.append({
        "review_budget": budget,
        "predictions_reviewed": review_count,
        "errors_caught": int(errors_caught),
        "error_capture_rate": error_capture_rate
    })


# ============================================
# RESULTS
# ============================================

result_df = pd.DataFrame(results)

result_df["review_budget_percent"] = (
    result_df["review_budget"] * 100
)

result_df["error_capture_percent"] = (
    result_df["error_capture_rate"] * 100
)


print("\nResults:")

print(
    result_df[
        [
            "review_budget_percent",
            "predictions_reviewed",
            "errors_caught",
            "error_capture_percent"
        ]
    ].to_string(index=False)
)


# ============================================
# SAVE
# ============================================

OUTPUT = "results/static_multifactor_results.csv"

result_df.to_csv(
    OUTPUT,
    index=False
)

df.to_csv(
    "results/validation_signals_multifactor.csv",
    index=False
)

print("\nSaved results to:")
print(OUTPUT)

print("\nSaved enriched signals to:")
print("results/validation_signals_multifactor.csv")