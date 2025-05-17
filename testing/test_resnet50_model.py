# testing/test_resnet50_model.py

from loader import resnet50_model
from sklearn.metrics.pairwise import cosine_similarity

# Load ResNet-50 model and preprocessing
model = resnet50_model.load_model()
transform = resnet50_model.get_transform()

# Define paths to test images
img1_path = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2_path = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image4.jpg"

# Extract features
vec1 = resnet50_model.extract_features(img1_path, model, transform)
vec2 = resnet50_model.extract_features(img2_path, model, transform)

# Calculate cosine similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

# Verdict
if similarity > 0.90:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")