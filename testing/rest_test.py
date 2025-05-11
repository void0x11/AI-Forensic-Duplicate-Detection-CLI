from loader import restmodel
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once using the loaded module
model_instance = restmodel.load_model()

# Paths to your test images (inside testing/ folder)
img1 = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2 = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image7.jpg"

# Extract features using the imported module
vec1 = restmodel.extract_features(img1, model_instance)
vec2 = restmodel.extract_features(img2, model_instance)

# Calculate similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]

# Output result
print(f"Similarity between images: {similarity:.4f}")

# Optional: Simple verdict
threshold = 0.90
if similarity > threshold:
    print("✅ Images are near-duplicates!")
else:
    print("❌ Images are different.")