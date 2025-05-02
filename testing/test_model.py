from ai_model import model
from sklearn.metrics.pairwise import cosine_similarity

# Load the model once
model = load_model()

# Paths to your test images (inside testing/ folder)
img1_path = 'testing/img1.jpg'
img2_path = 'testing/img2.jpg'

# Extract features
vec1 = extract_features(img1_path, model)
vec2 = extract_features(img2_path, model)

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