from dataset import Dataset
from mapper import Mapper
from preprocessing import Preprocessor
from correlation import Correlation
from pathmanager import PathManager
from pca import PCA_reducer
from autoencoder_reducer import Autoencoder_Reducer
from analysis import CorrelationAnalyzer


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


datasets_ae = {}
aefiles = pathm.reducedfiles_ae(tumors)
for (t,file) in zip(tumors,aefiles):
    ae = Autoencoder_Reducer(path=file, 
                             dataset= datasets[t].T, 
                             encoding_dim=50, 
                             epochs=20, 
                             batch_size=32)
    datasets_ae[t] = ae.getMatrixReduced()


datasets_pca = {}
pcafiles = pathm.reducefiles_pca(tumors)

for (t,file) in zip(tumors, pcafiles):
    pca = PCA_reducer(path=file, dataset= datasets[t], threshold=0.9)
    datasets_pca[t] = pca.getMatrixReduced()


threshold = 0.9


corrfiles = pathm.correlationfiles(tumors,threshold=threshold)
corrdata = {}

for t,file in zip(tumors,corrfiles):
    correlator = Correlation(datasets[t])
    corrdata[t] = correlator.getCorrelationMatrix(output_path=file,chunk_size=1500,threshold=threshold)

del datasets


corrfilesae = pathm.correlationfilesae(tumors,threshold=threshold)
corrdata_ae = {}


for t, file in zip(tumors, corrfilesae):
    correlator = Correlation(datasets_ae[t].T)
    corrdata_ae[t] = correlator.getCorrelationMatrix(output_path=file, chunk_size= 1500, threshold=threshold)

del datasets_ae

corrfilespca = pathm.correlationfilespca(tumors,threshold=threshold)
corrdata_pca = {}

for t, file in zip(tumors, corrfilespca):
    correlator = Correlation(datasets_pca[t].T)
    corrdata_pca[t] = correlator.getCorrelationMatrix(output_path=file, chunk_size= 1500, threshold=threshold)

del datasets_pca


for t in tumors:
    analyzer = CorrelationAnalyzer(tumor_name=t, 
                                   df_raw=corrdata[t], 
                                   df_ae=corrdata_ae[t], 
                                   df_pca=corrdata_pca[t])
    
    # 1. Calcolo metriche numeriche (Jaccard)
    analyzer.print_jaccard_overlap()
    
    # 2. Generazione Grafici
    analyzer.plot_scatter()

    # ! OPTIONAL !: Se la RAM è piena, puoi cancellare i df di questo tumore ora
    # del corrdata[t], corrdata_ae[t], corrdatapca[t]
    # gc.collect()