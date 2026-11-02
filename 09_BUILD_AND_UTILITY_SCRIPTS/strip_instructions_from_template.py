import docx
import os

filepath = 'build_exact_mentor_report.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add instruction-stripping logic immediately after loading the template
strip_logic = '''
    print(f"  Captured {len(builtin_tables)} built-in tables from template.")
    
    # 0. STRIP "Instructions to Students" from the template
    delete_mode = False
    for p in list(doc.paragraphs):
        txt = p.text.strip()
        if "Instructions to Students" in txt:
            delete_mode = True
        
        if delete_mode:
            p._element.getparent().remove(p._element)
            if "Candidate PES1PG25CA101" in txt or "Project Title" in txt or "Karan Shetty" in txt or "MCA" in txt:
                # We reached the cover page, stop deleting!
                pass # Wait, if I just blindly delete, I might delete the cover page if it's on the same run!
'''
# Actually, the instructions to students is usually BEFORE or AFTER the cover page.
# If I just check if the paragraph contains "Instructions to Students", "For every research paper include:", "[VERIFY BEFORE SUBMISSION", I can delete them specifically!
