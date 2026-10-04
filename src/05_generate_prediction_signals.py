import pandas as pd
import numpy as np
import joblib
from scipy.stats import entropy

# ============================================
# PATHS
# ============================================

X_FILE = "results/X_validation.csv"
Y_FILE = "results/y_validation.csv"

MODEL_FILE = "models/xgboost.pkl"

OUTPUT_FILE = "results/validation_signals.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading validation data...")

X = pd.read_csv(X_FILE)
y = pd.read_csv(Y_FILE).squeeze()

print("Validation shape:", X.shape)


# ============================================
# LOAD MODEL
# ============================================

print("\nLoading XGBoost model...")

model = joblib.load(MODEL_FILE)


# ============================================
# GENERATE PREDICTIONS
# ============================================

print("\nGenerating predictions...")

probabilities = model.predict_proba(X)

predicted_label = np.argmax(probabilities, axis=1)

confidence = np.max(probabilities, axis=1)


# ============================================
# UNCERTAINTY
# ============================================

print("Calculating uncertainty...")

uncertainty = 1 - confidence


# ============================================
# BINARY ENTROPY
# ============================================

print("Calculating prediction entropy...")

epsilon = 1e-10

p = probabilities[:, 1]

prediction_entropy = -(
    p * np.log2(p + epsilon)
    + (1 - p) * np.log2(1 - p + epsilon)
)


# ============================================
# ACTUAL ERROR
# ============================================

actual_error = (predicted_label != y.values).astype(int)


# ============================================
# CREATE SIGNAL TABLE
# ============================================

signals = pd.DataFrame({
    "prediction_id": np.arange(len(y)),

    "true_label": y.values,

    "predicted_label": predicted_label,

    "attack_probability": probabilities[:, 1],

    "confidence": confidence,

    "uncertainty": uncertainty,

    "prediction_entropy": prediction_entropy,

    "actual_error": actual_error
})


# ============================================
# SAVE
# ============================================

signals.to_csv(OUTPUT_FILE, index=False)


# ============================================
# SUMMARY
# ============================================

print("\n================================")
print("PREDICTION SIGNALS GENERATED")
print("================================")

print("Rows:", len(signals))

print("\nPrediction distribution:")
print(signals["predicted_label"].value_counts())

print("\nActual label distribution:")
print(signals["true_label"].value_counts())

print("\nErrors detected:")
print(signals["actual_error"].sum())

print(
    "\nValidation error rate:",
    round(signals["actual_error"].mean() * 100, 2),
    "%"
)

print(
    "Average confidence:",
    round(signals["confidence"].mean(), 4)
)

print(
    "Average uncertainty:",
    round(signals["uncertainty"].mean(), 4)
)

print(
    "Average entropy:",
    round(signals["prediction_entropy"].mean(), 4)
)

print("\nSaved to:")
print(OUTPUT_FILE)