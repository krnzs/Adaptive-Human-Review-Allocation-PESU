import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    
    bg = patches.Rectangle((0, 0), 12, 6.2, facecolor="#F8FAFC", edgecolor="none")
    ax.add_patch(bg)
    
    # Title
    ax.text(6.0, 5.75, "CONCEPTUAL HUMAN-REVIEW ALLOCATION PIPELINE", 
            fontsize=12, fontweight='bold', color="#0B192C", ha='center')

    # Stage 1: Data Input
    box1 = patches.FancyBboxPatch((0.5, 2.0), 1.9, 2.4, boxstyle="round,pad=0.2",
                                  facecolor="#FFFFFF", edgecolor="#0066CC", linewidth=1.5)
    ax.add_patch(box1)
    ax.text(1.45, 3.8, "DATA INPUT", fontsize=10.5, fontweight='bold', color="#0B192C", ha='center')
    ax.text(1.45, 3.0, "• BigFlow-NIDS\n  (500K sample)\n• 49 Numerical\n  Features\n• Chronological Split", 
            fontsize=8.5, color="#475569", ha='center', va='center')
    
    # Arrow 1 -> 2
    arrow1 = patches.FancyArrowPatch((2.6, 3.2), (3.2, 3.2), arrowstyle='-|>', 
                                    mutation_scale=16, color="#0066CC", linewidth=1.8)
    ax.add_patch(arrow1)

    # Stage 2: ML Model
    box2 = patches.FancyBboxPatch((3.4, 2.0), 1.9, 2.4, boxstyle="round,pad=0.2",
                                  facecolor="#FFFFFF", edgecolor="#0066CC", linewidth=1.5)
    ax.add_patch(box2)
    ax.text(4.35, 3.8, "ML MODEL", fontsize=10.5, fontweight='bold', color="#0B192C", ha='center')
    ax.text(4.35, 3.0, "• Feature Scaling\n• Primary: XGBoost\n• Predicts Label\n  (Benign vs Attack)\n• Probabilities P(y|x)", 
            fontsize=8.5, color="#475569", ha='center', va='center')

    # Arrow 2 -> 3
    arrow2 = patches.FancyArrowPatch((5.5, 3.2), (6.1, 3.2), arrowstyle='-|>', 
                                    mutation_scale=16, color="#0066CC", linewidth=1.8)
    ax.add_patch(arrow2)

    # Stage 3: Reliability Analysis (Hub)
    box3 = patches.FancyBboxPatch((6.3, 0.8), 2.7, 4.6, boxstyle="round,pad=0.2",
                                  facecolor="#EFF6FF", edgecolor="#2563EB", linewidth=2.0)
    ax.add_patch(box3)
    ax.text(7.65, 4.95, "RELIABILITY ANALYSIS", fontsize=11, fontweight='bold', color="#1E3A8A", ha='center')
    ax.text(7.65, 4.65, "(Complementary Signals)", fontsize=8, color="#3B82F6", ha='center')
    
    signals = [
        ("Confidence", "Certainty of prediction (1 - max P)", "#DBEAFE"),
        ("OOD / Novelty", "Distance to training reference", "#DBEAFE"),
        ("Feature Drift", "Population Stability Index (PSI)", "#DBEAFE"),
        ("Historical Error", "Proximity to known model mistakes", "#DBEAFE")
    ]
    for i, (sig_name, sig_desc, col) in enumerate(signals):
        y_pos = 3.9 - (i * 0.9)
        s_box = patches.FancyBboxPatch((6.5, y_pos - 0.25), 2.3, 0.62, boxstyle="round,pad=0.1",
                                       facecolor=col, edgecolor="#93C5FD", linewidth=1)
        ax.add_patch(s_box)
        ax.text(7.65, y_pos + 0.1, sig_name, fontsize=8.5, fontweight='bold', color="#1E3A8A", ha='center')
        ax.text(7.65, y_pos - 0.12, sig_desc, fontsize=7.2, color="#475569", ha='center')

    # Arrow 3 -> 4
    arrow3 = patches.FancyArrowPatch((9.2, 3.2), (9.7, 3.2), arrowstyle='-|>', 
                                    mutation_scale=16, color="#0066CC", linewidth=1.8)
    ax.add_patch(arrow3)

    # Stage 4: Triage Decisions
    # High-Risk
    box_human = patches.FancyBboxPatch((9.8, 3.4), 1.9, 1.8, boxstyle="round,pad=0.15",
                                      facecolor="#FEF2F2", edgecolor="#DC2626", linewidth=1.8)
    ax.add_patch(box_human)
    ax.text(10.75, 4.65, "SIMULATED REVIEW", fontsize=9.5, fontweight='bold', color="#991B1B", ha='center')
    ax.text(10.75, 3.95, "• High Risk Cases\n• Fixed Review Budget\n  (1%, 2%, 5%, 10%)\n• Ground-truth Oracle", 
            fontsize=8, color="#7F1D1D", ha='center', va='center')

    # Lower-Risk
    box_auto = patches.FancyBboxPatch((9.8, 1.0), 1.9, 1.8, boxstyle="round,pad=0.15",
                                     facecolor="#F0FDF4", edgecolor="#16A34A", linewidth=1.8)
    ax.add_patch(box_auto)
    ax.text(10.75, 2.25, "AUTOMATED OUTPUT", fontsize=9.5, fontweight='bold', color="#166534", ha='center')
    ax.text(10.75, 1.55, "• Lower Risk Cases\n• Automated Execution\n• Incur No Review Cost", 
            fontsize=8, color="#14532D", ha='center', va='center')

    # Split routing arrows
    arrow_up = patches.FancyArrowPatch((9.1, 3.6), (9.7, 4.2), arrowstyle='-|>', 
                                      mutation_scale=13, color="#DC2626", linewidth=1.8)
    ax.add_patch(arrow_up)
    
    arrow_down = patches.FancyArrowPatch((9.1, 2.7), (9.7, 2.0), arrowstyle='-|>', 
                                        mutation_scale=13, color="#16A34A", linewidth=1.8)
    ax.add_patch(arrow_down)

    plt.tight_layout()
    out_file = os.path.join(OUT_DIR, "diagram_system_architecture.png")
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_file}")

def create_temporal_shift_diagram():
    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    bg = patches.Rectangle((0, 0), 12, 5.2, facecolor="#F8FAFC", edgecolor="none")
    ax.add_patch(bg)

    ax.text(6, 4.8, "CHRONOLOGICAL SPLIT & OBSERVED TEMPORAL SHIFT", 
            fontsize=12, fontweight='bold', color="#0B192C", ha='center')

    # Timeline Arrow
    timeline = patches.FancyArrowPatch((1.0, 0.8), (11.0, 0.8), arrowstyle='->', 
                                      mutation_scale=18, color="#64748B", linewidth=2.5)
    ax.add_patch(timeline)
    ax.text(1.2, 0.5, "EARLIER FLOW RECORDS", fontsize=8, fontweight='bold', color="#64748B")
    ax.text(10.8, 0.5, "LATER FLOW RECORDS", fontsize=8, fontweight='bold', color="#64748B", ha='right')

    # Split 1: Train
    box_train = patches.FancyBboxPatch((0.8, 1.3), 3.2, 3.0, boxstyle="round,pad=0.15",
                                      facecolor="#FFFFFF", edgecolor="#0066CC", linewidth=1.8)
    ax.add_patch(box_train)
    ax.text(2.4, 3.9, "TRAINING SPLIT", fontsize=10.5, fontweight='bold', color="#0066CC", ha='center')
    ax.text(2.4, 3.4, "350,000 Flows", fontsize=10, fontweight='bold', color="#0B192C", ha='center')
    ax.text(2.4, 2.4, "• Model training baseline\n• Computes feature reference\n  centroid (μ) and covariance (Σ)\n• Establishes training error set", 
            fontsize=8.5, color="#475569", ha='center', va='center')

    # Split 2: Validation
    box_val = patches.FancyBboxPatch((4.4, 1.3), 3.2, 3.0, boxstyle="round,pad=0.15",
                                    facecolor="#FFFFFF", edgecolor="#10B981", linewidth=1.8)
    ax.add_patch(box_val)
    ax.text(6.0, 3.9, "VALIDATION SPLIT", fontsize=10.5, fontweight='bold', color="#10B981", ha='center')
    ax.text(6.0, 3.4, "75,000 Flows", fontsize=10, fontweight='bold', color="#0B192C", ha='center')
    ax.text(6.0, 2.4, "• Attack Prevalence: ~0.33%\n• Model Errors: 753 (~1.00%)\n• Avg Model Confidence: ~98.65%\n• Baseline evaluation period", 
            fontsize=8.5, color="#475569", ha='center', va='center')

    # Split 3: Shifted Test
    box_test = patches.FancyBboxPatch((8.0, 1.3), 3.2, 3.0, boxstyle="round,pad=0.15",
                                     facecolor="#FEF2F2", edgecolor="#EF4444", linewidth=2.0)
    ax.add_patch(box_test)
    ax.text(9.6, 3.9, "SHIFTED TEST SPLIT", fontsize=10.5, fontweight='bold', color="#EF4444", ha='center')
    ax.text(9.6, 3.4, "75,000 Flows", fontsize=10, fontweight='bold', color="#0B192C", ha='center')
    ax.text(9.6, 2.4, "• Attack Prevalence: ~6.30%\n• Model Errors: 3,427 (~4.57%)\n• Avg Model Confidence: ~96.82%\n• More challenging later period", 
            fontsize=8.5, color="#991B1B", ha='center', va='center')

    plt.tight_layout()
    out_file = os.path.join(OUT_DIR, "diagram_temporal_shift_timeline.png")
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_file}")

def create_results_line_chart():
    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=300)
    
    budgets = [1, 2, 5, 10]
    random_vals = [1.167, 2.130, 5.515, 9.921]
    conf_vals = [13.510, 26.729, 65.451, 84.009]
    static_vals = [17.509, 33.995, 54.567, 65.422]
    adaptive_vals = [17.800, 34.257, 45.900, 52.349]
    
    ax.plot(budgets, random_vals, marker='o', linewidth=2, color='#94A3B8', linestyle='--', label='Random Audit')
    ax.plot(budgets, conf_vals, marker='s', linewidth=2.2, color='#2563EB', label='Confidence-Based')
    ax.plot(budgets, static_vals, marker='^', linewidth=2.2, color='#F59E0B', label='Static Multi-Factor')
    ax.plot(budgets, adaptive_vals, marker='D', linewidth=2.5, color='#DC2626', label='Feedback Adaptive')
    
    ax.set_title("Shifted-Test Error Capture vs. Review Budget", fontsize=11, fontweight='bold', color='#0B192C', pad=12)
    ax.set_xlabel("Review Budget (% of Total Test Records)", fontsize=9.5, fontweight='bold', color='#334155')
    ax.set_ylabel("Percentage of Total Errors Captured (%)", fontsize=9.5, fontweight='bold', color='#334155')
    ax.set_xticks(budgets)
    ax.set_xticklabels(['1%', '2%', '5%', '10%'])
    ax.set_ylim(0, 95)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left', fontsize=8.5, framealpha=0.95)
    
    # Highlight points at 1% and 2%
    ax.annotate('Adaptive higher\nat tight budgets', xy=(2, 34.26), xytext=(2.2, 42),
                arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1, headwidth=5),
                fontsize=8, fontweight='bold', color='#DC2626')
    
    # Highlight points at 10%
    ax.annotate('Confidence higher\nat larger budgets', xy=(10, 84.01), xytext=(7.2, 85),
                arrowprops=dict(facecolor='#2563EB', shrink=0.08, width=1, headwidth=5),
                fontsize=8, fontweight='bold', color='#2563EB')
                
    plt.tight_layout()
    out_file = os.path.join(OUT_DIR, "diagram_results_line_chart.png")
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_file}")

def create_phase2_flowchart():
    fig, ax = plt.subplots(figsize=(12, 5.0), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.0)
    ax.axis('off')

    bg = patches.Rectangle((0, 0), 12, 5.0, facecolor="#F8FAFC", edgecolor="none")
    ax.add_patch(bg)

    ax.text(6, 4.55, "PLANNED / PHASE 2: DATASET-AGNOSTIC RELIABILITY PLATFORM (FUTURE WORK)", 
            fontsize=11.5, fontweight='bold', color="#0B192C", ha='center')

    steps = [
        ("1. TABULAR INGESTION", "• Upload CSV/Excel/Parquet\n• Arbitrary tabular data\n• Domain-agnostic inputs", 0.6, "#0066CC"),
        ("2. AUTO-PROFILING", "• Infer data types\n• Handle missing values\n• Check column cardinality\n• Summary distributions", 2.9, "#0284C7"),
        ("3. TASK & MODEL", "• Detect classification\n  or regression\n• Train baseline models\n• Calibrated probabilities", 5.2, "#0D9488"),
        ("4. RELIABILITY ENGINE", "• Confidence scoring\n• Tabular OOD distance\n• Decile PSI drift\n• Mistake pattern lookup", 7.5, "#4F46E5"),
        ("5. ALLOCATION & UI", "• Budget-aware review\n• SHAP explainability\n• Compliance reporting\n• Interactive dashboard", 9.8, "#16A34A")
    ]

    for title, desc, x_pos, col in steps:
        box = patches.FancyBboxPatch((x_pos, 1.1), 1.8, 2.9, boxstyle="round,pad=0.15",
                                     facecolor="#FFFFFF", edgecolor=col, linewidth=1.6)
        ax.add_patch(box)
        
        banner = patches.FancyBboxPatch((x_pos, 3.4), 1.8, 0.6, boxstyle="round,pad=0.08",
                                       facecolor=col, edgecolor="none")
        ax.add_patch(banner)
        ax.text(x_pos + 0.9, 3.7, title, fontsize=7.5, fontweight='bold', color="#FFFFFF", ha='center', va='center')
        ax.text(x_pos + 0.9, 2.2, desc, fontsize=7.2, color="#334155", ha='center', va='center')

        if x_pos < 9.0:
            arrow = patches.FancyArrowPatch((x_pos + 1.95, 2.5), (x_pos + 2.35, 2.5), arrowstyle='-|>', 
                                            mutation_scale=13, color="#64748B", linewidth=1.8)
            ax.add_patch(arrow)

    plt.tight_layout()
    out_file = os.path.join(OUT_DIR, "diagram_phase2_platform.png")
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_file}")

if __name__ == "__main__":
    create_architecture_diagram()
    create_temporal_shift_diagram()
    create_results_line_chart()
    create_phase2_flowchart()
