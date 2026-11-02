import os
import glob
import pandas as pd

proj_dir = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project"
out_txt = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\workspace_summary.txt"

with open(out_txt, "w", encoding="utf-8") as out:
    out.write("=== CHECKING FOR DASHBOARD FILES ===\n")
    dashboard_files = [f for f in glob.glob(os.path.join(proj_dir, "**/*"), recursive=True) if any(k in f.lower() for k in ["app.py", "dashboard", "streamlit", "gradio", "flask"])]
    out.write(f"Dashboard related files: {dashboard_files}\n\n")

    out.write("=== CHECKING RESULTS DIRECTORY CSVs ===\n")
    results_dir = os.path.join(proj_dir, "results")
    if os.path.exists(results_dir):
        for f in sorted(os.listdir(results_dir)):
            fpath = os.path.join(results_dir, f)
            if f.endswith(".csv"):
                sz = os.path.getsize(fpath)
                try:
                    df = pd.read_csv(fpath)
                    out.write(f"CSV: {f:35s} | {sz:8d} bytes | shape: {df.shape} | cols: {list(df.columns)[:5]}\n")
                except Exception as e:
                    out.write(f"CSV: {f:35s} | {sz:8d} bytes | error: {e}\n")
            elif f.endswith((".png", ".jpg")):
                out.write(f"IMG: {f:35s} | {os.path.getsize(fpath):8d} bytes\n")

    out.write("\n=== CHECKING ROOT DIRECTORY IMAGES ===\n")
    for f in sorted(os.listdir(proj_dir)):
        if f.endswith((".png", ".jpg")):
            fpath = os.path.join(proj_dir, f)
            out.write(f"ROOT IMG: {f:35s} | {os.path.getsize(fpath):8d} bytes\n")

print("Saved to workspace_summary.txt")
