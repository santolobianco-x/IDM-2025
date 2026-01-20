import pandas as pd

class Preprocessor:

    def __init__(self, dataset):
        self.dataset = dataset

    def rmrows(self):
        self.dataset = self.dataset[self.dataset['Età equivalente'] >= 12]
        return self.dataset
    
    def rmcolumns(self,cols):
        self.dataset = self.dataset.drop(columns=cols)
        return self.dataset
    
    def encode(self, cols):
        for col in cols:
            if col in self.dataset.columns:
                self.dataset[col] = self.dataset[col].map({'F': 0, 'M': 1})
        return self.dataset
    