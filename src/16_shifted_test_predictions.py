import pandas as pd
import numpy as np
import joblib


# ============================================
# PATHS
# ============================================

X_FILE = "results/X_shifted_test.csv"
Y_FILE = "results/y_shifted_test.csv"

MODEL_FILE = "models/xgboost.pkl"

OUTPUT_FILE = "results/shifted_test_signals.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading shifted test data...")

X = pd.read_csv(X_FILE)
y = pd.read_csv(Y_FILE).squeeze()

print("Shifted test shape:", X.shape)


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

predicted_label = np.argmax(
    probabilities,
    axis=1
)

confidence = np.max(
    probabilities,
    axis=1
)


# ============================================
# UNCERTAINTY
# ============================================

uncertainty = 1 - confidence


# ============================================
# ENTROPY
# ============================================

epsilon = 1e-10

p = probabilities[:, 1]

prediction_entropy = -(
    p * np.log2(p + epsilon)
    + (1 - p)
    * np.log2(1 - p + epsilon)
)


# ============================================
# ACTUAL ERROR
# ============================================

actual_error = (
    predicted_label != y.values
).astype(int)


# ============================================
# CREATE SIGNAL TABLE
# ============================================

signals = pd.DataFrame({

    "prediction_id":
        np.arange(len(y)),

    "true_label":
        y.values,

    "predicted_label":
        predicted_label,

    "attack_probability":
        probabilities[:, 1],

    "confidence":
        confidence,

    "uncertainty":
        uncertainty,

    "prediction_entropy":
        prediction_entropy,

    "actual_error":
        actual_error
})


# ============================================
# SUMMARY
# ============================================

print("\n================================")
print("SHIFTED TEST PREDICTIONS")
print("================================")

print(
    "Rows:",
    len(signals)
)

print(
    "\nActual label distribution:"
)

print(
    signals["true_label"].value_counts()
)

print(
    "\nPrediction distribution:"
)

print(
    signals["predicted_label"].value_counts()
)

print(
    "\nErrors:",
    signals["actual_error"].sum()
)

print(
    "\nError rate:",
    round(
        signals["actual_error"].mean() * 100,
        4
    ),
    "%"
)

print(
    "\nAverage confidence:",
    round(
        signals["confidence"].mean(),
        4
    )
)


# ============================================
# SAVE
# ============================================

signals.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nSaved to:")
print(OUTPUT_FILE)