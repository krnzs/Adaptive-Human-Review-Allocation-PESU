with open('build_exact_mentor_report.py', 'r', encoding='utf-8') as f:
    text = f.read()

strip_logic = '''
    # STRIP INSTRUCTIONS TO STUDENTS
    delete_mode = False
    for p in doc.paragraphs:
        txt = p.text.strip()
        if txt == "Instructions to Students":
            delete_mode = True
        
        if delete_mode:
            # We stop deleting once we see something looking like a main heading like "1. TITLE" or the cover page
            if "Project Title" in txt or txt == "1. TITLE" or "Abstract" in txt:
                delete_mode = False
            else:
                p._p.getparent().remove(p._p)
                continue
                
        # Targeted deletions of other boilerplate
        if "[VERIFY BEFORE SUBMISSION" in txt or "where applicable" in txt or "For every research paper include" in txt or "[Enter Project Title]" in txt:
            try:
                p._p.getparent().remove(p._p)
            except Exception:
                pass

    # Re-fetch paragraphs after deletion
    paragraphs = doc.paragraphs
'''

# insert it right after print(f"  Captured {len(builtin_tables)} built-in tables from template.")
if 'STRIP INSTRUCTIONS TO STUDENTS' not in text:
    text = text.replace(
        'print(f"  Captured {len(builtin_tables)} built-in tables from template.")',
        'print(f"  Captured {len(builtin_tables)} built-in tables from template.")\n' + strip_logic
    )

with open('build_exact_mentor_report.py', 'w', encoding='utf-8') as f:
    f.write(text)
