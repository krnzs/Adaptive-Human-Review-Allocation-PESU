import pandas as pd
import numpy as np

# ============================================
# PATHS
# ============================================

DRIFT_FILE = "results/drift_results.csv"
SIGNALS_FILE = "results/validation_signals_multifactor.csv"

OUTPUT_FILE = "results/validation_signals_drift.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading drift results...")

drift = pd.read_csv(DRIFT_FILE)

print("Drift features:", len(drift))

print("\nLoading prediction signals...")

df = pd.read_csv(SIGNALS_FILE)

print("Prediction rows:", len(df))


# ============================================
# SELECT DRIFTED FEATURES
# ============================================

# Use features with PSI >= 0.10
drifted_features = drift[
    drift["psi"] >= 0.10
]["feature"].tolist()

print("\nDrifted features:", len(drifted_features))

print(drifted_features)


# ============================================
# LOAD VALIDATION FEATURES
# ============================================

X_validation = pd.read_csv(
    "results/X_validation.csv"
)


# ============================================
# CALCULATE PER-FEATURE DEVIATION
# ============================================

print("\nCalculating prediction-level drift...")


# We need training statistics
X_train = pd.read_csv(
    "results/X_train.csv"
)

train_mean = X_train.mean()
train_std = X_train.std()

# Avoid division by zero
train_std = train_std.replace(0, 1)


# Standardized deviation
z_scores = (
    X_validation - train_mean
) / train_std


# Absolute deviation
absolute_deviation = z_scores.abs()


# ============================================
# WEIGHT BY FEATURE PSI
# ============================================

psi_lookup = drift.set_index("feature")["psi"]

weighted_scores = []

for feature in drifted_features:

    if feature not in absolute_deviation.columns:
        continue

    feature_deviation = (
        absolute_deviation[feature]
    )

    feature_psi = psi_lookup[feature]

    weighted_scores.append(
        feature_deviation * feature_psi
    )


# ============================================
# COMBINE FEATURES
# ============================================

if weighted_scores:

    drift_score = pd.concat(
        weighted_scores,
        axis=1
    ).sum(axis=1)

else:

    drift_score = pd.Series(
        0,
        index=X_validation.index
    )


# ============================================
# NORMALIZE TO 0–1
# ============================================

drift_percentile = (
    drift_score.rank(pct=True)
)


# ============================================
# ADD TO SIGNAL TABLE
# ============================================

df["drift_score"] = drift_score

df["drift_risk"] = drift_percentile


# ============================================
# SAVE
# ============================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================
# SUMMARY
# ============================================

print("\n================================")
print("DRIFT RISK CREATED")
print("================================")

print(
    "\nDrift score statistics:"
)

print(
    df["drift_score"].describe()
)

print(
    "\nDrift risk statistics:"
)

print(
    df["drift_risk"].describe()
)

print(
    "\n95th percentile drift risk:",
    round(
        df["drift_risk"].quantile(0.95),
        4
    )
)

print(
    "\nSaved to:"
)

print(OUTPUT_FILE)