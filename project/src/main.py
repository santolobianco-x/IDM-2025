from dataset import Dataset
from mapper import Mapper
from preprocessing import Preprocessor
from correlation import Correlation 
from pathmanager import PathManager



tumors = ["TCGA-BRCA","TCGA-COAD","TCGA-LUAD", "TCGA-OV", "TCGA-PAAD", "TCGA-PRAD"]
mapper = Mapper("gene_mapping.tsv")


pathm = PathManager()
rawpaths = pathm.rawfiles(tumors)
procpaths = pathm.processedfiles(tumors)


datasets = {}
available_tumors = []

for t,rawpath, procpath in zip(tumors,rawpaths,procpaths):
    try:
        dataset = Dataset(rawpath,procpath).prepare(mapper)
        datasets[t] = dataset
        available_tumors.append(t)
    except FileNotFoundError as e:
        print(f"{e}")
        continue


tumors = available_tumors


if len(tumors) == 0:
    print("No tumor dataset available")
    exit(1)


preproc = Preprocessor()
for t in tumors:
    datasets[t] = preproc.preprocess(datasets[t])
    print(t)
    print(datasets[t].head(2))
    print(datasets[t].shape)




threshold = 0.90
corrfiles = pathm.correlationfiles(tumors,threshold=threshold)

for t, outputfile in zip(tumors, corrfiles):
    try:
        correlator = Correlation(datasets[t])
        correlator.chunked_correlation(output_path=outputfile,chunk_size=2500,threshold=threshold)
    except FileExistsError as e:
        print(e)


