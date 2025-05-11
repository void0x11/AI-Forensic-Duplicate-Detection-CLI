# src/ai_model/efficientnet_b1_model.py

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

def load_model():
    model = models.efficientnet_b1(weights=models.EfficientNet_B1_Weights.DEFAULT)
    model.classifier = torch.nn.Identity()  # Remove classification head
    model.eval()
    return model

def get_transform():
    return models.EfficientNet_B1_Weights.DEFAULT.transforms()

def extract_features(image_path, model, transform):
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)  # [1, 3, H, W]
    
    with torch.no_grad():
        features = model(img_tensor)  # Output shape: [1, 1280]
    
    return features.view(-1).numpy()