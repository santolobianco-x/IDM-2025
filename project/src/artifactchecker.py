import numpy as np
import pandas as pd


class ArtifactChecker:

    def __init__(self, corr_data, dataset, epsilon=0.2, name=""):
        self.corr_data = corr_data
        self.dataset = dataset
        self.epsilon = epsilon
        self.name = name

    def run(self):
        df = self.corr_data[["GeneA", "GeneB", "Correlation"]].copy()
        if df.empty:
            return df

        X = np.asarray(self.dataset.values, dtype=np.float32, order="C")
        

    
        mean = X.mean(axis=0, keepdims=True)
        std = X.std(axis=0, keepdims=True, ddof=1)
        std[std == 0] = 1e-9
        X = (X - mean) / std

        idxgene = {g: i for i, g in enumerate(self.dataset.columns)}
        idx_a = df["GeneA"].map(idxgene).to_numpy(np.int32)
        idx_b = df["GeneB"].map(idxgene).to_numpy(np.int32)

        valid = (idx_a >= 0) & (idx_b >= 0)
        df = df[valid].reset_index(drop=True)
        idx_a = idx_a[valid]
        idx_b = idx_b[valid]

        n_pairs = len(df)
        batch_size = 200_000
        corr_orig = np.empty(n_pairs, dtype=np.float32)

        for start in range(0, n_pairs, batch_size):
            end = min(start + batch_size, n_pairs)
            a = idx_a[start:end]
            b = idx_b[start:end]

            Xa = X[:, a]
            Xb = X[:, b]
        
        
            numerator = np.einsum('ij,ij->j', Xa, Xb)
            denominator = np.sqrt( np.einsum('ij,ij->j', Xa, Xa) * np.einsum('ij,ij->j', Xb, Xb) + 1e-9)
            corr_orig[start:end] = numerator / denominator

        df["Corr_Original"] = corr_orig
        diff = np.abs(df["Correlation"].to_numpy(np.float32) - corr_orig)
        df["Diff"] = diff
        df["Artifact"] = diff > self.epsilon    

        self._print_summary(df)
        return df

    def _print_summary(self, df):
        total = len(df)
        artifacts = int(df["Artifact"].sum())
        print(f"\n[{self.name}] Artifact Summary:")
        print(f"  Total pairs: {total}")
        print(f"  Artifacts:   {artifacts} ({100*artifacts/total:.2f}%)")
