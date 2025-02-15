# Frontend – Streamlit

Ce dossier contient tout le code de la **partie Frontend** basée sur [Streamlit](https://streamlit.io/).  
Deux interfaces principales sont proposées :

1. **Interface Patient** (`patient.py`) : permet de répondre à un questionnaire médical et de consulter l’espace post-consultation.
2. **Interface Médecin** (`doctor.py`) : propose une vue liste des patients avec un système de score/tri et la possibilité de générer des PDF.

## Table des matières
1. [Structure](#structure)
2. [Installation et lancement local (hors Docker)](#installation-et-lancement-local-hors-docker)
3. [Utilisation via Docker Compose](#utilisation-via-docker-compose)
4. [Aperçu des fonctionnalités](#aperçu-des-fonctionnalités)
5. [Navigation dans l’UI](#navigation-dans-lui)
6. [Variables d’environnement](#variables-denvironnement)
7. [Contribuer](#contribuer)

---

## Structure


```
frontend/
├── frontend.md              <-- Documentation spécifique au frontend
├── Dockerfile               <-- Dockerfile pour construire l'image du frontend
├── requirements.txt         <-- Dépendances Python (Streamlit, etc.)
├── main.py                  <-- Point d'entrée Streamlit (page d'accueil)
└── pages/
    ├── doctor.py            <-- Interface Médecin
    └── patient.py           <-- Interface Patient
```

---

## Installation et lancement local (hors Docker)

1. **Cloner le repo** et se rendre dans le dossier `frontend` :
   ```bash
   git clone https://github.com/votre-compte/doctogreed-hackathon.git
   cd doctogreed-hackathon/frontend
   
   ```

2.  **Créer un environnement virtuel** (optionnel) et l’activer :
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    
    ```
    
3.  **Installer les dépendances** :
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
4.  **Lancer Streamlit** :
    
    ```bash
    streamlit run main.py
    
    ```
    
    Par défaut, l’interface est accessible sur [http://localhost:8501](http://localhost:8501).
    

----------

## Utilisation via Docker Compose

L’orchestration se fait via le fichier `docker-compose.yaml` à la racine :

```bash
docker-compose up --build

```

-   Le service **frontend** est alors accessible sur [http://localhost:8501](http://localhost:8501).

---
## Aperçu des fonctionnalités

-   **Accueil** (`main.py`) :
    -   Interface stylisée (fond bleu) pour accueillir l’utilisateur.
-   **Interface Médecin** (`pages/doctor.py`) :
    -   Visualisation des patients et de leur score de santé.
    -   Génération et téléchargement de PDF via [fpdf](https://pyfpdf.github.io/fpdf2/).
    -   Possibilité de rédiger un diagnostic et de l’exporter en PDF.
-   **Interface Patient** (`pages/patient.py`) :
    -   Questionnaire médical (slider, questions booléennes, etc.).
    -   Possibilité de télécharger des rapports post-consultation.
    -   Section d’historique (ex. consultations antérieures, ordonnances).

---

## Navigation dans l’UI

-   **Barre latérale** : Permet de passer de l’**Accueil** au **Chatbot** (questionnaire) ou à l’**Espace post-consultation**.
-   **Onglets** dans la page Médecin :
    -   **Priorité des Patients** : liste classée par score.
    -   **Diagnostic & PDF** : rédiger un diagnostic ou générer des PDF.

----------

## Variables d’environnement

-   (Optionnel) Si vous souhaitez configurer des secrets ou credentials pour des appels API, vous pouvez utiliser [st.secrets](https://docs.streamlit.io/streamlit-cloud/configure-the-app-using-streamlit-secrets) ou des variables d’environnement.

----------

## Contribuer

Pour toute proposition d’amélioration ou de correction :

1.  Créez une **branche** dédiée (`feature/xxx` ou `fix/xxx`).
2.  Ouvrez une **Pull Request** pour discussion.
3.  Signalez toute anomalie via les **Issues**.

Pour plus d’informations sur la mise en place globale, consultez le README principal.

