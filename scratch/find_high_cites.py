import re
with open("generate_manuscript_docx.py", "r", encoding="utf-8") as f:
    text = f.read()

matches = re.finditer(r'\[([0-9,\s\-–]+)\]', text)
for m in matches:
    val = m.group(1)
    if any(c in val for c in ['19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36']):
        start = max(0, m.start() - 50)
        end = min(len(text), m.end() + 50)
        snippet = text[start:end].replace('\n', ' ')
        print(f"Match [{val}]: ...{snippet}...")
