import pandas as pd
import numpy as np

def sequential_feedback_eval():
    df = pd.read_csv('results/shifted_test_all_signals.csv')
    df['confidence_risk'] = 1 - df['confidence']
    df['historical_risk'] = df['historical_error_risk'].rank(pct=True)
    
    val_signals = pd.read_csv('results/validation_signals.csv')
    validation_error_rate = val_signals['actual_error'].mean()
    
    # 5 chronological batches
    N_batches = 5
    batch_size = len(df) // N_batches
    
    budgets = [0.01, 0.02, 0.05, 0.10]
    results = []
    
    for B in budgets:
        # Reset weights for this budget
        # Init with something like confidence=0.4, ood=0.2, drift=0.2, hist=0.2 (or whatever is base)
        weights = {'confidence': 0.25, 'ood': 0.25, 'drift': 0.25, 'historical': 0.25}
        
        errors_caught_seq = 0
        errors_caught_static = 0
        errors_caught_conf = 0
        
        total_errors_so_far = 0
        
        for i in range(N_batches):
            start = i * batch_size
            end = len(df) if i == N_batches - 1 else (i + 1) * batch_size
            batch_df = df.iloc[start:end].copy()
            
            total_errors_so_far += batch_df['actual_error'].sum()
            K = int(np.floor(B * len(batch_df)))
            if K == 0: continue
            
            # 1) Sequential Adaptive Score
            batch_df['seq_score'] = (
                weights['confidence'] * batch_df['confidence_risk'] +
                weights['ood'] * batch_df['ood_percentile'] +
                weights['drift'] * batch_df['drift_risk'] +
                weights['historical'] * batch_df['historical_risk']
            )
            
            # 2) Static Score (equal weight)
            batch_df['static_score'] = (
                0.25 * batch_df['confidence_risk'] +
                0.25 * batch_df['ood_percentile'] +
                0.25 * batch_df['drift_risk'] +
                0.25 * batch_df['historical_risk']
            )
            
            # Review Sequential
            seq_reviewed = batch_df.sort_values('seq_score', ascending=False).head(K)
            batch_seq_errors = seq_reviewed['actual_error'].sum()
            errors_caught_seq += batch_seq_errors
            
            # Review Static
            static_reviewed = batch_df.sort_values('static_score', ascending=False).head(K)
            errors_caught_static += static_reviewed['actual_error'].sum()
            
            # Review Conf
            conf_reviewed = batch_df.sort_values('confidence_risk', ascending=False).head(K)
            errors_caught_conf += conf_reviewed['actual_error'].sum()
            
            # Update weights
            audit_yield = batch_seq_errors / K
            if audit_yield > validation_error_rate:
                w4 = min(0.40, weights['historical'] * 1.15)
                # Renormalize
                w_other = 1.0 - w4
                # sum of other weights
                sum_others = weights['confidence'] + weights['ood'] + weights['drift']
                weights['historical'] = w4
                if sum_others > 0:
                    weights['confidence'] = weights['confidence'] / sum_others * w_other
                    weights['ood'] = weights['ood'] / sum_others * w_other
                    weights['drift'] = weights['drift'] / sum_others * w_other

        # Save result for budget B
        results.append({
            'budget': B,
            'sequential_caught': errors_caught_seq,
            'static_caught': errors_caught_static,
            'conf_caught': errors_caught_conf,
            'total_errors': total_errors_so_far
        })

    res_df = pd.DataFrame(results)
    res_df.to_csv('results/sequential_feedback.csv', index=False)
    print(res_df)

if __name__ == '__main__':
    sequential_feedback_eval()
