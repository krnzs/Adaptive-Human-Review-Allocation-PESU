import docx

def remove_instructions(doc):
    # Instructions to Students is usually at the very beginning of the template
    # Let's find the paragraph that says "Instructions to Students" and delete until we hit "TITLE" or something similar
    paragraphs = doc.paragraphs
    delete_mode = False
    
    for p in paragraphs:
        text = p.text.strip()
        if "Instructions to Students" in text:
            delete_mode = True
        
        # We can just delete paragraphs that contain generic instructional text
        if "Instructions to Students" in text or "[VERIFY" in text or "For every research paper include" in text or "where applicable" in text:
            p.clear()
            p._element.getparent().remove(p._element)
