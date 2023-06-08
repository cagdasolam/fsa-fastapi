import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torch.autograd import Variable
from PIL import Image

class_file_path = '/app/klasor_listesi.txt'

with open(class_file_path, 'r') as file:
    classes = file.read().splitlines()



    model = resnet50(pretrained=False)
    model.fc = torch.nn.Linear(2048, 195)  # Again, change 195 to match the number of classes you have
    model.load_state_dict(torch.load("/app/model195.model"))
    model.eval()
    

    # Add the softmax function
    softmax = torch.nn.Softmax(dim=1)

    # Change the threshold value to the desired accuracy threshold (e.g. 0.7 for 70%)
    thresholds = 0.2

    # Transforms
    transformer = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


    def prediction_image(image):
        image = Image.open('path_to_your_image.jpg')  # Enter the path to the image you want to predict
        image = image_transforms(image).float()
        image = Variable(image, requires_grad=True)
        image = image.unsqueeze(0)

        # Make the prediction
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        image = image.to(device)
        model = model.to(device)
        output = model(image)

        # Get the predicted class
        _, predicted_class = torch.max(output, 1)

        return predicted_class.item()

        
