
import time
import requests
import subprocess
import os
from datetime import datetime

# ========== CONFIGURATION ==========
SERVER_URL = "http://127.0.0.1:5000/version"  # Change to actual server if needed
VERSION_FILE = "/home/avikdutta/raspi/current_version.txt"
REPO_DIR = "/home/avikdutta/raspi"
SLEEP_INTERVAL =  180 # seconds (3 minutes)
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
    log("Running git pull...")
    result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
    return result.stdout + result.stderr

def run_updated_scripts():
    log("🚀 Running updated main.py")
    subprocess.Popen(["python3", "main.py"], cwd=REPO_DIR)

    # If needed, uncomment to run camera.py as well
    # log("🎥 Running updated camera.py")
    # subprocess.Popen(["python3", "camera.py"], cwd=REPO_DIR)

def check_for_update():
    log("🔍 Forced pull mode")
    output = git_pull()
    log(output)

# ========== MAIN LOOP ==========
log("📦 OTA updater started. Monitoring every 3 minutes.")
while True:
    check_for_update()
    time.sleep(SLEEP_INTERVAL)
