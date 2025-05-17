from loader import clip_model
from sklearn.metrics.pairwise import cosine_similarity

# Load the CLIP model and preprocessing
model, preprocess = clip_model.load_model()

# Define your test images
img1 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image5.jpg"
img2 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image6.jpg"

# Extract features (AI perceptual hashes)
vec1 = clip_model.extract_features(img1, model, preprocess)
vec2 = clip_model.extract_features(img2, model, preprocess)

# Calculate similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

# Verdict
if similarity > 0.92:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")