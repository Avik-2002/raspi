import os
import requests

# Paths and URLs
VERSION_FILE = "/home/avikdutta/raspi/current_version.txt"
MAIN_SCRIPT = "/home/avikdutta/raspi/main.py"
SERVER_VERSION_URL = "http://localhost:5000/version"

# Get the current version saved locally
def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "v0.0.0"
    with open(VERSION_FILE, "r") as f:
        return f.read().strip()

# Get the latest version from the server (Flask or real)
def get_server_version():
    try:
        response = requests.get(SERVER_VERSION_URL)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Failed to connect to version server: {e}")
        return None

# Force pull latest code from GitHub
def update_code():
    print("🛠️ Pulling latest code from GitHub...")
    os.system("cd /home/avikdutta/raspi && git reset --hard && git pull origin main")

# Run the updated Python app
def run_main():
    print("🚀 Running the main application...")
    os.system(f"python3 {MAIN_SCRIPT}")

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

