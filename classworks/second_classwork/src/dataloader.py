import pandas as pd
import numpy as np

class DataLoader:

    def __init__(self, path):
        self.path = path
        self.sheets = None

    def load(self):
        self.sheets = pd.read_excel(self.path, sheet_name=None, header = 1)
        print(f"Fogli caricati: {list(self.sheets.keys())}")
        return self.sheets
    
    def get_sheet(self,name):
        
        if self.sheets is None:
            raise RuntimeError("Dataset non caricato")
        df = self.sheets.get(name) 

        if df is None:
            raise ValueError(f"Foglio '{name}' non trovato nel file.")
        return pd.DataFrame(df)
    
    def printfirstrow(self, sheet_name, occur = 5):
        df = self.get_sheet(sheet_name)
        print(df.head(occur))

    def printinfo(self, sheet_name):
        df = self.get_sheet(sheet_name)
        print(df.info())