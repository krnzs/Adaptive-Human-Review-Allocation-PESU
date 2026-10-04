"""
PES UNIVERSITY - DEPARTMENT OF COMPUTER APPLICATIONS
MCA CAPSTONE PROJECT 2025-27 - PHASE I REVIEW II REPORT
MASTER SECTION CONTENT MERGER
"""

from report_content_part1 import get_part1_content
from report_content_part2 import get_part2_content

def get_all_section_content():
    content = {}
    content.update(get_part1_content())
    content.update(get_part2_content())
    return content

if __name__ == "__main__":
    all_c = get_all_section_content()
    print(f"Total sections defined: {len(all_c)}")
    for k in list(all_c.keys())[:10]:
        print(f"  {k} -> {len(all_c[k])} items")
