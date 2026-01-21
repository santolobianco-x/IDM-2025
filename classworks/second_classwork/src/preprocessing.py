import pandas as pd
from sklearn.model_selection import train_test_split

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


def splitdata(X, y, testsize = 0.2, random_state = 42):
        return train_test_split(X, y, test_size=testsize, random_state=random_state, stratify = y)
    