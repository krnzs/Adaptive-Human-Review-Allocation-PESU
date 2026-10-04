import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# ADAPTIVE HUMAN-REVIEW ALLOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ------------------------------------------------------------
# Load adaptive risk signals
# ------------------------------------------------------------

df = pd.read_csv(
    RESULTS_DIR / "adaptive_risk_signals.csv"
)

# ------------------------------------------------------------
# Review budgets
# ------------------------------------------------------------

budgets = [0.01, 0.02, 0.05, 0.10]

results = []

total_predictions = len(df)
total_errors = df["actual_error"].sum()

# ------------------------------------------------------------
# Allocate human review
# ------------------------------------------------------------

for budget in budgets:

    review_count = int(total_predictions * budget)

    # Highest-risk predictions receive human review
    review_queue = df.sort_values(
        "adaptive_risk_score",
        ascending=False
    ).head(review_count)

    errors_caught = review_queue["actual_error"].sum()

    error_capture = (
        errors_caught / total_errors * 100
        if total_errors > 0 else 0
    )

    errors_per_1000 = (
        errors_caught / review_count * 1000
        if review_count > 0 else 0
    )

    results.append({
        "review_budget_percent": budget * 100,
        "reviews": review_count,
        "errors_caught": int(errors_caught),
        "total_errors": int(total_errors),
        "error_capture_percent": error_capture,
        "errors_per_1000_reviews": errors_per_1000
    })

# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

output_file = (
    RESULTS_DIR / "adaptive_review_results.csv"
)

results_df.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("=" * 65)
print("ADAPTIVE HUMAN-REVIEW ALLOCATION")
print("=" * 65)

print(f"Total predictions : {total_predictions:,}")
print(f"Total errors      : {total_errors:,}")

print("\nReview performance:")
print(
    results_df[
        [
            "review_budget_percent",
            "reviews",
            "errors_caught",
            "error_capture_percent",
            "errors_per_1000_reviews"
        ]
    ].to_string(index=False)
)

print(f"\nSaved to: {output_file}")
print("=" * 65)