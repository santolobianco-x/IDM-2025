import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

class CorrelationAnalyzer:
    def __init__(self, tumor_name, corr, corr_ae=None, corr_pca=None):
        
        self.tumor = tumor_name
        self.corr = corr
        self.corr_ae = corr_ae
        self.corr_pca = corr_pca

        self._prepare_data()

    def _prepare_data(self):
        print(f"Indicizzazione coppie per {self.tumor}...")
        
        
        if self.corr is not None and not self.corr.empty:
            self.corr['pair'] = self.corr['GeneA'] + "_" + self.corr['GeneB']
        
        if self.corr_ae is not None and not self.corr_ae.empty:
            self.corr_ae['pair'] = self.corr_ae['GeneA'] + "_" + self.corr_ae['GeneB']
            
        if self.corr_pca is not None and not self.corr_pca.empty:
            self.corr_pca['pair'] = self.corr_pca['GeneA'] + "_" + self.corr_pca['GeneB']

    def run_full_analysis(self): 
        self._plot_distributions()
        
        if self.corr_ae is not None:
            self._analyze_method(self.corr_ae, "AE")
        
        if self.corr_pca is not None:
            self._analyze_method(self.corr_pca, "PCA")

        self._plot_scatter()

        print(f"--- Analisi completata per {self.tumor} ---\n")

    def _plot_distributions(self):
        plt.figure(figsize=(10, 6))
        
        sns.kdeplot(self.corr['Correlation'].dropna(), label='Raw Data', fill=True, alpha=0.3, color='blue')
        
        if self.corr_ae is not None:
            sns.kdeplot(self.corr_ae['Correlation'].dropna(), label='Autoencoder', fill=True, alpha=0.3, color='red')
            
        if self.corr_pca is not None:
            sns.kdeplot(self.corr_pca['Correlation'].dropna(), label='PCA', fill=True, alpha=0.3, color='green')
        
        plt.title(f"Distribuzione dei Coefficienti di Correlazione - {self.tumor}")
        plt.xlabel("Coefficiente di Correlazione (Pearson)")
        plt.ylabel("Densità")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()
        

    def _analyze_method(self, df_target, method_name):
        print(f"Confronto ORIGINALE vs {method_name}...")
        set_raw = set(self.corr['pair'])
        set_target = set(df_target['pair'])
        
        intersection = len(set_raw.intersection(set_target))
        union = len(set_raw.union(set_target))
        jaccard = intersection / union if union > 0 else 0
        
        print(f"   -> Jaccard Index (Similarità Topologica): {jaccard:.4f}")
        
        
        merged = pd.merge(self.corr, df_target, on='pair', suffixes=('_raw', f'_{method_name}'))
        
        if merged.empty:
            print(f"Attenzione: Nessuna coppia in comune trovata tra RAW e {method_name} (controllare le soglie).")
            return

        x = merged['Correlation_raw']
        y = merged[f'Correlation_{method_name}']

        
        rmse = np.sqrt(np.mean((x - y)**2))
        

        if len(merged) > 100000:
            idx = np.random.choice(len(merged), 100000, replace=False)
            sp_corr, _ = spearmanr(x.iloc[idx], y.iloc[idx])
        else:
            sp_corr, _ = spearmanr(x, y)

        
        print(f"   -> RMSE: {rmse:.4f}")
        print(f"   -> Spearman Correlation: {sp_corr:.4f}")
        print(f"   -> Coppie comuni analizzate: {len(merged)}")


    def _plot_scatter(self):
        if self.corr is None: return

        _, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        
        if self.corr_ae is not None:
            merged = pd.merge(self.corr, self.corr_ae, on="pair", suffixes=('_raw', '_ae'))
            plot_data = merged.sample(20000) if len(merged) > 20000 else merged
            
            sns.scatterplot(ax=axes[0], x=plot_data['Correlation_raw'], y=plot_data['Correlation_ae'], 
                            alpha=0.2, s=15, color='blue')
            
            axes[0].plot([-1, 1], [-1, 1], 'r--') 
            axes[0].set_xlim(-1, 1)
            axes[0].set_ylim(-1, 1)
            axes[0].axhline(0, color='black', linewidth=0.5)
            axes[0].axvline(0, color='black', linewidth=0.5)
            
            axes[0].set_title(f"RAW vs AE (n={len(merged)})")

        
        if self.corr_pca is not None:
            merged = pd.merge(self.corr, self.corr_pca, on="pair", suffixes=('_raw', '_pca'))
            plot_data = merged.sample(20000) if len(merged) > 20000 else merged
            
            sns.scatterplot(ax=axes[1], x=plot_data['Correlation_raw'], y=plot_data['Correlation_pca'], 
                            alpha=0.2, s=15, color='green')
            
            axes[1].plot([-1, 1], [-1, 1], 'r--')
            axes[1].set_xlim(-1, 1)
            axes[1].set_ylim(-1, 1)
            axes[1].axhline(0, color='black', linewidth=0.5)
            axes[1].axvline(0, color='black', linewidth=0.5)

            axes[1].set_title(f"RAW vs PCA (n={len(merged)})")

        plt.suptitle(f"Analisi Correlazione: {self.tumor}")
        plt.tight_layout()
        plt.show()