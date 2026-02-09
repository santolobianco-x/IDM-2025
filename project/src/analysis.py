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
        print(f"Indexing gene pairs for {self.tumor}...")
        
        
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

        self._plot_hub_genes(top_n=5)

        print(f"---Analysis completed for {self.tumor} ---\n")

    def _plot_distributions(self):
        plt.figure(figsize=(10, 6))
        
        sns.kdeplot(self.corr['Correlation'].dropna(), label='Raw Data', fill=True, alpha=0.3, color='blue')
        
        if self.corr_ae is not None:
            sns.kdeplot(self.corr_ae['Correlation'].dropna(), label='Autoencoder', fill=True, alpha=0.3, color='red')
            
        if self.corr_pca is not None:
            sns.kdeplot(self.corr_pca['Correlation'].dropna(), label='PCA', fill=True, alpha=0.3, color='green')
        
        plt.title(f"Distribution of Correlation Coefficients - {self.tumor}")
        plt.xlabel("Correlation Coefficient (Pearson)")
        plt.ylabel("Density")
        plt.legend()
        plt.xlim(-1, 1)
        plt.grid(alpha=0.25)
        plt.show()
        

    def _analyze_method(self, df_target, method_name):
        print(f"Comparing RAW vs {method_name}...")
        set_raw = set(self.corr['pair'])
        set_target = set(df_target['pair'])
        
        intersection = len(set_raw.intersection(set_target))
        union = len(set_raw.union(set_target))
        jaccard = intersection / union if union > 0 else 0
        
        print(f" -> Jaccard Index (Topological Similarity): {jaccard:.4f}")
        
        
        merged = pd.merge(self.corr, df_target, on='pair', suffixes=('_raw', f'_{method_name}'))
        
        if merged.empty:
            print(f"Warning: No common pairs found between RAW and {method_name} (check thresholds).")
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
        print(f" -> Common pairs analyzed: {len(merged)}")


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

        plt.suptitle(f"Correlation Analysis: {self.tumor}")
        plt.tight_layout()
        plt.show()

    def _get_top_hubs(self, df, top_n=5):
        if df is None or df.empty:
            return pd.Series(dtype=int)
        
        all_genes = pd.concat([df['GeneA'], df['GeneB']])
        return all_genes.value_counts().head(top_n)

    def _plot_hub_genes(self, top_n=5):
        
        _, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
        
        
        raw_hubs = self._get_top_hubs(self.corr, top_n)
        sns.barplot(ax=axes[0], x=raw_hubs.values, y=raw_hubs.index, hue=raw_hubs.index, palette='Blues_r', legend=False)
        axes[0].set_title(f"Top {top_n} Hubs - RAW")
        axes[0].set_xlabel("Numero di Connessioni (>0.9)")

        
        ae_hubs = self._get_top_hubs(self.corr_ae, top_n)
        sns.barplot(ax=axes[1], x=ae_hubs.values, y=ae_hubs.index, hue=ae_hubs.index, palette='Reds_r', legend=False)
        axes[1].set_title(f"Top {top_n} Hubs - Autoencoder")
        axes[1].set_xlabel("Numero di Connessioni (>0.9)")

        
        pca_hubs = self._get_top_hubs(self.corr_pca, top_n)
        sns.barplot(ax=axes[2], x=pca_hubs.values, y=pca_hubs.index, hue=pca_hubs.index, palette='Greens_r', legend=False)
        axes[2].set_title(f"Top {top_n} Hubs - PCA")
        axes[2].set_xlabel("Numero di Connessioni (>0.9)")

        plt.suptitle(f"Hub Gene Connectivity Analysis: {self.tumor}", fontsize=16)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()