import re

with open("build_mdpi_geosciences_manuscript.py", "r", encoding="utf-8") as f:
    py_code = f.read()

# Extract all string literals passed to text(), bullet(), equation(), h1(), h2(), h3()
all_texts = re.findall(r'(?:text|bullet|equation|h1|h2|h3)\(\s*["\'](.*?)["\']\s*[,)]', py_code, re.DOTALL)
combined = " ".join(all_texts)

# Find all citations [X]
citations = re.findall(r'\[([0-9,\s\-–]+)\]', combined)
print("Found in text/bullet:", citations)

cited = set()
for c in citations:
    parts = re.split(r'[,;\s]+', c.strip())
    for p in parts:
        if '-' in p or '–' in p:
            dash = '-' if '-' in p else '–'
            sub = p.split(dash)
            if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                for n in range(int(sub[0]), int(sub[1]) + 1):
                    cited.add(n)
        elif p.isdigit():
            cited.add(int(p))

print("Total cited:", len(cited))
print("Cited IDs:", sorted(list(cited)))
missing = set(range(1, 37)) - cited
print("Missing IDs:", sorted(list(missing)))
