import pandas as pd
import numpy as np

FILE = "results/validation_signals.csv"

df = pd.read_csv(FILE)

print("Loading prediction signals...")
print("Rows:", len(df))


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [0.01, 0.02, 0.05, 0.10]


# ============================================
# CONFIDENCE-BASED REVIEW
# ============================================

results = []

total_errors = df["actual_error"].sum()

print("\n================================")
print("CONFIDENCE-BASED REVIEW")
print("================================")

print("Total actual errors:", total_errors)


for budget in budgets:

    review_count = int(len(df) * budget)

    # Lowest confidence predictions are reviewed first
    review_df = df.sort_values(
        by="confidence",
        ascending=True
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
# DISPLAY RESULTS
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

OUTPUT = "results/confidence_review_results.csv"

result_df.to_csv(
    OUTPUT,
    index=False
)

print("\nSaved to:")
print(OUTPUT)