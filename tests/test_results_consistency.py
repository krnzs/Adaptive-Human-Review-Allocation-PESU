"""
test_results_consistency.py
Executable pytest suite verifying approved reference results and crossover behavior.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results"

def test_approved_strategy_error_captures():
    """Assert exact error counts across all strategies and review budgets."""
    comp_file = RESULTS_DIR / "final_shifted_strategy_comparison.csv"
    assert comp_file.exists(), f"Missing {comp_file}"
    
    df = pd.read_csv(comp_file)
    
    expected = {
        (1.0, "Random"): 40,
        (1.0, "Confidence"): 463,
        (1.0, "OOD"): 1,
        (1.0, "Static_MultiFactor"): 600,
        (1.0, "Feedback_Adaptive"): 610,
        
        (2.0, "Random"): 73,
        (2.0, "Confidence"): 916,
        (2.0, "OOD"): 9,
        (2.0, "Static_MultiFactor"): 1165,
        (2.0, "Feedback_Adaptive"): 1174,
        
        (5.0, "Random"): 189,
        (5.0, "Confidence"): 2243,
        (5.0, "OOD"): 12,
        (5.0, "Static_MultiFactor"): 1870,
        (5.0, "Feedback_Adaptive"): 1573,
        
        (10.0, "Random"): 340,
        (10.0, "Confidence"): 2879,
        (10.0, "OOD"): 12,
        (10.0, "Static_MultiFactor"): 2242,
        (10.0, "Feedback_Adaptive"): 1794,
    }
    
    for (budget, strat), exp_err in expected.items():
        sub = df[(df["review_budget_percent"] == budget) & (df["strategy"] == strat)]
        assert not sub.empty, f"Missing {strat} at {budget}%"
        actual_err = int(sub["errors_caught"].values[0])
        assert actual_err == exp_err, f"{strat} at {budget}%: expected {exp_err}, got {actual_err}"

def test_honest_crossover_behavior():
    """Assert that Adaptive Multi-Factor wins at 1% and 2%, while Confidence wins at 5% and 10%."""
    comp_file = RESULTS_DIR / "final_shifted_strategy_comparison.csv"
    df = pd.read_csv(comp_file)
    
    def get_err(b, strat):
        return int(df[(df["review_budget_percent"] == b) & (df["strategy"] == strat)]["errors_caught"].values[0])
        
    # At 1% budget: Adaptive (610) > Confidence (463)
    assert get_err(1.0, "Feedback_Adaptive") > get_err(1.0, "Confidence")
    
    # At 2% budget: Adaptive (1174) > Confidence (916)
    assert get_err(2.0, "Feedback_Adaptive") > get_err(2.0, "Confidence")
    
    # At 5% budget: Confidence (2243) > Adaptive (1573) [CROSSOVER]
    assert get_err(5.0, "Confidence") > get_err(5.0, "Feedback_Adaptive")
    
    # At 10% budget: Confidence (2879) > Adaptive (1794) [CROSSOVER]
    assert get_err(10.0, "Confidence") > get_err(10.0, "Feedback_Adaptive")

def test_extended_metrics_and_bootstrap_cis():
    """Assert PR-AUC, Balanced Accuracy, ECE, and 1% bootstrap confidence interval."""
    # 1. Extended model metrics
    metrics_file = RESULTS_DIR / "extended_model_metrics.csv"
    assert metrics_file.exists()
    df_met = pd.read_csv(metrics_file, index_col=0)
    st = df_met.loc["Shifted Test"]
    
    assert abs(float(st["PR-AUC"]) - 0.7444) < 0.001
    assert abs(float(st["Balanced_Acc"]) - 0.7321) < 0.001
    assert abs(float(st["ECE"]) - 0.0200) < 0.001
    
    # 2. Bootstrap intervals
    ci_file = RESULTS_DIR / "extended_bootstrap_cis.csv"
    assert ci_file.exists()
    df_ci = pd.read_csv(ci_file)
    b1 = df_ci[df_ci["budget"] == 0.01].iloc[0]
    
    ci_low = float(b1["adapt_vs_conf_2.5"]) * 100
    ci_high = float(b1["adapt_vs_conf_97.5"]) * 100
    
    assert abs(ci_low - 3.45) < 0.1
    assert abs(ci_high - 5.28) < 0.1
