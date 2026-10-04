import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# HUMAN-REVIEW FEEDBACK LOOP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ------------------------------------------------------------
# Load adaptive signals
# ------------------------------------------------------------

df = pd.read_csv(
    RESULTS_DIR / "adaptive_risk_signals.csv"
)

# ------------------------------------------------------------
# Simulated human-review budgets
# ------------------------------------------------------------

budgets = [0.01, 0.02, 0.05, 0.10]

results = []

# ------------------------------------------------------------
# Baseline historical error rate
# ------------------------------------------------------------

baseline_error_rate = df["actual_error"].mean()

print("=" * 70)
print("HUMAN-REVIEW FEEDBACK LOOP")
print("=" * 70)

print(
    f"Baseline prediction error rate: "
    f"{baseline_error_rate * 100:.4f}%"
)

# ------------------------------------------------------------
# Simulate review → feedback → historical update
# ------------------------------------------------------------

for budget in budgets:

    review_count = int(len(df) * budget)

    # Highest-risk predictions are reviewed
    reviewed = (
        df.sort_values(
            "adaptive_risk_score",
            ascending=False
        )
        .head(review_count)
        .copy()
    )

    # Ground truth acts as the simulated review outcome
    reviewed["review_confirmed_error"] = (
        reviewed["actual_error"]
    )

    errors_found = int(
        reviewed["review_confirmed_error"].sum()
    )

    reviewed_error_rate = (
        errors_found / review_count
        if review_count > 0 else 0
    )

    # --------------------------------------------------------
    # Estimate error concentration
    # --------------------------------------------------------

    error_concentration = (
        reviewed_error_rate / baseline_error_rate
        if baseline_error_rate > 0 else 0
    )

    # --------------------------------------------------------
    # Simulated feedback update
    #
    # Cases identified as errors receive increased
    # historical-error importance.
    # --------------------------------------------------------

    feedback_strength = min(
        error_concentration,
        5.0
    )

    updated_historical_weight = (
        0.20 * (1 + 0.10 * feedback_strength)
    )

    # Keep weight bounded
    updated_historical_weight = min(
        updated_historical_weight,
        0.35
    )

    results.append({
        "review_budget_percent": budget * 100,
        "reviews": review_count,
        "errors_found": errors_found,
        "reviewed_error_rate_percent":
            reviewed_error_rate * 100,
        "baseline_error_rate_percent":
            baseline_error_rate * 100,
        "error_concentration":
            error_concentration,
        "updated_historical_weight":
            updated_historical_weight
    })

# ------------------------------------------------------------
# Save feedback results
# ------------------------------------------------------------

results_df = pd.DataFrame(results)

output_file = (
    RESULTS_DIR / "review_feedback_results.csv"
)

results_df.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("\nFeedback results:")
print(
    results_df.to_string(index=False)
)

print(f"\nSaved to: {output_file}")
print("=" * 70)