# tracker.py
# Live monitoring module for real-time file duplicate/tampering alerts

import os
import time
import json
import numpy as np
from datetime import datetime
from loader import daily_snapshot, scan_duplicates

CHECK_INTERVAL = 30  # seconds between checks (can be adjusted)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ALERT_LOG = os.path.join(BASE_DIR, "reports", "tracker_alerts.txt")


def status(msg):
    print(f"[*] {msg}")

def info(msg):
    print(f"[+] {msg}")

def warning(msg):
    print(f"[!] {msg}")


def monitor_folder(folder_path):
    status(f"Tracker started on folder: {folder_path}")
    status(f"Checking every {CHECK_INTERVAL} seconds\n")

    snapshot_file = os.path.join(BASE_DIR, "reports", "tracker_baseline_snapshot.txt")

    if not os.path.exists(snapshot_file):
        info("No previous baseline snapshot found. Generating...")
        baseline = daily_snapshot.generate_snapshot(folder_path)
        daily_snapshot.daily_snapshot.save_snapshot(baseline, "tracker_baseline_snapshot.txt")
        info("Baseline snapshot saved. Waiting for changes...")
        time.sleep(CHECK_INTERVAL)

    baseline = daily_snapshot.load_snapshot("tracker_baseline_snapshot.txt")
    for path in baseline:
        entry = baseline[path]
        if entry["mode"] == "AI":
            entry["value"] = np.array(entry["value"])

    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_snapshot = daily_snapshot.generate_snapshot(folder_path)
            for path in current_snapshot:
                entry = current_snapshot[path]
                if entry["mode"] == "AI":
                    entry["value"] = np.array(entry["value"])

            changes = daily_snapshot.compare_snapshots(baseline, current_snapshot, threshold=1.0)

            if not changes:
                status(f"{timestamp}: No snapshot changes.")
                time.sleep(CHECK_INTERVAL)
                continue

            warning(f"{timestamp}: Snapshot changed. Re-scanning duplicates...")
            new_duplicates = scan_duplicates.scan_folder_for_duplicates(folder_path)

            # Build set of baseline duplicate file paths
            old_dup_paths = set()
            baseline_dups = []  # load from previous alert log if needed

            # Detect newly duplicated files only
            new_only = []
            for f1, f2, tag in new_duplicates:
                if f1 not in old_dup_paths or f2 not in old_dup_paths:
                    new_only.append((f1, f2, tag))

            if changes or new_only:
                with open(ALERT_LOG, "a") as f:
                    f.write(f"\n=== ALERT [{timestamp}] ===\n")
                    if changes:
                        f.write("[Snapshot Changes Detected]:\n")
                        for path, change_type in changes:
                            f.write(f"{path} ==> {change_type}\n")
                    if new_only:
                        f.write("[New Duplicate Files Detected]:\n")
                        for f1, f2, tag in new_only:
                            f.write(f"{tag}:\n → {f1}\n → {f2}\n")
                warning(f"ALERT logged ({len(changes)} changes, {len(new_only)} new duplicates).")
            else:
                status(f"{timestamp}: Snapshot changed but no new duplicates.")

            # Update baseline snapshot file
            save_snapshot(current_snapshot, "tracker_baseline_snapshot.txt")
            baseline = current_snapshot

        except Exception as e:
            warning(f"Error during monitoring: {e}")

        time.sleep(CHECK_INTERVAL)


# CLI entry point
if __name__ == "__main__":
    import argparse
    import keyboard  # Requires `pip install keyboard`

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Target folder to monitor continuously")
    args = parser.parse_args()

    try:
        info("Press ESC to stop the tracker.")
        monitor_folder(args.folder)
    except KeyboardInterrupt:
        print("\n[!] Tracker stopped by user.")