# src/text_model/sbert_model.py

from sentence_transformers import SentenceTransformer

def load_model():
    """
    Load pretrained Sentence-BERT model.
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

def read_text_from_file(file_path):
    """
    Read raw text from a file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_features_from_file(file_path, model):
    """
    Load text from file and return its SBERT embedding.
    """
    text = read_text_from_file(file_path)
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding