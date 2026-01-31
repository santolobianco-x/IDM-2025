import numpy as np
import os

class Correlation:
    def __init__(self, dataset):
        self.dataset = dataset
 
    def chunked_correlation(self, output_path, chunk_size=500, threshold=None, overwrite=False ):
        if os.path.exists(output_path) and not overwrite:
            raise FileExistsError(f"File: '{output_path} already exists. Set overwrite=True to replace it.'")
        
        n_genes = self.dataset.shape[1]
        MAX_BUFFER_LINES = 30000


        with open(output_path, "w") as f:
            f.write(f"GeneA\tGeneB\tCorrelation\tThreshold = {threshold}\n")

            for i in range(0, n_genes, chunk_size):
                firstBlock = self.dataset.iloc[:, i:i+chunk_size]
                firstCols = firstBlock.columns
                firstSize = firstBlock.shape[1]

                for j in range(i, n_genes, chunk_size):
                    secondBlock = self.dataset.iloc[:, j:j+chunk_size]
                    secondCols = secondBlock.columns
                    secondSize = secondBlock.shape[1]

                
                    corr_block = np.corrcoef(firstBlock.T, secondBlock.T)[:firstSize, firstSize:].astype(np.float32)

                    lines = []  # lista per accumulare le righe del blocco

                    for a in range(firstSize):
                        b_start = a + 1 if i == j else 0

                        for b in range(b_start, secondSize):
                            val = corr_block[a, b]
                            if threshold is None or abs(val) > threshold:
                                # accumula la riga nel blocco
                                lines.append(f"{firstCols[a]}\t{secondCols[b]}\t{val:.7f}\n")
                                if len(lines) >= MAX_BUFFER_LINES:
                                    f.writelines(lines)
                                    lines = []
                    if lines:
                        f.writelines(lines)
