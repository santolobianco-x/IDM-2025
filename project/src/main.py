from dataset import Dataset
from mapper import Mapper
from preprocessing import Preprocessor
from correlation import Correlation 
from pathmanager import PathManager
from pca import PCA_reducer
from autoencoder_reducer import Autoencoder_Reducer
import pandas as pd


tumors = ["TCGA-BRCA","TCGA-COAD","TCGA-LUAD", "TCGA-OV", "TCGA-PAAD", "TCGA-PRAD"]
mapper = Mapper("gene_mapping.tsv")
preproc = Preprocessor()


pathm = PathManager()
rawpaths = pathm.rawfiles(tumors)
procpaths = pathm.processedfiles(tumors)


datasets = {}
available_tumors = []

for t,rawpath, procpath in zip(tumors,rawpaths,procpaths):
    try:
        dataset = Dataset(rawpath,procpath).prepare(mapper, preproc)
        datasets[t] = dataset
        available_tumors.append(t)
    except FileNotFoundError as e:
        print(f"{e}")
        continue


tumors = available_tumors


if len(tumors) == 0:
    print("No tumor dataset available")
    exit(1)


dataset_ae = {}
aefiles = pathm.reducedfiles_ae(tumors)
for (t,file) in zip(tumors,aefiles):
    ae = Autoencoder_Reducer(path=file, 
                             dataset= datasets[t].T, 
                             encoding_dim=50, 
                             epochs=20, 
                             batch_size=32)
    dataset_ae[t] = ae.getMatrixReduced()
datasets_pca = {}


pcafiles = pathm.reducefiles_pca(tumors)

for (t,file) in zip(tumors, pcafiles):
    pca = PCA_reducer(path=file, dataset= datasets[t], threshold=0.9)
    datasets_pca[t] = pca.getMatrixReduced()




"""
threshold = 0.90
corrfiles = pathm.correlationfiles(tumors,threshold=threshold)

for t, outputfile in zip(tumors, corrfiles):
    try:
        correlator = Correlation(datasets[t])
        correlator.chunked_correlation(output_path=outputfile,chunk_size=1500,threshold=threshold)
    except FileExistsError as e:
        print(e)
"""





"""
df = datasets_pca[tumors[1]].head(10)
df.to_csv(f"data/light.tsv", sep="\t")
"""


