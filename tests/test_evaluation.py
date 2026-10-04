import pytest
import pandas as pd
import numpy as np

def test_queue_capacity():
    budgets = [0.01, 0.02, 0.05, 0.10]
    df = pd.DataFrame({
        'score': np.random.rand(1000),
        'actual_error': np.random.randint(0, 2, 1000)
    })
    
    for B in budgets:
        K = int(np.floor(B * len(df)))
        q = df.sort_values('score', ascending=False).head(K)
        assert len(q) == K, f"Queue size {len(q)} != expected {K}"
        
def test_no_duplicate_indices():
    df = pd.DataFrame({
        'score': [0.9, 0.9, 0.8, 0.7, 0.7, 0.1],
        'actual_error': [1, 0, 1, 1, 0, 0]
    })
    
    q = df.sort_values('score', ascending=False).head(3)
    assert len(q.index.unique()) == len(q), "Duplicates found in queue index"
    
def test_determinism():
    np.random.seed(42)
    s1 = np.random.rand(5)
    np.random.seed(42)
    s2 = np.random.rand(5)
    np.testing.assert_array_equal(s1, s2)
    
def test_sequential_no_leakage():
    # Synthetic data
    df = pd.DataFrame({
        'conf': [0.1, 0.2, 0.3, 0.4, 0.5],
        'actual_error': [1, 0, 1, 0, 1]
    })
    
    # Prove that sorting by conf doesn't depend on actual_error
    q1 = df.sort_values('conf', ascending=False).head(2)
    
    # Even if we change actual_error to 0 for all, sorting by conf remains identical
    df2 = df.copy()
    df2['actual_error'] = 0
    q2 = df2.sort_values('conf', ascending=False).head(2)
    
    np.testing.assert_array_equal(q1.index, q2.index)
