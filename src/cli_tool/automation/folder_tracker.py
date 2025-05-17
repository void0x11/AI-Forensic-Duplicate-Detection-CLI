# tracker.py
# Live monitoring module for real-time file duplicate/tampering alerts

import os
import time
import json
from datetime import datetime
from loader import daily_snapshot, scan_duplicates

CHECK_INTERVAL = 30  # seconds between checks (can be adjusted)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ALERT_LOG = os.path.join(BASE_DIR, "reports", "tracker_alerts.txt")
TRACKER_STATE = os.path.join(BASE_DIR, "reports", "tracker_state.json")

def status(msg):
    print(f"[*] {msg}")

def info(msg):
    print(f"[+] {msg}")

def warning(msg):
    print(f"[!] {msg}")

def load_state():
    if os.path.exists(TRACKER_STATE):
        with open(TRACKER_STATE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(TRACKER_STATE, 'w') as f:
        json.dump(state, f, indent=2)

import numpy as np

def monitor_folder(folder_path):
    status(f"Tracker started on folder: {folder_path}")
    status(f"Checking every {CHECK_INTERVAL} seconds\n")

    state = load_state()
    baseline_snapshot = state.get("baseline_snapshot")
    if baseline_snapshot:
        for path in baseline_snapshot:
            entry = baseline_snapshot[path]
            if entry["mode"] == "AI":
                entry["value"] = np.array(entry["value"])
    baseline_duplicates = state.get("baseline_duplicates", [])

    if baseline_snapshot is None:
        info("No previous snapshot found. Creating baseline...")
        snapshot = daily_snapshot.generate_snapshot(folder_path)
        state["baseline_snapshot"] = snapshot
        info("Running initial duplicate scan...")
        duplicates = scan_duplicates.scan_folder_for_duplicates(folder_path)
        state["baseline_duplicates"] = duplicates
        save_state(state)
        info("Initial baseline established.")

    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_snapshot = daily_snapshot.generate_snapshot(folder_path)
            for path in current_snapshot:
                entry = current_snapshot[path]
                if entry["mode"] == "AI":
                    entry["value"] = np.array(entry["value"])
            changes = daily_snapshot.compare_snapshots(state["baseline_snapshot"], current_snapshot, threshold=1.0)

            if not changes:
                status(f"{timestamp}: No snapshot changes.")
                time.sleep(CHECK_INTERVAL)
                continue

            warning(f"{timestamp}: Snapshot changed. Re-scanning duplicates...")
            new_duplicates = scan_duplicates.scan_folder_for_duplicates(folder_path)

            # Build set of baseline duplicate file paths
            old_dup_paths = set()
            for entry in state["baseline_duplicates"]:
                old_dup_paths.add(entry[0])
                old_dup_paths.add(entry[1])

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

            # Update baseline
            state["baseline_snapshot"] = current_snapshot
            state["baseline_duplicates"] = new_duplicates
            save_state(state)

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
        while True:
            monitor_folder(args.folder)
            if keyboard.is_pressed('esc'):
                print("\n[!] ESC key pressed. Exiting tracker.")
                break
    except KeyboardInterrupt:
        print("\n[!] Tracker stopped by user.")