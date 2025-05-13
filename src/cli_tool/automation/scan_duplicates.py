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

# === Documentation ===
"""
scan_duplicates.py
------------------

This script performs AI-powered duplicate and near-duplicate detection across files in a specified folder.

Supported File Types:
- Images: .jpg, .jpeg, .png, .bmp
- Text/Code: .txt, .md, .log, .py, .sh, .c, .java, etc.

How it Works:
1. Files are grouped by type and compared pairwise.
2. For images:
   - Stage 1: Perceptual hash (pHash) filtering using Hamming distance.
   - Stage 2: Deep feature extraction using DINOv2 and ResNet50.
   - The minimum similarity score between the two models is used to reduce false positives.
3. For text/code:
   - Deep embeddings are extracted using SBERT + CodeBERT.
   - Cosine similarity is computed after concatenating both embeddings.

Thresholds:
- Perceptual Hash Similarity Threshold: 40%
- AI Similarity Threshold: 40%

Output:
- A list of tuples indicating pairs of similar files and their match type:
  - EXACT_DUPLICATE
  - NEAR_DUPLICATE (sim=0.97)

Usage:
    python scan_duplicates.py --folder /path/to/folder

This module is designed for forensic analysis, version control, and robust similarity detection.
"""


# Load dynamically via loader system
from loader import (
    dinov2_model,
    resnet50_model,
    sbert_deep_model,
    codebert_model,
    pcphash,
    daily_snapshot
)

# Use file type detection from snapshot system
detect_file_type = daily_snapshot.detect_file_type

# Thresholds
PHASH_LENGTH = 64
PHASH_SIMILARITY_THRESHOLD = 0.40
PHASH_MAX_DISTANCE = int((1 - PHASH_SIMILARITY_THRESHOLD) * PHASH_LENGTH)
AI_SIMILARITY_THRESHOLD = 0.40

# Load models
dinov2 = dinov2_model.load_model()
dinov2_transform = dinov2_model.get_transform()

resnet50 = resnet50_model.load_model()
resnet50_transform = resnet50_model.get_transform()

sbert = sbert_deep_model.load_model()
tokenizer, codebert = codebert_model.load_model()

# Main function
def scan_folder_for_duplicates(folder_path):
    files = []
    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            full_path = os.path.join(root, f)
            ftype = detect_file_type(full_path)
            if ftype in ["image", "text"]:
                files.append((full_path, ftype))

    duplicates = []

    for (file1, type1), (file2, type2) in combinations(files, 2):
        if type1 != type2:
            continue

        # ----------- IMAGE FILES -----------
        if type1 == "image":
            # Stage 1: Perceptual Hash
            hash1 = pcphash.compute_phash(file1)
            hash2 = pcphash.compute_phash(file2)
            if hash1 is None or hash2 is None:
                continue

            dist = pcphash.hamming_distance(hash1, hash2)

            if dist == 0:
                duplicates.append((file1, file2, "EXACT_DUPLICATE"))
                continue
            elif dist <= PHASH_MAX_DISTANCE:
                # Stage 2: Use dinov2 + resnet50 → pick best score
                sim_scores = []

                # DINOv2
                vec1_dino = dinov2_model.extract_features(file1, dinov2, dinov2_transform)
                vec2_dino = dinov2_model.extract_features(file2, dinov2, dinov2_transform)
                if vec1_dino is not None and vec2_dino is not None and vec1_dino.shape == vec2_dino.shape:
                    sim_dino = cosine_similarity([vec1_dino], [vec2_dino])[0][0]
                    sim_scores.append(sim_dino)

                # ResNet50
                vec1_res = resnet50_model.extract_features(file1, resnet50, resnet50_transform)
                vec2_res = resnet50_model.extract_features(file2, resnet50, resnet50_transform)
                if vec1_res is not None and vec2_res is not None and vec1_res.shape == vec2_res.shape:
                    sim_res = cosine_similarity([vec1_res], [vec2_res])[0][0]
                    sim_scores.append(sim_res)

                # Pick highest similarity
                if sim_scores:
                    best_sim = min(sim_scores)
                    if best_sim >= AI_SIMILARITY_THRESHOLD:
                        duplicates.append((file1, file2, f"NEAR_DUPLICATE (sim={best_sim:.2f})"))
                continue

        # ----------- TEXT / CODE FILES -----------
        elif type1 == "text":
            vec1a = sbert_deep_model.extract_features_from_file(file1, sbert)
            vec1b = codebert_model.extract_features_from_file(file1, tokenizer, codebert)
            vec2a = sbert_deep_model.extract_features_from_file(file2, sbert)
            vec2b = codebert_model.extract_features_from_file(file2, tokenizer, codebert)

            if any(v is None for v in [vec1a, vec1b, vec2a, vec2b]):
                continue

            v1 = np.concatenate([vec1a, vec1b])
            v2 = np.concatenate([vec2a, vec2b])
            if v1.shape != v2.shape:
                continue

            sim = cosine_similarity([v1], [v2])[0][0]
            if sim >= AI_SIMILARITY_THRESHOLD:
                duplicates.append((file1, file2, f"NEAR_DUPLICATE (sim={sim:.2f})"))

    return duplicates

def save_report(duplicates):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_path = os.path.join(SCAN_DIR, f"duplicates_{timestamp}.json")
    print(f"💾 Attempting to save report at: {report_path}")

    report_data = [
        {"file1": f1, "file2": f2, "match_type": tag}
        for f1, f2, tag in duplicates
    ]

    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=2)

    print(f"\n📝 Duplicate report saved to: {report_path}")


# CLI
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Target folder to scan for duplicates")
    args = parser.parse_args()

    results = scan_folder_for_duplicates(args.folder)

    if results:
        print("🔍 Potential duplicates found:")
        for f1, f2, tag in results:
            print(f"{tag}:\n → {f1}\n → {f2}\n")
        save_report(results)
    else:
        print("✅ No duplicates found.")