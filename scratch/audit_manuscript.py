import os
import re

with open("build_mdpi_geosciences_manuscript.py", "r", encoding="utf-8") as f:
    code = f.read()

print("="*60)
print("1. FIGURE VERIFICATION")
print("="*60)
fig_calls = re.findall(r'add_fig\(\s*["\']([^"\']+)["\'],\s*(\d+),\s*["\']([^"\']+)["\']', code)
for path, num, cap in fig_calls:
    exists = os.path.exists(path)
    sz = os.path.getsize(path) / 1024 if exists else 0
    print(f"Figure {num}: exists={exists}, size={sz:.1f} KB, path={path}")

print("\n" + "="*60)
print("2. IN-TEXT FIGURE & TABLE CITATION AUDIT")
print("="*60)
# Extract all text calls
text_blocks = re.findall(r'text\(\s*["\'](.*?)["\']\s*[,)]', code, re.DOTALL)
full_text = " ".join(text_blocks)

for i in range(1, 8):
    cites = len(re.findall(rf'Figure\s+{i}\b', full_text))
    print(f"Figure {i} in-text citations: {cites}")

for i in range(1, 6):
    cites = len(re.findall(rf'Table\s+{i}\b', full_text))
    print(f"Table {i} in-text citations: {cites}")

print("\n" + "="*60)
print("3. REFERENCE CITATION SEQUENCE AUDIT")
print("="*60)
# Find all brackets [X] in full text
bracket_matches = re.findall(r'\[([\d\s,\-–]+)\]', full_text)
print("Found citation clusters:", bracket_matches)

cited_refs = set()
for b in bracket_matches:
    parts = re.split(r'[,;\s]+', b.strip())
    for p in parts:
        if '-' in p or '–' in p:
            dash = '-' if '-' in p else '–'
            sub = p.split(dash)
            if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                for num in range(int(sub[0]), int(sub[1]) + 1):
                    cited_refs.add(num)
        elif p.isdigit():
            cited_refs.add(int(p))

print(f"Total unique references cited in text: {len(cited_refs)}")
print("Cited numbers:", sorted(list(cited_refs)))

# Find total references in the bibliography
refs_block = re.findall(r'refs\s*=\s*\[(.*?)\]\s*\n\s*for', code, re.DOTALL)
if refs_block:
    ref_entries = re.findall(r'"([^"]+)"', refs_block[0])
    print(f"Total references in bibliography list: {len(ref_entries)}")
    missing_cites = set(range(1, len(ref_entries) + 1)) - cited_refs
    if missing_cites:
        print("WARNING: References in bibliography NEVER cited in text:", sorted(list(missing_cites)))
    else:
        print("SUCCESS: Every reference in bibliography is cited in text!")

print("\n" + "="*60)
print("4. ABSTRACT WORD COUNT")
print("="*60)
abs_match = re.search(r'r_abs_lbl\.bold = True\s+p_abs\.add_run\(\s*"(.*?)"\s*\)', code, re.DOTALL)
if abs_match:
    abstract_text = abs_match.group(1).replace('\n', ' ')
    words = abstract_text.split()
    print(f"Abstract word count: {len(words)} words")
