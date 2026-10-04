import pandas as pd
import numpy as np
import joblib


# ============================================
# PATHS
# ============================================

TRAIN_X = "results/X_train.csv"
TRAIN_Y = "results/y_train.csv"
VAL_X = "results/X_validation.csv"

SIGNALS_FILE = "results/adaptive_risk_signals.csv"

OUTPUT_FILE = "results/validation_signals_historical.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading training data...")

X_train = pd.read_csv(TRAIN_X)
y_train = pd.read_csv(TRAIN_Y).squeeze()

print("Training:", X_train.shape)

print("\nLoading validation data...")

X_val = pd.read_csv(VAL_X)

print("Validation:", X_val.shape)


# ============================================
# LOAD MODEL
# ============================================

print("\nLoading XGBoost model...")

model = joblib.load("models/xgboost.pkl")


# ============================================
# TRAINING PREDICTIONS
# ============================================

print("\nGenerating historical predictions...")

train_predictions = model.predict(X_train)

historical_error = (
    train_predictions != y_train.values
).astype(int)

global_error_rate = historical_error.mean()

print(
    "Historical training errors:",
    historical_error.sum()
)

print(
    "Historical error rate:",
    round(global_error_rate * 100, 4),
    "%"
)


# ============================================
# SELECT FEATURES
# ============================================

pattern_features = [
    "L4_SRC_PORT",
    "L4_DST_PORT",
    "PROTOCOL",
    "L7_PROTO",
    "IN_BYTES",
    "IN_PKTS",
    "OUT_BYTES",
    "OUT_PKTS",
    "TCP_FLAGS",
    "FLOW_DURATION_MILLISECONDS"
]

pattern_features = [
    f for f in pattern_features
    if f in X_train.columns
]

print(
    "\nPattern features:",
    pattern_features
)


# ============================================
# CREATE BIN DATASETS
# ============================================

print("\nBuilding historical error patterns...")

train_pattern = pd.DataFrame(index=X_train.index)
val_pattern = pd.DataFrame(index=X_val.index)

created_features = []


for feature in pattern_features:

    train_values = X_train[feature]
    val_values = X_val[feature]

    # Continuous/high-cardinality features
    if train_values.nunique() > 10:

        bins = np.quantile(
            train_values,
            np.linspace(0, 1, 11)
        )

        bins = np.unique(bins)

        if len(bins) > 2:

            bins[0] = -np.inf
            bins[-1] = np.inf

            train_bins = pd.cut(
                train_values,
                bins=bins,
                labels=False,
                include_lowest=True
            )

            val_bins = pd.cut(
                val_values,
                bins=bins,
                labels=False,
                include_lowest=True
            )

        else:

            train_bins = train_values
            val_bins = val_values

    else:

        # Low-cardinality features
        train_bins = train_values
        val_bins = val_values

    train_pattern[feature] = train_bins
    val_pattern[feature] = val_bins

    created_features.append(feature)


print(
    "\nPattern bins created:",
    len(created_features)
)


# ============================================
# CALCULATE HISTORICAL ERROR RATES
# ============================================

print("\nCalculating historical error rates...")

risk_components = []


for feature in created_features:

    temp = pd.DataFrame({
        "bin": train_pattern[feature],
        "error": historical_error
    })

    error_rates = (
        temp
        .groupby("bin", observed=True)["error"]
        .mean()
    )

    validation_risk = (
        val_pattern[feature]
        .map(error_rates)
        .fillna(global_error_rate)
    )

    risk_components.append(
        validation_risk.values
    )


# ============================================
# COMBINE ERROR PATTERNS
# ============================================

risk_matrix = np.column_stack(
    risk_components
)

historical_error_risk = (
    risk_matrix.mean(axis=1)
)


# ============================================
# LOAD EXISTING SIGNALS
# ============================================

df = pd.read_csv(SIGNALS_FILE)

df["historical_error_risk"] = (
    historical_error_risk
)

df["historical_error_percentile"] = (
    df["historical_error_risk"]
    .rank(pct=True)
)


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
print("HISTORICAL ERROR RISK CREATED")
print("================================")

print(
    "\nHistorical error risk statistics:"
)

print(
    df["historical_error_risk"].describe()
)

print(
    "\n95th percentile:",
    round(
        df["historical_error_risk"]
        .quantile(0.95),
        6
    )
)

print("\nSaved to:")
print(OUTPUT_FILE)