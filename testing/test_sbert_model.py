from loader import sbert_model
from sklearn.metrics.pairwise import cosine_similarity

# Load model
model = sbert_model.load_model()

# Paths to two text files
file1 = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/script.sh"
file2 = r"/home/kali/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/zcript.sh"

# Extract semantic vectors
vec1 = sbert_model.extract_features_from_file(file1, model)
vec2 = sbert_model.extract_features_from_file(file2, model)

# Compare similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

if similarity > 0.95:
    print("✅ Text files are semantically similar!")
else:
    print("❌ Text files are different.")