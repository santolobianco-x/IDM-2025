# IDM-2025
## First classwork - Data Mining Introduction
Il dataset impiegato per l'analisi è **AnonymizedFidelity**, ossia un insieme di dati che si riferisce agli articoli acquistati in un supermercato. L'obiettivo è l'analisi su più livelli:
* **analisi delle frequenze;**
* **stratificazione temporale;**
* **estrazione di regole di associazione;**
* **clustering su dati la cui dimensionalità è stata ridotta.**

I prodotti sono stati organizzati in una gerarchia composta da quattro livelli:
* **Livello 1: macro-categorie(descr_liv1)**
* **Livello 2: sotto-categorie(descr_liv2)**
* **Livello 3: categorie specifiche(descr_liv3)**
* **Livello 4: categorie nel dettaglio(descr_liv4)**

Durante la stesura del codice, su indicazione del professore, si è seguito un approccio di programmazione orientata agli oggetti. In particolare il file **main** si occupa di istanziare gli oggetti e di richiamarne i relativi **metodi**, mentre in ciascun file è contenuta una **classe specifica**.

Seguendo l'ordine di utilizzo delle varie classi descriviamo i file e il loro contenuto.


### 1 dataloader.py
- Import utilizzate: **pandas**.
- Classe: **Dataloader**
- Metodi della classe:
  * **__init__** costruttore della classe, utilizzato per inizializzare l’attributo **path** e conservarne una copia all’interno dell’oggetto, in modo da poter accedere successivamente al file da caricare;
  * **load** carica il file **path.csv** all'interno di un **dataframe**;
  * **printfirst** metodo che accetta un intero **occur**(default = 5) e che stampa i primi **occur** record del dataset;
  * **info** restituisce informazioni sulle feature del dataset, come tipologia e struttura dei dati.
 
 ### 2 preprocessing.py
 - Import utilizzate: **pandas**, **time(from datetime)**.
 - Classe: **Preprocessor**
 - Metodi della classe:
   * **__init__** costruttore della classe, utilizzato per inizializzare l'attributo **dataset** e conservarne una copia all'interno dell'oggetto, in moodo da lavorare su una copia del dataset;
   * **drop_col** al fine di allegerire la computazione in fase di analisi, rimuove un insieme di feature irrilevanti rispetto all'obiettivo prefissato. Queste feature rimosse sono: ***["db_id", "puntovendita_id", "cassa", "cassiere", "nummero_scontrino","num_riga", "r_peso", "r_iva", "r_sconto","tipologia", "descr_tipologia", "cod_rep", "descr_rep", "cat_mer"]***.
   * **removeshoppers** come richiesto, elemina dal dataset gli articoli con **descr_liv4 == 'shoppers'** in quanto irrilevanti per l'analisi;
   * **convertdatetime** converte le feature **data** e **ora** dal tipo **object** al tipo **datetime**, dopo aver rimosso eventuali valori mancanti. Questa conversione è necessaria per consentire successive operazioni di estrazione temporale;
   * **monthrange** (static method) assegna ciascuna data a una specifica fascia temporale mensile(*RANGE 1*, *RANGE 2*, *RANGE3*) sulla base del giorno e del mese;
   * **timetorange** (static method) suddivide la giornata in tre fasce orarie (**SLOT 1**, **SLOT 2**, **SLOT 3**) in base all'orario dell'acquisto;
   * **createslices** crea due feature derivate:
     - **fascia_mese**, ottenuta applicando *monthtorange*;
     - **fascia_oraria**, ottenuta applicando *timetorange*;
   * **getdataset** restituisce il dataset preprocessato pronto per le successive fasi di analisi.



### 3 frequencyanalisys.py
- Import utilizzate: **pandas**, **pyplot(from matplotlib)**
- Classe: **FrequencyAnalizer**
- Metodi della classe:
  * **__init__** costruttore della classe, utilizzato per inizializzare l'attributo **dataset** e conservare una copia all'interno dell'oggetto, in modo da lavorare su una copia del dataset;
  * **printplot (staticmethod)** metodo che accetta come parametri due **series** (5 elementi più frequenti e 5 elementi meno frequenti) e due **stringhe**(saranno utilizzate come titoli dei grafici). Sulla base delle **series** costruisce dei **barplot**;
  * **analyze** metodo utilizzato per calcolare la frequenza degli elementi nel dataset e per richiamare **printplot**.  Il metodo può essere invocato più volte per analizzare i diversi livelli gerarchici presenti nel dataset. **NB**: il metodo accetta delle stringhe in input al fine di poter essere riutilizzato sia per l’analisi complessiva sia per quella stratificata;
  * **analyzelevels** metodo che richiama **analyze** e passa come parametri due stringhe(titoli dei grafici);
  * **stratifiedlevels** metodo che istanzia un oggetto **FrequencyAnalyzer** e passa i subset per l'analisi stratificata. Sono presenti due costrutti **for** che permettono di partizionare il dataset in base alle variabili **month_range** e **time_slot**.



### 4 association.py
- Import utilizzate: **pandas**, **TransactionEncoder (from mlxtend.preprocessing)**, **apriori(from mlxtend.frequent_patterns), association_rules(from mlxtend.frequent_patterns), fpgrowth (from mlxtend.frequent_patterns)**
- Classe; **Association**
- Metodi della classe:
  * **__init__** costruttore della classe, utilizzato per inizializzare l'attributo **dataset** e conservarne una copia all'interno dell'oggetto. Vengono inoltre inizializzati gli attributi **transactions** e **rules**, che conterranno transazioni e regole di associazione;
  * **create_transaction** metodo che costruisce l'insieme delle transazioni a partire da dataset. Gli articoli rappresentati mediante la variabile *descr_liv4* vengono raggruppati per **scontrino_id**, ottenendo una lista di prodotti per ciascuna transazione;
  * **apriorirules** applica l'algoritmo **Apriori** per l'estrazione degli itemset frequenti e delle regole di associazione. Le transazini vengono prima trasformate in una rappresentazione binaria tramite **TransactionEncoder**. Successivamente vengono estratti gli itemset frequenti con una soglia **threshold** e imponendo una soglia minima di confidenza **confidence**;
  * **fpgrowthrules** applica l’algoritmo **FP-Growth** per l’estrazione degli itemset frequenti. Anche in questo caso, le regole di associazione vengono calcolate imponendo una soglia minima di **confidence**;
  * **showrules**: metodo che stampa a schermo le prime **n** regole di associazione estratte, mostrando per ciascuna regola gli attributi principali:  
    **antecedents**, **consequents**, **support**, **confidence** e **lift**.

### 5 clustering.py
- Import utilizzate: **pandas**, **PCA(frm sklearn.decomposition)**,**KMeans (from sklearn.cluster)**, **silhouette_score (from sklearn.metrics)**
- Classe: **Clustering**
- Metodi della classe:
  * **__init__**: costruttore della classe, utilizzato per inizializzare l’attributo **dataset** e conservarne una copia all’interno dell’oggetto. Vengono inoltre inizializzati gli attributi **matrix**, **matrixreduced** e **clusters**.
  * **preparematrix**: metodo che filtra il dataset mantenendo esclusivamente le righe in cui il campo **tessera** non è nullo.Successivamente costruisce una matrice in cui:
    - le righe rappresentano le **tessere**,
    - le colonne rappresentano i **prodotti (descr_liv4)**,
      
  * **reducedimensionality**: metodo che applica la **PCA** alla matrice per ridurne la dimensionalità. Il numero di componenti principali è specificato tramite il parametro **components**;
  * **elbow (staticmethod)**: metodo che implementa il **metodo del gomito** per la selezione del numero ottimale di cluster. Il metodo restituisce la variazione dell’inerzia tra cluster consecutivi;
  * **silhouette (staticmethod)**: metodo che calcola il **Silhouette Score** per diversi valori di *k*.Il metodo restituisce un dizionario che associa a ciascun valore di *k* il relativo punteggio di silhouette;
  * **clustering**: metodo che applica l’algoritmo **KMeans** sulla matrice a dimensionalità ridotta. Il numero di cluster può essere:
    - selezionato automaticamente tramite **elbow**,
    - selezionato automaticamente tramite **silhouette**,
    - oppure impostato manualmente tramite il parametro **k**.
