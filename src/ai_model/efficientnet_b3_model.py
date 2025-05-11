# src/ai_model/efficientnet_b3_model.py

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

def load_model():
    model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.DEFAULT)
    model.classifier = torch.nn.Identity()  # Remove classification head
    model.eval()
    return model

def get_transform():
    return models.EfficientNet_B3_Weights.DEFAULT.transforms()

def extract_features(image_path, model, transform):
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)
    
    with torch.no_grad():
        features = model(img_tensor)
    
    return features.view(-1).numpy()