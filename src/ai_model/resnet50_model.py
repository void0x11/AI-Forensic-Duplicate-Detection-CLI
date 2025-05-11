import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

def load_model():
    """
    Load pretrained ResNet-50 model and strip the classifier layer to return a feature extractor.
    """
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model = torch.nn.Sequential(*list(model.children())[:-1])  # Remove FC layer
    model.eval()
    return model

def get_transform():
    """
    Return preprocessing pipeline compatible with ResNet-50.
    """
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet means
            std=[0.229, 0.224, 0.225]    # ImageNet stds
        )
    ])

def extract_features(image_path, model, transform):
    """
    Extract a 2048-dimension feature vector from an image using ResNet-50.
    """
    img = Image.open(image_path).convert('RGB')
    img = transform(img).unsqueeze(0)  # Add batch dimension: [1, 3, 224, 224]
    
    with torch.no_grad():
        features = model(img)  # Output: [1, 2048, 1, 1]
    
    return features.view(-1).numpy()  # Shape: (2048,)
