# src/cli_tool/automation/daily_snapshot.py

import os
import json
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
from loader import clip_model, sbert_deep_model

SNAPSHOT_DIR = "snapshots"
REPORT_DIR = "reports"

os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        return "image"
    elif ext in [".txt", ".md", ".log"]:
        return "text"
    return "unknown"


def load_model_for_type(file_type):
    if file_type == "image":
        model, preprocess = clip_model.load_model()
        return model, preprocess, clip_model
    elif file_type == "text":
        model = sbert_deep_model.load_model()
        return model, None, sbert_deep_model
    return None, None, None


def hash_file(file_path, model, extra, module, file_type):
    try:
        if file_type == "image":
            return module.extract_features(file_path, model, extra)
        elif file_type == "text":
            return module.extract_features_from_file(file_path, model)
    except:
        return None


def generate_snapshot(folder_path):
    snapshot = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_type = detect_file_type(full_path)
            if file_type not in ["image", "text"]:
                continue
            model, extra, module = load_model_for_type(file_type)
            if model is None:
                continue
            vec = hash_file(full_path, model, extra, module, file_type)
            if vec is not None:
                snapshot[full_path] = vec.tolist()
    return snapshot


def save_snapshot(snapshot, name):
    path = os.path.join(SNAPSHOT_DIR, name)
    with open(path, 'w') as f:
        json.dump(snapshot, f)
    return path


def load_snapshot(name):
    path = os.path.join(SNAPSHOT_DIR, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_latest_snapshot(exclude_name=None):
    files = sorted(os.listdir(SNAPSHOT_DIR))
    if not files:
        return None, None
    latest = files[-1]
    if exclude_name and latest == exclude_name:
        return None, None
    return latest, load_snapshot(latest)


def compare_snapshots(prev, current, threshold=0.90):
    changed = []
    for path, vec in current.items():
        if path not in prev:
            changed.append((path, "NEW"))
        else:
            sim = cosine_similarity([vec], [prev[path]])[0][0]
            if sim < threshold:
                changed.append((path, f"MODIFIED (Similarity: {sim:.2f})"))
    return changed


def main(folder):
    today = datetime.now().strftime("%Y-%m-%d")
    snapshot = generate_snapshot(folder)
    snapshot_filename = f"{today}.json"
    snapshot_path = save_snapshot(snapshot, snapshot_filename)
    print(f"✅ Snapshot saved: {snapshot_path}")

    prev_name, prev_snapshot = load_latest_snapshot(exclude_name=snapshot_filename)
    if prev_snapshot:
        print(f"🔍 Comparing with previous snapshot: {prev_name}")
        changes = compare_snapshots(prev_snapshot, snapshot)
        if changes:
            report_path = os.path.join(REPORT_DIR, f"diff_{today}_vs_{prev_name}")
            with open(report_path, "w") as f:
                json.dump(changes, f, indent=2)
            print(f"📝 Changes detected: {len(changes)} (saved to {report_path})")
        else:
            print("✅ No significant changes since last snapshot.")
    else:
        print("ℹ️ No previous snapshot to compare.")


# CLI entry point
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Folder to snapshot")
    args = parser.parse_args()
    main(args.folder)