#Introduzione al Data Mining 2025

La cartella contiene i materiali sviluppati durante il corso, organizzati in:

- First classwork  
- Second classwork  
- Progetto  

Tutti i lavori seguono un approccio **object-oriented**, con `main` come orchestratore e classi modulari per le singole fasi della pipeline.

---

##First Classwork – Market Basket Analysis

**Dataset:** AnonymizedFidelity (transazioni di un supermercato)

**Attività principali:**

- preprocessing e creazione di variabili temporali
- analisi delle frequenze sui livelli gerarchici dei prodotti
- analisi stratificata per fascia oraria e mensile
- estrazione di regole di associazione:
  - Apriori  
  - FP-Growth
- clustering dei clienti dopo riduzione dimensionale con **PCA**

---

##Second Classwork – Classificazione clinica

**Dataset:** DAES (fogli ASD, GDD, Controlli)

**Pipeline:**

- caricamento dati multi-sheet
- preprocessing e codifica delle feature
- visualizzazione tramite **PCA**
- addestramento modelli di classificazione:
  - Decision Tree
  - Random Forest
  - SVM
  - K-NN
- tecniche di **ensemble learning**:
  - bagging
  - boosting

---

##Progetto – Correlazioni geniche con Autoencoder e PCA

**Dataset:** TCGA RNA-Seq (diversi tumori)

**Workflow:**

- preprocessing e normalizzazione dei dati genomici
- riduzione dimensionale:
  - **PCA** (lineare)  
  - **Autoencoder** (non lineare, PyTorch)
- calcolo delle correlazioni gene-gene a blocchi
- confronto tra dati originali e ridotti tramite:
  - Jaccard Index  
  - RMSE  
  - Spearman
- rilevamento degli **artefatti di correlazione**
- visualizzazione delle distribuzioni e scatter plot

---

Panoramica generale dei contenuti del corso e delle tecniche utilizzate.
