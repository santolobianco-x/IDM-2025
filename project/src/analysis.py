import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class CorrelationAnalyzer:
    def __init__(self, tumor_name, df_raw, df_ae=None, df_pca=None):
        self.tumor = tumor_name
        self.df_raw = df_raw
        self.df_ae = df_ae
        self.df_pca = df_pca
        
        # Prepariamo i dati appena la classe viene istanziata
        self._prepare_data()

    def _prepare_data(self):
        """Crea la colonna 'pair' univoca per i confronti"""
        print(f"Indicizzazione coppie per {self.tumor}...")
        
        # Funzione helper per creare la chiave ordinata
        def create_pair_key(row):
            return "_".join(sorted([str(row['GeneA']), str(row['GeneB'])]))

        if self.df_raw is not None and not self.df_raw.empty:
            self.df_raw['pair'] = self.df_raw.apply(create_pair_key, axis=1)
        
        if self.df_ae is not None and not self.df_ae.empty:
            self.df_ae['pair'] = self.df_ae.apply(create_pair_key, axis=1)
            
        if self.df_pca is not None and not self.df_pca.empty:
            self.df_pca['pair'] = self.df_pca.apply(create_pair_key, axis=1)

    def print_jaccard_overlap(self):
        """Calcola e stampa l'indice di Jaccard"""
        if self.df_raw is None: return

        set_raw = set(self.df_raw['pair'])
        
        print(f"\n--- Analisi Sovrapposizione (Jaccard) - {self.tumor} ---")

        # Confronto RAW vs AE
        if self.df_ae is not None:
            set_ae = set(self.df_ae['pair'])
            intersection = len(set_raw.intersection(set_ae))
            union = len(set_raw.union(set_ae))
            jaccard = intersection / union if union > 0 else 0
            print(f"RAW vs AE:  {jaccard:.4f} (Coppie comuni: {intersection})")

        # Confronto RAW vs PCA
        if self.df_pca is not None:
            set_pca = set(self.df_pca['pair'])
            intersection = len(set_raw.intersection(set_pca))
            union = len(set_raw.union(set_pca))
            jaccard = intersection / union if union > 0 else 0
            print(f"RAW vs PCA: {jaccard:.4f} (Coppie comuni: {intersection})")

    def plot_scatter(self, save_dir="data/results"):
        """Genera i grafici a dispersione"""
        if self.df_raw is None: return

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # --- Plot AE ---
        if self.df_ae is not None:
            merged = pd.merge(self.df_raw, self.df_ae, on="pair", suffixes=('_raw', '_ae'))
            plot_data = merged.sample(20000) if len(merged) > 20000 else merged
            
            sns.scatterplot(ax=axes[0], x=plot_data['Correlation_raw'], y=plot_data['Correlation_ae'], 
                            alpha=0.2, s=15, color='blue')
            
            # --- MODIFICA QUI ---
            axes[0].plot([-1, 1], [-1, 1], 'r--') 
            axes[0].set_xlim(-1, 1)  # Forza asse X da -1 a 1
            axes[0].set_ylim(-1, 1)  # Forza asse Y da -1 a 1
            axes[0].axhline(0, color='black', linewidth=0.5) # Linea centrale
            axes[0].axvline(0, color='black', linewidth=0.5) # Linea centrale
            # --------------------
            
            axes[0].set_title(f"RAW vs AE (n={len(merged)})")

        # --- Plot PCA ---
        if self.df_pca is not None:
            merged = pd.merge(self.df_raw, self.df_pca, on="pair", suffixes=('_raw', '_pca'))
            plot_data = merged.sample(20000) if len(merged) > 20000 else merged
            
            sns.scatterplot(ax=axes[1], x=plot_data['Correlation_raw'], y=plot_data['Correlation_pca'], 
                            alpha=0.2, s=15, color='green')
            
            # --- MODIFICA QUI ---
            axes[1].plot([-1, 1], [-1, 1], 'r--')
            axes[1].set_xlim(-1, 1)
            axes[1].set_ylim(-1, 1)
            axes[1].axhline(0, color='black', linewidth=0.5)
            axes[1].axvline(0, color='black', linewidth=0.5)
            # --------------------

            axes[1].set_title(f"RAW vs PCA (n={len(merged)})")

        plt.suptitle(f"Analisi Correlazione: {self.tumor}")
        # ... resto del codice ...
        plt.tight_layout()
        
        # Salva il plot
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        plt.savefig(os.path.join(save_dir, f"{self.tumor}_scatter_analysis.png"))
        plt.close()
        print(f"Grafico salvato per {self.tumor}")





        