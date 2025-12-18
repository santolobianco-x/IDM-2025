import pandas as pd
from matplotlib import pyplot as plt


class FrequencyAnalyzer:
    def __init__(self,data):
        self.database : pd.DataFrame = data


    @staticmethod
    def printplot(most,least,title1, title2):
        

        plt.figure(figsize=(10,6))
        plt.subplot(1,2,1)
        most.plot(kind='bar', title = title1)
        plt.xlabel("Element")
        plt.grid()
        plt.ylabel("Frequency")
        plt.xticks(rotation=25)

        plt.subplot(1,2,2)
        least.plot(kind='bar',title=title2)
        plt.xlabel("Element")
        plt.ylabel("Frequency")
        plt.grid()
        plt.xticks(rotation=25)

        plt.tight_layout()
        plt.show()


    def analyze(self,title1,title2):
        coltoanalyze =['descr_liv1','descr_liv2','descr_liv3','descr_liv4']
        i = 1
        for c in coltoanalyze:
            mostfive = self.database[c].value_counts().sort_values(ascending=False).head(5)
            leastfive = self.database[c].value_counts().sort_values(ascending=True).head(5)
            strlvl = f"- Level {i}"
            t1 = title1 + strlvl
            t2 = title2 + strlvl
            FrequencyAnalyzer.printplot(mostfive,leastfive,t1,t2)
            i = i+1


    def analyzelevels(self):
        title1 = f"Top 5 most frequent elements "
        title2 = f"Top 5 least frequent elements "
        self.analyze(title1,title2)



    def stratifiedlevels(self):
        month_range = ['RANGE 1','RANGE 2','RANGE 3']
        for r in month_range:
            subset = self.database[self.database['fascia_mese'] == r]
            title1 = f"Top 5 most frequent elements - {r} "
            title2 = f"Top 5 least frequent elements - {r}"
            fa = FrequencyAnalyzer(subset)
            fa.analyze(title1,title2)


        time_slot = ['SLOT 1','SLOT 2','SLOT 3']
        for s in time_slot:
            subset = self.database[self.database['fascia_oraria'] == s]
            title1 = f"Top 5 most frequent elements - {s} "
            title2 = f"Top 5 least frequent elements - {s}"
            fa = FrequencyAnalyzer(subset)
            fa.analyze(title1,title2)


