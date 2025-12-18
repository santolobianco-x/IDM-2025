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
 
 ###



