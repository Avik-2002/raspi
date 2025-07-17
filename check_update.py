import time
import requests
import subprocess
import os
from datetime import datetime

# ========== CONFIGURATION ==========
SERVER_URL = "http://127.0.0.1:5000/version"  # Replace with actual server if remote
VERSION_FILE = "/home/avikdutta/raspi/current_version.txt"
REPO_DIR = "/home/avikdutta/raspi"
SLEEP_INTERVAL = 60  # seconds (1 minute)
# ===================================

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}", flush=True)

def get_server_version():
    try:
        response = requests.get(SERVER_URL, timeout=5)
        return response.text.strip()
    except requests.RequestException as e:
        log(f"❌ Could not connect to server: {e}")
        return None

def get_local_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as file:
            return file.read().strip()
    return None

def set_local_version(version):
    with open(VERSION_FILE, 'w') as file:
        file.write(version)

def git_pull():
    os.chdir(REPO_DIR)

    # Discard all local changes to avoid merge conflict
    subprocess.run(['git', 'reset', '--hard'], capture_output=True, text=True)
    subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True)

    result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
    return result.stdout + result.stderr

def run_updated_scripts():
    log("🚀 Running updated main.py")
    subprocess.Popen(["python3", "main.py"], cwd=REPO_DIR)

def check_for_update():
    log("🔍 Checking for update...")

    server_version = get_server_version()
    log(f"🔎 Server version: {server_version}")

    if server_version is None:
        return

    local_version = get_local_version()
    log(f"📂 Local version: {local_version}")

    if server_version != local_version:
        log("🆕 Update available! Pulling changes from GitHub...")
        output = git_pull()
        log(output)
        log("✅ Git pull complete.")
        set_local_version(server_version)
        run_updated_scripts()
    else:
        log("✅ Already up to date.")

# ========== MAIN LOOP ==========
log("📦 OTA updater started. Monitoring every 1 minute.")
while True:
    check_for_update()
    time.sleep(SLEEP_INTERVAL)
