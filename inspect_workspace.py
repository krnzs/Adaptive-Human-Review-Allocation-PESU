import os
import glob
import pandas as pd

proj_dir = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"

print("=== CHECKING FOR DASHBOARD FILES ===")
dashboard_files = [f for f in glob.glob(os.path.join(proj_dir, "**/*"), recursive=True) if any(k in f.lower() for k in ["app.py", "dashboard", "streamlit", "gradio", "flask"])]
print("Dashboard related files:", dashboard_files)

print("\n=== CHECKING RESULTS DIRECTORY CSVs ===")
results_dir = os.path.join(proj_dir, "results")
if os.path.exists(results_dir):
    for f in os.listdir(results_dir):
        if f.endswith(".csv"):
            fpath = os.path.join(results_dir, f)
            sz = os.path.getsize(fpath)
            try:
                df = pd.read_csv(fpath)
                print(f"CSV: {f:35s} | {sz:8d} bytes | shape: {df.shape}")
            except Exception as e:
                print(f"CSV: {f:35s} | {sz:8d} bytes | error: {e}")
        elif f.endswith((".png", ".jpg")):
            fpath = os.path.join(results_dir, f)
            print(f"IMG: {f:35s} | {os.path.getsize(fpath):8d} bytes")

print("\n=== CHECKING ROOT DIRECTORY IMAGES ===")
for f in os.listdir(proj_dir):
    if f.endswith((".png", ".jpg")):
        fpath = os.path.join(proj_dir, f)
        print(f"ROOT IMG: {f:35s} | {os.path.getsize(fpath):8d} bytes")

print("\n=== CHECKING SRC DIRECTORY SCRIPTS ===")
src_dir = os.path.join(proj_dir, "src")
if os.path.exists(src_dir):
    scripts = sorted([f for f in os.listdir(src_dir) if f.endswith(".py")])
    for s in scripts:
        print(f"SRC: {s}")
