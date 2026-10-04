import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================

FILE = r"C:\Users\Admin CDS\OneDrive\Desktop\Datasets\BigFlow_sample.csv"

TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15


# ============================================================
# LOAD DATA
# ============================================================

print("Loading BigFlow sample...")

df = pd.read_csv(FILE)

print(f"Total rows loaded: {len(df):,}")


# ============================================================
# CONVERT TIMESTAMP
# ============================================================

df["timestamp"] = pd.to_datetime(
    df["FLOW_START_MILLISECONDS"],
    unit="ms"
)

# Sort chronologically
df = df.sort_values("timestamp").reset_index(drop=True)


# ============================================================
# DISPLAY TIME RANGE
# ============================================================

print("\n========== TIME RANGE ==========")

print("Earliest:")
print(df["timestamp"].min())

print("\nLatest:")
print(df["timestamp"].max())


# ============================================================
# CREATE TEMPORAL SPLITS
# ============================================================

n = len(df)

train_end = int(n * TRAIN_RATIO)

validation_end = int(
    n * (TRAIN_RATIO + VALIDATION_RATIO)
)

train = df.iloc[:train_end].copy()

validation = df.iloc[
    train_end:validation_end
].copy()

shifted_test = df.iloc[
    validation_end:
].copy()


# ============================================================
# DISPLAY SPLIT INFORMATION
# ============================================================

print("\n========== SPLITS ==========")

print(f"Training rows:   {len(train):,}")
print(f"Validation rows: {len(validation):,}")
print(f"Shifted test:    {len(shifted_test):,}")


print("\n========== SPLIT TIME RANGES ==========")

print("\nTRAIN")
print(train["timestamp"].min())
print(train["timestamp"].max())

print("\nVALIDATION")
print(validation["timestamp"].min())
print(validation["timestamp"].max())

print("\nSHIFTED TEST")
print(shifted_test["timestamp"].min())
print(shifted_test["timestamp"].max())


# ============================================================
# LABEL DISTRIBUTION
# ============================================================

print("\n========== LABEL DISTRIBUTION ==========")

print("\nTRAIN:")
print(train["Label"].value_counts(normalize=True))

print("\nVALIDATION:")
print(validation["Label"].value_counts(normalize=True))

print("\nSHIFTED TEST:")
print(shifted_test["Label"].value_counts(normalize=True))


# ============================================================
# SAVE SPLITS
# ============================================================

OUTPUT_DIR = "results"

train.to_csv(
    f"{OUTPUT_DIR}/train.csv",
    index=False
)

validation.to_csv(
    f"{OUTPUT_DIR}/validation.csv",
    index=False
)

shifted_test.to_csv(
    f"{OUTPUT_DIR}/shifted_test.csv",
    index=False
)

print("\n========== COMPLETE ==========")
print("Temporal split files saved in the results folder.")