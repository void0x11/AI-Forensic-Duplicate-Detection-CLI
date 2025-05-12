# src/text_model/sbert_deep_model.py

from sentence_transformers import SentenceTransformer

def load_model():
    """
    Load the all-mpnet-base-v2 SBERT model (high accuracy).
    """
    return SentenceTransformer('all-mpnet-base-v2')

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_features_from_file(file_path, model):
    text = read_text_from_file(file_path)
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding