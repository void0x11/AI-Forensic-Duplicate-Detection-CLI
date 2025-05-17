# testing/test_codebert_model.py

from loader import codebert_model
from sklearn.metrics.pairwise import cosine_similarity

# Load model
tokenizer, model = codebert_model.load_model()

# Files
file1 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/script.sh"
file2 = r"/home/void/Github/AI-Forensic-Duplicate-Detection-CLI/src/ai_model/sample_cases/zcript.sh"

# Extract vector embeddings
vec1 = codebert_model.extract_features_from_file(file1, tokenizer, model)
vec2 = codebert_model.extract_features_from_file(file2, tokenizer, model)

# Compare similarity
similarity = cosine_similarity([vec1], [vec2])[0][0]
print(f"Similarity: {similarity:.4f}")

if similarity > 0.85:
    print("✅ Code files are semantically similar!")
else:
    print("❌ Code files are different.")