import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# ADAPTIVE RISK SCORING ENGINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

# ------------------------------------------------------------
# Load signals
# ------------------------------------------------------------

signals = pd.read_csv(
    RESULTS_DIR / "validation_signals_multifactor.csv"
)

drift = pd.read_csv(
    RESULTS_DIR / "validation_signals_drift.csv"
)

historical = pd.read_csv(
    RESULTS_DIR / "validation_signals_historical.csv"
)

# ------------------------------------------------------------
# Merge signals
# ------------------------------------------------------------

df = signals.copy()

df["drift_score"] = drift["drift_score"].values
df["drift_risk"] = drift["drift_risk"].values

df["historical_error_risk"] = historical[
    "historical_error_risk"
].values

# ------------------------------------------------------------
# Risk components
# ------------------------------------------------------------

df["confidence_risk"] = 1 - df["confidence"]

df["ood_risk"] = df["ood_percentile"]

df["historical_risk"] = (
    df["historical_error_risk"]
    .rank(pct=True)
)

# ------------------------------------------------------------
# Determine environment drift
# ------------------------------------------------------------

mean_drift = df["drift_score"].mean()

high_drift_fraction = (
    df["drift_score"] >=
    df["drift_score"].quantile(0.75)
).mean()

# ------------------------------------------------------------
# Adaptive regime
#
# Thresholds are based on the validation distribution itself.
# ------------------------------------------------------------

drift_q50 = df["drift_score"].quantile(0.50)
drift_q75 = df["drift_score"].quantile(0.75)

if mean_drift <= drift_q50:
    regime = "LOW"
elif mean_drift <= drift_q75:
    regime = "MODERATE"
else:
    regime = "HIGH"

# ------------------------------------------------------------
# Adaptive weights
# ------------------------------------------------------------

if regime == "LOW":

    weights = {
        "confidence": 0.60,
        "ood": 0.15,
        "drift": 0.10,
        "historical": 0.15
    }

elif regime == "MODERATE":

    weights = {
        "confidence": 0.45,
        "ood": 0.15,
        "drift": 0.25,
        "historical": 0.15
    }

else:

    weights = {
        "confidence": 0.30,
        "ood": 0.15,
        "drift": 0.35,
        "historical": 0.20
    }

# ------------------------------------------------------------
# Calculate adaptive risk score
# ------------------------------------------------------------

df["adaptive_risk_score"] = (
    weights["confidence"] * df["confidence_risk"]
    + weights["ood"] * df["ood_risk"]
    + weights["drift"] * df["drift_risk"]
    + weights["historical"] * df["historical_risk"]
)

# ------------------------------------------------------------
# Adaptive priority
# ------------------------------------------------------------

df["adaptive_priority"] = (
    df["adaptive_risk_score"]
    .rank(pct=True)
)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

output_file = RESULTS_DIR / "adaptive_risk_signals.csv"

df.to_csv(output_file, index=False)

# ------------------------------------------------------------
# Report
# ------------------------------------------------------------

print("=" * 60)
print("ADAPTIVE RISK SCORING")
print("=" * 60)

print(f"Mean drift score       : {mean_drift:.4f}")
print(f"High-drift fraction    : {high_drift_fraction:.4f}")
print(f"Drift Q50              : {drift_q50:.4f}")
print(f"Drift Q75              : {drift_q75:.4f}")
print(f"Detected regime        : {regime}")

print("\nAdaptive weights:")
for key, value in weights.items():
    print(f"  {key:12s}: {value:.2f}")

print("\nAdaptive risk statistics:")
print(
    df["adaptive_risk_score"].describe()
)

print(f"\nSaved to: {output_file}")
print("=" * 60)