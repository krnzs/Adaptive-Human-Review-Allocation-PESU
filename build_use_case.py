import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

OUT_DIR = "diagrams"
os.makedirs(OUT_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# System Boundary
boundary = patches.Rectangle((3, 0.5), 6.5, 5, fill=False, edgecolor='#0B192C', linewidth=2, linestyle='--')
ax.add_patch(boundary)
ax.text(6.25, 5.2, "Adaptive Review System (Offline Phase-I)", fontsize=12, fontweight='bold', ha='center')

# Actors
ax.text(1, 4.5, "ML\nPractitioner", fontsize=10, fontweight='bold', ha='center', bbox=dict(boxstyle="circle,pad=0.5", facecolor="#E2E8F0"))
ax.text(1, 2.5, "System\nEvaluator", fontsize=10, fontweight='bold', ha='center', bbox=dict(boxstyle="circle,pad=0.5", facecolor="#E2E8F0"))
ax.text(1, 0.8, "Simulated\nReview Oracle", fontsize=10, fontweight='bold', ha='center', bbox=dict(boxstyle="circle,pad=0.5", facecolor="#FEF2F2", edgecolor="#EF4444"))

# Use Cases
use_cases = [
    (5, 4.5, "Dataset Ingestion & Split"),
    (5, 3.8, "Model Training & Signals"),
    (5, 3.1, "Risk Scoring"),
    (5, 2.4, "Budget Allocation"),
    (7.5, 3.1, "Review Queue Evaluation"),
    (7.5, 2.4, "Feedback Evaluation"),
    (7.5, 1.7, "Dashboard Analysis")
]

for x, y, label in use_cases:
    ellipse = patches.Ellipse((x, y), 2.2, 0.5, facecolor="#DBEAFE", edgecolor="#1D4ED8", linewidth=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, label, fontsize=8, ha='center', va='center', fontweight='bold')

# Connections (Lines)
ax.plot([1.5, 3.9], [4.5, 4.5], color='#64748B')
ax.plot([1.5, 3.9], [4.5, 3.8], color='#64748B')
ax.plot([1.5, 3.9], [2.5, 3.1], color='#64748B')
ax.plot([1.5, 3.9], [2.5, 2.4], color='#64748B')
ax.plot([1.5, 6.4], [2.5, 3.1], color='#64748B')
ax.plot([1.5, 6.4], [2.5, 2.4], color='#64748B')
ax.plot([1.5, 6.4], [2.5, 1.7], color='#64748B')

# Oracle connects to Evaluation
ax.plot([1.5, 6.4], [0.8, 3.1], color='#EF4444', linestyle=':')
ax.plot([1.5, 6.4], [0.8, 2.4], color='#EF4444', linestyle=':')

plt.tight_layout()
plt.savefig("diagrams/v2_use_case.png", dpi=300)
plt.close()
