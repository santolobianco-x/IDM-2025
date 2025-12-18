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
     - **fascia_oraria**, ottenuta applicando *timetorange*
   * **getdataset** restituisce il dataset preprocessato pronto per le successive fasi di analisi.



### 3 frequencyanalisys.py


