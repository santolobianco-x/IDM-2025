import pandas as pd

class DataLoader:

    def __init__(self,path):
        self.path = path
        self.dataset = None

    def load(self):
        self.dataset = pd.read_csv(self.path)
        return self.dataset
    
    def printfirst(self,occur):
        if self.dataset is None:
            raise RuntimeError("Dataset non caricato.")
        print(self.dataset.head(occur))

    def info(self):
        if self.dataset is None:
            raise RuntimeError("Dataset non caricato.")
        return self.dataset.info() 