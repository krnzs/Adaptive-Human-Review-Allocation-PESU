import os

files = ['report_content_part1.py', 'report_content_part2.py', 'build_full_v2_deck.py']

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Progress percentage
    text = text.replace("85%", "96.4%")
    text = text.replace("12 of 14", "13 of 14")
    
    # 2. Add clarifications if not present
    if "PENDING METRICS" not in text and filepath == "report_content_part2.py":
        # Let's insert a bullet point in the Future Work or Conclusion
        insert_text = '''
        ("p", "PENDING IMPLEMENTATIONS (Per Review-II Feedback):", "1. "),
        ("bullet", "PR-AUC, Balanced Accuracy, and formal Calibration metrics (ECE) are NOT YET IMPLEMENTED and will be added in Phase-II."),
        ("bullet", "Minority-class isolation results, False-Negative (FN) capture, and False-Positive (FP) capture rates are NOT YET IMPLEMENTED and are deferred to Phase-II."),
        ("bullet", "A full additive ablation study (Confidence vs Conf+OOD vs Conf+OOD+Drift vs Conf+OOD+Drift+HistErr) is NOT YET IMPLEMENTED."),
        ("bullet", "A public repository or stable demo URL is NOT YET IMPLEMENTED and will be released upon project completion."),
        '''
        text = text.replace('("p", "17. CONCLUSION AND FUTURE WORK", True),', '("p", "17. CONCLUSION AND FUTURE WORK", True),\n' + insert_text)

    # 3. Leakage & Feedback
    text = text.replace("real-time feedback", "offline simulated feedback")
    text = text.replace("real-time adaptive", "offline simulated adaptive")
    text = text.replace("live feedback", "simulated feedback")

    # 4. Clarifying PSI
    # We will search for any mention of PSI and ensure we don't say it's instance level.
    # Actually, we can add a specific bullet for it in Part 2.
    if "BATCH-LEVEL PSI CONVERSION" not in text and filepath == "report_content_part2.py":
        psi_clarification = '''
        ("p", "BATCH-LEVEL TO INSTANCE-LEVEL CONVERSION:"),
        ("bullet", "Batch-level PSI is calculated over the entire evaluation window to determine the global 'Drift Regime' (Low, Moderate, or High)."),
        ("bullet", "This global regime dictates the proportional weights assigned to the signals (e.g., higher weight to drift-risk during High-Regime)."),
        ("bullet", "Instance-level priority is then calculated by applying these global weights to the specific instance's OOD percentile and historical error risk."),
        '''
        if '("p", "8.1 Methodology Overview' in text:
            text = text.replace('("p", "8.1 Methodology Overview', psi_clarification + '\n        ("p", "8.1 Methodology Overview')
            
    # 5. Historical Error
    text = text.replace("historical errors", "training-set mistakes")
    text = text.replace("historical error risk", "historical error risk (training-set mistakes)")

    # 6. Label availability
    if "Ground-truth labels are strictly held out" not in text and filepath == "report_content_part2.py":
        leakage = '''
        ("p", "LEAKAGE CONTROL & LABEL AVAILABILITY:"),
        ("bullet", "Model training and centroid generation use exclusively the Chronological Training Split."),
        ("bullet", "Hyperparameter tuning and risk-weight calibration use exclusively the Validation Split."),
        ("bullet", "Ground-truth labels for the Shifted Test Split are STRICTLY HELD OUT during prediction. They are only revealed to the system after an instance is selected for 'review' in the offline simulation, preventing look-ahead leakage."),
        '''
        if '("p", "LEAKAGE CONTROL' not in text:
            text = text.replace('("p", "8.2 Proposed System Architecture', leakage + '\n        ("p", "8.2 Proposed System Architecture')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
