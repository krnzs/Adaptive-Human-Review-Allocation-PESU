import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('diagrams', exist_ok=True)

def generate_15_1():
    try:
        df = pd.read_csv('results/final_shifted_strategy_comparison.csv')
        df['budget'] = df['review_budget_percent'].astype(str) + '%'
        
        plt.figure(figsize=(10, 6))
        for strategy in df['strategy'].unique():
            strat_df = df[df['strategy'] == strategy]
            plt.plot(strat_df['budget'], strat_df['error_capture_percent'], marker='o', label=strategy, linewidth=2)
            
        plt.title('Figure 15.1 - Comparative Error Capture Rate Across Review Budgets')
        plt.xlabel('Review Budget (%)')
        plt.ylabel('Error Capture Rate (%)')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('diagrams/figure_15_1.png', dpi=300)
        plt.close()
        print("Generated Figure 15.1")
    except Exception as e:
        print("Error generating 15.1:", e)

def generate_15_3():
    try:
        df = pd.read_csv('results/final_shifted_strategy_comparison.csv')
        df['budget'] = df['review_budget_percent'].astype(str) + '%'
        df['efficiency'] = df['errors_per_1000_reviews']
        
        plt.figure(figsize=(10, 6))
        for strategy in df['strategy'].unique():
            strat_df = df[df['strategy'] == strategy]
            plt.plot(strat_df['budget'], strat_df['efficiency'], marker='o', label=strategy, linewidth=2)
            
        plt.title('Figure 15.3 - Review Efficiency Across Allocation Budgets')
        plt.xlabel('Review Budget (%)')
        plt.ylabel('Errors Caught per 1,000 Reviews')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('diagrams/figure_15_3.png', dpi=300)
        plt.close()
        print("Generated Figure 15.3")
    except Exception as e:
        print("Error generating 15.3:", e)

if __name__ == '__main__':
    generate_15_1()
    generate_15_3()
