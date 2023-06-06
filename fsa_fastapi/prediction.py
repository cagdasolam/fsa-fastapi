import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.autograd import Variable
from PIL import Image

class_file_path = './product_names.txt'

with open(class_file_path, 'r') as file:
    classes = file.read().splitlines()


    class ConvNet(nn.Module):
        def __init__(self, num_classes=12):
            super(ConvNet, self).__init__()

            self.layer1 = nn.Sequential(
                nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(num_features=12),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Dropout2d(p=0.2)
            )

            self.layer2 = nn.Sequential(
                nn.Conv2d(in_channels=12, out_channels=20, kernel_size=3, stride=1, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Dropout2d(p=0.3)
            )

            self.layer3 = nn.Sequential(
                nn.Conv2d(in_channels=20, out_channels=32, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(num_features=32),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Dropout2d(p=0.4)
            )

            self.layer4 = nn.Sequential(
                nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(num_features=64),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Dropout2d(p=0.5)
            )

            self.layer5 = nn.Sequential(
                nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1),
                nn.BatchNorm2d(num_features=128),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2),
                nn.Dropout2d(p=0.6)
            )

            self.fc = nn.Linear(in_features=18 * 18 * 32, out_features=num_classes)

        def forward(self, input):
            output = self.layer1(input)
            output = self.layer2(output)
            output = self.layer3(output)
            output = output.view(-1, 18 * 18 * 32)
            output = self.fc(output)
            return output


    checkpoint = torch.load('model2.model', map_location=torch.device('cpu'))
    model = ConvNet(num_classes=12)
    model.load_state_dict(checkpoint)
    model.eval()

    # Add the softmax function
    softmax = torch.nn.Softmax(dim=1)

    # Change the threshold value to the desired accuracy threshold (e.g. 0.7 for 70%)
    thresholds = 0.7

    # Transforms
    transformer = transforms.Compose([
        transforms.Resize((150, 150)),
        transforms.ToTensor(),  # 0-255 to 0-1, numpy to tensors
        transforms.Normalize([0.5, 0.5, 0.5],  # 0-1 to [-1,1] , formula (x-mean)/std
                             [0.5, 0.5, 0.5])
    ])


    def prediction_image(image):
        image_tensor = transformer(image).float()
        image_tensor = image_tensor.unsqueeze(0)

        if torch.cuda.is_available():
            image_tensor = image_tensor.cuda()

        input = Variable(image_tensor)
        output = model(input)

        # Apply the softmax function to the output
        probabilities = softmax(output).data.numpy()[0]

        preds = []

        for index, prob in enumerate(probabilities):
            # Check if the probability is above the threshold for the current class
            if prob >= thresholds:
                preds.append(classes[index])

        if len(preds) > 0:
            return preds[0]  # Return the first predicted class
        else:
            return None
