from loader import sbert_deep_model
from sklearn.metrics.pairwise import cosine_similarity

# Load high-accuracy SBERT model
model = sbert_deep_model.load_model()

# Files to compare
file1 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/script.sh"
file2 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/zcript.sh"

# Extract embeddings
vec1 = sbert_deep_model.extract_features_from_file(file1, model)
vec2 = sbert_deep_model.extract_features_from_file(file2, model)

# Similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

if similarity > 0.85:
    print("✅ Texts are semantically similar!")
else:
    print("❌ Texts are different.")