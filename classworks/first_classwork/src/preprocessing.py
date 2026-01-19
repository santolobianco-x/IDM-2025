import pandas as pd 
from datetime import time

class Preprocessor:
    def __init__(self,data):
        self.dataset = data.copy()

    def dropcol(self):
        colToDrop = ["db_id", "puntovendita_id", "cassa", "cassiere", "nummero_scontrino",
            "num_riga", "r_peso", "r_iva", "r_sconto",
            "tipologia", "descr_tipologia", "cod_rep", "descr_rep", "cat_mer"]
        
        self.dataset = self.dataset.drop(columns = colToDrop)
        return self
    
    def removeshoppers(self):
        self.dataset = self.dataset[self.dataset['descr_liv4'].str.lower() != 'shoppers']
        return self
    
    def convertdatetime(self):
        self.dataset.dropna(subset=['data','ora'], inplace=True)


        self.dataset['data'] = pd.to_datetime(self.dataset['data'])
        self.dataset['ora'] = pd.to_datetime(self.dataset['ora']+ ":00", format="%H:%M:%S").dt.time
        return self
    

    @staticmethod
    def monthtorange(m,d):
        if m < 5:
            return "RANGE 1"
        elif m == 5 and d <= 15:
            return "RANGE 1"
        elif m < 10:
            return "RANGE 2"
        else:
            return "RANGE 3"


    @staticmethod   
    def timetorange(h,m):
        current = time(h,m)
        if time(8,30) <= current <= time(12,30):
            return "SLOT 1"
        elif time(12,30) < current <= time(16,30):
            return "SLOT 2"
        elif time(16,30) < current <= time(20,30):
            return "SLOT 3"
        else:
            return None

    
    def createslices(self):
        self.dataset['fascia_mese'] = self.dataset.apply(lambda row: Preprocessor.monthtorange(row['data'].month,row['data'].day), axis= 1)
        self.dataset['fascia_oraria'] = self.dataset['ora'].apply( lambda t: Preprocessor.timetorange(t.hour, t.minute))
        return self
    
    def getdataset(self):
        return self.dataset