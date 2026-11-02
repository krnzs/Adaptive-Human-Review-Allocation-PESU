import os
import glob

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    modified = False
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

files = glob.glob('PES1PG25CA101-KARANSHETTYKN-Report/chapters/*.tex')
for f in files:
    replacements = [
        # Percentage string replacements
        ('13 of 14 requirements complete (93\\%)', '13 of 14 functional requirements are fully implemented; FR14 is partially implemented.'),
        ('13 of 14 requirements complete (93%)', '13 of 14 functional requirements are fully implemented; FR14 is partially implemented.'),
        ('13.5 of 14 Modules Implemented (96.4\\%)', '13 of 14 functional requirements are fully implemented; FR14 is partially implemented.'),
        
        # Add TODOs for feedback loop and historical errors
        ('simulated ground-truth review oracle', 'simulated ground-truth review oracle\n\n% TODO: INCONSISTENCY DETECTED - Ensure the feedback loop logic described here exactly matches the implementation in src/28_sequential_feedback_eval.py'),
        ('Training errors', 'Training errors\n\n% TODO: Ensure this accurately reflects how the historical-error risk score is calculated in the source code.'),
        ('training errors', 'training errors\n\n% TODO: Ensure this accurately reflects how the historical-error risk score is calculated in the source code.')
    ]
    replace_in_file(f, replacements)
