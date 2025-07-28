import os
import shutil
import subprocess
import time

SCAN_DIR = os.getenv("SCAN_DIR", "scripts")
QUARANTINE_DIR = os.getenv("QUARANTINE_DIR", "quarantine")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))


def scan_once():
    os.makedirs(QUARANTINE_DIR, exist_ok=True)
    for root, _, files in os.walk(SCAN_DIR):
        for name in files:
            path = os.path.join(root, name)
            try:
                result = subprocess.run(
                    ["clamscan", path], capture_output=True, text=True
                )
            except FileNotFoundError:
                print("clamscan not found; install ClamAV for scanning")
                return
            if result.returncode == 1:
                rel = os.path.relpath(path, SCAN_DIR)
                qpath = os.path.join(QUARANTINE_DIR, rel)
                os.makedirs(os.path.dirname(qpath), exist_ok=True)
                shutil.move(path, qpath)
                print(f"Infected file {path} moved to {qpath}")
            elif result.returncode != 0:
                print(f"Error scanning {path}: {result.stderr.strip()}")


def main():
    while True:
        scan_once()
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
