import re

files = ['build_full_v2_deck.py', 'generate_v2_pdf.py']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('Drift Monitoring [1], [8], [9]', 'Drift Monitoring [11], [12]')
    text = text.replace('Cao et al., ICCV 2023 [1]; Yang et al., IJCV 2024 [8]', 'Lu et al., IEEE TKDE 2019 [11]; Iwashita & Papa, IEEE Access 2019 [12]')
    
    text = text.replace('Learning to Defer (L2D) [2], [3], [7]', 'Learning to Defer (L2D) [2], [3], [7], [14]')
    text = text.replace('(Mozannar & Sontag, 2020 [2]; Wei et al., 2024 [3]; Liu et al., 2022 [7])', '(Mozannar & Sontag, 2020 [2]; Wei et al., 2024 [3]; Liu et al., 2022 [7]; Hendrickx et al., 2024 [14])')
    
    text = text.replace('Human-in-the-Loop Intrusion Detection [6], [10]', 'Human-in-the-Loop Intrusion Detection [6], [13]')
    text = text.replace('(Kim et al., IEEE TIFS 2024 [6]; He et al., IEEE COMST 2023 [10])', '(Kim et al., IEEE TIFS 2024 [6]; Mosqueira-Rey et al., 2023 [13])')

    text = re.sub(r'\[11\] M\. B\. Uddin.*?\]', r'[11] J. Lu et al., "Learning under Concept Drift: A Review," IEEE Trans. Knowl. Data Eng., vol. 31, no. 12, pp. 2346-2363, 2019. [IEEE & Scopus]', text, flags=re.IGNORECASE|re.DOTALL)
    
    text = re.sub(r'\[12\] T\. Hastie.*?2009\.', r'[12] A. S. Iwashita and J. P. Papa, "An Overview on Concept Drift Learning," IEEE Access, vol. 7, pp. 1532-1547, 2019. [IEEE & Scopus]', text, flags=re.IGNORECASE|re.DOTALL)
    
    text = re.sub(r'\[13\] C\. M\. Bishop.*?2006\.', r'[13] E. Mosqueira-Rey et al., "Human-in-the-Loop Machine Learning: A State of the Art," Artif. Intell. Rev., vol. 56, no. 4, pp. 3005-3054, 2023. [Scopus Indexed]', text, flags=re.IGNORECASE|re.DOTALL)
    
    text = re.sub(r'\[14\] T\. Chen.*?2939785\.', r'[14] K. Hendrickx et al., "Machine Learning with a Reject Option: A Survey," Mach. Learn., vol. 113, no. 5, pp. 1973-2010, 2024. [Scopus Indexed]', text, flags=re.IGNORECASE|re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
