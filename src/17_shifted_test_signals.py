import pandas as pd
import numpy as np
import joblib


# ============================================
# PATHS
# ============================================

TRAIN_FILE = "results/X_train.csv"
TEST_FILE = "results/X_shifted_test.csv"

BASE_SIGNALS = "results/shifted_test_signals.csv"

DRIFT_FILE = "results/drift_results.csv"

OUTPUT_FILE = "results/shifted_test_all_signals.csv"


# ============================================
# LOAD DATA
# ============================================

print("Loading training data...")
X_train = pd.read_csv(TRAIN_FILE)

print("Training:", X_train.shape)

print("\nLoading shifted test data...")
X_test = pd.read_csv(TEST_FILE)

print("Shifted test:", X_test.shape)


# ============================================
# LOAD BASE PREDICTION SIGNALS
# ============================================

df = pd.read_csv(BASE_SIGNALS)


# ============================================
# PART 1 — OOD SCORE
# ============================================

print("\n================================")
print("CALCULATING OOD RISK")
print("================================")

reference = X_train.sample(
    n=min(50000, len(X_train)),
    random_state=42
)

mean = reference.mean().values

std = reference.std().values.copy()
std[std == 0] = 1

reference_scaled = (
    (reference.values - mean) / std
)

test_scaled = (
    (X_test.values - mean) / std
)

covariance = np.cov(
    reference_scaled,
    rowvar=False
)

covariance += (
    np.eye(covariance.shape[0]) * 1e-6
)

inverse_covariance = np.linalg.pinv(
    covariance
)

diff = test_scaled

ood_score = np.sqrt(
    np.einsum(
        "ij,jk,ik->i",
        diff,
        inverse_covariance,
        diff
    )
)

df["ood_score"] = ood_score

df["ood_percentile"] = (
    pd.Series(ood_score).rank(pct=True).values
)


print(
    "Average OOD score:",
    round(ood_score.mean(), 4)
)

print(
    "95th percentile:",
    round(np.quantile(ood_score, 0.95), 4)
)

print(
    "99th percentile:",
    round(np.quantile(ood_score, 0.99), 4)
)


# ============================================
# PART 2 — DRIFT RISK
# ============================================

print("\n================================")
print("CALCULATING DRIFT RISK")
print("================================")

drift = pd.read_csv(DRIFT_FILE)

drifted_features = drift[
    drift["psi"] >= 0.10
]["feature"].tolist()

print(
    "Drifted features:",
    len(drifted_features)
)

print(drifted_features)


train_mean = X_train.mean()
train_std = X_train.std()

train_std = train_std.replace(
    0,
    1
)

test_z = (
    X_test - train_mean
) / train_std

absolute_deviation = test_z.abs()

psi_lookup = drift.set_index(
    "feature"
)["psi"]


drift_components = []


for feature in drifted_features:

    if feature not in absolute_deviation.columns:
        continue

    weighted_deviation = (
        absolute_deviation[feature]
        * psi_lookup[feature]
    )

    drift_components.append(
        weighted_deviation.values
    )


if drift_components:

    drift_matrix = np.column_stack(
        drift_components
    )

    drift_score = drift_matrix.sum(axis=1)

else:

    drift_score = np.zeros(
        len(X_test)
    )


df["drift_score"] = drift_score

df["drift_risk"] = (
    pd.Series(drift_score).rank(pct=True).values
)


print(
    "Average drift score:",
    round(drift_score.mean(), 4)
)

print(
    "95th percentile:",
    round(np.quantile(drift_score, 0.95), 4)
)


# ============================================
# PART 3 — HISTORICAL ERROR RISK
# ============================================

print("\n================================")
print("CALCULATING HISTORICAL ERROR RISK")
print("================================")

model = joblib.load(
    "models/xgboost.pkl"
)

train_predictions = model.predict(
    X_train
)

historical_error = (
    train_predictions
    != pd.read_csv(
        "results/y_train.csv"
    ).squeeze().values
).astype(int)

global_error_rate = (
    historical_error.mean()
)


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


risk_components = []


for feature in pattern_features:

    train_values = X_train[feature]
    test_values = X_test[feature]

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

            test_bins = pd.cut(
                test_values,
                bins=bins,
                labels=False,
                include_lowest=True
            )

        else:

            train_bins = train_values
            test_bins = test_values

    else:

        train_bins = train_values
        test_bins = test_values


    temp = pd.DataFrame({
        "bin": train_bins,
        "error": historical_error
    })

    error_rates = (
        temp
        .groupby(
            "bin",
            observed=True
        )["error"]
        .mean()
    )

    mapped_risk = (
        test_bins
        .map(error_rates)
        .fillna(global_error_rate)
    )

    risk_components.append(
        mapped_risk.values
    )


historical_error_risk = np.column_stack(
    risk_components
).mean(axis=1)


df["historical_error_risk"] = (
    historical_error_risk
)

df["historical_error_percentile"] = (
    pd.Series(
        historical_error_risk
    ).rank(pct=True).values
)


print(
    "Average historical error risk:",
    round(
        historical_error_risk.mean(),
        6
    )
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
print("SHIFTED TEST SIGNALS COMPLETE")
print("================================")

print(
    "Rows:",
    len(df)
)

print(
    "\nColumns:",
    len(df.columns)
)

print("\nAvailable signals:")

print(
    [
        "confidence",
        "ood_percentile",
        "drift_risk",
        "historical_error_percentile"
    ]
)

print("\nSaved to:")
print(OUTPUT_FILE)