# Progetto Data Mining - AUTOENCODER SU PROFILI DI ESPRESSIONE PER CALCOLO DELLE CORRELAZIONI TRA GENI.

## Analisi delle Correlazioni Geniche tramite Autoencoder e PCA

Il dataset impiegato per l'analisi proviene dal database **TCGA (The Cancer Genome Atlas)** e comprende profili di espressione RNA-Seq (STAR-FPKM) relativi a diverse tipologie di tumori:

* **TCGA-BRCA** (Mammella)
* **TCGA-COAD** (Colon)
* **TCGA-LUAD** (Polmone)
* **TCGA-OV** (Ovaio)
* **TCGA-PAAD** (Pancreas)
* **TCGA-PRAD** (Prostata)

L'obiettivo è l'analisi delle correlazioni tra geni su più livelli:

* **Mappatura e Preprocessing** dei dati genomici;
* **Riduzione lineare** della dimensionalità tramite PCA;
* **Riduzione non lineare** tramite Autoencoder (Deep Learning);
* **Analisi comparativa** della conservazione della topologia e degli Hub Genes.

Durante la stesura del codice si è seguito un approccio di **programmazione orientata agli oggetti (OOP)**. Il file **main.py** funge da orchestratore per istanziare gli oggetti e richiamarne i relativi metodi, garantendo modularità e riusabilità.

---

### 1 pathmanager.py

* **Responsabilità:** Gestione centralizzata dei percorsi di input/output.
* **Metodi principali:**
* `__init__`: Crea automaticamente la struttura delle cartelle (`data/raw`, `results`, `ae`, `pca`).
* `rawfile` / `processedfile`: Genera i path per i file grezzi e processati.
* `correlationfiles`: Gestisce i path per i risultati delle matrici di correlazione basate sulla soglia impostata.



### 2 mapper.py

* **Classe:** `Mapper`
* **Metodi:**
* `__init__`: Carica il file di mappatura `gene_mapping.tsv` e crea un dizionario di lookup.
* `map`: Converte una lista di **Ensembl ID** nei rispettivi **Gene Symbols** (es. da ENSG00000141510 a TP53).



### 3 preprocessing.py

* **Classe:** `Preprocessor`
* **Metodi:**
* `preprocess`: Coordina l'intera pipeline di pulizia.
* `_traspose_matrix`: Inverte la matrice per avere i pazienti come righe e i geni come colonne (formato standard per ML).
* `_filter_constant_genes`: Rimuove i geni che non presentano varianza (inutili per la correlazione).
* `_normalize`: Applica lo `StandardScaler` per portare i dati di espressione su una scala comune.



### 4 dataset.py

* **Classe:** `Dataset`
* **Metodi:**
* `prepare`: Verifica se esiste già una versione processata del dataset; in caso contrario, avvia la generazione tramite Mapper e Preprocessor.
* `_generate_processed`: Gestisce il caricamento del file TSV, la rimozione delle versioni degli ID (suffissi post-punto) e la gestione dei duplicati.



### 5 pca.py

* **Classe:** `PCA_reducer`
* **Metodi:**
* `getMatrixReduced`: Carica o calcola la matrice ridotta linearmente.
* `_apply_pca`: Implementa la **PCA** di Scikit-learn, impostando il numero di componenti in base alla varianza spiegata desiderata (es. 90%).



### 6 aenetwork.py / autoencoder.py

* **Classe:** `AENetwork` (PyTorch) & `Autoencoder` (Wrapper)
* **Descrizione:** Definisce l'architettura della rete neurale (Encoder/Decoder).
* **Metodi:**
* `fit`: Addestra la rete neurale per minimizzare l'errore di ricostruzione (MSELoss) utilizzando l'ottimizzatore Adam.
* `encode` / `transform`: Estrae lo spazio latente (le **30 dimensioni** compresse) dal dataset originale.



### 7 autoencoder_reducer.py

* **Classe:** `Autoencoder_Reducer`
* **Metodi:**
* **`__init__`**: costruttore della classe, inizializza il percorso di salvataggio, il dataset originale e i parametri della rete (dimensione latente fissata a **30**, epoche e batch size);
* **`getMatrixReduced`**: metodo principale che verifica la presenza di una matrice già ridotta su disco. Se non presente, avvia il processo di generazione richiamando `_apply_autoencoder`;
* **`_apply_autoencoder`**: metodo che:
    * Istanzia la classe `Autoencoder` con la corretta dimensione di input
    * Esegue il **fit** (addestramento) del modello sui dati di espressione;
    * Applica la funzione **transform** per proiettare i dati nello spazio latente;
    * Converte il risultato in un DataFrame indicizzato e lo salva in formato TSV per utilizzi futuri.

### 8 correlation.py

* **Classe:** `Correlation`
* **Metodi:**
* `chunked_correlation`: Calcola la correlazione di Pearson per ogni coppia di geni. Per gestire l'elevato carico computazionale, il calcolo avviene a **blocchi (chunk)**, salvando su file solo i valori che superano una determinata **soglia (threshold)**.
* `getCorrelationMatrix`: Metodo di accesso principale che restituisce il DataFrame delle coppie correlate.



### 9 analysis.py


* **Classe:** `CorrelationAnalyzer`
* **Metodi della classe:**
* **`__init__`**: costruttore della classe, utilizzato per inizializzare il nome del tumore e le tre matrici di correlazione (Raw, Autoencoder e PCA). Al termine dell'inizializzazione richiama automaticamente `_prepare_data`;
* **`_prepare_data`**: metodo interno che si occupa dell'indicizzazione delle coppie di geni. Crea una colonna univoca **'pair'** (ottenuta concatenando *GeneA* e *GeneB*) per permettere il confronto diretto tra le diverse matrici tramite operazioni di merge;
* **`run_full_analysis`**: orchestratore principale che esegue l'intera pipeline di analisi statistica e visualizzazione, richiamando in sequenza i metodi per i grafici di distribuzione, il calcolo delle metriche e l'analisi degli Hub Genes;
* **`_plot_distributions`**: genera un grafico di densità (**KDE Plot**) per confrontare le distribuzioni dei coefficienti di correlazione delle tre matrici, permettendo di analizzare come i modelli ridotti distribuiscono i pesi rispetto ai dati originali;
* **`_analyze_method`**: calcola e stampa a video le metriche quantitative di confronto:
* **`_plot_scatter`**: costruisce grafici a dispersione (**Scatter Plot**) campionando 20.000 coppie per visualizzare la fedeltà dei singoli valori di correlazione rispetto alla matrice originale;
* **`_get_top_hubs`**: metodo di supporto che identifica i geni con il maggior numero di connessioni elevate (>0.9), definendo i cosiddetti **Hub Genes** del network;
* **`_plot_hub_genes`**: produce istogrammi comparativi dei primi 5 Hub Genes identificati in ciascuna matrice, evidenziando quali geni regolatori sono stati preservati o enfatizzati dalle tecniche di riduzione.


---

### Requisiti

Per eseguire il progetto è necessario installare le seguenti librerie:
`pandas`, `numpy`, `torch`, `scikit-learn`, `matplotlib`, `seaborn`, `scipy`.
