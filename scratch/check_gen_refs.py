import re
with open("generate_manuscript_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

# find reference list
ref_matches = re.findall(r'p_ref\.add_run\(\s*f?"([0-9]+\.\s+[^"]+)"\)', text)
print("Refs found in generate_manuscript_docx.py:", len(ref_matches))
if ref_matches:
    print("First 3:", ref_matches[:3])
    print("Last 3:", ref_matches[-3:])
