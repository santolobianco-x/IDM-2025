import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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
        plot = pd.DataFrame({
            "PC1": Xpca[:,0],
            "PC2": Xpca[:,1],
            "class": y.values
        })
        plt.figure(figsize=(8,6))
        sns.scatterplot(
            data=plot, 
            x="PC1", 
            y= "PC2", 
            hue="class", 
            alpha = 0.85,
            s= 40,
            edgecolor = "black",
            linewidth = 0.9)
        plt.title(title, fontsize=14, fontweight="bold") 
        plt.xlabel("PC1", fontsize=12) 
        plt.ylabel("PC2", fontsize=12) 
        plt.tight_layout() 
        plt.show()


    def explainvariance(self):
        return self.pca.explained_variance_ratio_