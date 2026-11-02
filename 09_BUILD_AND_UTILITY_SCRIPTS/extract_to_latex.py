import os
import sys

# Add current dir to path to import
sys.path.insert(0, os.path.abspath('.'))

from report_content_part1 import content as c1
from report_content_part2 import content as c2

content = {**c1, **c2}

def clean_latex(text):
    text = text.replace('%', '\\%').replace('&', '\\&').replace('_', '\\_')
    text = text.replace('?', '-').replace('?', '"').replace('?', '"')
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
                    f.write(' & '.join(clean_latex(str(h)) for h in headers) + ' \\\\\n\\midrule\n')
                    for row in data:
                        f.write(' & '.join(clean_latex(str(c)) for c in row) + ' \\\\\n')
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

write_section('abstract', ['1. Abstract'])
write_section('introduction', ['2. Introduction', '3. Problem Statement'])
write_section('literature_review', ['4. Literature Survey']) # Will merge all 4.x in real script, wait...
