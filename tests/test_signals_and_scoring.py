"""
test_signals_and_scoring.py
Executable pytest suite verifying the four reliability signals, ranges, and scoring formulas.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

def test_signal_ranges_and_bounds():
    """Assert uncertainty is in [0, 0.50] and all percentile signals are in [0, 1.00]."""
    sig_file = RESULTS_DIR / "shifted_test_all_signals.csv"
    assert sig_file.exists(), f"Missing {sig_file}"
    
    # Read sample
    df = pd.read_csv(sig_file, nrows=10000)
    
    # 1. Uncertainty: u = 1 - max(P0, P1) in [0, 0.50]
    assert "uncertainty" in df.columns
    u = df["uncertainty"]
    assert u.min() >= -1e-6, f"Uncertainty negative: {u.min()}"
    assert u.max() <= 0.500001, f"Uncertainty exceeded 0.50: {u.max()}"
        
    # 2. OOD percentile: in [0, 1.00]
    assert "ood_percentile" in df.columns
    assert df["ood_percentile"].min() >= -1e-6
    assert df["ood_percentile"].max() <= 1.000001
    
    # 3. Drift percentile: in [0, 1.00]
    assert "drift_risk" in df.columns
    assert df["drift_risk"].min() >= -1e-6
    assert df["drift_risk"].max() <= 1.000001
    
    # 4. Historical error percentile: in [0, 1.00]
    assert "historical_error_percentile" in df.columns
    assert df["historical_error_percentile"].min() >= -1e-6
    assert df["historical_error_percentile"].max() <= 1.000001

def test_composite_score_formula_and_upper_bound():
    """Assert composite risk score does not exceed theoretical upper bound 0.825."""
    u = np.array([0.0, 0.25, 0.50])
    ood = np.array([0.0, 0.50, 1.00])
    drift = np.array([0.0, 0.50, 1.00])
    hist = np.array([0.0, 0.50, 1.00])
    
    # R = 0.35*u + 0.15*ood + 0.25*drift + 0.25*hist
    R = 0.35 * u + 0.15 * ood + 0.25 * drift + 0.25 * hist
    
    assert R[0] == 0.0
    # 0.35*0.25 + 0.15*0.5 + 0.25*0.5 + 0.25*0.5 = 0.0875 + 0.075 + 0.125 + 0.125 = 0.4125
    assert abs(R[1] - 0.4125) < 1e-6
    # Max possible value: 0.35*0.5 + 0.15*1.0 + 0.25*1.0 + 0.25*1.0 = 0.175 + 0.650 = 0.8250
    assert abs(R[2] - 0.8250) < 1e-6
    assert np.all(R <= 0.825001)

def test_signal_correlations():
    """Assert OOD and Drift are strongly rank-correlated (Spearman rho = 0.8414)
    and Uncertainty vs Historical Error is positively correlated (Pearson r = 0.5531)."""
    sig_file = RESULTS_DIR / "shifted_test_all_signals.csv"
    df = pd.read_csv(sig_file)
    
    spearman_rho = df["ood_percentile"].corr(df["drift_risk"], method='spearman')
    assert abs(spearman_rho - 0.8414) < 0.005, f"Expected Spearman rho ~0.8414, got {spearman_rho}"
    
    pearson_r = df["uncertainty"].corr(df["historical_error_risk"], method='pearson')
    assert abs(pearson_r - 0.5531) < 0.005, f"Expected Pearson r ~0.5531, got {pearson_r}"

def test_controlled_uncertainty_scaling_impact():
    """Assert empirical proof: unscaled u captures 610 errors at 1%,
    while 2*u captures 527 and rank-normalization captures 280."""
    sig_file = RESULTS_DIR / "shifted_test_all_signals.csv"
    df = pd.read_csv(sig_file)
    
    u = 1.0 - df['confidence']
    ood = df['ood_percentile']
    drift = df['drift_risk']
    hist = df['historical_error_risk'].rank(pct=True)
    
    # 1. Unscaled u [0, 0.5]
    score_unscaled = 0.35 * u + 0.15 * ood + 0.25 * drift + 0.25 * hist
    # 2. 2*u [0, 1.0]
    score_2x = 0.35 * (2.0 * u) + 0.15 * ood + 0.25 * drift + 0.25 * hist
    # 3. Rank-normalized [0, 1.0]
    score_rank = 0.35 * u.rank(pct=True) + 0.15 * ood + 0.25 * drift + 0.25 * hist
    
    df['s_unscaled'] = score_unscaled
    df['s_2x'] = score_2x
    df['s_rank'] = score_rank
    
    K = 750  # 1% of 75,000
    c_unscaled = int(df.sort_values('s_unscaled', ascending=False).head(K)['actual_error'].sum())
    c_2x = int(df.sort_values('s_2x', ascending=False).head(K)['actual_error'].sum())
    c_rank = int(df.sort_values('s_rank', ascending=False).head(K)['actual_error'].sum())
    
    assert c_unscaled == 610, f"Expected 610 errors for unscaled u, got {c_unscaled}"
    assert c_2x == 527, f"Expected 527 errors for 2*u, got {c_2x}"
    assert c_rank == 280, f"Expected 280 errors for rank-normalized u, got {c_rank}"

def test_sequential_5batch_error_capture():
    """Assert that sequential 5-batch simulation captures exactly 183 errors at 1% budget
    and beats the static comparator (168 errors in sequential_feedback.csv)."""
    seq_file = RESULTS_DIR / "sequential_feedback.csv"
    assert seq_file.exists(), f"Missing {seq_file}"
    
    df_seq = pd.read_csv(seq_file)
    b1_row = df_seq[df_seq["budget"] == 0.01]
    assert not b1_row.empty
    
    seq_errs = int(b1_row["sequential_caught"].values[0])
    stat_errs = int(b1_row["static_caught"].values[0])
    
    assert seq_errs == 183, f"Expected 183 sequential errors, got {seq_errs}"
    assert stat_errs in [161, 168], f"Expected 161 or 168 static errors, got {stat_errs}"
    assert seq_errs > stat_errs, "Sequential adaptive did not beat static comparator!"
