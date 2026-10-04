import pandas as pd
import numpy as np

# ============================================================
# FILES
# ============================================================

TRAIN_FILE = "results/train.csv"
VALIDATION_FILE = "results/validation.csv"
TEST_FILE = "results/shifted_test.csv"


# ============================================================
# COLUMNS TO REMOVE
# ============================================================

DROP_COLUMNS = [
    "FLOW_START_MILLISECONDS",
    "FLOW_END_MILLISECONDS",
    "IPV4_SRC_ADDR",
    "IPV4_DST_ADDR",
    "Attack",
    "timestamp"
]


# ============================================================
# LOAD DATA
# ============================================================

print("Loading training data...")
train = pd.read_csv(TRAIN_FILE)

print("Loading validation data...")
validation = pd.read_csv(VALIDATION_FILE)

print("Loading shifted test data...")
test = pd.read_csv(TEST_FILE)


# ============================================================
# REMOVE NON-PREDICTIVE / LEAKAGE COLUMNS
# ============================================================

train = train.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)

validation = validation.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)

test = test.drop(
    columns=DROP_COLUMNS,
    errors="ignore"
)


# ============================================================
# SEPARATE FEATURES AND TARGET
# ============================================================

X_train = train.drop(columns=["Label"])
y_train = train["Label"]

X_validation = validation.drop(columns=["Label"])
y_validation = validation["Label"]

X_test = test.drop(columns=["Label"])
y_test = test["Label"]


# ============================================================
# KEEP NUMERIC FEATURES ONLY
# ============================================================

X_train = X_train.select_dtypes(include=[np.number])
X_validation = X_validation[X_train.columns]
X_test = X_test[X_train.columns]


# ============================================================
# HANDLE INFINITE VALUES
# ============================================================

X_train = X_train.replace(
    [np.inf, -np.inf],
    np.nan
)

X_validation = X_validation.replace(
    [np.inf, -np.inf],
    np.nan
)

X_test = X_test.replace(
    [np.inf, -np.inf],
    np.nan
)


# ============================================================
# MEDIAN IMPUTATION
# ============================================================

medians = X_train.median()

X_train = X_train.fillna(medians)
X_validation = X_validation.fillna(medians)
X_test = X_test.fillna(medians)


# ============================================================
# SAVE PROCESSED DATA
# ============================================================

X_train.to_csv(
    "results/X_train.csv",
    index=False
)

y_train.to_csv(
    "results/y_train.csv",
    index=False
)

X_validation.to_csv(
    "results/X_validation.csv",
    index=False
)

y_validation.to_csv(
    "results/y_validation.csv",
    index=False
)

X_test.to_csv(
    "results/X_shifted_test.csv",
    index=False
)

y_test.to_csv(
    "results/y_shifted_test.csv",
    index=False
)


# ============================================================
# REPORT
# ============================================================

print("\n================================")
print("PREPROCESSING COMPLETE")
print("================================")

print("Training shape:", X_train.shape)
print("Validation shape:", X_validation.shape)
print("Shifted test shape:", X_test.shape)

print("\nFeatures used:")
print(list(X_train.columns))

print("\nMissing values remaining:")
print("Train:", X_train.isna().sum().sum())
print("Validation:", X_validation.isna().sum().sum())
print("Test:", X_test.isna().sum().sum())

print("\nPreprocessed files saved in results/")