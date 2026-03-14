import torch
from ml_model.model import AutoEncoder

model = AutoEncoder()
model.load_state_dict(torch.load("ml_model/autoencoder.pth"))
model.eval()

THRESHOLD = 0.002

def detect(feature):
    x = torch.tensor([feature], dtype=torch.float32)
    recon = model(x)
    error = torch.mean((x - recon) ** 2).item()
    return error, error > THRESHOLD
