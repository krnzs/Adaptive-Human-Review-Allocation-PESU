import pandas as pd
import numpy as np
import joblib

# ============================================
# PATHS
# ============================================

TRAIN_FILE = "results/X_train.csv"
VALIDATION_FILE = "results/X_validation.csv"
SIGNALS_FILE = "results/validation_signals.csv"

OUTPUT_FILE = "results/validation_signals_ood.csv"


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
# SAMPLE TRAINING DATA
# ============================================

# Full covariance on 350k × 49 is expensive.
# Use a representative sample to estimate
# the training distribution.

sample_size = min(50000, len(X_train))

X_reference = X_train.sample(
    n=sample_size,
    random_state=42
)

print("\nReference sample:", X_reference.shape)


# ============================================
# CALCULATE MEAN
# ============================================

print("\nCalculating training distribution...")

mean = X_reference.mean(axis=0).values


# ============================================
# CALCULATE STANDARD DEVIATION
# ============================================

std = X_reference.std(axis=0).values.copy()

# Prevent division by zero
std[std == 0] = 1


# ============================================
# STANDARDIZE
# ============================================

X_ref_scaled = (
    (X_reference.values - mean) / std
)

X_val_scaled = (
    (X_validation.values - mean) / std
)


# ============================================
# COVARIANCE MATRIX
# ============================================

print("Calculating covariance matrix...")

covariance = np.cov(
    X_ref_scaled,
    rowvar=False
)

# Regularization for numerical stability
covariance += np.eye(covariance.shape[0]) * 1e-6


# ============================================
# INVERSE COVARIANCE
# ============================================

print("Calculating inverse covariance...")

inverse_covariance = np.linalg.pinv(covariance)


# ============================================
# MAHALANOBIS DISTANCE
# ============================================

print("Calculating OOD scores...")

diff = X_val_scaled - mean * 0

ood_scores = np.sqrt(
    np.einsum(
        "ij,jk,ik->i",
        diff,
        inverse_covariance,
        diff
    )
)


# ============================================
# LOAD EXISTING SIGNALS
# ============================================

signals = pd.read_csv(SIGNALS_FILE)

signals["ood_score"] = ood_scores


# ============================================
# OOD RANK
# ============================================

signals["ood_percentile"] = (
    signals["ood_score"]
    .rank(pct=True)
)


# ============================================
# SAVE
# ============================================

signals.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================
# SUMMARY
# ============================================

print("\n================================")
print("OOD DETECTION COMPLETE")
print("================================")

print("Rows:", len(signals))

print(
    "\nOOD score statistics:"
)

print(
    signals["ood_score"].describe()
)

print(
    "\nHighest OOD score:",
    round(signals["ood_score"].max(), 4)
)

print(
    "Average OOD score:",
    round(signals["ood_score"].mean(), 4)
)

print(
    "95th percentile:",
    round(
        signals["ood_score"].quantile(0.95),
        4
    )
)

print(
    "99th percentile:",
    round(
        signals["ood_score"].quantile(0.99),
        4
    )
)

print("\nSaved to:")
print(OUTPUT_FILE)