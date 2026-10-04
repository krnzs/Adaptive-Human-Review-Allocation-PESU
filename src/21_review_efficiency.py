import pandas as pd

FILE = "results/shifted_test_all_signals.csv"

df = pd.read_csv(FILE)

total_errors = df["actual_error"].sum()

print("Total errors:", total_errors)


# ============================================
# SIGNALS
# ============================================

df["confidence_risk"] = 1 - df["confidence"]

df["ood_risk"] = df["ood_percentile"]

df["drift_risk"] = df["drift_risk"]

df["historical_risk"] = (
    df["historical_error_percentile"]
)


# Static multi-factor
df["static_score"] = (
    0.40 * df["confidence_risk"]
    + 0.15 * df["ood_risk"]
    + 0.20 * df["drift_risk"]
    + 0.25 * df["historical_risk"]
)


# Dynamic adaptive
df["dynamic_score"] = (
    0.50 * df["confidence_risk"]
    + 0.15 * df["ood_risk"]
    + 0.25 * df["drift_risk"]
    + 0.10 * df["historical_risk"]
)


# ============================================
# STRATEGIES
# ============================================

strategies = {

    "Random": None,

    "Confidence":
        "confidence_risk",

    "OOD":
        "ood_risk",

    "Static_MultiFactor":
        "static_score",

    "Dynamic_Adaptive":
        "dynamic_score"
}


budgets = [
    0.01,
    0.02,
    0.05,
    0.10
]


results = []


# ============================================
# EVALUATION
# ============================================

for budget in budgets:

    review_count = int(
        len(df) * budget
    )

    for strategy, signal in strategies.items():

        if strategy == "Random":

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

        errors_caught = int(
            review_df["actual_error"].sum()
        )

        errors_per_1000 = (
            errors_caught
            / review_count
            * 1000
        )

        capture_rate = (
            errors_caught
            / total_errors
            * 100
        )

        results.append({

            "strategy":
                strategy,

            "review_budget_percent":
                budget * 100,

            "reviews":
                review_count,

            "errors_caught":
                errors_caught,

            "error_capture_percent":
                capture_rate,

            "errors_per_1000_reviews":
                errors_per_1000
        })


# ============================================
# RESULTS
# ============================================

results_df = pd.DataFrame(results)

print("\n================================")
print("REVIEW EFFICIENCY")
print("================================")

print(
    results_df.to_string(
        index=False
    )
)


print("\n================================")
print("ERRORS PER 1000 REVIEWS")
print("================================")

pivot = results_df.pivot(
    index="review_budget_percent",
    columns="strategy",
    values="errors_per_1000_reviews"
)

print(
    pivot.round(2).to_string()
)


# ============================================
# SAVE
# ============================================

results_df.to_csv(
    "results/review_efficiency.csv",
    index=False
)

print(
    "\nSaved to:"
)

print(
    "results/review_efficiency.csv"
)