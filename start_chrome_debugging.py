import os
import subprocess
import time
import urllib.request
import json

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_dir = r"C:\Users\wavy\chrome-dev-profile"
os.makedirs(profile_dir, exist_ok=True)

# Check if port 9222 is already listening
try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=1) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Chrome already running on 9222")
except Exception:
    print("Launching Chrome on 9222...")
    subprocess.Popen([
        chrome_exe,
        "--remote-debugging-port=9222",
        f"--user-data-dir={profile_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "about:blank"
    ])
    time.sleep(3)
    with urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=5) as resp:
        data = json.loads(resp.read().decode('utf-8'))

ws_url = data.get("webSocketDebuggerUrl", "")
ws_path = "/" + ws_url.split("/", 3)[-1] if "/" in ws_url else ""
print(f"ws_path: {ws_path}")

target_port_file = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
with open(target_port_file, "w", encoding="ascii") as f:
    f.write(f"9222\n{ws_path}\n")

print(f"DevToolsActivePort written to {target_port_file}")
