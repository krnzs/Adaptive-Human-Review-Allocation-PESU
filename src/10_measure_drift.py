import pandas as pd
import numpy as np

# ============================================
# PATHS
# ============================================

TRAIN_FILE = "results/X_train.csv"
VALIDATION_FILE = "results/X_validation.csv"

OUTPUT_FILE = "results/drift_results.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading training data...")
X_train = pd.read_csv(TRAIN_FILE)

print("Training shape:", X_train.shape)

print("\nLoading validation data...")
X_validation = pd.read_csv(VALIDATION_FILE)

print("Validation shape:", X_validation.shape)


# ============================================
# PSI FUNCTION
# ============================================

def calculate_psi(reference, current, bins=10):

    reference = np.asarray(reference, dtype=float)
    current = np.asarray(current, dtype=float)

    reference = reference[np.isfinite(reference)]
    current = current[np.isfinite(current)]

    if len(reference) == 0 or len(current) == 0:
        return np.nan

    # Quantile bins from reference/training data
    quantiles = np.linspace(0, 1, bins + 1)

    breakpoints = np.quantile(
        reference,
        quantiles
    )

    # Remove duplicate breakpoints
    breakpoints = np.unique(breakpoints)

    # Constant feature
    if len(breakpoints) < 2:
        return 0.0

    # Extend boundaries
    breakpoints[0] = -np.inf
    breakpoints[-1] = np.inf

    reference_counts, _ = np.histogram(
        reference,
        bins=breakpoints
    )

    current_counts, _ = np.histogram(
        current,
        bins=breakpoints
    )

    # Convert to proportions
    reference_pct = (
        reference_counts / len(reference)
    )

    current_pct = (
        current_counts / len(current)
    )

    # Avoid log(0)
    epsilon = 1e-6

    reference_pct = np.clip(
        reference_pct,
        epsilon,
        None
    )

    current_pct = np.clip(
        current_pct,
        epsilon,
        None
    )

    psi = np.sum(
        (current_pct - reference_pct)
        * np.log(current_pct / reference_pct)
    )

    return psi


# ============================================
# CALCULATE FEATURE DRIFT
# ============================================

print("\nCalculating feature drift...")

results = []

for column in X_train.columns:

    psi_value = calculate_psi(
        X_train[column],
        X_validation[column]
    )

    results.append({
        "feature": column,
        "psi": psi_value
    })


drift_df = pd.DataFrame(results)

drift_df = drift_df.sort_values(
    by="psi",
    ascending=False
)


# ============================================
# CLASSIFY DRIFT
# ============================================

def classify_drift(psi):

    if psi < 0.10:
        return "Low"

    elif psi < 0.25:
        return "Moderate"

    else:
        return "High"


drift_df["drift_level"] = (
    drift_df["psi"]
    .apply(classify_drift)
)


# ============================================
# SAVE
# ============================================

drift_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================
# SUMMARY
# ============================================

print("\n================================")
print("DISTRIBUTION DRIFT ANALYSIS")
print("================================")

print("\nTop 15 drifting features:")

print(
    drift_df.head(15).to_string(
        index=False
    )
)


print("\nDrift level counts:")

print(
    drift_df["drift_level"]
    .value_counts()
)


print("\nAverage PSI:",
      round(drift_df["psi"].mean(), 4))

print("\nHighest PSI:",
      round(drift_df["psi"].max(), 4))

print("\nSaved to:")
print(OUTPUT_FILE)