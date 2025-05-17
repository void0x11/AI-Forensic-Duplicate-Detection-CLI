import os
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from loader import clip_model, sbert_deep_model, codebert_model, utilhash

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE_REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SNAPSHOT_DIR = os.path.join(BASE_REPORTS_DIR, "snapshots")
REPORT_DIR = os.path.join(BASE_REPORTS_DIR, "diffs")

os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

def status(msg):
    print(f"[*] {msg}")

def info(msg):
    print(f"[+] {msg}")

def warning(msg):
    print(f"[!] {msg}")

def detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text_extensions = [
        ".txt", ".md", ".log", ".sh", ".bash", ".zsh", ".conf", ".ini", ".cfg",
        ".profile", ".bashrc", ".zshrc", ".py", ".c", ".cpp", ".java", ".js"
    ]
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    binary_extensions = [".appimage", ".deb", ".rpm", ".tar.gz", ".tgz", ".tar", ".gz", ".zip", ".bin", ".run"]

    if ext in text_extensions:
        return "text"
    elif ext in image_extensions:
        return "image"
    elif ext in binary_extensions:
        return "binary"

    if ext == "" and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(2048)
            return "text"
        except:
            return "unknown"

    return "unknown"

def sanitize_path(path):
    return path.replace("/", "_").replace("\\", "_").strip("_")

def generate_snapshot_filename(folder_path):
    now = datetime.now()
    folder_id = sanitize_path(folder_path)
    return f"{folder_id}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

def extract_timestamp_from_name(filename):
    try:
        time_str = "_".join(filename.split("_")[-2:]).replace(".txt", "")
        return datetime.strptime(time_str, "%Y-%m-%d_%H-%M-%S")
    except Exception:
        return None

def load_model_for_type(file_type, file_path=None):
    if file_type == "image":
        try:
            model, preprocess = clip_model.load_model()
            return model, preprocess, clip_model
        except:
            return None, None, None
    elif file_type == "text":
        if file_path and file_path.endswith((".sh", ".py", ".c", ".cpp", ".java", ".js")):
            try:
                sbert = sbert_deep_model.load_model()
                tokenizer, codebert = codebert_model.load_model()
                return (sbert, (tokenizer, codebert)), None, "hybrid"
            except:
                return None, None, None
        else:
            try:
                model = sbert_deep_model.load_model()
                return model, None, sbert_deep_model
            except:
                return None, None, None
    return None, None, None

def hash_file(file_path, model, extra, module, file_type):
    try:
        if file_type == "image":
            return module.extract_features(file_path, model, extra)
        elif file_type == "text":
            if module == "hybrid":
                sbert, (tokenizer, codebert) = model
                vec1 = sbert_deep_model.extract_features_from_file(file_path, sbert)
                vec2 = codebert_model.extract_features_from_file(file_path, tokenizer, codebert)
                return np.concatenate([vec1, vec2]) if vec1 is not None and vec2 is not None else vec1 or vec2
            else:
                return module.extract_features_from_file(file_path, model)
    except:
        return None
    return None

def generate_snapshot(folder_path):
    snapshot = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_type = detect_file_type(full_path)

            if file_type in ["image", "text"]:
                model, extra, module = load_model_for_type(file_type, full_path)
                if model is None:
                    continue
                vec = hash_file(full_path, model, extra, module, file_type)
                if vec is not None:
                    snapshot[full_path] = {"mode": "AI", "value": vec.tolist()}
            else:
                file_hash = utilhash.compute_sha256(full_path)
                snapshot[full_path] = {"mode": "HASH", "value": file_hash}
    return snapshot

def save_snapshot(snapshot, filename):
    path = os.path.join(SNAPSHOT_DIR, filename)
    with open(path, 'w') as f:
        for filepath, entry in snapshot.items():
            if entry["mode"] == "AI":
                f.write(f"{filepath}::AI::{','.join(map(str, entry['value']))}\n")
            else:
                f.write(f"{filepath}::HASH::{entry['value']}\n")
    return path

def load_snapshot(filename):
    path = os.path.join(SNAPSHOT_DIR, filename)
    if not os.path.exists(path):
        return None
    snapshot = {}
    with open(path, 'r') as f:
        for line in f:
            if "::AI::" in line:
                filepath, vec_str = line.strip().split("::AI::")
                vector = list(map(float, vec_str.split(",")))
                snapshot[filepath] = {"mode": "AI", "value": vector}
            elif "::HASH::" in line:
                filepath, hashval = line.strip().split("::HASH::")
                snapshot[filepath] = {"mode": "HASH", "value": hashval}
    return snapshot

def compare_snapshots(prev, current, threshold=0.999999):
    changed = []
    for path, entry in current.items():
        if path not in prev:
            changed.append((path, "NEW"))
        elif entry["mode"] == "HASH" or prev[path]["mode"] == "HASH":
            if entry["value"] != prev[path]["value"]:
                changed.append((path, "MODIFIED (hash only - unsupported)"))
        else:
            sim = cosine_similarity([entry["value"]], [prev[path]["value"]])[0][0]
            if sim < threshold:
                changed.append((path, f"MODIFIED (Similarity: {sim:.6f})"))
    return changed

def load_latest_snapshot(before_filename=None):
    if not before_filename:
        return None, None
    current_time = extract_timestamp_from_name(before_filename)
    current_prefix = "_".join(before_filename.split("_")[:-2])
    snapshots = []
    for f in os.listdir(SNAPSHOT_DIR):
        if not f.endswith(".txt") or not f.startswith(current_prefix):
            continue
        file_time = extract_timestamp_from_name(f)
        if file_time and file_time < current_time:
            snapshots.append((file_time, f))
    if not snapshots:
        return None, None
    snapshots.sort()
    latest_name = snapshots[-1][1]
    return latest_name, load_snapshot(latest_name)

def main(folder):
    snapshot_filename = generate_snapshot_filename(folder)
    snapshot = generate_snapshot(folder)
    snapshot_path = save_snapshot(snapshot, snapshot_filename)
    info(f"Snapshot saved: {snapshot_path}")

    prev_name, prev_snapshot = load_latest_snapshot(before_filename=snapshot_filename)
    if prev_snapshot:
        info(f"Comparing with previous snapshot: {prev_name}")
        changes = compare_snapshots(prev_snapshot, snapshot)
        if changes:
            diff_name = f"diff_{snapshot_filename.replace('.txt', '')}_vs_{prev_name.replace('.txt','')}.txt"
            report_path = os.path.join(REPORT_DIR, diff_name)
            with open(report_path, "w") as f:
                for path, msg in changes:
                    f.write(f"{path} ==> {msg}\n")
            warning(f"Changes detected: {len(changes)} (saved to {report_path})")
        else:
            status("No significant changes since last snapshot.")
    else:
        status("No previous snapshot to compare.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Folder to snapshot")
    args = parser.parse_args()
    main(args.folder)