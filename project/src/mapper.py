import pandas as pd

class Mapper:
    def __init__(self, mapping_file="gene_mapping.tsv"):
        df = pd.read_csv(mapping_file, sep="\t")
        self.mapping = dict(zip(df["ensembl_id"], df["gene_name"]))

    def map(self, ensembl_ids):
        return {
            gene_id: self.mapping.get(gene_id, gene_id)
            for gene_id in ensembl_ids
        }
