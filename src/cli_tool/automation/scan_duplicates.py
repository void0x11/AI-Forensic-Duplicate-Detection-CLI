import os
import numpy as np
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json

# === Report Directory Setup ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BASE_REPORTS_DIR = os.path.join(BASE_DIR, "reports")
SCAN_DIR = os.path.join(BASE_REPORTS_DIR, "scan")

os.makedirs(SCAN_DIR, exist_ok=True)

# Load dynamically via loader system
from loader import (
    dinov2_model,
    resnet50_model,
    sbert_deep_model,
    codebert_model,
    pcphash,
    utilhash,
    daily_snapshot
)

# Use file type detection from snapshot system
detect_file_type = daily_snapshot.detect_file_type

def detect_subtype(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    name = os.path.basename(file_path).lower()

    if any(kw in name for kw in ["hash", "md5", "sha256", "sha1"]) and ext in [".txt", ".log", ".hash"]:
        return "hashfile"

    if ext in [".py", ".java", ".cpp", ".c", ".sh"]:
        return "code"
    return "text"

# Thresholds
PHASH_LENGTH = 64
PHASH_SIMILARITY_THRESHOLD = 0.40
PHASH_MAX_DISTANCE = int((1 - PHASH_SIMILARITY_THRESHOLD) * PHASH_LENGTH)
AI_SIMILARITY_THRESHOLD = 0.50
SAFE_SIMILARITY_CAP = 0.95

# Load models
dinov2 = dinov2_model.load_model()
dinov2_transform = dinov2_model.get_transform()
resnet50 = resnet50_model.load_model()
resnet50_transform = resnet50_model.get_transform()
sbert = sbert_deep_model.load_model()
tokenizer, codebert = codebert_model.load_model()

def compute_sha256(file_path):
    return utilhash.compute_sha256(file_path)

def scan_folder_for_duplicates(folder_path):
    type_groups = {"image": [], "text": [], "code": [], "hashfile": []}

    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            full_path = os.path.join(root, f)
            ftype = detect_file_type(full_path)
            subtype = detect_subtype(full_path)
            if subtype in type_groups:
                type_groups[subtype].append(full_path)

    duplicates = []

    for group_name, group_files in type_groups.items():
        if group_name == "hashfile":
            continue  # Skip AI processing for hash-like text files

        checked = set()
        for file1, file2 in combinations(group_files, 2):
            if (file1, file2) in checked or (file2, file1) in checked:
                continue
            checked.add((file1, file2))

            hash1 = compute_sha256(file1)
            hash2 = compute_sha256(file2)
            if hash1 == hash2:
                duplicates.append((file1, file2, "EXACT_DUPLICATE"))
                continue

            if group_name == "image":
                hash1 = pcphash.compute_phash(file1)
                hash2 = pcphash.compute_phash(file2)
                if hash1 is None or hash2 is None:
                    continue

                dist = pcphash.hamming_distance(hash1, hash2)
                if dist > PHASH_MAX_DISTANCE:
                    continue

                sim_scores = []
                vec1_dino = dinov2_model.extract_features(file1, dinov2, dinov2_transform)
                vec2_dino = dinov2_model.extract_features(file2, dinov2, dinov2_transform)
                if vec1_dino is not None and vec2_dino is not None and vec1_dino.shape == vec2_dino.shape:
                    sim_scores.append(cosine_similarity([vec1_dino], [vec2_dino])[0][0])

                vec1_res = resnet50_model.extract_features(file1, resnet50, resnet50_transform)
                vec2_res = resnet50_model.extract_features(file2, resnet50, resnet50_transform)
                if vec1_res is not None and vec2_res is not None and vec1_res.shape == vec2_res.shape:
                    sim_scores.append(cosine_similarity([vec1_res], [vec2_res])[0][0])

                if sim_scores:
                    best_sim = min(sim_scores)
                    if best_sim >= AI_SIMILARITY_THRESHOLD:
                        duplicates.append((file1, file2, f"NEAR_DUPLICATE (sim={best_sim:.2f})"))

            elif group_name in ["text", "code"]:
                try:
                    with open(file1, 'rb') as f:
                        content1 = f.read().decode('utf-8', errors='ignore')
                    with open(file2, 'rb') as f:
                        content2 = f.read().decode('utf-8', errors='ignore')
                    if len(content1.strip()) < 4 or len(content2.strip()) < 4:
                        continue  # Skip files that are too short to compare meaningfully

                    vec1a = sbert_deep_model.extract_features_from_file(file1, sbert)
                    vec1b = codebert_model.extract_features_from_file(file1, tokenizer, codebert)
                    vec2a = sbert_deep_model.extract_features_from_file(file2, sbert)
                    vec2b = codebert_model.extract_features_from_file(file2, tokenizer, codebert)
                except:
                    continue

                if any(v is None or not isinstance(v, np.ndarray) for v in [vec1a, vec1b, vec2a, vec2b]):
                    continue

                v1 = np.concatenate([vec1a, vec1b])
                v2 = np.concatenate([vec2a, vec2b])

                if np.std(v1) < 1e-6 or np.std(v2) < 1e-6:
                    continue
                if v1.shape != v2.shape:
                    continue

                sim = cosine_similarity([v1], [v2])[0][0]

                if sim >= AI_SIMILARITY_THRESHOLD:
                    duplicates.append((file1, file2, f"NEAR_DUPLICATE (sim={sim:.2f})"))

    return duplicates

def save_report(duplicates):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(SCAN_DIR, f"duplicates_{timestamp}.json")
    print(f"\n💾 Attempting to save report at: {report_path}")

    report_data = [
        {"file1": f1, "file2": f2, "match_type": tag}
        for f1, f2, tag in duplicates
    ]

    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)

    print(f"📝 Duplicate report saved to: {report_path}")

# CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Target folder to scan for duplicates")
    args = parser.parse_args()

    try:
        results = scan_folder_for_duplicates(args.folder)

        if results:
            print("\n🔍 Potential duplicates found:")
            for f1, f2, tag in results:
                print(f"{tag}:\n → {f1}\n → {f2}\n")
            save_report(results)
        else:
            print("✅ No duplicates found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")