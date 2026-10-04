import pandas as pd

FILE = "results/shifted_test_all_signals.csv"

OUTPUT = "results/adaptive_shifted_review_results.csv"

df = pd.read_csv(FILE)

print("Loading shifted test signals...")
print("Rows:", len(df))


# ============================================
# RISK SIGNALS
# ============================================

confidence_risk = 1 - df["confidence"]

ood_risk = df["ood_percentile"]

drift_risk = df["drift_risk"]

historical_risk = df[
    "historical_error_percentile"
]


# ============================================
# ADAPTIVE SCORE
# ============================================

# Weights learned from the validation environment.
# They are NOT recalculated using shifted-test labels.

confidence_weight = 0.5437
ood_weight = 0.1812
drift_weight = 0.2750

# Historical error was not part of the original
# adaptive score, so we first test the same
# adaptive mechanism on shifted data.

df["adaptive_risk_score"] = (
    confidence_weight * confidence_risk
    + ood_weight * ood_risk
    + drift_weight * drift_risk
)


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [0.01, 0.02, 0.05, 0.10]

total_errors = df["actual_error"].sum()

results = []


print("\n================================")
print("ADAPTIVE SHIFTED-TEST REVIEW")
print("================================")

print("Total errors:", total_errors)


for budget in budgets:

    review_count = int(
        len(df) * budget
    )

    review_df = (
        df
        .sort_values(
            by="adaptive_risk_score",
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
# DISPLAY
# ============================================

result_df = pd.DataFrame(results)

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

print("\nSaved to:")
print(OUTPUT)