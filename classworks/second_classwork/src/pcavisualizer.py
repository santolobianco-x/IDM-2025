import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

class PCAVisualizer: 

    def __init__(self, ncomponents = 2):
        self.ncomponents  = ncomponents
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.ncomponents)

    def reduce(self, data):
        datascaled = self.scaler.fit_transform(data)
        datareduced = self.pca.fit_transform(datascaled)
        return datareduced
    
    def plot(self, Xpca, y, title = "PCA 2D"):
        plt.figure(figsize=(8,6))
        classes = y.unique()
        for c in classes:
            idx = y == c
            plt.scatter(Xpca[idx,0], Xpca[idx,1], label = c, alpha=0.7)
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title(title)
        plt.grid()
        plt.show()
        
