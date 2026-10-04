import pandas as pd

FILE = r"C:\Users\Admin CDS\OneDrive\Desktop\Datasets\BigFlow_sample.csv"

print("Loading dataset...")

df = pd.read_csv(FILE, nrows=1000)

print("\n========== DATASET TEST ==========")

print("Rows loaded:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nLabel distribution:")
print(df["Label"].value_counts())

print("\nAttack distribution:")
print(df["Attack"].value_counts())

print("\nDataset connection successful!")