# -*- coding: utf-8 -*-
import os

for filename in ['artmug_live_full.html', 'index.html']:
    filepath = os.path.join(r"d:\Study\artmug side menu", filename)
    if not os.path.exists(filepath):
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Fix broken loop syntax: "for (let i = 0; i <div id="sec-notice"></div>< allEls.length; i++) {"
    broken_str = '<div id="sec-notice"></div><'
    if broken_str in content:
        content = content.replace(broken_str, '<')
        print(f"Fixed broken loop in {filename}")

    # 2. Insert <div id="sec-notice"></div> properly right before '<b><font color="#666666">신청 전 주의사항</font></b>'
    target_heading = '<b><font color="#666666">신청 전 주의사항</font></b>'
    if target_heading in content:
        # Check if already preceded by id="sec-notice"
        if '<div id="sec-notice">' not in content:
            content = content.replace(target_heading, f'<div id="sec-notice"></div>{target_heading}')
            print(f"Properly inserted #sec-notice before heading in {filename}")
        else:
            print(f"#sec-notice already exists in {filename}")
    else:
        # Fallback search for just '신청 전 주의사항' in body
        print(f"Target heading not found exactly in {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filename}")
