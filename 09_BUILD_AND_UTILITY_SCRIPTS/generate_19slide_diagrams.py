"""
Generate polished diagrams for the 19-slide capstone presentation.
Style: rounded shapes, subtle color-coding by stage, clean academic look.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

OUT = r"C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\diagrams"
os.makedirs(OUT, exist_ok=True)

# ── Colour palette (consistent with PPTX) ──────────────────────
NAVY       = '#0B192C'
ACCENT     = '#0066CC'
DARK_GRAY  = '#334155'
LIGHT_BG   = '#F8FAFC'
WHITE      = '#FFFFFF'
GREEN      = '#16A34A'
RED        = '#DC2626'
AMBER      = '#D97706'
LIGHT_BLUE = '#DBEAFE'
LIGHT_GREEN= '#DCFCE7'
LIGHT_RED  = '#FEE2E2'
LIGHT_AMBER= '#FEF3C7'
PURPLE     = '#7C3AED'
LIGHT_PURPLE='#EDE9FE'
TEAL       = '#0D9488'
LIGHT_TEAL = '#CCFBF1'
BORDER     = '#94A3B8'


def styled_box(ax, x, y, w, h, text, bg, border_color, text_color=NAVY,
               fontsize=11, icon=None, bold=True, ha='center'):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                         facecolor=bg, edgecolor=border_color, linewidth=1.5)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    full_text = f"{icon} {text}" if icon else text
    ax.text(x + w/2, y + h/2, full_text,
            ha=ha if ha != 'center' else 'center', va='center',
            fontsize=fontsize, color=text_color, weight=weight,
            wrap=True, family='sans-serif')


def arrow(ax, x1, y1, x2, y2, color=BORDER):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2))


# ═══════════════════════════════════════════════════════════════
# 1. SYSTEM ARCHITECTURE DIAGRAM (Slide 4 / Slide 11)
# ═══════════════════════════════════════════════════════════════
def make_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(14, 5.5), dpi=200)
    ax.set_xlim(0, 14); ax.set_ylim(0, 5.5)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    # Row 1: Data Input → ML Model → Predictions
    styled_box(ax, 0.3, 3.6, 2.2, 1.2, 'DATA INPUT\n(Network Flows)', LIGHT_BLUE, ACCENT, fontsize=10, icon='')
    arrow(ax, 2.5, 4.2, 3.2, 4.2, ACCENT)
    styled_box(ax, 3.2, 3.6, 2.2, 1.2, 'ML MODEL\n(XGBoost)', LIGHT_BLUE, ACCENT, fontsize=10, icon='')
    arrow(ax, 5.4, 4.2, 6.1, 4.2, ACCENT)
    styled_box(ax, 6.1, 3.6, 2.2, 1.2, 'PREDICTIONS\n+ Probabilities', LIGHT_BLUE, ACCENT, fontsize=10, icon='')

    # Arrow down to signal layer
    arrow(ax, 7.2, 3.6, 7.2, 2.95, DARK_GRAY)

    # Row 2: Four Signals
    sig_x = [0.3, 3.2, 6.1, 9.0]
    sig_labels = ['Confidence\nScore', 'OOD\nDistance', 'Drift\n(PSI)', 'Historical\nError']
    sig_colors = [LIGHT_BLUE, LIGHT_GREEN, LIGHT_AMBER, LIGHT_RED]
    sig_borders = [ACCENT, GREEN, AMBER, RED]
    for i, (sx, lab, sc, sb) in enumerate(zip(sig_x, sig_labels, sig_colors, sig_borders)):
        styled_box(ax, sx, 1.6, 2.2, 1.2, lab, sc, sb, fontsize=10)

    # Label
    ax.text(5.7, 2.95, 'RELIABILITY SIGNALS', ha='center', va='bottom',
            fontsize=9, color=DARK_GRAY, weight='bold', style='italic')

    # Arrows from all signals to Risk Score
    for sx in sig_x:
        arrow(ax, sx + 1.1, 1.6, 11.2, 1.05, BORDER)

    # Risk Score → Review / Auto
    styled_box(ax, 9.0, 3.6, 2.5, 1.2, 'RISK\nSCORING', LIGHT_PURPLE, PURPLE, fontsize=10)
    arrow(ax, 8.3, 4.2, 9.0, 4.2, DARK_GRAY)

    styled_box(ax, 10.0, 0.3, 3.5, 1.2, 'COMPOSITE\nRISK SCORE', LIGHT_PURPLE, PURPLE, fontsize=10)

    # Decision outputs
    styled_box(ax, 11.8, 3.6, 1.8, 1.2, 'REVIEW\n(Top-k)', LIGHT_RED, RED, fontsize=10)
    arrow(ax, 11.5, 4.2, 11.8, 4.2, RED)

    # Budget label
    ax.text(12.7, 3.45, 'Budget: 1-10%', ha='center', va='top',
            fontsize=8, color=RED, style='italic')

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_system_architecture.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [1/7] System architecture diagram")


# ═══════════════════════════════════════════════════════════════
# 2. ML PROCESS FLOW (Slide 11)
# ═══════════════════════════════════════════════════════════════
def make_process_flow():
    fig, ax = plt.subplots(1, 1, figsize=(14, 3.5), dpi=200)
    ax.set_xlim(0, 14); ax.set_ylim(0, 3.5)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    steps = [
        ('Chronological\nData Split', LIGHT_BLUE, ACCENT),
        ('Feature\nPreprocessing', LIGHT_BLUE, ACCENT),
        ('Model Training\n& Selection', LIGHT_GREEN, GREEN),
        ('Signal\nGeneration', LIGHT_AMBER, AMBER),
        ('Risk Score\nComputation', LIGHT_PURPLE, PURPLE),
        ('Review\nAllocation', LIGHT_RED, RED),
        ('Strategy\nEvaluation', LIGHT_TEAL, TEAL),
    ]
    w, h = 1.6, 1.4
    gap = 0.2
    start_x = 0.3
    y = 1.0
    for i, (label, bg, brd) in enumerate(steps):
        x = start_x + i * (w + gap)
        styled_box(ax, x, y, w, h, label, bg, brd, fontsize=9)
        if i < len(steps) - 1:
            arrow(ax, x + w, y + h/2, x + w + gap, y + h/2, DARK_GRAY)

    ax.text(7.0, 2.8, 'ML PIPELINE: DESIGN METHODOLOGY', ha='center',
            fontsize=12, color=NAVY, weight='bold')

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_process_flow.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [2/7] Process flow diagram")


# ═══════════════════════════════════════════════════════════════
# 3. ER / CONCEPTUAL SCHEMA DIAGRAM (Slide 12)
# ═══════════════════════════════════════════════════════════════
def make_er_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 6), dpi=200)
    ax.set_xlim(0, 14); ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    ax.text(7.0, 5.7, 'CONCEPTUAL DATA SCHEMA', ha='center',
            fontsize=14, color=NAVY, weight='bold')

    # Entity 1: Predictions
    styled_box(ax, 0.3, 3.2, 3.0, 2.2, '', LIGHT_BLUE, ACCENT, fontsize=9)
    ax.text(1.8, 5.1, 'Predictions', ha='center', fontsize=11,
            color=ACCENT, weight='bold')
    fields1 = ['flow_id (PK)', 'features [49 cols]', 'predicted_label',
               'true_label', 'predict_proba', 'split (train/val/test)']
    for i, f in enumerate(fields1):
        ax.text(0.6, 4.7 - i*0.26, f, fontsize=8.5, color=DARK_GRAY,
                family='monospace')

    # Entity 2: Signals
    styled_box(ax, 4.0, 3.2, 3.0, 2.2, '', LIGHT_GREEN, GREEN, fontsize=9)
    ax.text(5.5, 5.1, 'Reliability Signals', ha='center', fontsize=11,
            color=GREEN, weight='bold')
    fields2 = ['flow_id (FK)', 'confidence_risk', 'ood_score',
               'drift_score', 'historical_risk', 'composite_risk']
    for i, f in enumerate(fields2):
        ax.text(4.3, 4.7 - i*0.26, f, fontsize=8.5, color=DARK_GRAY,
                family='monospace')

    # Entity 3: Review Queue
    styled_box(ax, 7.7, 3.2, 3.0, 2.2, '', LIGHT_AMBER, AMBER, fontsize=9)
    ax.text(9.2, 5.1, 'Review Queue', ha='center', fontsize=11,
            color=AMBER, weight='bold')
    fields3 = ['flow_id (FK)', 'risk_score', 'budget_tier (%)',
               'reviewed_flag', 'review_result', 'strategy_name']
    for i, f in enumerate(fields3):
        ax.text(8.0, 4.7 - i*0.26, f, fontsize=8.5, color=DARK_GRAY,
                family='monospace')

    # Entity 4: Experiments
    styled_box(ax, 10.7, 3.2, 3.0, 2.2, '', LIGHT_PURPLE, PURPLE, fontsize=9)
    ax.text(12.2, 5.1, 'Experiments', ha='center', fontsize=11,
            color=PURPLE, weight='bold')
    fields4 = ['experiment_id (PK)', 'strategy_name', 'budget_percent',
               'errors_caught', 'error_capture_%', 'errors_per_1000']
    for i, f in enumerate(fields4):
        ax.text(11.0, 4.7 - i*0.26, f, fontsize=8.5, color=DARK_GRAY,
                family='monospace')

    # Relationships (arrows)
    arrow(ax, 3.3, 4.3, 4.0, 4.3, DARK_GRAY)
    ax.text(3.65, 4.45, '1:1', ha='center', fontsize=8, color=DARK_GRAY, weight='bold')

    arrow(ax, 7.0, 4.3, 7.7, 4.3, DARK_GRAY)
    ax.text(7.35, 4.45, '1:N', ha='center', fontsize=8, color=DARK_GRAY, weight='bold')

    arrow(ax, 10.7, 4.3, 10.7, 4.3, DARK_GRAY)
    ax.annotate('', xy=(10.7, 4.3), xytext=(10.0, 4.3),
                arrowprops=dict(arrowstyle='->', color=DARK_GRAY, lw=1.5))
    ax.text(10.35, 4.45, 'N:1', ha='center', fontsize=8, color=DARK_GRAY, weight='bold')

    # Storage note
    styled_box(ax, 2.0, 0.3, 10.0, 1.8, '', RQ_BG := '#EEF2FF', ACCENT)
    ax.text(7.0, 1.8, 'Physical Storage (Current Implementation)', ha='center',
            fontsize=10, color=NAVY, weight='bold')
    storage = [
        'Predictions: results/shifted_test.csv, results/validation.csv',
        'Signals: results/shifted_test_all_signals.csv, results/validation_signals.csv',
        'Review Queue: results/shifted_review_comparison.csv, results/final_shifted_strategy_comparison.csv',
        'Experiments: results/final_experiment_summary.csv',
        'Models: models/xgboost.pkl, models/scaler.pkl',
    ]
    for i, s in enumerate(storage):
        ax.text(2.3, 1.5 - i*0.22, s, fontsize=8, color=DARK_GRAY, family='monospace')

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_er_schema.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [3/7] ER / conceptual schema diagram")


# ═══════════════════════════════════════════════════════════════
# 4. TEMPORAL SPLIT TIMELINE (Slide 14)
# ═══════════════════════════════════════════════════════════════
def make_timeline():
    fig, ax = plt.subplots(1, 1, figsize=(12, 3.5), dpi=200)
    ax.set_xlim(0, 12); ax.set_ylim(0, 3.5)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    ax.text(6, 3.2, 'CHRONOLOGICAL DATA SPLIT (500K Flows)',
            ha='center', fontsize=13, color=NAVY, weight='bold')

    # Three blocks
    blocks = [
        (0.5, 4.5, 'TRAIN\n350,000 flows', LIGHT_BLUE, ACCENT, '70%'),
        (5.2, 2.8, 'VALIDATION\n75,000 flows', LIGHT_GREEN, GREEN, '15%'),
        (8.2, 2.8, 'SHIFTED TEST\n75,000 flows', LIGHT_RED, RED, '15%'),
    ]
    for x, w, label, bg, brd, pct in blocks:
        styled_box(ax, x, 1.2, w, 1.5, label, bg, brd, fontsize=10)
        ax.text(x + w/2, 1.05, pct, ha='center', fontsize=9, color=brd, weight='bold')

    # Timeline arrow
    ax.annotate('', xy=(11.5, 0.6), xytext=(0.3, 0.6),
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.5))
    ax.text(6, 0.3, 'Chronological Order (Earlier  -->  Later)', ha='center',
            fontsize=10, color=DARK_GRAY, style='italic')

    # Stats annotations
    ax.text(2.75, 0.85, 'Attack: ~0.33%', ha='center', fontsize=8, color=ACCENT)
    ax.text(6.6, 0.85, 'Attack: ~0.33%\nError: ~1.0%', ha='center', fontsize=7.5, color=GREEN)
    ax.text(9.6, 0.85, 'Attack: ~6.30%\nError: ~4.57%', ha='center', fontsize=7.5, color=RED)

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_temporal_split.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [4/7] Temporal split timeline")


# ═══════════════════════════════════════════════════════════════
# 5. SIGNALS + REVIEW ALLOCATION DIAGRAM (Slide 15)
# ═══════════════════════════════════════════════════════════════
def make_signals_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 4.5), dpi=200)
    ax.set_xlim(0, 14); ax.set_ylim(0, 4.5)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    # Four signal boxes
    signals = [
        ('Confidence\n1 - max P(y|x)', LIGHT_BLUE, ACCENT),
        ('OOD Distance\nMahalanobis-like', LIGHT_GREEN, GREEN),
        ('Drift (PSI)\nFeature-level shift', LIGHT_AMBER, AMBER),
        ('Historical Error\nError proximity', LIGHT_RED, RED),
    ]
    sx_positions = [0.3, 3.2, 6.1, 9.0]
    for (label, bg, brd), sx in zip(signals, sx_positions):
        styled_box(ax, sx, 2.8, 2.5, 1.3, label, bg, brd, fontsize=9.5)

    # Arrows to combiner
    for sx in sx_positions:
        arrow(ax, sx + 1.25, 2.8, 5.7, 1.95, BORDER)

    # Combiner
    styled_box(ax, 4.5, 1.0, 2.5, 1.0, 'Weighted\nCombination', LIGHT_PURPLE, PURPLE, fontsize=10)

    # Arrow to risk score
    arrow(ax, 7.0, 1.5, 7.8, 1.5, PURPLE)

    # Risk score
    styled_box(ax, 7.8, 1.0, 2.2, 1.0, 'Composite\nRisk Score', LIGHT_PURPLE, PURPLE, fontsize=10)

    # Arrow to review tiers
    arrow(ax, 10.0, 1.5, 10.8, 1.5, RED)

    # Review budget tiers
    styled_box(ax, 10.8, 0.5, 2.8, 2.0, '', LIGHT_RED, RED, fontsize=9)
    ax.text(12.2, 2.2, 'Review Budget', ha='center', fontsize=10,
            color=RED, weight='bold')
    tiers = ['1% = 750 reviews', '2% = 1,500 reviews',
             '5% = 3,750 reviews', '10% = 7,500 reviews']
    for i, t in enumerate(tiers):
        ax.text(12.2, 1.85 - i*0.3, t, ha='center', fontsize=8.5, color=DARK_GRAY)

    # Title
    ax.text(7.0, 4.2, 'RELIABILITY SIGNALS  -->  RISK SCORING  -->  REVIEW ALLOCATION',
            ha='center', fontsize=12, color=NAVY, weight='bold')

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_signals_allocation.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [5/7] Signals + allocation diagram")


# ═══════════════════════════════════════════════════════════════
# 6. RESULTS LINE CHART (Slide 17)
# ═══════════════════════════════════════════════════════════════
def make_results_chart():
    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5), dpi=200)

    budgets = [1, 2, 5, 10]

    # Verified data from final_shifted_strategy_comparison.csv
    random_pct      = [1.17,  2.13,   5.52,   9.92]
    confidence_pct  = [13.51, 26.73,  65.45,  84.01]
    ood_pct         = [0.03,  0.26,   0.35,   0.35]
    multi_pct       = [17.51, 33.99,  54.57,  65.42]
    feedback_pct    = [17.80, 34.26,  45.90,  52.35]

    ax.plot(budgets, random_pct,     'o--', color='#94A3B8', lw=2, ms=7, label='Random')
    ax.plot(budgets, confidence_pct, 's-',  color=ACCENT,    lw=2.5, ms=8, label='Confidence-Only')
    ax.plot(budgets, ood_pct,        'D:',  color='#7C3AED', lw=1.5, ms=6, label='OOD-Only')
    ax.plot(budgets, multi_pct,      '^-',  color=AMBER,     lw=2.5, ms=8, label='Static Multi-Factor')
    ax.plot(budgets, feedback_pct,   'v-',  color=GREEN,     lw=2.5, ms=8, label='Feedback Adaptive')

    ax.set_xlabel('Review Budget (%)', fontsize=13, color=DARK_GRAY)
    ax.set_ylabel('Errors Captured (%)', fontsize=13, color=DARK_GRAY)
    ax.set_title('Error Capture vs. Review Budget (Shifted Test)',
                 fontsize=15, color=NAVY, weight='bold', pad=12)
    ax.set_xticks(budgets)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10, loc='upper left', framealpha=0.9)
    ax.tick_params(labelsize=11)

    fig.patch.set_facecolor(LIGHT_BG)
    ax.set_facecolor(WHITE)
    fig.tight_layout(pad=0.5)
    fig.savefig(os.path.join(OUT, 'diagram_results_chart.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [6/7] Results line chart")


# ═══════════════════════════════════════════════════════════════
# 7. PHASE-2 COMPACT FLOW (not a separate slide, but reusable)
# ═══════════════════════════════════════════════════════════════
def make_phase2_flow():
    fig, ax = plt.subplots(1, 1, figsize=(12, 3), dpi=200)
    ax.set_xlim(0, 12); ax.set_ylim(0, 3)
    ax.axis('off')
    fig.patch.set_facecolor(LIGHT_BG)

    steps = [
        ('Diverse Tabular\nDatasets', LIGHT_BLUE, ACCENT),
        ('Auto-Profiling\n& Preprocessing', LIGHT_GREEN, GREEN),
        ('Multi-Task\nModeling', LIGHT_AMBER, AMBER),
        ('Reliability\nEngine v2', LIGHT_PURPLE, PURPLE),
        ('Online Drift\n& Recalibration', LIGHT_RED, RED),
        ('Explainability\nInterface', LIGHT_TEAL, TEAL),
    ]
    w, h = 1.65, 1.2
    gap = 0.15
    start_x = 0.3
    y = 0.9
    for i, (label, bg, brd) in enumerate(steps):
        x = start_x + i * (w + gap)
        styled_box(ax, x, y, w, h, label, bg, brd, fontsize=8.5)
        if i < len(steps) - 1:
            arrow(ax, x + w, y + h/2, x + w + gap, y + h/2, DARK_GRAY)

    ax.text(6.0, 2.5, 'PHASE-2 PLANNED EXTENSIONS', ha='center',
            fontsize=12, color=NAVY, weight='bold')

    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'diagram_phase2_flow.png'),
                dpi=200, bbox_inches='tight', facecolor=LIGHT_BG)
    plt.close(fig)
    print("  [7/7] Phase-2 flow diagram")


# ── Run all ──────────────────────────────────────────────────
if __name__ == '__main__':
    print("Generating polished diagrams...")
    make_architecture()
    make_process_flow()
    make_er_diagram()
    make_timeline()
    make_signals_diagram()
    make_results_chart()
    make_phase2_flow()
    print("\nAll 7 diagrams saved to:", OUT)
