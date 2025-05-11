import torch
import open_clip
from PIL import Image

def load_model():
    """
    Load the pretrained CLIP model and its preprocessing transforms.
    """
    model, _, preprocess = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='laion2b_s34b_b79k'
    )
    model.eval()
    return model, preprocess

def extract_features(image_path, model, preprocess):
    """
    Extract a 512-dimension feature vector (AI hash) from an image using CLIP.
    """
    img = Image.open(image_path).convert('RGB')
    img_tensor = preprocess(img).unsqueeze(0)  # [1, 3, 224, 224]
    
    with torch.no_grad():
        features = model.encode_image(img_tensor)
    
    return features[0].numpy()  # Shape: (512,)
