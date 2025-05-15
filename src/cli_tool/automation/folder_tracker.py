# tracker.py
# Live monitoring module for real-time file duplicate/tampering alerts

import os
import time
import threading
from datetime import datetime
from loader import daily_snapshot, scan_duplicates

CHECK_INTERVAL = 30  # seconds between checks (can be adjusted)

ALERT_LOG = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
    "reports",
    "tracker_alerts.txt"
)

# Set to keep track of previously seen snapshot paths
last_snapshot = {}

# Live monitor function
def monitor_folder(folder_path):
    global last_snapshot
    print(f"📡 Tracker started on folder: {folder_path}")
    print(f"🔁 Checking every {CHECK_INTERVAL} seconds\n")

    while True:
        try:
            # Take snapshot
            current_snapshot = daily_snapshot.generate_snapshot(folder_path)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            changes = daily_snapshot.compare_snapshots(last_snapshot, current_snapshot, threshold=0.98)

            # Detect duplicates
            duplicates = scan_duplicates.scan_folder_for_duplicates(folder_path)

            # Save and alert if anything detected
            if changes or duplicates:
                with open(ALERT_LOG, "a") as f:
                    f.write(f"\n=== ALERT [{timestamp}] ===\n")

                    if changes:
                        f.write("[Snapshot Changes Detected]:\n")
                        for path, change_type in changes:
                            f.write(f"{path} ==> {change_type}\n")

                    if duplicates:
                        f.write("[Duplicate Files Detected]:\n")
                        for f1, f2, tag in duplicates:
                            f.write(f"{tag}:\n → {f1}\n → {f2}\n")

                print(f"⚠️ ALERT at {timestamp}: Changes or duplicates found. Logged to tracker_alerts.txt")
            else:
                print(f"✅ {timestamp}: No suspicious activity detected.")

            # Update snapshot for next iteration
            last_snapshot = current_snapshot

        except Exception as e:
            print(f"🔥 Error during monitoring: {e}")

        time.sleep(CHECK_INTERVAL)


# CLI entry point
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Target folder to monitor continuously")
    args = parser.parse_args()

    monitor_thread = threading.Thread(target=monitor_folder, args=(args.folder,), daemon=True)
    monitor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Tracker stopped.")