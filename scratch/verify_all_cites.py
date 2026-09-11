import re

with open("build_mdpi_geosciences_manuscript.py", "r", encoding="utf-8") as f:
    code = f.read()

# Match text, bullet, equation, h1, h2, h3
calls = re.findall(r'(?:text|bullet|equation|h1|h2|h3)\(\s*["\'](.*?)["\']\s*[,)]', code, re.DOTALL)
full_text = " ".join(calls)

# Match [X]
matches = re.findall(r'\[([0-9,\s\-–]+)\]', full_text)
print("All clusters:", matches)

all_cited = set()
for b in matches:
    parts = re.split(r'[,;\s]+', b.strip())
    for p in parts:
        if '-' in p or '–' in p:
            dash = '-' if '-' in p else '–'
            sub = p.split(dash)
            if len(sub) == 2 and sub[0].isdigit() and sub[1].isdigit():
                for n in range(int(sub[0]), int(sub[1]) + 1):
                    all_cited.add(n)
        elif p.isdigit():
            all_cited.add(int(p))

print("Total cited numbers:", len(all_cited))
print("Sorted:", sorted(list(all_cited)))
missing = set(range(1, 37)) - all_cited
print("Missing:", missing)
