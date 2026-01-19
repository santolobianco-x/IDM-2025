import pandas as pd
from dataloader import DataLoader
from preprocessing import Preprocessor
from frequencyanalisys import FrequencyAnalyzer
from association import Association
from clustering import Clustering

loader = DataLoader("data/AnonymizedFidelity.csv")

data : pd.DataFrame= loader.load()


print("FIRST FIVE OCCURENCIES")
loader.printfirst(5)


print("INFO")
print(loader.info())


preprocessor = Preprocessor(data)
data : pd.DataFrame = preprocessor.removeshoppers().dropcol().convertdatetime().createslices().getdataset()
print(data.head(15))



frequencyanalyzer = FrequencyAnalyzer(data)
frequencyanalyzer.analyzelevels()
frequencyanalyzer.stratifiedlevels()



associator = Association(data)
print("APRIORI threshold = 0.05 confidence = 0.2 maxnumrules = 20")
apriori = associator.create_transaction().apriorirules(0.05,0.2).showrules(20)

print("FPGROWTH threshold = 0.05 confidence = 0.15 maxnumrules = 30")
fpgrowth = associator.create_transaction().fpgrowthrules(0.05,0.15).showrules(30)




cluster = Clustering(data)
cluster.preparematrix().reducedimensionality(components=10)
bestk,labels = cluster.clustering(method='elbow',kmax=10)
results = pd.DataFrame(
    {
        'tessera': cluster.matrix.index,
        'cluster': labels
    }
)

print(results)
labSeries = pd.Series(labels)
print(labSeries.value_counts())