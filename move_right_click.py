# -*- coding: utf-8 -*-
import os

for filename in ['artmug_live_full.html', 'index.html']:
    filepath = os.path.join(r"d:\Study\artmug side menu", filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    tag = '<div id="rightClick" class="hidden" style="display:none"></div>'
    
    # Remove existing instances
    content = content.replace(f'{tag}\n', '').replace(tag, '')

    # Find the script containing rightClickElem
    target_str = 'const rightClickElem = document.getElementById("rightClick")'
    if target_str in content:
        script_idx = content.rfind('<script', 0, content.find(target_str))
        if script_idx != -1:
            content = content[:script_idx] + f"{tag}\n" + content[script_idx:]
            print(f"Placed rightClick div right before script in {filename}")
        else:
            idx = content.find(target_str)
            content = content[:idx] + f"{tag}\n" + content[idx:]
            print(f"Placed rightClick div before line in {filename}")
    else:
        # Fallback before </body>
        if '</body>' in content:
            content = content.replace('</body>', f'{tag}\n</body>')
        print(f"Placed rightClick div before </body> in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filename}")
