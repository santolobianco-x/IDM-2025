import numpy as np
import pandas as pd
import os
import gc

class Correlation:
    def __init__(self, dataset):
        self.dataset = dataset
        self.n_samples = dataset.shape[0]
 
    def getCorrelationMatrix(self, output_path, chunk_size=2000, threshold=None, overwrite=False):
        if os.path.exists(output_path) and not overwrite:
            print(f"Correlation matrix: {output_path}")
        else:
            if os.path.exists(output_path):
                try:
                    os.remove(output_path)
                    print(f"Old file removed: {output_path}")
                except OSError as e:
                    print(f"Error removing file: {e}")
                    
            else:
                print(f"Correlation matrix not found, generating:{output_path}")
            self.chunked_correlation(output_path,chunk_size, threshold)
        return pd.read_csv(output_path,sep='\t')

    
        
    def chunked_correlation(self, op, size=2000, threshold=None):    
        n_genes = self.dataset.shape[1]
        gene_names = self.dataset.columns.values
        
        with open(op, "w") as f:
            f.write(f"GeneA\tGeneB\tCorrelation\n")

        for i in range(0, n_genes, size):
            
            
            rawFirstBlock = self.dataset.iloc[:, i:i+size].values.T.astype(np.float32)
            firstCols = gene_names[i:i+size]
            
            
            mean_i = rawFirstBlock.mean(axis=1, keepdims=True)
            std_i = rawFirstBlock.std(axis=1, keepdims=True)
            std_i[std_i == 0] = 1e-9 
            firstBlock = (rawFirstBlock - mean_i) / std_i
            
            del rawFirstBlock, mean_i, std_i


            for j in range(i, n_genes, size):
                
                
                rawSecondBlock = self.dataset.iloc[:, j:j+size].values.T.astype(np.float32)
                secondCols = gene_names[j:j+size]
                
                
                mean_j = rawSecondBlock.mean(axis=1, keepdims=True)
                std_j = rawSecondBlock.std(axis=1, keepdims=True)
                std_j[std_j == 0] = 1e-9
                secondBlock = (rawSecondBlock - mean_j) / std_j
                
                del rawSecondBlock, mean_j, std_j

                
                corr_block = np.dot(firstBlock, secondBlock.T) / (self.n_samples - 1)

                
                if i == j:
                    mask = np.triu(np.ones(corr_block.shape, dtype=bool), k=1)
                else:
                    mask = np.ones(corr_block.shape, dtype=bool)

                if threshold is not None:
                    mask = mask & (np.abs(corr_block) > threshold)

                rows, cols = np.where(mask)
                
                
                if len(rows) > 0:
                    df_chunk = pd.DataFrame({
                        'GeneA': firstCols[rows],   
                        'GeneB': secondCols[cols], 
                        'Correlation': corr_block[rows, cols]
                    })
                    
                    df_chunk.to_csv(op, mode='a', sep='\t', header=False, index=False, float_format='%.7f')
                    
                    del df_chunk

                
                del secondBlock, corr_block, mask, rows, cols
                
            del firstBlock
            gc.collect()