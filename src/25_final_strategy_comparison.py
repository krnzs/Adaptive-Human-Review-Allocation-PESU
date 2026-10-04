import pandas as pd
from pathlib import Path

# ============================================================
# FINAL STRATEGY COMPARISON
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ------------------------------------------------------------
# Load original strategies
# ------------------------------------------------------------

comparison = pd.read_csv(
    RESULTS_DIR / "shifted_review_comparison.csv"
)

# Original file contains:
# strategy
# review_budget_percent
# errors_caught
# error_capture_percent

original = comparison[
    [
        "strategy",
        "review_budget_percent",
        "errors_caught",
        "error_capture_percent"
    ]
].copy()

# Calculate efficiency
original["reviews"] = (
    len(pd.read_csv(
        RESULTS_DIR / "shifted_test_all_signals.csv"
    ))
    * original["review_budget_percent"] / 100
).astype(int)

original["errors_per_1000_reviews"] = (
    original["errors_caught"]
    / original["reviews"]
    * 1000
)

# ------------------------------------------------------------
# Load feedback-adaptive strategy
# ------------------------------------------------------------

feedback = pd.read_csv(
    RESULTS_DIR / "shifted_feedback_adaptive_results.csv"
)

feedback = feedback[
    [
        "strategy",
        "review_budget_percent",
        "reviews",
        "errors_caught",
        "error_capture_percent",
        "errors_per_1000_reviews"
    ]
].copy()

# ------------------------------------------------------------
# Combine
# ------------------------------------------------------------

final = pd.concat(
    [original, feedback],
    ignore_index=True
)

# ------------------------------------------------------------
# Strategy order
# ------------------------------------------------------------

strategy_order = [
    "Random",
    "Confidence",
    "OOD",
    "Static_MultiFactor",
    "Feedback_Adaptive"
]

final["strategy"] = pd.Categorical(
    final["strategy"],
    categories=strategy_order,
    ordered=True
)

final = final.sort_values(
    ["review_budget_percent", "strategy"]
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_file = (
    RESULTS_DIR /
    "final_shifted_strategy_comparison.csv"
)

final.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("=" * 80)
print("FINAL SHIFTED-TEST STRATEGY COMPARISON")
print("=" * 80)

print(
    final.to_string(index=False)
)

print("\n" + "=" * 80)
print("ERROR CAPTURE BY REVIEW BUDGET")
print("=" * 80)

for budget in sorted(
    final["review_budget_percent"].unique()
):

    subset = final[
        final["review_budget_percent"] == budget
    ]

    print(f"\nReview budget: {budget:.0f}%")

    print(
        subset[
            [
                "strategy",
                "reviews",
                "errors_caught",
                "error_capture_percent",
                "errors_per_1000_reviews"
            ]
        ].to_string(index=False)
    )

print(f"\nSaved to: {output_file}")
print("=" * 80)