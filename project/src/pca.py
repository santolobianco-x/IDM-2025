from sklearn.decomposition import PCA
import numpy as np
import os
import pandas as pd

class PCA_reducer:
    def __init__(self, path, dataset, threshold = 0.9):
        self.path = path
        self.dataset = dataset
        self.threshold = threshold


    def getMatrixReduced(self):
        if os.path.exists(self.path):
            print(f"Dataset reduced by PCA found: {self.path}")
            return pd.read_csv(self.path, sep="\t", index_col=0)
        
        print(f"Dataset reduced by PCA not found, generating: {self.path}")
        reduced = self._apply_pca()
        return reduced
        
    def _apply_pca(self):
        data_for_pca = self.dataset.T        
        pcamodel = PCA(n_components=self.threshold)
        reduced = pcamodel.fit_transform(data_for_pca)

        reduced = reduced.astype(np.float32)
        reduced = pd.DataFrame(reduced,
                               index= data_for_pca.index,
                               columns= [f"PC{i+1}" for i in range(reduced.shape[1])])
        
        reduced.to_csv(self.path, sep='\t')
        return reduced