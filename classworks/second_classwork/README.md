# IDM-2025

## Second classwork – Data Mining

Il dataset impiegato per il **Second Classwork** è il **Dataset DAES**, organizzato in tre fogli distinti (**ASD**, **GDD**, **Controlli**), ciascuno rappresentativo di una diversa classe clinica.

Le fasi che sono state sviluppate durante il classwork sono:

* **caricamento e gestione dei dati multi-sheet;**
* **preprocessing e pulizia del dataset;**
* **analisi esplorativa tramite PCA;**
* **addestramento e valutazione di modelli di classificazione;**
* **utilizzo di tecniche di ensemble (bagging e boosting).**

Durante la stesura del codice, su indicazione del professore, si è seguito un approccio di programmazione orientata agli oggetti. In particolare il file **main** si occupa di istanziare gli oggetti e di richiamarne i relativi metodi, mentre in ciascun file è contenuta una *classe specifica*.


Seguendo l’ordine di utilizzo delle varie classi, vengono descritti di seguito i file e il loro contenuto.

---

### 1 dataloader.py

* Import utilizzate: **pandas**, **numpy**.
* Classe: **DataLoader**
* Metodi della classe:

  * ****init****: costruttore della classe, utilizzato per inizializzare il percorso del file Excel (**path**) e l’attributo **sheets**;
  * **load**: carica il file Excel e memorizza tutti i fogli in un dizionario di **DataFrame**, stampando i nomi dei fogli caricati;
  * **get_sheet**: restituisce il **DataFrame** associato a un foglio specifico, gestendo eventuali errori di caricamento o nomi non validi;
  * **printfirstrow**: stampa le prime *occur* righe di un foglio specificato;
  * **printinfo**: stampa le informazioni strutturali del **DataFrame** (tipi delle feature e valori non nulli).



### 2 preprocessing.py

* Import utilizzate: **pandas**, **train_test_split (from sklearn.model_selection)**.

* Classe: **Preprocessor**

* Metodi della classe:

  * ****init****: costruttore che inizializza l’attributo **dataset** con una copia del DataFrame;
  * **rmrows**: rimuove dal dataset le osservazioni con **Età equivalente < 12 mesi**;
  * **rmcolumns**: rimuove un insieme di feature non rilevanti per l’analisi;
  * **encode**: codifica le feature categoriche binarie (ad esempio **Sesso**) tramite mapping numerico.

* Funzione esterna:

  * **splitdata**: suddivide il dataset in **training set** e **test set** utilizzando una suddivisione stratificata rispetto alla classe.



### 3 pcavisualizer.py

* Import utilizzate: **pandas**, **seaborn**, **matplotlib**, **PCA (from sklearn.decomposition)**, **StandardScaler (from sklearn.preprocessing)**.
* Classe: **PCAVisualizer**
* Metodi della classe:

  * ****init****: inizializza il numero di componenti principali, lo **StandardScaler** e l’oggetto **PCA**;
  * **reduce**: applica lo scaling alle feature e successivamente la **PCA** per ridurre la dimensionalità del dataset;
  * **plot**: visualizza i dati ridotti in uno spazio bidimensionale, colorando i punti in base alla classe di appartenenza;
  * **explainvariance**: restituisce il rapporto di varianza spiegata dalle componenti principali.



### 4 models.py

* Import utilizzate: **scikit-learn**.

* Classe: **Model**

* Funzionalità principali:

  * addestramento di diversi modelli di classificazione (**Decision Tree**, **Random Forest**, **SVC**, **K-NN**);
  * selezione automatica degli iperparametri;
  * valutazione delle prestazioni sul test set.

* Funzioni di ensemble:

  * **bagging_decisiontree**;
  * **boosting_decisiontree**;
  * **bagging_knn**;
  * **bagging_svc**.

Queste funzioni permettono di confrontare le prestazioni dei modelli base con tecniche di **ensemble learning**.


