with open("generate_manuscript_docx.py", "r", encoding="utf-8") as f:
    orig_code = f.read()

import re
cites_orig = re.findall(r'\[([0-9,\s\-–]+)\]', orig_code)
print("Original citations count:", len(cites_orig))

with open("paper_latex/Research_Article_Geosciences_Journal.tex", "r", encoding="utf-8") as f:
    tex_code = f.read()

tex_cites = re.findall(r'\\cite\{([^}]+)\}', tex_code)
print("Tex citations count:", len(tex_cites))
print("Sample tex citations:", tex_cites[:10])
