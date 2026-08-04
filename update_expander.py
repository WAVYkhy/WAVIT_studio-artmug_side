import os
import re

new_script = """<script>
  // 아트머그 공식 '상세설명 더보기' (.btn_open_btn, .detailinfo.showstep1) 강제 자동 펼침 함수
  function wmExpandArtmugContent() {
    try {
      // 1. 아트머그 공식 펼침 버튼 (.btn_open_btn) 클릭
      const btnOpen = document.querySelector('.btn_open_btn') || document.querySelector('.btn_open');
      if (btnOpen && typeof btnOpen.click === 'function') {
        btnOpen.click();
      }

      // 2. detailinfo 박스의 showstep1 클래스 직접 제거 및 높이 무제한 해제
      const detailInfo = document.querySelector('.detailinfo');
      if (detailInfo) {
        detailInfo.classList.remove('showstep1');
        detailInfo.style.maxHeight = 'none';
        detailInfo.style.height = 'auto';
        detailInfo.style.overflow = 'visible';
      }

      // 3. 더보기 버튼 영역 숨김
      const btnOpenWrap = document.querySelector('.btn_open');
      if (btnOpenWrap) {
        btnOpenWrap.classList.add('hide');
        btnOpenWrap.style.display = 'none';
      }

      // 4. 범용 텍스트 탐색 폴백 (ol, button, a, div, span)
      const candidates = document.querySelectorAll('.btn_open_btn, .btn_open, ol, button, a, div, span');
      for (let i = 0; i < candidates.length; i++) {
        const txt = (candidates[i].textContent || '').trim();
        if (txt.includes('상세설명') || txt.includes('더보기') || txt.includes('내용 더 보기') || txt.includes('펼쳐보기')) {
          if (typeof candidates[i].click === 'function') {
            candidates[i].click();
          }
        }
      }
    } catch (e) {}
  }

  function wmScrollTo(targetId) {
    try {
      // 본문 무조건 자동 펼침
      wmExpandArtmugContent();

      // 상위 부모 요소들의 inner scrollTop 및 높이 제한 해제
      const parents = document.querySelectorAll('.goods_detail_content, .goods_detail_wrap, #goods_detail, .detailinfo, div');
      parents.forEach(p => {
        if (p.scrollTop > 0) p.scrollTop = 0;
        if (p.style) {
          if (p.style.maxHeight) p.style.maxHeight = 'none';
          if (p.style.overflow === 'hidden') p.style.overflow = 'visible';
        }
      });

      // 0.25초 지연 대기 후 절대 Y 좌표로 윈도우 스크롤 이동
      setTimeout(() => {
        let targetEl = document.getElementById(targetId);
        if (!targetEl) {
          if (targetId === 'sec-schedule') targetEl = document.querySelector('iframe[src*="schedule"]');
          else if (targetId === 'sec-portfolio') targetEl = document.querySelector('iframe[src*="sharp_embed"]');
          else if (targetId === 'sec-quote') targetEl = document.querySelector('iframe[src*="WAVIT-quote"]');
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
  }

  function wmScrollToTop() {
    try {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {}
  }

  (function() {
    let menuEl = null;
    let initialOffsetTop = 0;

    function initMenuFollower() {
      menuEl = document.querySelector('.artmug-side-menu');
      if (!menuEl) return;

      if (menuEl.parentElement) {
        menuEl.parentElement.style.overflow = 'visible';
        menuEl.parentElement.style.height = 'auto';
      }

      const rect = menuEl.getBoundingClientRect();
      initialOffsetTop = rect.top + window.scrollY;

      window.addEventListener('scroll', handleScroll, { passive: true });
    }

    function handleScroll() {
      if (!menuEl) return;
      try {
        const pBar = document.getElementById('wmProgressBar');
        if (pBar) {
          const total = document.documentElement.scrollHeight - window.innerHeight;
          if (total > 0) {
            const pct = (window.scrollY / total) * 100;
            pBar.style.width = Math.min(100, Math.max(0, pct)) + '%';
          }
        }

        const currentY = window.scrollY;
        if (currentY > (initialOffsetTop - 80)) {
          const moveY = currentY - initialOffsetTop + 80;
          menuEl.style.transform = 'translateY(' + moveY + 'px)';
        } else {
          menuEl.style.transform = 'translateY(0px)';
        }
      } catch (e) {}
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initMenuFollower);
    } else {
      initMenuFollower();
    }
  })();

  (function() {
    const DISCORD_USER_ID = "680023951157624875";

    function updateOnlineStatus(statusType) {
      const badge = document.getElementById('wmStatusBadge');
      const text = document.getElementById('wmStatusText');
      if (!badge || !text) return;
      
      badge.className = 'wm-status';
      if (statusType === 'online') {
        badge.classList.add('is-online');
        text.textContent = 'ONLINE';
      } else if (statusType === 'idle' || statusType === 'dnd') {
        badge.classList.add('is-idle');
        text.textContent = 'AWAY';
      } else {
        badge.classList.add('is-offline');
        text.textContent = 'OFFLINE';
      }
    }

    if (DISCORD_USER_ID) {
      fetch('https://api.lanyard.rest/v1/users/' + DISCORD_USER_ID)
        .then(res => res.json())
        .then(data => {
          if (data && data.success && data.data) {
            updateOnlineStatus(data.data.discord_status);
          }
        })
        .catch(() => updateOnlineStatus('online'));
    }
  })();
</script>"""

for filename in ['artmug_live_full.html', 'index.html']:
    filepath = os.path.join(r"d:\Study\artmug side menu", filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        start_script = html.find('function wmExpandArtmugContent()')
        if start_script != -1:
            script_tag_start = html.rfind('<script>', 0, start_script)
            script_tag_end = html.find('</script>', start_script) + 9
            if script_tag_start != -1 and script_tag_end != -1:
                html = html[:script_tag_start] + new_script + html[script_tag_end:]
                with open(filepath, 'w', encoding='utf-8') as f_out:
                    f_out.write(html)
                print(f"Successfully updated expander script in {filename}")
            else:
                print(f"Script tags not found around wmExpandArtmugContent in {filename}")
        else:
            print(f"wmExpandArtmugContent not found in {filename}")
