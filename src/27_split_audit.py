import pandas as pd
import joblib

def audit_split(name, X_file, y_file, orig_file, model):
    df_orig = pd.read_csv(orig_file)
    X = pd.read_csv(X_file)
    y = pd.read_csv(y_file).squeeze()
    
    rows = len(X)
    attacks = y.sum()
    attack_prev = attacks / rows
    
    preds = model.predict(X)
    
    if hasattr(model, 'predict_proba'):
        probs = model.predict_proba(X)
        confs = probs.max(axis=1)
    else:
        confs = [0] * rows
        
    mean_conf = confs.mean()
    
    errors = (preds != y).astype(int)
    error_rate = errors.mean()
    
    fp = ((preds == 1) & (y == 0)).sum()
    fn = ((preds == 0) & (y == 1)).sum()
    
    min_time = df_orig['timestamp'].min() if 'timestamp' in df_orig.columns else df_orig['FLOW_START_MILLISECONDS'].min()
    max_time = df_orig['timestamp'].max() if 'timestamp' in df_orig.columns else df_orig['FLOW_START_MILLISECONDS'].max()
    
    return {
        'split': name,
        'rows': rows,
        'attacks': attacks,
        'attack_prevalence': attack_prev,
        'model_error_rate': error_rate,
        'FP': fp,
        'FN': fn,
        'mean_confidence': mean_conf,
        'min_timestamp': min_time,
        'max_timestamp': max_time
    }

def main():
    model = joblib.load('models/xgboost.pkl')
    
    splits = [
        ('Train', 'results/X_train.csv', 'results/y_train.csv', 'results/train.csv'),
        ('Validation', 'results/X_validation.csv', 'results/y_validation.csv', 'results/validation.csv'),
        ('Shifted Test', 'results/X_shifted_test.csv', 'results/y_shifted_test.csv', 'results/shifted_test.csv')
    ]
    
    results = []
    for name, Xf, yf, origf in splits:
        results.append(audit_split(name, Xf, yf, origf, model))
        
    df = pd.DataFrame(results)
    df.to_csv('results/split_audit.csv', index=False)
    print(df)
    
if __name__ == '__main__':
    main()
