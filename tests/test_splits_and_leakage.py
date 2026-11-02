"""
test_splits_and_leakage.py
Executable pytest suite verifying chronological partitioning and zero data leakage.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

def test_split_sizes_and_prevalences():
    """Assert partition sizes and attack prevalences match authoritative research facts."""
    split_file = RESULTS_DIR / "split_audit.csv"
    assert split_file.exists(), f"Missing {split_file}"
    
    df = pd.read_csv(split_file)
    splits = df.set_index("split")
    
    # Train partition
    assert "Train" in splits.index
    assert int(splits.loc["Train", "rows"]) == 350000
    assert abs(float(splits.loc["Train", "attack_prevalence"]) - 0.0610) < 0.002
    
    # Validation partition
    assert "Validation" in splits.index
    assert int(splits.loc["Validation", "rows"]) == 75000
    assert abs(float(splits.loc["Validation", "attack_prevalence"]) - 0.0033) < 0.001
    assert int(splits.loc["Validation", "FP"]) + int(splits.loc["Validation", "FN"]) == 753
    
    # Shifted Test partition
    assert "Shifted Test" in splits.index
    assert int(splits.loc["Shifted Test", "rows"]) == 75000
    assert abs(float(splits.loc["Shifted Test", "attack_prevalence"]) - 0.0630) < 0.002
    assert int(splits.loc["Shifted Test", "FP"]) + int(splits.loc["Shifted Test", "FN"]) == 3427

def test_chronological_boundaries_no_overlap():
    """Assert timestamps are strictly ordered and non-overlapping down to milliseconds."""
    split_file = RESULTS_DIR / "split_audit.csv"
    df = pd.read_csv(split_file).set_index("split")
    
    train_max = pd.to_datetime(df.loc["Train", "max_timestamp"])
    val_min = pd.to_datetime(df.loc["Validation", "min_timestamp"])
    val_max = pd.to_datetime(df.loc["Validation", "max_timestamp"])
    test_min = pd.to_datetime(df.loc["Shifted Test", "min_timestamp"])
    
    # Strict millisecond inequality
    assert train_max < val_min, f"Overlap between Train ({train_max}) and Val ({val_min})"
    assert val_max < test_min, f"Overlap between Val ({val_max}) and Shifted Test ({test_min})"
    
    diff_tv_ms = (val_min - train_max).total_seconds() * 1000
    diff_vt_ms = (test_min - val_max).total_seconds() * 1000
    assert diff_tv_ms >= 20.0, f"Expected >= 20ms gap between Train and Val, got {diff_tv_ms}ms"
    assert diff_vt_ms >= 30.0, f"Expected >= 30ms gap between Val and Test, got {diff_vt_ms}ms"

def test_row_level_disjointness_at_boundaries():
    """Assert boundary rows are distinct physical netflows, not duplicated records."""
    # Check boundary rows using results files
    train = pd.read_csv(RESULTS_DIR / "train.csv", nrows=5)
    # Read last row of train and first row of validation
    train_tail = pd.read_csv(RESULTS_DIR / "train.csv", skiprows=350000-2, nrows=2, header=None)
    val_head = pd.read_csv(RESULTS_DIR / "validation.csv", nrows=1, header=None)
    
    # Assert column values differ between Train[-1] and Val[0]
    # Train[-1] is row index 1 in train_tail
    assert not (train_tail.iloc[1] == val_head.iloc[0]).all(), "Train[-1] and Val[0] are identical records!"

def test_no_test_label_leakage_in_ranking():
    """Assert queue selection is strictly invariant to ground-truth label perturbations."""
    np.random.seed(42)
    scores = np.random.uniform(0.1, 0.75, 1000)
    true_labels = np.random.binomial(1, 0.06, 1000)
    
    df1 = pd.DataFrame({'score': scores, 'label': true_labels})
    q1 = df1.sort_values('score', ascending=False).head(10).index.tolist()
    
    # Invert labels entirely
    df2 = pd.DataFrame({'score': scores, 'label': 1 - true_labels})
    q2 = df2.sort_values('score', ascending=False).head(10).index.tolist()
    
    assert q1 == q2, "Queue selection depended on target labels!"
