import pandas as pd
from sklearn.preprocessing import StandardScaler


class Preprocessor:

    def __init__(self):
        self.scaler = StandardScaler()

    def preprocess(self, dataset):
        self.dataset = dataset.copy()
        self.dataset = self._traspose_matrix()
        self.dataset = self._filter_constant_genes()
        self.dataset = self._normalize()
        return self.dataset


    def _traspose_matrix(self):
        return self.dataset.T
    

    def _filter_constant_genes(self):
        return self.dataset.loc[:, self.dataset.var(axis=0) > 0]
    
    def _normalize(self):
        return  pd.DataFrame(self.scaler.fit_transform(self.dataset),
                                    index=self.dataset.index,
                                    columns=self.dataset.columns
                                    )
        
    