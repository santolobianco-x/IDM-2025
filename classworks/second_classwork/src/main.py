from dataloader import DataLoader
from preprocessing import Preprocessor
from pcavisualizer import PCAVisualizer
import pandas as pd

loader = DataLoader("data/Dataset DAES.xlsx")
loader.load()


datasets = {}
dfnames = ["ASD", "GDD", "Controlli"]

#LOADING DATASETS
for name in dfnames:
    print(f"======{name}======")
    datasets[name] = loader.get_sheet(name)
    loader.printfirstrow(name,10)
    loader.printinfo(name)


#CLEANING DATASETS
coltorm = ["Pazienti","Età cronologica (mesi)","Scala B","Scala D","TOT.","Score di rischio"]
for name in dfnames:
    preproc = Preprocessor(datasets[name])
    datasets[name] = preproc.rmrows()
    datasets[name] = preproc.rmcolumns(cols=coltorm)
    datasets[name] = preproc.encode(["Sesso"])


dflist = []
for name, df in datasets.items():
    dfc = df.copy()
    dfc["class"] = name
    dflist.append(dfc)

dfconcatenated = pd.concat(dflist, ignore_index=True)

dfconcatenated = dfconcatenated.dropna()

X = dfconcatenated.drop(columns=['class'])
y = dfconcatenated['class']



pca = PCAVisualizer(2)
Xpca = pca.reduce(X)
pca.plot(Xpca,y)