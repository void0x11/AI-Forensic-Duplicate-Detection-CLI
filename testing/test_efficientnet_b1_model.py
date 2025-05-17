from loader import efficientnet_b1_model
from sklearn.metrics.pairwise import cosine_similarity

model = efficientnet_b1_model.load_model()
transform = efficientnet_b1_model.get_transform()

img1_path = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image3.jpg"
img2_path = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/image4.jpg"

vec1 = efficientnet_b1_model.extract_features(img1_path, model, transform)
vec2 = efficientnet_b1_model.extract_features(img2_path, model, transform)

similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

if similarity > 0.90:
    print("✅ Images are perceptually similar!")
else:
    print("❌ Images are different.")