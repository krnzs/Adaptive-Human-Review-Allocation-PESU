import re

files = ['build_full_v2_deck.py', 'generate_v2_pdf.py']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = re.sub(r'\"\[11\] J\. Lu et al\., \"Learning', r'"[11] J. Lu et al., \\"Learning', text)
    text = re.sub(r'Review,\" IEEE Trans', r'Review,\\" IEEE Trans', text)

    text = re.sub(r'\"\[12\] A\. S\. Iwashita and J\. P\. Papa, \"An Overview', r'"[12] A. S. Iwashita and J. P. Papa, \\"An Overview', text)
    text = re.sub(r'Learning,\" IEEE Access', r'Learning,\\" IEEE Access', text)

    text = re.sub(r'\"\[13\] E\. Mosqueira-Rey et al\., \"Human', r'"[13] E. Mosqueira-Rey et al., \\"Human', text)
    text = re.sub(r'Art,\" Artif', r'Art,\\" Artif', text)

    text = re.sub(r'\"\[14\] K\. Hendrickx et al\., \"Machine', r'"[14] K. Hendrickx et al., \\"Machine', text)
    text = re.sub(r'Survey,\" Mach', r'Survey,\\" Mach', text)

    text = re.sub(r'\"\[15\] M\. Sarhan, S\. Layeghy, and M\. Portmann, \"Towards', r'"[15] M. Sarhan, S. Layeghy, and M. Portmann, \\"Towards', text)
    text = re.sub(r'Datasets,\" Mob', r'Datasets,\\" Mob', text)

    text = re.sub(r'\"\[16\] M\. B\. Uddin and M\. S\. Arefin, \"BigFlow', r'"[16] M. B. Uddin and M. S. Arefin, \\"BigFlow', text)
    text = re.sub(r'Dataset,\" Data', r'Dataset,\\" Data', text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
