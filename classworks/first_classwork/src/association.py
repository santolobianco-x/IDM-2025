import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

class Association:

    def __init__(self,data):
        self.dataset : pd.DataFrame = data.copy()
        self.transactions = None
        self.rules = None

    def create_transaction(self):
        self.dataset['descr_liv4'] = self.dataset['descr_liv4'].astype(str)
        t = self.dataset.groupby('scontrino_id')['descr_liv4'].apply(list)
        self.transactions = t.tolist()
        return self
    
    def apriorirules(self, threshold = 0.05, minconfidence = 0.3):
        transenc = TransactionEncoder()
        transencAry = transenc.fit(self.transactions).transform(self.transactions)
        data = pd.DataFrame(transencAry,columns=transenc.columns_)


        freqitemsets = apriori(data,min_support=threshold,use_colnames=True)


        self.rules = association_rules(freqitemsets,metric='confidence', min_threshold=minconfidence)
        return self
    

    def fpgrowthrules(self, threshold = 0.05, minconfidence = 0.3):
        transec = TransactionEncoder()
        transecAry = transec.fit(self.transactions).transform(self.transactions)
        data = pd.DataFrame(transecAry,columns = transec.columns_)

        freqitemsets = fpgrowth(data,min_support=threshold, use_colnames=True)

        self.rules = association_rules(freqitemsets, metric='confidence', min_threshold=minconfidence)
        return self
    
    def showrules(self, n = 10):
        df = self.rules.copy()
        print(df[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(n))