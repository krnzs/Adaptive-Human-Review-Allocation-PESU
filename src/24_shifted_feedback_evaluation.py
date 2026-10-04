import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# SHIFTED-TEST FEEDBACK-INFORMED EVALUATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ------------------------------------------------------------
# Load shifted-test signals
# ------------------------------------------------------------

df = pd.read_csv(
    RESULTS_DIR / "shifted_test_all_signals.csv"
)

# ------------------------------------------------------------
# Required columns
# ------------------------------------------------------------

required = [
    "actual_error",
    "confidence",
    "ood_percentile",
    "drift_risk",
    "historical_error_risk"
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )

# ------------------------------------------------------------
# Risk components
# ------------------------------------------------------------

df["confidence_risk"] = 1 - df["confidence"]

df["historical_risk"] = (
    df["historical_error_risk"]
    .rank(pct=True)
)

# ------------------------------------------------------------
# Feedback-informed adaptive score
#
# Validation feedback showed that historical-error
# information is useful, so we increase its influence
# compared with the original adaptive configuration.
#
# These are transparent heuristic weights.
# ------------------------------------------------------------

weights = {
    "confidence": 0.35,
    "ood": 0.15,
    "drift": 0.25,
    "historical": 0.25
}

df["feedback_adaptive_score"] = (
    weights["confidence"] * df["confidence_risk"]
    + weights["ood"] * df["ood_percentile"]
    + weights["drift"] * df["drift_risk"]
    + weights["historical"] * df["historical_risk"]
)

# ------------------------------------------------------------
# Evaluation budgets
# ------------------------------------------------------------

budgets = [0.01, 0.02, 0.05, 0.10]

results = []

total_predictions = len(df)
total_errors = int(df["actual_error"].sum())

# ------------------------------------------------------------
# Evaluate adaptive strategy
# ------------------------------------------------------------

for budget in budgets:

    review_count = int(
        total_predictions * budget
    )

    reviewed = (
        df.sort_values(
            "feedback_adaptive_score",
            ascending=False
        )
        .head(review_count)
    )

    errors_caught = int(
        reviewed["actual_error"].sum()
    )

    capture = (
        errors_caught / total_errors * 100
        if total_errors > 0 else 0
    )

    efficiency = (
        errors_caught / review_count * 1000
        if review_count > 0 else 0
    )

    results.append({
        "strategy": "Feedback_Adaptive",
        "review_budget_percent": budget * 100,
        "reviews": review_count,
        "errors_caught": errors_caught,
        "total_errors": total_errors,
        "error_capture_percent": capture,
        "errors_per_1000_reviews": efficiency
    })

# ------------------------------------------------------------
# Save results
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

output_file = (
    RESULTS_DIR /
    "shifted_feedback_adaptive_results.csv"
)

results_df.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("=" * 70)
print("FEEDBACK-INFORMED ADAPTIVE EVALUATION")
print("=" * 70)

print(
    f"Shifted-test predictions : {total_predictions:,}"
)

print(
    f"Shifted-test errors      : {total_errors:,}"
)

print("\nWeights used:")
for name, value in weights.items():
    print(f"  {name:12s}: {value:.2f}")

print("\nResults:")
print(
    results_df[
        [
            "strategy",
            "review_budget_percent",
            "reviews",
            "errors_caught",
            "error_capture_percent",
            "errors_per_1000_reviews"
        ]
    ].to_string(index=False)
)

print(f"\nSaved to: {output_file}")
print("=" * 70)