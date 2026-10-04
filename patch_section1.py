import os

def patch_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: could not find {repr(old)} in {filepath}")
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Fix report parts
part1 = "report_content_part1.py"
if os.path.exists(part1):
    patch_file(part1, [
        ("Implementation Status: 13 fully implemented + FR14 partially implemented (50%) = 13.5/14 = 96.4%", 
         "13 of 14 requirements complete (93%)"),
        ("13.5 out of 14 FRs complete (96.4%).", 
         "13 of 14 functional requirements are fully implemented; 1 (the interactive dashboard, FR14) is partially implemented as a local Streamlit demo."),
        ("FR14: Interactive Dashboard/UI (50% - Partially Implemented locally)", 
         "FR14: Interactive Dashboard/UI (Partial - Local Streamlit demo)"),
        ("13.5 out of 14 Modules Implemented (96.4%)", "13 of 14 requirements complete (93%)")
    ])

part2 = "report_content_part2.py"
if os.path.exists(part2):
    patch_file(part2, [
        ("Implementation Status: 13 fully implemented + FR14 partially implemented (50%) = 13.5/14 = 96.4%", 
         "13 of 14 requirements complete (93%)"),
        ("13.5 of 14 Modules Implemented", "13 of 14 requirements complete (93%)")
    ])

# Fix PPT
ppt = "generate_presentation_deck.py"
if os.path.exists(ppt):
    patch_file(ppt, [
        ("13.5 of 14 Modules Implemented (96.4%)", "13 of 14 requirements complete (93%)"),
        ("13.5 of 14 functional requirements are fully implemented", "13 of 14 functional requirements are fully implemented; 1 (the interactive dashboard, FR14) is partially implemented as a local Streamlit demo."),
        ("13.5 out of 14 Modules Implemented (96.4%)", "13 of 14 requirements complete (93%)"),
        ("Implementation Status: 13 fully implemented + FR14 partially implemented (50%) = 13.5/14 = 96.4%", "13 of 14 requirements complete (93%)"),
        ("13 of 14 Modules Implemented (92.8% Complete)", "13 of 14 requirements complete (93%)"),
        ("96.4%", "13 of 14 requirements complete (93%)")
    ])

print("Section 1 patch complete.")
