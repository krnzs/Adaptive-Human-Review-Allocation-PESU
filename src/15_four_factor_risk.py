import pandas as pd

FILE = "results/validation_signals_historical.csv"
OUTPUT_FILE = "results/four_factor_risk_signals.csv"

df = pd.read_csv(FILE)

print("Loading signals...")
print("Rows:", len(df))


# ============================================
# NORMALIZED SIGNALS
# ============================================

confidence_risk = 1 - df["confidence"]
ood_risk = df["ood_percentile"]
drift_risk = df["drift_risk"]
historical_risk = df["historical_error_percentile"]


# ============================================
# FOUR-FACTOR SCORE
# ============================================

df["four_factor_score"] = (
    0.40 * confidence_risk
    + 0.15 * ood_risk
    + 0.20 * drift_risk
    + 0.25 * historical_risk
)


# ============================================
# RANK
# ============================================

df["four_factor_percentile"] = (
    df["four_factor_score"].rank(pct=True)
)


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [0.01, 0.02, 0.05, 0.10]

results = []

total_errors = df["actual_error"].sum()

print("\n================================")
print("FOUR-FACTOR REVIEW STRATEGY")
print("================================")

print("Total actual errors:", total_errors)


for budget in budgets:

    review_count = int(len(df) * budget)

    review_df = df.sort_values(
        by="four_factor_score",
        ascending=False
    ).head(review_count)

    errors_caught = review_df["actual_error"].sum()

    error_capture_rate = (
        errors_caught / total_errors
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

result_df.to_csv(
    "results/four_factor_review_results.csv",
    index=False
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSaved results to:")
print("results/four_factor_review_results.csv")

print("\nSaved enriched signals to:")
print(OUTPUT_FILE)