import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier

def compute_historical_risk(ref_X, ref_error, test_X):
    # Same logic as src/14: bin 10 top features into 10 quantiles, compute error rates, sum for test_X
    features = ['L4_SRC_PORT', 'L4_DST_PORT', 'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'OUT_BYTES', 'IN_PKTS', 'OUT_PKTS', 'TCP_FLAGS', 'FLOW_DURATION_MILLISECONDS']
    risk = np.zeros(len(test_X))
    for f in features:
        bins = pd.qcut(ref_X[f], q=10, duplicates='drop')
        temp = pd.DataFrame({'bin': bins, 'error': ref_error})
        rates = temp.groupby('bin')['error'].mean()
        
        # apply to test
        def map_val(val):
            for interval, rate in rates.items():
                if val in interval: return rate
            return rates.mean()
        
        risk += test_X[f].apply(map_val).fillna(rates.mean()).values
    return risk

def main():
    X_train = pd.read_csv('results/X_train.csv')
    y_train = pd.read_csv('results/y_train.csv').squeeze()
    X_val = pd.read_csv('results/X_validation.csv')
    y_val = pd.read_csv('results/y_validation.csv').squeeze()
    X_test = pd.read_csv('results/X_shifted_test.csv')
    y_test = pd.read_csv('results/y_shifted_test.csv').squeeze()
    
    model = joblib.load('models/xgboost.pkl')
    test_actual_error = (model.predict(X_test) != y_test).astype(int)
    total_errors = test_actual_error.sum()
    
    print("1. Existing (Training) Variant")
    train_err = (model.predict(X_train) != y_train).astype(int)
    risk_train = compute_historical_risk(X_train, train_err, X_test)
    
    print("2. Validation Variant")
    val_err = (model.predict(X_val) != y_val).astype(int)
    risk_val = compute_historical_risk(X_val, val_err, X_test)
    
    print("3. OOF Variant (Time-ordered)")
    folds = 3
    chunk = len(X_train) // folds
    oof_preds = np.zeros(len(X_train))
    oof_err = np.zeros(len(X_train))
    
    for k in range(1, folds):
        X_tr = X_train.iloc[:k*chunk]
        y_tr = y_train.iloc[:k*chunk]
        X_te = X_train.iloc[k*chunk:(k+1)*chunk]
        y_te = y_train.iloc[k*chunk:(k+1)*chunk]
        
        # Clone params to retrain
        m = XGBClassifier(**model.get_params())
        m.fit(X_tr, y_tr)
        p = m.predict(X_te)
        oof_err[k*chunk:(k+1)*chunk] = (p != y_te).astype(int)
        
    # We only use the OOF part (ignoring fold 0 where we didn't predict)
    oof_mask = np.arange(chunk, len(X_train))
    risk_oof = compute_historical_risk(X_train.iloc[oof_mask], oof_err[oof_mask], X_test)
    
    # Evaluate
    df = pd.DataFrame({'actual_error': test_actual_error, 'risk_train': risk_train, 'risk_val': risk_val, 'risk_oof': risk_oof})
    
    budgets = [0.01, 0.02, 0.05, 0.10]
    res = []
    
    for b in budgets:
        K = int(b * len(df))
        c_train = df.sort_values('risk_train', ascending=False).head(K)['actual_error'].sum()
        c_val = df.sort_values('risk_val', ascending=False).head(K)['actual_error'].sum()
        c_oof = df.sort_values('risk_oof', ascending=False).head(K)['actual_error'].sum()
        
        res.append({
            'budget': b,
            'train_variant_caught': c_train,
            'val_variant_caught': c_val,
            'oof_variant_caught': c_oof,
            'total_errors': total_errors
        })
        
    res_df = pd.DataFrame(res)
    res_df.to_csv('results/historical_error_variants.csv', index=False)
    print(res_df)
    print("\nCurrently, the pipeline uses the 'Training' variant.")

if __name__ == '__main__':
    main()
