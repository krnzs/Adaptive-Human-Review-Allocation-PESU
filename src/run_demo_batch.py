import pandas as pd
import time

def run_demo():
    print("========================================")
    print(" ADAPTIVE HUMAN-REVIEW ALLOCATION DEMO")
    print("========================================")
    
    start_time = time.time()
    
    print("1. Loading shifted test batch (N = 5000)...")
    df = pd.read_csv('results/shifted_test_all_signals.csv').head(5000).copy()
    total_errors = df['actual_error'].sum()
    print(f"   Batch contains {total_errors} actual model errors.")
    
    print("2. Calculating adaptive risk scores...")
    df['confidence_risk'] = 1 - df['confidence']
    df['historical_risk'] = df['historical_error_risk'].rank(pct=True)
    
    weights = {"confidence": 0.35, "ood": 0.15, "drift": 0.25, "historical": 0.25}
    
    df['adaptive_score'] = (
        weights["confidence"] * df["confidence_risk"] +
        weights["ood"] * df["ood_percentile"] +
        weights["drift"] * df["drift_risk"] +
        weights["historical"] * df["historical_risk"]
    )
    
    print("3. Allocating 5% review budget (250 items)...")
    budget = 0.05
    k = int(len(df) * budget)
    
    reviewed = df.sort_values('adaptive_score', ascending=False).head(k)
    errors_caught = reviewed['actual_error'].sum()
    
    print("4. Review results:")
    print(f"   Errors caught  : {errors_caught} out of {total_errors}")
    print(f"   Capture rate   : {errors_caught / total_errors * 100:.1f}%")
    print(f"   Time elapsed   : {time.time() - start_time:.2f} seconds")
    print("========================================")

if __name__ == '__main__':
    run_demo()
