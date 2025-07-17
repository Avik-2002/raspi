import os

import time
import requests
import subprocess
import os
from datetime import datetime

# Paths and URLs
# ========== CONFIGURATION ==========
SERVER_URL = "http://127.0.0.1:5000/version"  # Change to actual server if needed
VERSION_FILE = "/home/avikdutta/raspi/current_version.txt"
MAIN_SCRIPT = "/home/avikdutta/raspi/main.py"
SERVER_VERSION_URL = "http://localhost:5000/version"
REPO_DIR = "/home/avikdutta/raspi"
SLEEP_INTERVAL =  180 # seconds (3 minutes)
# ===================================

# Get the current version saved locally
def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "v0.0.0"
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()
def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{timestamp} {msg}", flush=True)

# Get the latest version from the server (Flask or real)
def get_server_version():
    try:
        response = requests.get(SERVER_VERSION_URL)
        response = requests.get(SERVER_URL, timeout=5)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Failed to connect to version server: {e}")
    except requests.RequestException as e:
        log(f"❌ Could not connect to server: {e}")
        return None

# Force pull latest code from GitHub
def update_code():
    print("🛠️ Pulling latest code from GitHub...")
    os.system("cd /home/avikdutta/raspi && git reset --hard && git pull origin main")

# Run the updated Python app
def run_main():
    print("🚀 Running the main application...")
    os.system(f"python3 {MAIN_SCRIPT}")
def get_local_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as file:
            return file.read().strip()
    return None

# Update local version number
def set_local_version(version):
    with open(VERSION_FILE, "w") as f:
        f.write(version)

# Main logic
def main():
    print("🔍 Checking for update...")

    server_version = get_server_version()
    local_version = get_local_version()

    print(f"🔎 Server version: {server_version}")
    print(f"📂 Local version: {local_version}")

    if server_version and server_version != local_version:
        print("🆕 Update available. Updating now...")
        update_code()
        set_local_version(server_version)
        run_main()
    else:
        print("✅ Already up to date.")

if __name__ == "__main__":
    main()

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
