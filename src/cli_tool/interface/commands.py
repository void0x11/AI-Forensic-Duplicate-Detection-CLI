import argparse
import os
from sklearn.metrics.pairwise import cosine_similarity

# Import all models via loader
from loader import (
    resnet18_model, resnet50_model, resnet101_model,
    efficientnet_b1_model, efficientnet_b3_model,
    clip_model, dinov2_model,
    sbert_model, sbert_deep_model,
    codebert_model,
    daily_snapshot
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
            return clip_model.load_model(), clip_model
        elif name == "dinov2":
            return dinov2_model.load_model(), dinov2_model
        elif name == "resnet18":
            return resnet18_model.load_model(), resnet18_model
        elif name == "resnet50":
            return resnet50_model.load_model(), resnet50_model
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
            return codebert_model.load_model(), codebert_model
        else:
            return None, None
    except Exception:
        return None, None

def main():
    try:
        parser = argparse.ArgumentParser(description="AI Hashing Tool for File Analysis")
        parser.add_argument("--file1", help="Path to the first file")
        parser.add_argument("--file2", help="Path to the second file")
        parser.add_argument("--model", help="Model to use explicitly")
        parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold")
        parser.add_argument("--auto", action="store_true", help="Auto-select model based on file type")
        parser.add_argument("--mode", choices=["compare", "snapshot"], help="Automation mode")
        parser.add_argument("--folder", help="Target folder (required for snapshot mode)")
        args = parser.parse_args()

        # === Handle snapshot mode ===
        if args.mode == "snapshot":
            if not args.folder:
                print("❌ Please provide --folder with snapshot mode.")
                return
            daily_snapshot.main(args.folder)
            return

        # === Handle compare mode ===
        if args.mode != "compare":
            print("❌ Please use --mode compare or --mode snapshot.")
            return

        if not args.file1 or not args.file2:
            print("❌ Please provide both --file1 and --file2 for comparison.")
            return

        if not os.path.exists(args.file1) or not os.path.exists(args.file2):
            print("❌ One or both file paths are invalid.")
            return

        if args.auto and args.model:
            print("❌ You can't use --model and --auto together. Choose one.")
            return

        # Determine model name
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

        # Load model
        model, module = load_model_by_name(model_name)
        if model is None or module is None:
            print(f"❌ Failed to load model: {model_name}")
            return

        # Extract features
        if "sbert" in model_name:
            vec1 = module.extract_features_from_file(args.file1, model)
            vec2 = module.extract_features_from_file(args.file2, model)

        elif model_name == "codebert":
            tokenizer = model[0]
            model = model[1]
            vec1 = module.extract_features_from_file(args.file1, tokenizer, model)
            vec2 = module.extract_features_from_file(args.file2, tokenizer, model)

        elif model_name == "clip":
            model, preprocess = clip_model.load_model()
            vec1 = clip_model.extract_features(args.file1, model, preprocess)
            vec2 = clip_model.extract_features(args.file2, model, preprocess)

        else:
            transform = module.get_transform()
            vec1 = module.extract_features(args.file1, model, transform)
            vec2 = module.extract_features(args.file2, model, transform)

        # Compute similarity
        similarity = cosine_similarity([vec1], [vec2])[0][0]
        print(f"Similarity: {similarity:.4f}")

        # Output verdict
        if similarity > args.threshold:
            print("✅ Files are perceptually similar.")
        else:
            print("❌ Files are different.")

    except Exception:
        print("❌ An unexpected error occurred. Please check your input and try again.")

if __name__ == "__main__":
    main()