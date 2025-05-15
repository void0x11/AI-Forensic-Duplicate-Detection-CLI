import argparse
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Import all models and tools via loader
from loader import (
    resnet18_model, resnet50_model, resnet101_model,
    efficientnet_b1_model, efficientnet_b3_model,
    clip_model, dinov2_model,
    sbert_model, sbert_deep_model,
    codebert_model,
    daily_snapshot,
    scan_duplicates,
    tracker
)

def detect_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        return "image"
    elif ext in [".txt", ".md", ".log"]:
        return "text"
    elif ext in [".sh", ".py", ".c", ".java"]:
        return "code"
    return "unknown"

def load_model_by_name(name):
    try:
        if name == "clip":
            model, preprocess = clip_model.load_model()
            return (model, preprocess), clip_model

        elif name == "dinov2":
            model = dinov2_model.load_model()
            transform = dinov2_model.get_transform()
            return (model, transform), dinov2_model

        elif name == "resnet50":
            model = resnet50_model.load_model()
            transform = resnet50_model.get_transform()
            return (model, transform), resnet50_model

        elif name == "resnet18":
            return resnet18_model.load_model(), resnet18_model

        elif name == "resnet101":
            return resnet101_model.load_model(), resnet101_model

        elif name == "efficientnet_b1":
            return efficientnet_b1_model.load_model(), efficientnet_b1_model

        elif name == "efficientnet_b3":
            return efficientnet_b3_model.load_model(), efficientnet_b3_model

        elif name == "sbert":
            return sbert_model.load_model(), sbert_model

        elif name == "sbert_deep":
            return sbert_deep_model.load_model(), sbert_deep_model

        elif name == "codebert":
            tokenizer, model = codebert_model.load_model()
            return (tokenizer, model), codebert_model

        else:
            return None, None

    except Exception as e:
        print(f"❌ Error loading model '{name}': {e}")
        return None, None

def main():
    try:
        parser = argparse.ArgumentParser(description="AI Forensic CLI - Similarity & Snapshot Tool")
        parser.add_argument("--file1", help="Path to the first file")
        parser.add_argument("--file2", help="Path to the second file")
        parser.add_argument("--model", help="Model to use explicitly")
        parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold")
        parser.add_argument("--auto", action="store_true", help="Auto-select model based on file type")
        parser.add_argument("--mode", choices=["compare", "snapshot", "duplicates", "tracker"], help="Mode to run")
        parser.add_argument("--folder", help="Target folder for snapshot, duplicates, or tracker mode")
        args = parser.parse_args()

        # === Mode: snapshot ===
        if args.mode == "snapshot":
            if not args.folder:
                print("❌ Please provide --folder with snapshot mode.")
                return
            daily_snapshot.main(args.folder)
            return

        # === Mode: duplicates ===
        if args.mode == "duplicates":
            if not args.folder:
                print("❌ Please provide --folder with duplicates mode.")
                return
            results = scan_duplicates.scan_folder_for_duplicates(args.folder)
            if results:
                print("🔍 Duplicates Found:")
                for f1, f2, label in results:
                    print(f"{label}:\n → {f1}\n → {f2}\n")
                # ✅ Save the duplicates report
                scan_duplicates.save_report(results)
            else:
                print("✅ No duplicates found.")
            return

        # === Mode: tracker ===
        if args.mode == "tracker":
            if not args.folder:
                print("❌ Please provide --folder with tracker mode.")
                return
            print("🛰️ Starting live monitoring tracker...\n")
            tracker.monitor_folder(args.folder)
            return

        # === Mode: compare ===
        if args.mode != "compare":
            print("❌ Please use --mode compare, --mode snapshot, --mode duplicates, or --mode tracker.")
            return

        if not args.file1 or not args.file2:
            print("❌ Please provide both --file1 and --file2 for comparison.")
            return

        if not os.path.exists(args.file1) or not os.path.exists(args.file2):
            print("❌ One or both file paths are invalid.")
            return

        if args.auto and args.model:
            print("❌ You can't use --model and --auto together.")
            return

        # === Auto-select model ===
        if args.auto:
            file_type = detect_file_type(args.file1)
            if file_type == "image":
                model_name = "clip"
            elif file_type == "text":
                model_name = "sbert_deep"
            elif file_type == "code":
                model_name = "codebert"
            else:
                print("❌ Unsupported file type.")
                return
        elif args.model:
            model_name = args.model
        else:
            print("❌ Please provide a model using --model or use --auto.")
            return

        # === Load model ===
        model_data, module = load_model_by_name(model_name)
        if model_data is None or module is None:
            print(f"❌ Failed to load model: {model_name}")
            return

        # === Extract Features ===
        if "sbert" in model_name:
            vec1 = module.extract_features_from_file(args.file1, model_data)
            vec2 = module.extract_features_from_file(args.file2, model_data)

        elif model_name == "codebert":
            tokenizer, model = model_data
            vec1 = module.extract_features_from_file(args.file1, tokenizer, model)
            vec2 = module.extract_features_from_file(args.file2, tokenizer, model)

        elif model_name == "clip":
            model, preprocess = model_data
            vec1 = module.extract_features(args.file1, model, preprocess)
            vec2 = module.extract_features(args.file2, model, preprocess)

        else:
            model, transform = model_data
            vec1 = module.extract_features(args.file1, model, transform)
            vec2 = module.extract_features(args.file2, model, transform)

        # === Safety Check Before Similarity ===
        if not isinstance(vec1, np.ndarray) or not isinstance(vec2, np.ndarray):
            print("❌ One or both feature vectors are not valid numpy arrays.")
            return

        similarity = cosine_similarity([vec1], [vec2])[0][0]

        print(f"Similarity: {similarity:.4f}")

        if similarity >= args.threshold:
            print("✅ Files are perceptually similar.")
        else:
            print("❌ Files are different.")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()