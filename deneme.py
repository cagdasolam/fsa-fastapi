import os

import torch
from torchvision import models, transforms
import torch.nn as nn
from PIL import Image

# Load the model
model = models.resnet101(pretrained=True)
num_features = model.fc.in_features

model.avgpool = nn.AdaptiveAvgPool2d(1)
model.fc = nn.Sequential(
    nn.BatchNorm1d(num_features),
    nn.Dropout(p=0.25),
    nn.Linear(num_features, num_features),
    nn.ReLU(),
    nn.BatchNorm1d(num_features, eps=1e-05, momentum=0.1),
    nn.Dropout(p=0.5),
    nn.Linear(num_features, 195)
)

# Choose the best model from the k-fold cross validation
model.load_state_dict(torch.load('resnet101_fold_0.pth', map_location=torch.device(
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


# Load and preprocess an image
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = transformer(image).unsqueeze(0)
    return image.to(device)


# Make a prediction


class_file_path = './klasor_listesi.txt'
with open(class_file_path, 'r') as file:
    classes = file.read().splitlines()

    for image in os.listdir("productsimage"):

        dosya_yolu = os.path.join("./productsimage", image)

        # Sadece fotoğraf dosyalarını kontrol etmek için
        if os.path.isfile(dosya_yolu) and dosya_yolu.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            try:
                # Fotoğrafı aç

                img = preprocess_image(dosya_yolu)
                with torch.no_grad():
                    outputs = model(img)
                    _, preds = torch.max(outputs, 1)

                print('foto', dosya_yolu, " Predicted class: ", classes[preds.item()])

            except IOError:
                print("Fotoğraf açılırken bir hata oluştu:", dosya_yolu)