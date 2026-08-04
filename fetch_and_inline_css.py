import urllib.request
import os

css_urls = [
    'https://artmug.kr/skin/default/css/style.css?ver=339',
    'https://artmug.kr/skin/default/awesome/font-awesome.css'
]

combined_css = ""
for url in css_urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        css_data = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        # Fix relative image/font paths to point to https://artmug.kr/
        css_data = css_data.replace('url(../', 'url(https://artmug.kr/skin/default/')
        css_data = css_data.replace('url(\'../', 'url(\'https://artmug.kr/skin/default/')
        css_data = css_data.replace('url("../', 'url("https://artmug.kr/skin/default/')
        combined_css += f"\n/* --- Fetched: {url} --- */\n" + css_data
        print(f"Successfully downloaded CSS from {url}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

print("Total combined CSS length:", len(combined_css))

for filename in ['artmug_live_full.html', 'index.html']:
    filepath = os.path.join(r"d:\Study\artmug side menu", filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()

            inline_tag = f"<style id=\"artmug-inlined-css\">\n{combined_css}\n</style>"
            if '</head>' in html:
                html = html.replace('</head>', inline_tag + '\n</head>')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Successfully inlined CSS into {filename}")
        except Exception as e:
            print(f"Error updating {filename}: {e}")
