import os
import glob

def patch_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Fix report parts
part2 = "report_content_part2.py"
if os.path.exists(part2):
    patch_file(part2, [
        ("Attack prevalence = 0.35%", "Attack prevalence = 6.10%"),
        ("lambda = 1e-4", "eps = 1e-6"),
        ("13 of 14 Modules Implemented (92.8% Complete)", "Implementation Status: 13 fully implemented + FR14 partially implemented (50%) = 13.5/14 = 96.4%"),
        ("FR14 Interactive Dashboard/UI - 0%", "FR14 Interactive Dashboard/UI - 50%"),
        ("13 of 14 Modules Implemented", "13.5 of 14 Modules Implemented")
    ])

part1 = "report_content_part1.py"
if os.path.exists(part1):
    patch_file(part1, [
        ("FR14: Interactive Dashboard/UI (0% - Not Implemented)", "FR14: Interactive Dashboard/UI (50% - Partially Implemented locally)"),
        ("13 out of 14 FRs complete.", "13.5 out of 14 FRs complete (96.4%).")
    ])

# Let's fix the PPTX generator if it exists
ppt = "generate_presentation_deck.py"
if os.path.exists(ppt):
    patch_file(ppt, [
        ("Attack prevalence = 0.35%", "Attack prevalence = 6.10%"),
        ("lambda = 1e-4", "eps = 1e-6"),
        ("13 of 14 Modules Implemented", "13.5 of 14 Modules Implemented (96.4%)"),
        ("0%", "50%")
    ])

print("Patching complete.")
