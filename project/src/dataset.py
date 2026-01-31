import os
import pandas as pd


class Dataset:
    def __init__(self, raw_path, processed_path):
        self.raw_path = raw_path
        self.processed_path = processed_path
        self.df = None

    def prepare(self, mapper):
        if os.path.exists(self.processed_path):
            print(f"Processed dataset found: {self.processed_path}")
            self.df = pd.read_csv(self.processed_path, sep="\t", index_col=0)
        elif os.path.exists(self.raw_path):
            print(f"Dataset processed not found, generating: {self.processed_path}")
            self._generate_processed(mapper)
        else:
            raise FileNotFoundError(f"File raw not found: {self.raw_path}")
        
        return pd.DataFrame(self.df)
        
    def _generate_processed(self, mapper):
        self.df = pd.read_csv(self.raw_path, sep="\t")
        self.df = self.df.set_index("Ensembl_ID")

        self.df.index = self.df.index.str.split(".").str[0]


        mapping = mapper.map(self.df.index.tolist())
        self.df.index = [mapping.get(g,g) for g in self.df.index]


        self.df = self.df[~self.df.index.duplicated(keep="first")]

        self.df.to_csv(self.processed_path, sep="\t")



