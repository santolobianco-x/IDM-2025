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


pos_thresh = 0.8
neg_thresh = -0.5

rawpaths = pathm.rawfiles(tumors)


procpaths = pathm.processedfiles(tumors)
aepath = pathm.reducedfiles_ae(tumors) 
pcapath = pathm.reducedfiles_pca(tumors)



corrpath = pathm.correlationfiles(tumors)
corrpath_ae = pathm.correlationfilesae(tumors)
corrpath_pca = pathm.correlationfilespca(tumors)




for idx,t in enumerate(tumors):
    try:
        dataset = Dataset(raw_path=rawpaths[idx],processed_path=procpaths[idx])
        dataset = dataset.prepare(mapper,preproc)
        print(f"Dimension of '{procpaths[idx]}': {dataset.shape}")
    except FileNotFoundError as e:
        print(f"{e}")
        continue

    ae = Autoencoder_Reducer(path=aepath[idx],
                             dataset=dataset.T,
                             encoding_dim=45,
                             epochs=25,
                             batch_size=32)
    dataset_ae = ae.getMatrixReduced()
    print(f"Dimension of '{aepath[idx]}: {dataset_ae.shape}'")
    pca = PCA_reducer(path=pcapath[idx],
                      dataset=dataset,
                      threshold= 0.9)
    dataset_pca = pca.getMatrixReduced()
    print(f"Dimension of '{pcapath[idx]}: {dataset_pca.shape}'")

    correlator = Correlation(dataset=dataset)
    corrdata = correlator.getCorrelationMatrix(output_path=corrpath[idx],
                                               chunk_size=1500,
                                               pos_thresh=pos_thresh,
                                               neg_thresh=neg_thresh,
                                               overwrite=False)
    
    correlator_ae = Correlation(dataset=dataset_ae.T)
    corrdata_ae = correlator_ae.getCorrelationMatrix(output_path=corrpath_ae[idx],
                                                     chunk_size=1500,
                                                     pos_thresh=pos_thresh,
                                                     neg_thresh=neg_thresh,
                                                     overwrite=False)
    
    correlator_pca = Correlation(dataset=dataset_pca.T)
    corrdata_pca = correlator_pca.getCorrelationMatrix(output_path=corrpath_pca[idx],
                                                       chunk_size=1500,
                                                       pos_thresh=pos_thresh,
                                                       neg_thresh=neg_thresh,
                                                       overwrite=False)
    print()

    
    del dataset_ae, dataset_pca
    analyzer = CorrelationAnalyzer(tumor= t,
                                   dataset= dataset,
                                   corr=corrdata,
                                   corr_ae=corrdata_ae,
                                   corr_pca=corrdata_pca,
                                   epsilon=0.15)
    analyzer.run_full_analysis()
    print()

    del corrdata, corrdata_ae, corrdata_pca, dataset
    


