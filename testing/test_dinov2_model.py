from loader import dinov2_model
from sklearn.metrics.pairwise import cosine_similarity

# Load model and transform
model = dinov2_model.load_model()
transform = dinov2_model.get_transform()

# Image paths
img1 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image4.jpg"

# Extract features
vec1 = dinov2_model.extract_features(img1, model, transform)
vec2 = dinov2_model.extract_features(img2, model, transform)

# Similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

if similarity > 0.92:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")