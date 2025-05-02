import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

# 1. Load and prepare the model
def load_model():
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)  # Future-proof
    model = torch.nn.Sequential(*list(model.children())[:-1])
    model.eval()
    return model

# 2. Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# 3. Extract feature vector (AI perceptual hash)
def extract_features(image_path, model):
    img = Image.open(image_path).convert('RGB')
    img = transform(img).unsqueeze(0)  # [1, 3, 224, 224]
    with torch.no_grad():
        features = model(img)
    return features.view(-1).numpy()
