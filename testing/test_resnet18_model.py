from loader import resnet18_model
from sklearn.metrics.pairwise import cosine_similarity

# Load model and preprocessing
model = resnet18_model.load_model()
transform = resnet18_model.get_transform()

# Paths to test images
img1_path = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2_path = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image4.jpg"

# Extract feature vectors
vec1 = resnet18_model.extract_features(img1_path, model, transform)
vec2 = resnet18_model.extract_features(img2_path, model, transform)

# Compare features
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

# Verdict
if similarity > 0.90:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")