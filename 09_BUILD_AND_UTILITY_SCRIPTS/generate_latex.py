import os

project_dir = 'PES1PG25CA101-KARANSHETTYKN-Report'
os.makedirs(project_dir, exist_ok=True)
os.makedirs(os.path.join(project_dir, 'chapters'), exist_ok=True)
os.makedirs(os.path.join(project_dir, 'figures'), exist_ok=True)
os.makedirs(os.path.join(project_dir, 'tables'), exist_ok=True)

main_tex = r'''\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{amsmath}
\usepackage{float}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{xcolor}

\title{
    {\large Phase-I Review-II / Presentation-2 Report}\\\vspace{1cm}
    {\huge \textbf{Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift}}\\
}
\author{
    \textbf{Student:} Karan Shetty \\
    \textbf{SRN:} PES1PG25CA101 \\
    \textbf{Programme:} Master of Computer Applications \\
    \textbf{Guide:} Dilip Kumar Maripuri \\
    \vspace{1cm}\\
    Department of Computer Applications \\
    PES University
}
\date{\today}

\begin{document}

\maketitle

\tableofcontents
\listoffigures
\listoftables
\newpage

\include{chapters/abstract}
\include{chapters/introduction}
\include{chapters/literature_review}
\include{chapters/background}
\include{chapters/comparative_study}
\include{chapters/requirements}
\include{chapters/methodology}
\include{chapters/system_design}
\include{chapters/data_design}
\include{chapters/implementation}
\include{chapters/results}
\include{chapters/limitations}
\include{chapters/conclusion}

\bibliographystyle{ieeetr}
\bibliography{references}

\end{document}
'''
with open(os.path.join(project_dir, 'main.tex'), 'w', encoding='utf-8') as f:
    f.write(main_tex)

readme = '''# PES1PG25CA101-KARANSHETTYKN-Report

## Compilation Instructions
To compile the PDF report, you will need a standard LaTeX distribution such as TeX Live or MiKTeX.

Compile using pdflatex or latexmk:
\\\ash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
\\\
Or simply:
\\\ash
latexmk -pdf main.tex
\\\

## Structure
- \main.tex\: The entry point for the report.
- \chapters/\: Contains all the individual sections of the report.
- \igures/\: Place all your images (e.g., architecture diagrams, plots) here.
- \	ables/\: Additional table structures if separated.
- \eferences.bib\: Contains all IEEE style citations.

## MANUAL REVIEW REQUIRED
This project is generated from your existing source files. Please carefully review the chapters to ensure the text flows correctly. There are % TODO: placeholders in some chapters (e.g., system_design.tex, esults.tex, methodology.tex) for figures that need to be manually inserted from your project.

**Note:** The inconsistencies regarding the historical-error risk validation vs training have been flagged in the text with % TODO: comments for your review.
'''
with open(os.path.join(project_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme)

chapters = [
    'abstract', 'introduction', 'literature_review', 'background', 'comparative_study', 
    'requirements', 'methodology', 'system_design', 'data_design', 'implementation', 
    'results', 'limitations', 'conclusion'
]

for ch in chapters:
    with open(os.path.join(project_dir, 'chapters', f'{ch}.tex'), 'w', encoding='utf-8') as f:
        f.write(f'\\chapter{{{ch.replace("_", " ").title()}}}\n\n% TODO: Add content here extracted from existing project.\n')

with open(os.path.join(project_dir, 'references.bib'), 'w', encoding='utf-8') as f:
    f.write('% References\n')

print("Base structure created.")
