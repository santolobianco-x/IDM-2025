import os

class PathManager:
    def __init__(self, 
                 raw_dir="data/raw", 
                 processed_dir="data/processed", 
                 results_dir="data/results",
                 pca_dir= "data/pca",
                 autoencoder_dir = "data/ae"
                 ):
        
        self.raw_dir=raw_dir
        self.processed_dir=processed_dir
        self.results_dir=results_dir
        self.pca_dir=pca_dir
        self.autoencoder_dir = autoencoder_dir

        for path in [self.raw_dir, self.processed_dir, self.results_dir, self.autoencoder_dir, self.pca_dir]:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)

    def rawfile(self, tumor):
        return os.path.join(self.raw_dir, f"{tumor}.star_fpkm.tsv")
    
    def processedfile(self, tumor):
        return os.path.join(self.processed_dir, f"{tumor}.star_fpkm.processed.tsv")
    
    def reducedfile_pca(self, tumor):
        return os.path.join(self.pca_dir,f"{tumor}.reduced_pca.tsv")
    
    def reducedfile_ae(self,tumor):
        return os.path.join(self.autoencoder_dir,f"{tumor}.reduced_ae.tsv")
    
    def correlationfile(self, tumor, threshold):
        return os.path.join(self.results_dir, f"{tumor}.correlation_{threshold}.tsv")
    
    def rawfiles(self, tumors):
        return [self.rawfile(t) for t in tumors]
    
    def processedfiles(self, tumors):
        return [self.processedfile(t) for t in tumors]
    
    def reducefiles_pca(self, tumors):
        return [self.reducedfile_pca(t) for t in tumors]
    
    def reducedfiles_ae(self, tumors):
        return [self.reducedfile_ae(t) for t in tumors]
    
    def correlationfiles(self, tumors, threshold):
        return [self.correlationfile(t,threshold) for t in tumors]