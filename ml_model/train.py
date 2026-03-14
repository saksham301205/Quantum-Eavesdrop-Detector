import torch
import pandas as pd
from quantum_sim.bb84 import simulate_bb84
from features.extract_features import extract_features
from ml_model.model import AutoEncoder

model = AutoEncoder()
optimizer = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = torch.nn.MSELoss()

data = []
for _ in range(300):
    a, b = simulate_bb84(eavesdrop=False)
    data.append(extract_features(a, b))

df = pd.DataFrame(data, columns=["qber", "entropy", "key_len"])
df.to_csv("data/normal_data.csv", index=False)

train_data = torch.tensor(df.values, dtype=torch.float32)

for _ in range(400):
    output = model(train_data)
    loss = loss_fn(output, train_data)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

torch.save(model.state_dict(), "ml_model/autoencoder.pth")
print("Training complete")
