"""
Generate all diagrams needed for the expanded deck:
1. System architecture
2. ML process flow
3. Conceptual ER/data schema
4. Implementation module status chart
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\diagrams"
os.makedirs(OUT, exist_ok=True)

# Colors
NAVY = '#0B192C'
ACCENT = '#1E40AF'
GREEN = '#16A34A'
RED = '#DC2626'
AMBER = '#D97706'
PURPLE = '#7C3AED'
LIGHT = '#F8FAFC'
CARD = '#FFFFFF'
MUTED = '#64748B'
TEAL = '#0D9488'

def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=180, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  [OK] {name}")

# ====================================================================
# 1. SYSTEM ARCHITECTURE (horizontal pipeline)
# ====================================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 4.5))
ax.set_xlim(0, 14); ax.set_ylim(0, 4.5)
ax.axis('off'); fig.patch.set_facecolor('white')

stages = [
    (0.3, "1. DATA\nINGESTION", "500K BigFlow-NIDS\nChrono Split\n350K/75K/75K", ACCENT),
    (2.8, "2. PREPROCESS\n& ML", "StandardScaler (LR)\nTrain LR, RF, XGB\nXGB val AUC 0.9228", GREEN),
    (5.3, "3. RELIABILITY\nENGINE", "Pred. Probability\nMahalanobis OOD\nPSI Drift\nHistorical Error", AMBER),
    (7.8, "4. RISK\nSCORING", "Weighted Sum\nw1*conf + w2*ood\n+ w3*drift + w4*hist\nHeuristic Weights", PURPLE),
    (10.3, "5. REVIEW\nALLOCATION", "Top-K Selection\nBudgets: 1-10%\nSimulated Oracle\nCSV Reporting", RED),
]
for x, title, desc, color in stages:
    box = FancyBboxPatch((x, 0.3), 2.2, 3.8, boxstyle="round,pad=0.1",
                          facecolor=color, alpha=0.12, edgecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x+1.1, 3.7, title, ha='center', va='top', fontsize=10,
            fontweight='bold', color=color)
    ax.text(x+1.1, 2.8, desc, ha='center', va='top', fontsize=8, color=NAVY)

for i in range(4):
    x = stages[i][0] + 2.3
    ax.annotate('', xy=(x+0.3, 2.2), xytext=(x, 2.2),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=2))

ax.set_title("System Architecture: End-to-End Pipeline", fontsize=14,
             fontweight='bold', color=NAVY, pad=10)
save(fig, "v2_architecture.png")

# ====================================================================
# 2. ML PROCESS FLOW (vertical flowchart)
# ====================================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 5))
ax.set_xlim(0, 12); ax.set_ylim(0, 5)
ax.axis('off'); fig.patch.set_facecolor('white')

steps = [
    (0.2, "Raw Data\n500K flows", ACCENT),
    (1.9, "Chrono Split\n70/15/15%", ACCENT),
    (3.6, "Preprocess\nStdScaler, Median\nImpute, Drop IDs", GREEN),
    (5.3, "Train Models\nLR, RF, XGBoost", GREEN),
    (7.0, "Generate\nPredictions", AMBER),
    (8.7, "Extract 4\nSignals", PURPLE),
    (10.4, "Risk Score\n& Top-K", RED),
]
for x, label, color in steps:
    box = FancyBboxPatch((x, 1.2), 1.4, 2.6, boxstyle="round,pad=0.08",
                          facecolor=color, alpha=0.12, edgecolor=color, linewidth=1.5)
    ax.add_patch(box)
    ax.text(x+0.7, 2.5, label, ha='center', va='center', fontsize=9,
            fontweight='bold', color=color)

for i in range(6):
    x = steps[i][0] + 1.5
    ax.annotate('', xy=(x+0.2, 2.5), xytext=(x, 2.5),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))

ax.text(6.0, 4.5, "ML Process Flow: Chronological Split -> Train -> Signal Extraction -> Review Allocation",
        ha='center', fontsize=13, fontweight='bold', color=NAVY)
ax.text(6.0, 0.5, "Design: Chronological temporal split ensures no future data leakage. Preprocessing fitted on training data only.",
        ha='center', fontsize=9, color=MUTED, style='italic')
save(fig, "v2_process_flow.png")

# ====================================================================
# 3. CONCEPTUAL DATA SCHEMA (ER-style)
# ====================================================================
fig, ax = plt.subplots(1, 1, figsize=(14, 6))
ax.set_xlim(0, 14); ax.set_ylim(0, 6)
ax.axis('off'); fig.patch.set_facecolor('white')

entities = [
    (0.3, 3.3, 3.0, 2.4, "PREDICTIONS\n(validation_signals.csv)", 
     "predicted_label\nconfidence\nuncertainty\nprediction_entropy\nactual_error\nattack_probability", ACCENT),
    (3.8, 3.3, 3.0, 2.4, "SIGNALS\n(shifted_test_all_signals.csv)",
     "ood_score\nood_percentile\ndrift_score\ndrift_percentile\nhistorical_error_risk\nhistorical_error_pct", GREEN),
    (7.3, 3.3, 3.0, 2.4, "REVIEW QUEUE\n(strategy_comparison.csv)",
     "strategy\nreview_budget_percent\nreviews\nerrors_caught\nerror_capture_percent\nerrors_per_1000_reviews", PURPLE),
    (10.8, 3.3, 3.0, 2.4, "MODELS\n(models/*.pkl)",
     "xgboost.pkl\nscaler.pkl\n\nStored via joblib\nSHA-256 verified", RED),
]

for x, y, w, h, title, fields, color in entities:
    # Title bar
    box_t = FancyBboxPatch((x, y+h-0.6), w, 0.6, boxstyle="round,pad=0.05",
                            facecolor=color, alpha=0.9, edgecolor=color, linewidth=1.5)
    ax.add_patch(box_t)
    ax.text(x+w/2, y+h-0.3, title, ha='center', va='center', fontsize=8,
            fontweight='bold', color='white')
    # Fields
    box_f = FancyBboxPatch((x, y), w, h-0.6, boxstyle="round,pad=0.05",
                            facecolor='white', edgecolor=color, linewidth=1.5)
    ax.add_patch(box_f)
    ax.text(x+0.15, y+h-0.85, fields, va='top', fontsize=7, color=NAVY,
            family='monospace')

# Arrows
for i in range(3):
    x1 = entities[i][0] + entities[i][2]
    x2 = entities[i+1][0]
    mid_y = entities[i][1] + entities[i][3]/2
    ax.annotate('', xy=(x2, mid_y), xytext=(x1, mid_y),
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.5))

# Drift results entity (placed cleanly on the left bottom)
box_d_t = FancyBboxPatch((2.2, 2.0), 4.4, 0.5, boxstyle="round,pad=0.04",
                         facecolor=AMBER, alpha=0.9, edgecolor=AMBER, linewidth=1.5)
ax.add_patch(box_d_t)
ax.text(4.4, 2.25, "DRIFT ANALYSIS (drift_results.csv)", ha='center', va='center',
        fontsize=8.5, fontweight='bold', color='white')

box_d_f = FancyBboxPatch((2.2, 0.4), 4.4, 1.6, boxstyle="round,pad=0.04",
                         facecolor='white', edgecolor=AMBER, linewidth=1.5)
ax.add_patch(box_d_f)
ax.text(2.4, 1.85, "feature (49 flow feature columns)\npsi_value (float - Population Stability Index)\ndrift_level ('Low' | 'Moderate' | 'High')", 
        va='top', fontsize=7.5, color=NAVY, family='monospace')

# Connect SIGNALS to DRIFT ANALYSIS
ax.annotate('calculates PSI', xy=(4.4, 2.5), xytext=(5.3, 3.3),
            ha='center', fontsize=7.5, color=MUTED, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.2, ls='--'))

# File-based Persistence Specification (placed cleanly on the right bottom)
box_p_t = FancyBboxPatch((7.4, 2.0), 5.0, 0.5, boxstyle="round,pad=0.04",
                         facecolor=MUTED, alpha=0.9, edgecolor=MUTED, linewidth=1.5)
ax.add_patch(box_p_t)
ax.text(9.9, 2.25, "PERSISTENCE & STORAGE ARCHITECTURE", ha='center', va='center',
        fontsize=8.5, fontweight='bold', color='white')

box_p_f = FancyBboxPatch((7.4, 0.4), 5.0, 1.6, boxstyle="round,pad=0.04",
                         facecolor='#FEF3C7', edgecolor=AMBER, linewidth=1.2)
ax.add_patch(box_p_f)
p_info = (
    "• Primary Key: prediction_id (int64 across CSV tables)\n"
    "• Tabular Storage: RFC-4180 CSV tables (results/*.csv)\n"
    "• Model Serialization: joblib .pkl artifacts (models/*.pkl)\n"
    "• Cryptographic Integrity: SHA-256 verified (src/26)\n"
    "• Operational Architecture: Serverless File-Based Storage"
)
ax.text(7.6, 1.85, p_info, va='top', fontsize=7.5, color=NAVY, family='sans-serif')

ax.set_title("Conceptual Data Schema (File-Based Storage)", fontsize=14,
             fontweight='bold', color=NAVY, pad=12)
save(fig, "v2_data_schema.png")

# ====================================================================
# 4. RESULTS CHART (correct strategies: Random, Confidence, OOD, Static_MF, Feedback_Adaptive)
# ====================================================================
fig, ax = plt.subplots(1, 1, figsize=(10, 5.5))

budgets = [1, 2, 5, 10]
results = {
    'Random':            [1.17, 2.13, 5.52, 9.92],
    'Confidence':        [13.51, 26.73, 65.45, 84.01],
    'OOD-Only':          [0.03, 0.26, 0.35, 0.35],
    'Static Multi-Factor': [17.51, 33.99, 54.57, 65.42],
    'Feedback Adaptive':  [17.80, 34.26, 45.90, 52.35],
}
colors = {'Random': MUTED, 'Confidence': ACCENT, 'OOD-Only': RED,
          'Static Multi-Factor': AMBER, 'Feedback Adaptive': GREEN}
markers = {'Random': 's', 'Confidence': 'o', 'OOD-Only': 'x',
           'Static Multi-Factor': 'D', 'Feedback Adaptive': '^'}

for name, vals in results.items():
    ax.plot(budgets, vals, color=colors[name], marker=markers[name],
            linewidth=2, markersize=7, label=name)

ax.set_xlabel("Review Budget (%)", fontsize=12, fontweight='bold')
ax.set_ylabel("Errors Captured (%)", fontsize=12, fontweight='bold')
ax.set_title("Shifted-Test Error Capture: 5 Strategies at 4 Budgets", fontsize=13,
             fontweight='bold', color=NAVY)
ax.set_xticks(budgets)
ax.set_xticklabels(['1%', '2%', '5%', '10%'])
ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_ylim(-2, 90)
fig.patch.set_facecolor('white')
save(fig, "v2_results_chart.png")

# ====================================================================
# 5. IMPLEMENTATION MODULE STATUS
# ====================================================================
fig, ax = plt.subplots(1, 1, figsize=(12, 5))
ax.axis('off'); fig.patch.set_facecolor('white')

modules = [
    ("Data Ingestion & Verification", "01, 26", "100%", GREEN),
    ("Chronological Splitting", "02", "100%", GREEN),
    ("Preprocessing (clean, impute, scale)", "03", "100%", GREEN),
    ("Model Training (LR, RF, XGBoost)", "04", "100%", GREEN),
    ("Prediction Signal Generation", "05, 16", "100%", GREEN),
    ("Confidence-Based Review", "06", "100%", GREEN),
    ("OOD Detection (Mahalanobis)", "07, 08", "100%", GREEN),
    ("Static Multi-Factor Strategy", "09, 15", "100%", GREEN),
    ("Drift Measurement (PSI)", "10, 11", "100%", GREEN),
    ("Adaptive Risk Scoring", "12, 13", "100%", GREEN),
    ("Historical Error Proximity", "14", "100%", GREEN),
    ("Shifted-Test Evaluation", "16-22", "100%", GREEN),
    ("Feedback-Adaptive Strategy", "23, 24, 25", "100%", GREEN),
    ("Interactive Dashboard / UI", "—", "0%", RED),
]

# Table
col_widths = [4.5, 1.5, 1.0, 1.0]
headers = ["Module", "Scripts", "Status", "Complete"]
y = 4.6
for i, (h, w) in enumerate(zip(headers, col_widths)):
    x = 1.5 + sum(col_widths[:i])
    ax.add_patch(FancyBboxPatch((x, y-0.3), w, 0.35, boxstyle="round,pad=0.02",
                                 facecolor=NAVY, edgecolor=NAVY))
    ax.text(x+w/2, y-0.12, h, ha='center', va='center', fontsize=9,
            fontweight='bold', color='white')

for ri, (module, scripts, status, color) in enumerate(modules):
    y = 4.2 - ri * 0.3
    bg_c = '#F8FAFC' if ri % 2 == 0 else 'white'
    for i, (val, w) in enumerate(zip([module, scripts, status, status], col_widths)):
        x = 1.5 + sum(col_widths[:i])
        ax.add_patch(plt.Rectangle((x, y-0.27), w, 0.3, facecolor=bg_c, edgecolor='#CBD5E1', linewidth=0.5))
        col = color if i == 3 else NAVY
        ax.text(x+0.05, y-0.12, val if i < 3 else "", va='center', fontsize=7.5, color=col)
        if i == 3:
            ax.add_patch(plt.Rectangle((x+0.1, y-0.22), 0.7*(float(status.strip('%'))/100), 0.15,
                                        facecolor=color, alpha=0.7))

ax.text(5.5, 4.9, "Implementation Module Status (26 Scripts)", fontsize=13,
        fontweight='bold', color=NAVY, ha='center')
ax.text(5.5, -0.1, "13 fully implemented + FR14 partially impl. (50%) = 96.4%.",
        fontsize=10, color=MUTED, ha='center', style='italic')
ax.set_xlim(0.5, 10.5); ax.set_ylim(-0.4, 5.2)
save(fig, "v2_module_status.png")

print("\nAll diagrams generated successfully.")
