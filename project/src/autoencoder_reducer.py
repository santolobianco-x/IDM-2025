import os
import numpy as np
import pandas as pd
from autoencoder import Autoencoder

class Autoencoder_Reducer:
    def __init__(self, path, dataset, encoding_dim=50, epochs=20, batch_size =32):
        self.path = path
        self.dataset = dataset
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size

    def getMatrixReduced(self):
        if os.path.exists(self.path):
            print(f"Dataset reduced by Autoencoder found: {self.path}")
            return pd.read_csv(self.path, sep='\t', index_col=0)
        
        print(f"Dataset reduced by Autoencoder not found, generating:{self.path}")
        reduced = self._apply_autoencoder()
        return reduced
    
    def _apply_autoencoder(self):
        X = self.dataset.values.astype(np.float32)
        ae = Autoencoder(
            input_dim=X.shape[1],
            encoding_dim= self.encoding_dim,
            lr=0.001
        )

        ae.fit(X, epochs=self.epochs, batch_size=self.batch_size, verbose=0)

        Z = ae.transform(X)

        reduced = pd.DataFrame(Z, index=self.dataset.index, 
                               columns= [f"AE{i+1}" for i in range(Z.shape[1])])
        reduced.to_csv(self.path, sep='\t')
        return reduced