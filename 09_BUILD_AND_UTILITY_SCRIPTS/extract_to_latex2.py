import os
import sys

# Add current dir to path to import
sys.path.insert(0, os.path.abspath('.'))

from report_content_part1 import get_part1_content
from report_content_part2 import get_part2_content

content = {**get_part1_content(), **get_part2_content()}

def clean_latex(text):
    if not isinstance(text, str):
        return str(text)
    # Basic escapes
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('%', '\\%').replace('&', '\\&').replace('_', '\\_')
    text = text.replace('$', '\\$').replace('#', '\\#')
    # Typographic replacements for PDF generator unicode
    text = text.replace('?"', '--')
    text = text.replace('?', '$\\bullet$')
    text = text.replace('?"', '"').replace('?"', '"')
    return text

def write_section(filename, keys):
    with open(f'PES1PG25CA101-KARANSHETTYKN-Report/chapters/{filename}.tex', 'w', encoding='utf-8') as f:
        f.write(f'\\chapter{{{filename.replace("_", " ").title()}}}\n\n')
        
        for key in keys:
            if key not in content:
                continue
            
            section_title = key.split('. ', 1)[1] if '. ' in key else key
            f.write(f'\\section{{{clean_latex(section_title)}}}\n\n')
            
            for item in content[key]:
                if item[0] == 'p':
                    # Paragraph
                    f.write(f'{clean_latex(item[1])}\n\n')
                elif item[0] == 'table':
                    # Table
                    headers = item[1]
                    data = item[2]
                    f.write('\\begin{table}[H]\n\\centering\n')
                    cols = 'c' * len(headers)
                    f.write(f'\\begin{{tabular}}{{{cols}}}\n\\toprule\n')
                    f.write(' & '.join(clean_latex(h) for h in headers) + ' \\\\\n\\midrule\n')
                    for row in data:
                        f.write(' & '.join(clean_latex(c) for c in row) + ' \\\\\n')
                    f.write('\\bottomrule\n\\end{tabular}\n')
                    f.write(f'\\caption{{{clean_latex(section_title)} Table}}\n')
                    f.write('\\end{table}\n\n')
                elif item[0] == 'img':
                    # Image
                    f.write('\\begin{figure}[H]\n\\centering\n')
                    f.write(f'% TODO: Insert verified architecture diagram/image here: {item[1]}\n')
                    f.write(f'\\includegraphics[width=0.8\\textwidth]{{figures/placeholder.png}}\n')
                    f.write(f'\\caption{{Figure placeholder for {clean_latex(item[1])}}}\n')
                    f.write('\\end{figure}\n\n')

# Map the sections correctly
write_section('abstract', ['1. Abstract'])
write_section('introduction', ['2. Introduction', '3. Problem Statement'])
write_section('literature_review', [k for k in content.keys() if k.startswith('4.')])
write_section('background', ['5. Objectives of the Work', '6. Application Scope'])
write_section('comparative_study', ['7. Comparative Study'])
write_section('requirements', ['8. Limitations of Existing System', '9. Proposed System', '10. Target Users & Tools', '11. Functional Requirements', '12. Non-Functional Requirements'])
write_section('methodology', ['13. Methodology'])
write_section('system_design', ['14. System Design'])
write_section('data_design', ['15. Data Design'])
write_section('implementation', ['16. Implementation Details'])
write_section('results', ['18. Results and Evaluation'])
write_section('limitations', ['19. Project Limitations and Future Work'])
write_section('conclusion', ['21. Conclusion'])

# Add AI Disclosure and references manually if needed
print("Chapters written.")
