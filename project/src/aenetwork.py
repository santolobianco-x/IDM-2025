import torch.nn as nn

class AENetwork(nn.Module):
    def __init__(self, input_dim, encoding_dim):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim,128),
            nn.ReLU(),
            nn.Linear(128, encoding_dim)
        )

        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded
        

    def encode(self, x):
        return self.encoder(x)
    