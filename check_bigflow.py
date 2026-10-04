import pandas as pd

file = "BigFlow_sample.csv"

usecols = [
    "FLOW_START_MILLISECONDS",
    "FLOW_END_MILLISECONDS",
    "Label",
    "Attack"
]

min_time = None
max_time = None
total_rows = 0
all_counts = {}

print("Scanning BigFlow_sample.csv in chunks...")

for chunk in pd.read_csv(
    file,
    usecols=usecols,
    chunksize=100_000
):
    total_rows += len(chunk)

    current_min = chunk["FLOW_START_MILLISECONDS"].min()
    current_max = chunk["FLOW_START_MILLISECONDS"].max()

    min_time = current_min if min_time is None else min(min_time, current_min)
    max_time = current_max if max_time is None else max(max_time, current_max)

    counts = chunk.groupby(["Label", "Attack"]).size()

    for key, value in counts.items():
        all_counts[key] = all_counts.get(key, 0) + value

print("\n==============================")
print("BIGFLOW SAMPLE INSPECTION")
print("==============================")

print("Total rows:", total_rows)

print("\nEarliest timestamp:")
print(min_time)

print("\nLatest timestamp:")
print(max_time)

print("\nLabel / Attack distribution:")

for key, value in all_counts.items():
    print(key, ":", value)