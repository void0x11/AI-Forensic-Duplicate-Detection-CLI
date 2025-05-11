import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

def load_model():
    """
    Load pretrained ResNet-101 model and return it without the classification head.
    """
    model = models.resnet101(weights=models.ResNet101_Weights.DEFAULT)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove FC layer
    model.eval()
    return model

def get_transform():
    """
    Return the preprocessing transform compatible with ResNet-101 and ImageNet.
    """
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def extract_features(image_path, model, transform):
    """
    Extract a 2048-dimension feature vector from an image using ResNet-101.
    """
    img = Image.open(image_path).convert('RGB')
    img_tensor = transform(img).unsqueeze(0)  # [1, 3, 224, 224]
    
    with torch.no_grad():
        features = model(img_tensor)  # Output shape: [1, 2048, 1, 1]
    
    return features.view(-1).numpy()  # Flatten to shape: (2048,)