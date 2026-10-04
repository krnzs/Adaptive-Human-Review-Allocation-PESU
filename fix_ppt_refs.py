import re

with open('build_full_v2_deck.py', 'r', encoding='utf-8') as f:
    text = f.read()

# I will just rewrite Slide 24 completely
replacement_slide_24 = '''# SLIDE 24: REFERENCES (CONTINUED)
# ==============================================================================
s24 = create_base_slide("References & Bibliography", "Key Literature & Technical References (Part 2)")

add_card(s24, Inches(0.5), Inches(1.25), Inches(12.3), Inches(5.7))
tb_r2 = s24.shapes.add_textbox(Inches(0.7), Inches(1.35), Inches(11.9), Inches(5.5))
tf_r2 = tb_r2.text_frame
tf_r2.word_wrap = True

p = tf_r2.paragraphs[0]
p.text = "REFERENCES [9] TO [16]"
p.font.name = "Calibri"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = C_NAVY

refs_part2 = [
    "[9] P. W. Koh et al., \\"WILDS: A Benchmark of In-the-Wild Distribution Shifts,\\" ICML, PMLR, vol. 139, 2021.",
    "[10] K. He, D. D. Kim, and M. R. Asghar, \\"Adversarial Machine Learning for Network Intrusion Detection Systems,\\" IEEE Commun. Surv. Tutorials, vol. 25, no. 1, 2023.",
    "[11] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, \\"Learning under Concept Drift: A Review,\\" IEEE Trans. Knowl. Data Eng., vol. 31, no. 12, pp. 2346-2363, 2019.",
    "[12] A. S. Iwashita and J. P. Papa, \\"An Overview on Concept Drift Learning,\\" IEEE Access, vol. 7, pp. 1532-1547, 2019.",
    "[13] E. Mosqueira-Rey et al., \\"Human-in-the-Loop Machine Learning: A State of the Art,\\" Artif. Intell. Rev., vol. 56, no. 4, pp. 3005-3054, 2023.",
    "[14] K. Hendrickx et al., \\"Machine Learning with a Reject Option: A Survey,\\" Mach. Learn., vol. 113, no. 5, pp. 1973-2010, 2024.",
    "[15] M. Sarhan, S. Layeghy, and M. Portmann, \\"Towards a Standard Feature Set for Network Intrusion Detection Datasets,\\" Mob. Networks Appl., vol. 27, pp. 1082-1093, 2022.",
    "[16] M. B. Uddin and M. S. Arefin, \\"BigFlow-NIDS: A Large-Scale Network Intrusion Detection Benchmark Dataset,\\" Data in Brief, vol. 65, 2026."
]

for ref in refs_part2:
    p = tf_r2.add_paragraph()
    p.text = ref
    p.font.size = Pt(12)
    p.font.color.rgb = C_DARK
    p.space_after = Pt(10)

add_speaker_notes(s24, "These are the remaining references detailing NIDS adversarial testing, concept drift (Lu et al., Iwashita & Papa), and the BigFlow-NIDS benchmark dataset.")
'''

# Use regex to replace everything from # SLIDE 24: down to # SAVE PRESENTATION
text = re.sub(
    r'# SLIDE 24: REFERENCES - TEXTBOOKS.*?# ==============================================================================\n# SAVE PRESENTATION',
    replacement_slide_24 + '\n# ==============================================================================\n# SAVE PRESENTATION',
    text,
    flags=re.DOTALL
)

with open('build_full_v2_deck.py', 'w', encoding='utf-8') as f:
    f.write(text)
