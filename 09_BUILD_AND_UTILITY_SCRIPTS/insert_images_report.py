import re

files = ['report_content_part1.py', 'report_content_part2.py']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Figure 11.1
    text = re.sub(
        r'\(\"p\", \"Figure 11\.1.*?\"\)',
        r'("img", "diagrams/v2_architecture.png", "Figure 11.1 - End-to-End System Architecture")',
        text
    )
    # Figure 11.2
    text = re.sub(
        r'\(\"p\", \"Figure 11\.2.*?\"\)',
        r'("img", "diagrams/v2_use_case.png", "Figure 11.2 - UML Use-Case Diagram")',
        text
    )
    # Figure 11.3
    text = re.sub(
        r'\(\"p\", \"Figure 11\.3.*?\"\)',
        r'("img", "diagrams/v2_process_flow.png", "Figure 11.3 - End-to-End Operational Process Flow")',
        text
    )
    # Figure 12.1
    text = re.sub(
        r'\(\"p\", \"Figure 12\.1.*?\"\)',
        r'("img", "diagrams/v2_data_schema.png", "Figure 12.1 - Conceptual ER / Data Schema Diagram")',
        text
    )
    # Figure 14.1
    text = re.sub(
        r'\(\"p\", \"Figure 14\.1.*?\"\)',
        r'("img", "diagrams/v2_module_status.png", "Figure 14.1 - Implementation Progress")',
        text
    )
    # Figure 15.1
    text = re.sub(
        r'\(\"p\", \"Figure 15\.1.*?\"\)',
        r'("img", "diagrams/figure_15_1.png", "Figure 15.1 - Comparative Error Capture Rate Across Review Budgets")',
        text
    )
    # Figure 15.2
    text = re.sub(
        r'\(\"p\", \"Figure 15\.2.*?\"\)',
        r'("img", "diagrams/figure_15_2.png", "Figure 15.2 - Top 10 Features Exhibiting Highest PSI Drift")',
        text
    )
    # Figure 15.3
    text = re.sub(
        r'\(\"p\", \"Figure 15\.3.*?\"\)',
        r'("img", "diagrams/figure_15_3.png", "Figure 15.3 - Review Efficiency Across Allocation Budgets")',
        text
    )
    
    # Also remove "Instructions to Students" entirely.
    # The prompt explicitly asks to delete the Instructions to Students section.
    # The build_exact_mentor_report script doesn't actually print an "Instructions to Students" heading 
    # but I'll make sure there's no boilerplate text anywhere.
    text = text.replace('Instructions to Students', '')
    text = text.replace('[VERIFY', '')
    text = text.replace('where applicable', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
