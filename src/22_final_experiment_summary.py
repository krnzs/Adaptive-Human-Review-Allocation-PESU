import pandas as pd

# ============================================
# LOAD RESULTS
# ============================================

review = pd.read_csv(
    "results/review_efficiency.csv"
)

# ============================================
# SELECT FINAL COLUMNS
# ============================================

final = review[
    [
        "strategy",
        "review_budget_percent",
        "reviews",
        "errors_caught",
        "error_capture_percent",
        "errors_per_1000_reviews"
    ]
].copy()


# ============================================
# ROUND VALUES
# ============================================

final["error_capture_percent"] = (
    final["error_capture_percent"].round(2)
)

final["errors_per_1000_reviews"] = (
    final["errors_per_1000_reviews"].round(2)
)


# ============================================
# SAVE
# ============================================

OUTPUT = (
    "results/final_experiment_summary.csv"
)

final.to_csv(
    OUTPUT,
    index=False
)


# ============================================
# DISPLAY
# ============================================

print("\n================================")
print("FINAL EXPERIMENT SUMMARY")
print("================================")

print(
    final.to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT)