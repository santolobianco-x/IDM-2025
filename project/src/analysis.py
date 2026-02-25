import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from artifactchecker import ArtifactChecker
import gc


class CorrelationAnalyzer:

    def __init__(self, tumor, dataset, corr, corr_ae=None, corr_pca=None, epsilon=0.2):
        self.tumor = tumor
        self.dataset = dataset
        self.epsilon = epsilon

        print(f"[{self.tumor}] Indicizzazione coppie di geni in corso...")

        self.corr = self._prepare_df(corr)
        self.corr_ae = self._prepare_df(corr_ae)
        self.corr_pca = self._prepare_df(corr_pca)

        self.artifact_ae = None
        self.artifact_pca = None


    
    def _prepare_df(self, df):
        if df is None or df.empty:
            return None

        if not isinstance(df.index, pd.MultiIndex):
            df = df.drop_duplicates(subset=['GeneA', 'GeneB'])
            df = df.set_index(['GeneA', 'GeneB'])

        
        df = df[['Correlation']].astype(np.float32)

        return df.sort_index() 


   
    def _fast_spearman(self, x, y):
        rx = pd.Series(x).rank().values
        ry = pd.Series(y).rank().values
        return np.corrcoef(rx, ry)[0, 1]


    
    def _analyze_method(self, df_target, method_name):

        print(f"\n[Confronto RAW vs {method_name}]")

        idx_raw = self.corr.index
        idx_target = df_target.index

        
        intersection = idx_raw.isin(idx_target).sum()
        union = len(idx_raw) + len(idx_target) - intersection
        jaccard = intersection / union if union > 0 else 0

        print(f"Jaccard Index: {jaccard:.4f}")

        
        aligned = df_target.reindex(idx_raw).dropna()

        if aligned.empty:
            print("Nessuna coppia in comune.")
            return

        x = self.corr.loc[aligned.index, 'Correlation'].to_numpy()
        y = aligned['Correlation'].to_numpy()

        rmse = np.sqrt(np.mean((x - y) ** 2))

        if len(x) > 100000:
            idx = np.random.choice(len(x), 100000, replace=False)
            sp = self._fast_spearman(x[idx], y[idx])
        else:
            sp = self._fast_spearman(x, y)

        print(f"  -> RMSE: {rmse:.4f}")
        print(f"  -> Spearman: {sp:.4f}")
        print(f"  -> Coppie analizzate: {len(x)}")

        del aligned, x, y
        gc.collect()



    def _sample_series(self, s, n=200000):
        if len(s) <= n:
            return s
        return s.sample(n, random_state=0)

    def _plot_distributions(self):

        plt.figure(figsize=(10, 5))

        sns.kdeplot(self._sample_series(self.corr['Correlation']),
                    label='Raw', fill=True, alpha=0.2)

        if self.corr_ae is not None:
            sns.kdeplot(self._sample_series(self.corr_ae['Correlation']),
                        label='AE', fill=True, alpha=0.2)

        if self.corr_pca is not None:
            sns.kdeplot(self._sample_series(self.corr_pca['Correlation']),
                        label='PCA', fill=True, alpha=0.2)

        plt.xlim(-1, 1)
        plt.title(f"Distribuzione Correlazioni - {self.tumor}")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()


    
    def _balanced_sample(self, df, n_sample):

        art = df[df.Artifact]
        not_art = df[~df.Artifact]

        n_half = n_sample // 2

        return pd.concat([
            art.sample(min(len(art), n_half)),
            not_art.sample(min(len(not_art), n_half))
        ])
    
    
    
    def _plot_scatter(self):
        n = sum(x is not None for x in [self.artifact_ae, self.artifact_pca])
        if n == 0:
            return

        _, axes = plt.subplots(1, n, figsize=(7 * n, 6), squeeze=False)
        idx = 0

        if self.artifact_ae is not None:
            self._scatter_panel(axes[0, idx], self.artifact_ae, "AE", "steelblue")
            idx += 1

        if self.artifact_pca is not None:
            self._scatter_panel(axes[0, idx], self.artifact_pca, "PCA", "forestgreen")

        plt.suptitle(f"Analisi Artefatti: {self.tumor}", fontsize=14)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()


    def _scatter_panel(self, ax, artifact_df, label, color_ok, n_sample=20000):

        if artifact_df is None or artifact_df.empty:
            ax.set_axis_off()
            return

        sample = self._balanced_sample(artifact_df, n_sample)

        sns.scatterplot(
            data=sample,
            x="Corr_Original",
            y="Corr_Reduced" if "Corr_Reduced" in sample else "Correlation",
            hue="Artifact",
            palette={True: "red", False: color_ok},
            s=10,
            alpha=0.5,
            edgecolor=None,
            ax=ax
        )

        art_pct = (artifact_df['Artifact'].sum() / len(artifact_df)) * 100

        ax.plot([-1, 1], [-1, 1], 'r--', alpha=0.5)
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_title(f"RAW vs {label}\nArtefatti: {art_pct:.2f}%")
        ax.grid(alpha=0.2)



    def run_full_analysis(self):

        self._plot_distributions()

        if self.corr_ae is not None:
            self._analyze_method(self.corr_ae, "AE")

            corr_ae_reset = self.corr_ae.reset_index()

            checker = ArtifactChecker(
                corr_data=corr_ae_reset,
                dataset=self.dataset,
                epsilon=self.epsilon,
                name=f"{self.tumor}_AE"
            )

            self.artifact_ae = checker.run()

            del corr_ae_reset
            gc.collect()


        if self.corr_pca is not None:
            self._analyze_method(self.corr_pca, "PCA")

            corr_pca_reset = self.corr_pca.reset_index()

            checker = ArtifactChecker(
                corr_data=corr_pca_reset,
                dataset=self.dataset,
                epsilon=self.epsilon,
                name=f"{self.tumor}_PCA"
            )

            self.artifact_pca = checker.run()

            del corr_pca_reset
            gc.collect()

        self._plot_scatter()

        print(f"\n--- Analisi completata per {self.tumor} ---\n")
        gc.collect()