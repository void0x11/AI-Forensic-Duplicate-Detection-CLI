from transformers import AutoTokenizer, AutoModel
import torch

def load_model():
    """
    Load CodeBERT model and tokenizer (base).
    """
    tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
    model = AutoModel.from_pretrained("microsoft/codebert-base")
    model.eval()
    return tokenizer, model


def read_code_from_file(file_path):
    """
    Read raw code from file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_features_from_file(file_path, tokenizer, model):
    """
    Encode the file content and return the CLS embedding as feature vector.
    """
    code = read_code_from_file(file_path)
    inputs = tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use [CLS] token representation as embedding
    cls_embedding = outputs.last_hidden_state[:, 0, :]  # shape: [1, 768]
    return cls_embedding.squeeze().numpy()