import torch
import timm
import torchvision.transforms as transforms
from PIL import Image

def load_model():
    """
    Load pretrained DINOv2 model from timm and remove classification head.
    """
    model = timm.create_model("vit_base_patch14_reg4_dinov2", pretrained=True)
    model.reset_classifier(0)  # Remove classification head
    model.eval()
    return model

def get_transform():
    """
    Return transform compatible with DINOv2 input size (518x518).
    """
    return transforms.Compose([
        transforms.Resize((518, 518)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5]
        )
    ])


def extract_features(image_path, model, transform):
    """
    Extract a high-dimension perceptual feature vector from an image using DINOv2.
    """
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)  # [1, 3, 224, 224]

    with torch.no_grad():
        features = model(img_tensor)  # Output: [1, 768]
    
    return features.view(-1).numpy()  # Flatten to [768]