# Monday Demo Instructions

**Project:** Reliable Review Allocation Under Distribution Shift
**Student:** Karan Shetty K N (PES1PG25CA101)
**Guide:** Prof. Dilip Kumar Maripuri

## Prerequisites

Before running the demo script, ensure dependencies are installed:

```bash
# Activate virtual environment (if using one)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the Demo

### Option 1: Automated Demo Script

Run the comprehensive demo script:

```bash
python src/demo_monday.py
```

This will:
1. Load pre-trained XGBoost model
2. Generate predictions on shifted test set
3. Compute all reliability signals
4. Apply adaptive risk scoring
5. Demonstrate queue-capacity enforcement
6. Show error-capture results
7. Display class-specific (FN/FP) error capture
8. Explicitly show label revelation timing
9. Show ablation study results

### Option 2: Manual Step-by-Step Demo

For a more interactive demo, run scripts sequentially:

```bash
# Step 1: Generate shifted test predictions
python src/16_shifted_test_predictions.py

# Step 2: Compute all reliability signals
python src/17_shifted_test_signals.py

# Step 3: Compare strategies
python src/18_shifted_review_comparison.py

# Step 4: Run feedback-informed adaptive evaluation
python src/24_shifted_feedback_evaluation.py

# Step 5: Generate final comparison
python src/25_final_strategy_comparison.py
```

### Option 3: Streamlit Dashboard

Launch the interactive dashboard:

```bash
streamlit run dashboard/app.py
```

## Demo Talking Points

### 1. Problem Statement
- Human-review capacity is constrained (1%, 2%, 5%, 10% budgets)
- Models can be confident but wrong under distribution shift
- Need to prioritize which predictions to review

### 2. Solution Approach
- Multi-factor reliability engine combining:
  - Prediction confidence
  - Mahalanobis OOD distance
  - PSI-based drift detection
  - Historical error patterns

### 3. Key Results
- At 1% budget: Adaptive captures 17.80% vs Confidence 13.51%
- At 2% budget: Adaptive captures 34.26% vs Confidence 26.73%
- At 5% budget: Confidence leads (65.45% vs Adaptive 45.90%)
- At 10% budget: Confidence leads (84.01% vs Adaptive 52.35%)

**Interpretation:** Adaptive is better at tight budgets, confidence better at larger budgets

### 4. Class-Specific Results
- Adaptive captures 604 false negatives at 1% budget
- Confidence captures 238 false negatives at 1% budget
- Adaptive is better at catching missed attacks (FN)

### 5. Ablation Study
- Removing confidence: 0.35% (severe degradation)
- Removing historical: 0.73% (significant degradation)
- Removing OOD: 17.45% (minimal impact)
- Removing drift: 17.54% (minimal impact)

**Conclusion:** Confidence is the strongest signal, historical error provides complementary value

### 6. Leakage Control
- Historical error risk comes from TRAINING mistakes only
- Model selection uses validation only
- Adaptive weights are heuristic, not learned from test
- Ground-truth labels revealed ONLY AFTER review queue selection

### 7. Workflow Boundary
- Stage 1: Offline benchmarking (current Phase-I)
- Stage 2: Simulated reviewer feedback (current experiment)
- Stage 3: Future operational reviewer workflow (Phase-II)

## Files to Show

1. **results/final_shifted_strategy_comparison.csv** - Complete strategy comparison
2. **results/extended_strategy_eval.csv** - Ablation and FN/FP results
3. **results/split_audit.csv** - Dataset split statistics
4. **src/24_shifted_feedback_evaluation.py** - Shows label revelation timing
5. **LEAKAGE_AUDIT.md** - Leakage control verification

## Progress Reporting

**Implementation Status: 96.4%**
- FR1-FR13: 100% complete (13/13 functional requirements)
- FR14 (Dashboard): 50% complete (local prototype only)

**Calculation:** (13 × 100% + 1 × 50%) / 14 = 96.4%

## References

- BigFlow-NIDS: 500,000 real flows from 66.9M benchmark
- 49 numerical features
- Binary classification (benign vs attack)
- Temporal split: 70% train, 15% validation, 15% shifted test
