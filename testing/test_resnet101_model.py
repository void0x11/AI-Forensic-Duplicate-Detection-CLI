from loader import resnet101_model
from sklearn.metrics.pairwise import cosine_similarity

# Load ResNet-101 model and preprocessing
model = resnet101_model.load_model()
transform = resnet101_model.get_transform()

# Test image paths
img1_path = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2_path = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image4.jpg"

# Extract features
vec1 = resnet101_model.extract_features(img1_path, model, transform)
vec2 = resnet101_model.extract_features(img2_path, model, transform)

# Compute similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

# Verdict
if similarity > 0.90:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")