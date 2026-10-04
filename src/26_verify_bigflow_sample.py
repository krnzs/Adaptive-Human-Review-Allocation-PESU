import pandas as pd
from pathlib import Path
import hashlib

# ============================================================
# VERIFY BIGFLOW SAMPLE AGAINST ORIGINAL DATASET
# ============================================================

ORIGINAL = Path(
    r"C:\Users\Admin CDS\OneDrive\Desktop\Datasets\BigFlow-NIDS-V2.csv"
)

SAMPLE = Path(
    r"C:\Users\Admin CDS\OneDrive\Desktop\Datasets\BigFlow_sample.csv"
)

CHUNK_SIZE = 50_000

print("=" * 70)
print("BIGFLOW-NIDS SAMPLE VERIFICATION")
print("=" * 70)

# ------------------------------------------------------------
# Check files
# ------------------------------------------------------------

if not ORIGINAL.exists():
    raise FileNotFoundError(
        f"Original file not found:\n{ORIGINAL}"
    )

if not SAMPLE.exists():
    raise FileNotFoundError(
        f"Sample file not found:\n{SAMPLE}"
    )

# ------------------------------------------------------------
# Read sample
# ------------------------------------------------------------

print("\nReading sample...")

sample = pd.read_csv(SAMPLE)

print(f"Sample rows    : {len(sample):,}")
print(f"Sample columns : {len(sample.columns)}")

# ------------------------------------------------------------
# Create a unique fingerprint for each sample row
#
# We use several columns that together identify a flow.
# ------------------------------------------------------------

key_columns = [
    "FLOW_START_MILLISECONDS",
    "FLOW_END_MILLISECONDS",
    "IPV4_SRC_ADDR",
    "L4_SRC_PORT",
    "IPV4_DST_ADDR",
    "L4_DST_PORT",
    "PROTOCOL",
    "IN_BYTES",
    "OUT_BYTES",
    "Label",
    "Attack"
]

missing = [
    col for col in key_columns
    if col not in sample.columns
]

if missing:
    raise ValueError(
        f"Missing columns in sample: {missing}"
    )

# Convert values to strings and create row fingerprints
sample_keys = (
    sample[key_columns]
    .fillna("<NA>")
    .astype(str)
    .agg("|".join, axis=1)
)

sample_hashes = set(
    hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()
    for value in sample_keys
)

print(
    f"Unique sample fingerprints: "
    f"{len(sample_hashes):,}"
)

# ------------------------------------------------------------
# Scan original dataset in chunks
# ------------------------------------------------------------

print("\nScanning original BigFlow-NIDS file...")
print("The 14 GB file will NOT be loaded into memory.")
print()

matches = set()
rows_scanned = 0

use_columns = [
    col for col in key_columns
]

for chunk_number, chunk in enumerate(
    pd.read_csv(
        ORIGINAL,
        usecols=use_columns,
        chunksize=CHUNK_SIZE,
        low_memory=False
    ),
    start=1
):

    rows_scanned += len(chunk)

    chunk_keys = (
        chunk[key_columns]
        .fillna("<NA>")
        .astype(str)
        .agg("|".join, axis=1)
    )

    chunk_hashes = {
        hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()
        for value in chunk_keys
    }

    found = sample_hashes.intersection(
        chunk_hashes
    )

    matches.update(found)

    if chunk_number % 10 == 0:
        print(
            f"Scanned {rows_scanned:,} original rows | "
            f"Sample matches: {len(matches):,}"
        )

# ------------------------------------------------------------
# Final results
# ------------------------------------------------------------

match_count = len(matches)

match_percentage = (
    match_count / len(sample_hashes) * 100
)

print("\n" + "=" * 70)
print("VERIFICATION RESULT")
print("=" * 70)

print(
    f"Sample rows checked       : "
    f"{len(sample_hashes):,}"
)

print(
    f"Original rows scanned     : "
    f"{rows_scanned:,}"
)

print(
    f"Sample rows found         : "
    f"{match_count:,}"
)

print(
    f"Match percentage          : "
    f"{match_percentage:.4f}%"
)

if match_count == len(sample_hashes):
    print("\nRESULT: 100% OF SAMPLE ROWS WERE FOUND.")
    print(
        "The sample rows are present in the "
        "original BigFlow-NIDS file."
    )
else:
    print(
        "\nWARNING: Not every sample fingerprint "
        "was found in the original file."
    )

print("=" * 70)