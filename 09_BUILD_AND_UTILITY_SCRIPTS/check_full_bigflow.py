import pandas as pd

file = r"C:\Users\Admin CDS\OneDrive\Desktop\Datasets\BigFlow-NIDS-V2.csv"

usecols = [
    "FLOW_START_MILLISECONDS",
    "Attack"
]

min_time = None
max_time = None
total_rows = 0
attack_counts = {}

print("Scanning FULL BigFlow-NIDS in chunks...")
print("Only timestamp + attack columns are being read.")

for chunk in pd.read_csv(
    file,
    usecols=usecols,
    chunksize=100_000
):
    total_rows += len(chunk)

    current_min = chunk["FLOW_START_MILLISECONDS"].min()
    current_max = chunk["FLOW_START_MILLISECONDS"].max()

    min_time = (
        current_min
        if min_time is None
        else min(min_time, current_min)
    )

    max_time = (
        current_max
        if max_time is None
        else max(max_time, current_max)
    )

    counts = chunk["Attack"].value_counts()

    for attack, count in counts.items():
        attack_counts[attack] = attack_counts.get(attack, 0) + count

    if total_rows % 1_000_000 == 0:
        print(f"Processed {total_rows:,} rows...")

print("\n==============================")
print("FULL BIGFLOW INSPECTION")
print("==============================")

print(f"Total rows: {total_rows:,}")

print("\nEarliest timestamp:")
print(min_time)

print("\nLatest timestamp:")
print(max_time)

print("\nAttack distribution:")

for attack, count in sorted(
    attack_counts.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{attack}: {count:,}")