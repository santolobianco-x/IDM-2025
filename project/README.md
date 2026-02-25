# Progetto Data Mining - Analisi delle correlazioni geniche tramite Autoencoder e PCA

## Analisi delle Correlazioni Geniche tramite Autoencoder e PCA

Il dataset impiegato per l'analisi proviene dal database **TCGA** e comprende profili di espressione RNA-Seq (STAR-FPKM) relativi a diverse tipologie di tumori:

* **TCGA-BRCA** (Mammella)
* **TCGA-COAD** (Colon)
* **TCGA-LUAD** (Polmone)
* **TCGA-OV** (Ovaio)
* **TCGA-PAAD** (Pancreas)
* **TCGA-PRAD** (Prostata)

L'obiettivo è l'analisi delle correlazioni tra geni su più livelli:

* **Mappatura e Preprocessing** dei dati genomici;
* **Riduzione lineare** della dimensionalità tramite PCA;
* **Riduzione non lineare** tramite Autoencoder;
* **Analisi degli Artefatti**: identificazione delle coppie di geni la cui correlazione viene alterata dai processi di riduzione.

Durante la stesura del codice si è seguito un approccio di **programmazione orientata agli oggetti (OOP)**. Il file **main.py** funge da orchestratore per istanziare gli oggetti e richiamarne i relativi metodi, garantendo modularità e riusabilità.

---

### 1 pathmanager.py

* **Responsabilità:** Gestione centralizzata dei percorsi di input/output e creazione automatica delle directory.
* **Metodi principali:**
* `__init__`: Inizializza le directory per dati grezzi, processati, risultati, PCA e Autoencoder.
* `rawfile` / `processedfile`: Genera i path per i singoli file.
* `reducedfile_pca` / `reducedfile_ae`: Gestisce i path dei dataset a dimensionalità ridotta.
* `correlationfile` / `correlationfilepca` / `correlationfileae`: Gestisce i path per i risultati delle matrici di correlazione.



### 2 mapper.py

* **Classe:** `Mapper`
* **Metodi:**
* `__init__`: Carica il file di mappatura `gene_mapping.tsv` e crea un dizionario di lookup.
* `map`: Converte una lista di **Ensembl ID** nei rispettivi **Gene Symbols**.



### 3 preprocessing.py

* **Classe:** `Preprocessor`
* **Metodi:**
* `preprocess`: Coordina la pipeline di pulizia (trasposizione, filtraggio e normalizzazione).
* `_traspose_matrix`: Inverte la matrice per avere i pazienti come righe e i geni come colonne.
* `_filter_constant_genes`: Rimuove i geni che non presentano varianza (inutili per l'analisi).
* `_normalize`: Applica lo `StandardScaler` per normalizzare i dati di espressione.



### 4 dataset.py

* **Classe:** `Dataset`
* **Metodi:**
* `prepare`: Verifica l'esistenza di una versione processata del dataset; in caso contrario, avvia la generazione tramite `Mapper` e `Preprocessor`.
* `_generate_processed`: Carica il file TSV, pulisce gli ID Ensembl (rimozione versioni post-punto), gestisce i duplicati e salva il file processato.



### 5 pca.py

* **Classe:** `PCA_reducer`
* **Metodi:**
* `getMatrixReduced`: Carica o calcola la matrice ridotta linearmente.
* `_apply_pca`: Implementa la **PCA** di Scikit-learn, utilizzando una soglia di varianza spiegata (es. 90%) per determinare il numero di componenti.



### 6 aenetwork.py / autoencoder.py

* **Descrizione:** Implementazione della rete neurale tramite PyTorch per la riduzione non lineare.
* **AENetwork (Architettura):** Encoder e Decoder simmetrici con uno strato intermedio di **128 neuroni** e attivazioni **ReLU**.
* **Autoencoder (Wrapper):**
* `__init__`: Gestisce il rilevamento automatico del device (**CUDA**, **MPS** o **CPU**).
* `fit`: Addestra la rete per minimizzare l'errore di ricostruzione (**MSELoss**) usando l'ottimizzatore **Adam**.
* `transform`: Estrae lo spazio latente compresso.



### 7 autoencoder_reducer.py

* **Classe:** `Autoencoder_Reducer`
* **Metodi:**
* `getMatrixReduced`: Verifica la presenza della matrice ridotta su disco o ne avvia la generazione.
* `_apply_autoencoder`: Istanzia la classe `Autoencoder` (dimensione latente impostata a **45**), esegue l'addestramento e salva i risultati.



### 8 correlation.py

* **Classe:** `Correlation`
* **Metodi:**
* `getCorrelationMatrix`: Metodo principale che carica o calcola le correlazioni salvandole su file.
* `chunked_correlation`: Calcola la correlazione di Pearson a **blocchi (chunk)** per ottimizzare l'uso della memoria RAM, filtrando i risultati in base a soglie positive e negative (es. `> 0.8` o `< -0.5`).



### 9 artifactchecker.py 

* **Classe:** `ArtifactChecker`
* **Scopo:** Validazione dei risultati ridotti confrontandoli con i dati originali.
* **Metodi:**
* `run`: Calcola la correlazione originale per le coppie identificate nei modelli ridotti e calcola la differenza (**Diff**). Se la differenza supera una soglia **epsilon** (es. 0.15), la coppia è marcata come **Artefatto**.



### 10 analysis.py

* **Classe:** `CorrelationAnalyzer`
* **Metodi:**
* `run_full_analysis`: Esegue l'intera pipeline di analisi statistica e visualizzazione.
* `_analyze_method`: Calcola metriche quantitative come **Jaccard Index**, **RMSE** e la **Correlazione di Spearman** (basata sui ranghi) tra matrici originali e ridotte.
* `_plot_distributions`: Genera grafici di densità (**KDE Plot**) per confrontare le distribuzioni dei coefficienti di correlazione.
* `_plot_scatter`: Produce **Scatter Plot** bilanciati tra coppie reali e artefatti per visualizzare la fedeltà dei modelli rispetto ai dati originali.



---

### Requisiti

Per eseguire il progetto è necessario installare le seguenti librerie:
`pandas`, `numpy`, `torch`, `scikit-learn`, `matplotlib`, `seaborn`, `scipy`.