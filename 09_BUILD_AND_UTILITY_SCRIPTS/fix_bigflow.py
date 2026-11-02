import re

files = ['build_full_v2_deck.py', 'generate_v2_pdf.py']

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # BigFlow was cited as [11] in the text
    text = text.replace('BigFlow-NIDS [11]', 'BigFlow-NIDS [16]')
    text = text.replace('BigFlow-NIDS benchmark [11]', 'BigFlow-NIDS benchmark [16]')
    text = text.replace('BIGFLOW-NIDS BENCHMARK (2026) [11]', 'BIGFLOW-NIDS BENCHMARK (2026) [16]')
    
    # Append 15 and 16 to the references list on slide 24 (if it fits, otherwise just add it to the string block)
    if '[16] M. B. Uddin' not in text:
        # Find where [14] is and append 15 and 16
        text = text.replace('[14] K. Hendrickx et al., "Machine Learning with a Reject Option: A Survey," Mach. Learn., vol. 113, no. 5, pp. 1973-2010, 2024. [Scopus Indexed]',
                            '[14] K. Hendrickx et al., "Machine Learning with a Reject Option: A Survey," Mach. Learn., vol. 113, no. 5, pp. 1973-2010, 2024. [Scopus Indexed]",\n            "[15] M. Sarhan, S. Layeghy, and M. Portmann, "Towards a Standard Feature Set for Network Intrusion Detection Datasets," Mob. Networks Appl., vol. 27, pp. 1082-1093, 2022. [Scopus Indexed]",\n            "[16] M. B. Uddin and M. S. Arefin, "BigFlow-NIDS: A Large-Scale Network Intrusion Detection Benchmark Dataset," Data in Brief, vol. 65, Art. no. 112530, April 2026. [Scopus Indexed]')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
