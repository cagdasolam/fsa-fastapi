import torch
from torchvision import models, transforms
import torch.nn as nn

# Load the model

model = models.resnet50(pretrained=False)
model.avg_pool = nn.AdaptiveAvgPool2d(1)
model.last_linear = nn.Sequential(
    nn.BatchNorm1d(2048),
    nn.Dropout(p=0.25),
    nn.Linear(in_features=2048, out_features=2048),
    nn.ReLU(),
    nn.BatchNorm1d(2048, eps=1e-05, momentum=0.1),
    nn.Dropout(p=0.5),
    nn.Linear(in_features=2048, out_features=195)
)

# Choose the best model from the k-fold cross validation
model.load_state_dict(torch.load('new_model_fold_4.pth', map_location=torch.device(
    'cpu')))  # 0 yerine en iyi modeli seçtiğiniz fold numarasını kullanın
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
model.eval()

# Transforms
transformer = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
])

class_file_path = './klasor_listesi.txt'

with open(class_file_path, 'r') as file:
    classes = file.read().splitlines()


    def preprocess_image(img):
        image = transformer(img).unsqueeze(0)
        return image.to(device)


    def prediction_image(img):
        img = preprocess_image(img)
        with torch.no_grad():
            outputs = model(img)
            probs = nn.functional.softmax(outputs, dim=1)
            max_prob, preds = torch.max(probs, 1)

        if max_prob.item() >= 0.7:
            return classes[preds.item()]
        else:
            return None
