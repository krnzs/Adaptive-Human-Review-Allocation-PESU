import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score, precision_score, recall_score, f1_score

def ece(y_true, y_prob, n_bins=10):
    bins = np.linspace(0., 1., n_bins + 1)
    binids = np.digitize(y_prob, bins) - 1
    
    bin_sums = np.bincount(binids, weights=y_prob, minlength=n_bins)
    bin_true = np.bincount(binids, weights=y_true, minlength=n_bins)
    bin_total = np.bincount(binids, minlength=n_bins)
    
    nonzero = bin_total != 0
    prob_true = bin_true[nonzero] / bin_total[nonzero]
    prob_pred = bin_sums[nonzero] / bin_total[nonzero]
    
    return np.sum(np.abs(prob_true - prob_pred) * (bin_total[nonzero] / len(y_true)))

def get_metrics(model, X, y):
    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1] if hasattr(model, 'predict_proba') else preds
    
    return {
        'ROC-AUC': roc_auc_score(y, probs),
        'PR-AUC': average_precision_score(y, probs),
        'Balanced_Acc': balanced_accuracy_score(y, preds),
        'Precision': precision_score(y, preds, zero_division=0),
        'Recall': recall_score(y, preds, zero_division=0),
        'F1': f1_score(y, preds, zero_division=0),
        'ECE': ece(y, probs)
    }

def main():
    model = joblib.load('models/xgboost.pkl')
    
    X_val = pd.read_csv('results/X_validation.csv')
    y_val = pd.read_csv('results/y_validation.csv').squeeze()
    
    X_test = pd.read_csv('results/X_shifted_test.csv')
    y_test = pd.read_csv('results/y_shifted_test.csv').squeeze()
    
    val_metrics = get_metrics(model, X_val, y_val)
    test_metrics = get_metrics(model, X_test, y_test)
    
    df_metrics = pd.DataFrame([val_metrics, test_metrics], index=['Validation', 'Shifted Test'])
    df_metrics.to_csv('results/extended_model_metrics.csv')
    print("Model metrics saved.")
    
    df_signals = pd.read_csv('results/shifted_test_all_signals.csv')
    df_signals['confidence_risk'] = 1 - df_signals['confidence']
    df_signals['historical_risk'] = df_signals['historical_error_risk'].rank(pct=True)
    
    preds = model.predict(X_test)
    df_signals['pred'] = preds
    df_signals['actual_attack'] = y_test
    
    scores = {}
    np.random.seed(42)
    scores['random'] = np.random.rand(len(df_signals))
    scores['confidence'] = df_signals['confidence_risk']
    scores['ood'] = df_signals['ood_percentile']
    scores['drift'] = df_signals['drift_risk']
    scores['history'] = df_signals['historical_risk']
    scores['static'] = 0.25*scores['confidence'] + 0.25*scores['ood'] + 0.25*scores['drift'] + 0.25*scores['history']
    
    w = {"confidence": 0.35, "ood": 0.15, "drift": 0.25, "historical": 0.25}
    scores['adaptive'] = w['confidence']*scores['confidence'] + w['ood']*scores['ood'] + w['drift']*scores['drift'] + w['historical']*scores['history']
    df_signals['adaptive'] = scores['adaptive']
    
    scores['abl_no_conf'] = (scores['ood'] + scores['drift'] + scores['history'])/3
    scores['abl_no_ood'] = (scores['confidence'] + scores['drift'] + scores['history'])/3
    scores['abl_no_drift'] = (scores['confidence'] + scores['ood'] + scores['history'])/3
    scores['abl_no_hist'] = (scores['confidence'] + scores['ood'] + scores['drift'])/3
    
    c_rank = scores['confidence'].rank(pct=True)
    o_rank = scores['ood'].rank(pct=True)
    d_rank = scores['drift'].rank(pct=True)
    h_rank = scores['history'].rank(pct=True)
    scores['adaptive_rank_norm'] = w['confidence']*c_rank + w['ood']*o_rank + w['drift']*d_rank + w['historical']*h_rank
    
    budgets = [0.01, 0.02, 0.05, 0.10]
    total_errors = df_signals['actual_error'].sum()
    
    results = []
    
    for b in budgets:
        K = int(b * len(df_signals))
        for s_name, s_vals in scores.items():
            df_s = df_signals.copy()
            df_s['score'] = s_vals
            reviewed = df_s.sort_values('score', ascending=False).head(K)
            
            errs = reviewed['actual_error'].sum()
            fn = ((reviewed['pred'] == 0) & (reviewed['actual_attack'] == 1)).sum()
            fp = ((reviewed['pred'] == 1) & (reviewed['actual_attack'] == 0)).sum()
            attacks = reviewed['actual_attack'].sum()
            
            results.append({
                'strategy': s_name,
                'budget': b,
                'errors': errs,
                'error_capture_pct': errs / total_errors * 100 if total_errors > 0 else 0,
                'FN_captured': fn,
                'FP_captured': fp,
                'attacks_captured': attacks,
                'efficiency': errs / K * 1000 if K > 0 else 0
            })
            
    df_res = pd.DataFrame(results)
    df_res.to_csv('results/extended_strategy_eval.csv', index=False)
    
    print("Running bootstrap...")
    n_boot = 1000
    boot_res = []
    for b in budgets:
        K = int(b * len(df_signals))
        diffs_static = []
        diffs_conf = []
        for _ in range(n_boot):
            idx = np.random.choice(len(df_signals), len(df_signals), replace=True)
            df_boot = df_signals.iloc[idx]
            tot = df_boot['actual_error'].sum()
            if tot == 0: continue
            
            c_adapt = df_boot.sort_values('adaptive', ascending=False).head(K)['actual_error'].sum() / tot
            
            df_boot_static = df_boot.copy()
            df_boot_static['static'] = 0.25*df_boot['confidence_risk']+0.25*df_boot['ood_percentile']+0.25*df_boot['drift_risk']+0.25*df_boot['historical_risk']
            c_stat = df_boot_static.sort_values('static', ascending=False).head(K)['actual_error'].sum() / tot
            
            c_conf = df_boot.sort_values('confidence_risk', ascending=False).head(K)['actual_error'].sum() / tot
            
            diffs_static.append(c_adapt - c_stat)
            diffs_conf.append(c_adapt - c_conf)
            
        boot_res.append({
            'budget': b,
            'adapt_vs_static_mean': np.mean(diffs_static),
            'adapt_vs_static_2.5': np.percentile(diffs_static, 2.5),
            'adapt_vs_static_97.5': np.percentile(diffs_static, 97.5),
            'adapt_vs_conf_mean': np.mean(diffs_conf),
            'adapt_vs_conf_2.5': np.percentile(diffs_conf, 2.5),
            'adapt_vs_conf_97.5': np.percentile(diffs_conf, 97.5),
        })
        
    df_boot = pd.DataFrame(boot_res)
    df_boot.to_csv('results/extended_bootstrap_cis.csv', index=False)
    print("Extended evaluation complete.")

if __name__ == '__main__':
    main()
