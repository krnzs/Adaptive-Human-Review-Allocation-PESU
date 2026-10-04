import pandas as pd
import numpy as np

FILE = "results/shifted_test_all_signals.csv"

OUTPUT = "results/shifted_review_comparison.csv"

df = pd.read_csv(FILE)

print("Loading shifted test signals...")
print("Rows:", len(df))


# ============================================
# REVIEW BUDGETS
# ============================================

budgets = [0.01, 0.02, 0.05, 0.10]

total_errors = df["actual_error"].sum()

print("\n================================")
print("SHIFTED TEST REVIEW COMPARISON")
print("================================")

print("Total errors:", total_errors)


# ============================================
# CREATE RISK SIGNALS
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


# Static four-factor score
df["four_factor_score"] = (
    0.40 * df["confidence_risk"]
    + 0.15 * df["ood_risk"]
    + 0.20 * df["drift_risk_signal"]
    + 0.25 * df["historical_risk"]
)


# ============================================
# STRATEGIES
# ============================================

strategies = {

    "Random": None,

    "Confidence": "confidence_risk",

    "OOD": "ood_risk",

    "Static_MultiFactor": "four_factor_score"
}


results = []


# ============================================
# EVALUATE
# ============================================

for budget in budgets:

    review_count = int(
        len(df) * budget
    )

    for strategy, signal in strategies.items():

        if strategy == "Random":

            # Fixed random seed for reproducibility
            review_df = df.sample(
                n=review_count,
                random_state=42
            )

        else:

            review_df = (
                df
                .sort_values(
                    by=signal,
                    ascending=False
                )
                .head(review_count)
            )

        errors_caught = (
            review_df["actual_error"].sum()
        )

        capture_rate = (
            errors_caught / total_errors
            if total_errors > 0
            else 0
        )

        results.append({

            "strategy": strategy,

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

results_df = pd.DataFrame(results)

print("\nResults:")

print(
    results_df.to_string(
        index=False
    )
)


# ============================================
# PIVOT TABLE
# ============================================

pivot = results_df.pivot(
    index="review_budget_percent",
    columns="strategy",
    values="error_capture_percent"
)

print("\n================================")
print("ERROR CAPTURE COMPARISON")
print("================================")

print(
    pivot.round(2).to_string()
)


# ============================================
# SAVE
# ============================================

results_df.to_csv(
    OUTPUT,
    index=False
)

print("\nSaved to:")
print(OUTPUT)