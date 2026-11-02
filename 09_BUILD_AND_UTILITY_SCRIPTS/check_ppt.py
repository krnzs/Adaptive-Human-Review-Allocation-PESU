from pptx import Presentation

prs = Presentation(r'C:\Users\Admin CDS\OneDrive\Desktop\Capstone Project\Adaptive_Human_Review_Allocation_PESU_FINAL.pptx')
print('Total slides:', len(prs.slides))
for i, slide in enumerate(prs.slides[:5]):
    title = slide.shapes.title.text if slide.shapes.title else "No title"
    print(f'Slide {i+1}: {title}')
