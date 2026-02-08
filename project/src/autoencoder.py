import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from aenetwork import AENetwork
torch.manual_seed(42)
np.random.seed(42)



class Autoencoder:
    def __init__(self, input_dim, encoding_dim=50, lr=0.001):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim


        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")


        self.model = AENetwork(input_dim, encoding_dim).to(self.device)

        self.criterion = nn.MSELoss()

        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)



    def fit(self, X, epochs=20, batch_size=32, verbose = 1):
        X_tensor = torch.tensor(X, dtype=torch.float32)


        dataset = TensorDataset(X_tensor, X_tensor)
        dataloader = DataLoader(dataset, 
                                batch_size=batch_size, 
                                shuffle=True,
                                num_workers=0)

        self.model.train()
        for epoch in range(epochs):
            epoch_loss = 0.0
            for batch_in, batch_out in dataloader:
                batch_in, batch_out = batch_in.to(self.device), batch_out.to(self.device)

                self.optimizer.zero_grad()
                output = self.model(batch_in)
                loss = self.criterion(output, batch_out)
                loss.backward()
                self.optimizer.step()

                epoch_loss += loss.item()

            if verbose > 0:
                print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(dataloader):.6f}")


    def transform(self, X):
        self.model.eval()
        X_tensor = torch.tensor(X, dtype=torch.float32).to(self.device)


        with torch.no_grad():
            encoded = self.model.encode(X_tensor)

        return encoded.cpu().numpy()        