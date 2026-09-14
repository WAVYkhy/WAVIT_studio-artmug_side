# -*- coding: utf-8 -*-
import os
import re

nav_5_buttons_html = """  <!-- \ubaa9\ucc28 (5\uac1c \ud56d\ubaa9) -->
  <div class="wm-section-label">Quick Navigation</div>
  <ul class="wm-nav-list">
    <li class="wm-nav-item">
      <button type="button" onclick="wmScrollTo('sec-preview')">
        <span>\uc601\uc0c1 \ubbf8\ub9ac\ubcf4\uae30</span>
        <span class="wm-nav-arrow">&rarr;</span>
      </button>
    </li>
    <li class="wm-nav-item">
      <button type="button" onclick="wmScrollTo('sec-schedule')">
        <span>\uc791\uc5c5 \uc77c\uc815</span>
        <span class="wm-nav-arrow">&rarr;</span>
      </button>
    </li>
    <li class="wm-nav-item">
      <button type="button" onclick="wmScrollTo('sec-portfolio')">
        <span>\ud3ec\ud2b8\ud3f4\ub9ac\uc624</span>
        <span class="wm-nav-arrow">&rarr;</span>
      </button>
    </li>
    <li class="wm-nav-item">
      <button type="button" onclick="wmScrollTo('sec-quote')">
        <span>\uacac\uc801 \uacc4\uc0b0\uae30</span>
        <span class="wm-nav-arrow">&rarr;</span>
      </button>
    </li>
    <li class="wm-nav-item">
      <button type="button" onclick="wmScrollTo('sec-notice')">
        <span>\uc8fc\uc758\uc0ac\ud56d</span>
        <span class="wm-nav-arrow">&rarr;</span>
      </button>
    </li>
  </ul>"""

wm_scroll_to_js = """  function wmScrollTo(targetId) {
    try {
      // \ubcf8\ubb38 \ubb34\uc870\uac74 \uc790\ub3d9 \ud3bc\uce68
      wmExpandArtmugContent();

      // \uc0c1\uc704 \ubd80\ubaa8 \uc694\uc18c\ub4e4\uc758 inner scrollTop \ubc0f \ub192\uc774 \uc81c\ud55c \ud574\uc81c
      const parents = document.querySelectorAll('.goods_detail_content, .goods_detail_wrap, #goods_detail, .detailinfo, div');
      parents.forEach(p => {
        if (p.scrollTop > 0) p.scrollTop = 0;
        if (p.style) {
          if (p.style.maxHeight) p.style.maxHeight = 'none';
          if (p.style.overflow === 'hidden') p.style.overflow = 'visible';
        }
      });

      // 0.25\ucd08 \uc9c0\uc5f0 \ub300\uae30 \ud6c4 \uc808\ub300 Y \uc88c\ud45c\ub85c \uc708\ub3c4\uc6b0 \uc2a4\ud06c\ub864 \uc774\ub3d9
      setTimeout(() => {
        let targetEl = document.getElementById(targetId);
        if (!targetEl) {
          if (targetId === 'sec-preview') {
            targetEl = document.getElementById('sec-preview') ||
                       document.querySelector('.showcontent img') ||
                       document.querySelector('img[src*="17852640420"]') ||
                       document.querySelector('.showcontent');
          }
          else if (targetId === 'sec-schedule') {
            targetEl = document.querySelector('iframe[src*="schedule"]');
          }
          else if (targetId === 'sec-portfolio') {
            targetEl = document.querySelector('iframe[src*="sharp_embed"]');
          }
          else if (targetId === 'sec-quote') {
            targetEl = document.querySelector('iframe[src*="WAVIT-quote"]');
          }
          else if (targetId === 'sec-notice') {
            targetEl = document.getElementById('sec-notice');
            if (!targetEl) {
              const allEls = document.querySelectorAll('b, font, div, span, p');
              for (let i = 0; i < allEls.length; i++) {
                const text = allEls[i].textContent || '';
                if (text.includes('\\uc2e0\\uccad \\uc804 \\uc8fc\\uc758\\uc0ac\\ud56d') || text.includes('\\uc8fc\\uc758\\uc0ac\\ud56d')) {
                  targetEl = allEls[i];
                  break;
                }
              }
            }
          }
        }

        if (targetEl) {
          let p = targetEl.parentElement;
          while (p && p !== document.body) {
            if (p.scrollTop > 0) p.scrollTop = 0;
            p = p.parentElement;
          }

          const rect = targetEl.getBoundingClientRect();
          const absoluteY = rect.top + window.pageYOffset - 80;
          window.scrollTo({ top: Math.max(0, absoluteY), behavior: 'smooth' });
        }
      }, 250);
    } catch (e) {}
  }"""

files = ['artmug_live_full.html', 'index.html']
for filename in files:
    path = os.path.join(r"d:\Study\artmug side menu", filename)
    if not os.path.exists(path):
        continue

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Replace nav list
    nav_pattern = r'<!--.*?\ubaa9\ucc28.*?-->\s*<div class="wm-section-label">Quick Navigation</div>\s*<ul class="wm-nav-list">.*?</ul>'
    if re.search(nav_pattern, content, re.DOTALL):
        content = re.sub(nav_pattern, lambda m: nav_5_buttons_html, content, flags=re.DOTALL)
        print(f"Updated nav list (pattern 1) in {filename}")
    else:
        nav_pattern2 = r'<div class="wm-section-label">Quick Navigation</div>\s*<ul class="wm-nav-list">.*?</ul>'
        if re.search(nav_pattern2, content, re.DOTALL):
            content = re.sub(nav_pattern2, lambda m: nav_5_buttons_html, content, flags=re.DOTALL)
            print(f"Updated nav list (pattern 2) in {filename}")
        else:
            print(f"Warning: Could not find nav list in {filename}")

    # 2. Replace wmScrollTo function
    scroll_func_pattern = r'function wmScrollTo\(targetId\)\s*\{.*?\n  \}'
    if re.search(scroll_func_pattern, content, re.DOTALL):
        content = re.sub(scroll_func_pattern, lambda m: wm_scroll_to_js, content, flags=re.DOTALL)
        print(f"Updated wmScrollTo in {filename}")
    else:
        print(f"Warning: Could not find wmScrollTo in {filename}")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved {filename}")
