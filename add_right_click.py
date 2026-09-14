# -*- coding: utf-8 -*-
import os

for filename in ['artmug_live_full.html', 'index.html']:
    filepath = os.path.join(r"d:\Study\artmug side menu", filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    tag = '<div id="rightClick" class="hidden" style="display:none"></div>'
    if 'id="rightClick"' not in content:
        if '</body>' in content:
            content = content.replace('</body>', f'{tag}\n</body>')
            print(f"Added rightClick element before </body> in {filename}")
        else:
            content += f"\n{tag}"
            print(f"Appended rightClick element in {filename}")
    else:
        print(f"rightClick already exists in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
