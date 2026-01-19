import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class Clustering:
    def __init__(self,data):
        self.dataset : pd.DataFrame= data.copy()
        self.matrix = None
        self.matrixreduced = None
        self.clusters = None


    def preparematrix(self):
        self.dataset = self.dataset[self.dataset['tessera'].notna()]
        self.matrix = self.dataset.groupby(['tessera','descr_liv4']).size().unstack(fill_value=0)
        return self
    
    def reducedimensionality(self,components=10):
        pca = PCA(n_components=components)
        self.matrixreduced = pca.fit_transform(self.matrix)
        return self
    

    @staticmethod
    def elbow(matrixreduced, kmax = 10):
        inertias = []

        for k in range(1,kmax+1):
            Kmeans = KMeans(n_clusters=k,random_state=42)
            Kmeans.fit(matrixreduced)
            inertias.append(Kmeans.inertia_)

        delta = []
        for i in range(1,len(inertias)):
            delta.append(inertias[i-1]-inertias[i])
        return delta
        
    
    @staticmethod
    def silhouette(matrixreduced, kmin = 2, kmax = 10):
        scores = {}

        for k in range(kmin,kmax+1):
            Kmeans = KMeans(n_clusters=k, random_state=42)
            labels = Kmeans.fit_predict(matrixreduced)
            score = silhouette_score(matrixreduced,labels)
            scores[k] = score

        return scores
    

    def clustering(self, method='',kmin = 2, kmax = 10, k = 10):
        if self.matrixreduced is None:
            raise ValueError("Si deve prima applicare la PCA")


        if method == 'elbow':
            delta = self.elbow(self.matrixreduced,kmax)
            bestk = delta.index(max(delta))+2

            kmeans = KMeans(n_clusters=bestk, random_state=42)
            self.labels = kmeans.fit_predict(self.matrixreduced)
            
            return bestk, self.labels
        
        elif method == 'silhouette':
            scores = self.silhouette(self.matrixreduced,kmin,kmax)
            bestk = max(scores,key=scores.get)

            kmeans = KMeans(n_clusters=bestk,random_state=42)
            self.labels = kmeans.fit_predict(self.matrixreduced)

            return bestk,self.labels

        else:
            Kmeans = KMeans(n_clusters=k,random_state=42)
            self.labels = Kmeans.fit_predict(self.matrixreduced)
            return k, self.labels