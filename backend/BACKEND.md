
# Backend – FastAPI & Tortoise ORM

Ce dossier contient tout le code relatif au **backend**. L’API est construite avec [FastAPI](https://fastapi.tiangolo.com/), associée à [Tortoise ORM](https://tortoise-orm.readthedocs.io/) pour l’interaction avec PostgreSQL. Les conteneurs et la base de données sont gérés par Docker Compose.

## Table des matières
1. [Structure](#structure)
2. [Installation et lancement local (hors Docker)](#installation-et-lancement-local-hors-docker)
3. [Utilisation via Docker Compose](#utilisation-via-docker-compose)
4. [Endpoints principaux](#endpoints-principaux)
5. [Migration de schéma (Tortoise + Aerich)](#migration-de-schéma-tortoise--aerich)
6. [Variables d’environnement](#variables-denvironnement)
7. [Contribuer](#contribuer)

---

## Structure
```
backend/
├── backend.md               <-- Documentation spécifique au backend
├── Dockerfile               <-- Construction de l'image Docker du backend
├── requirements.txt         <-- Dépendances Python
└── app/
    ├── __init__.py
    ├── db_models.py         <-- Définition des modèles Tortoise
    ├── ds.py                <-- Intégration API Scaleway / OpenAI
    ├── enter_model.py       <-- Schémas Pydantic
    ├── main.py              <-- Point d'entrée FastAPI
    └── routes.py            <-- Routes définies via APIRouter
```

---

## Installation et lancement local (hors Docker)

Pour tester le backend rapidement en local (sans Docker) :

1. **Cloner le repo** et se rendre dans le dossier `backend` :
   ```bash
   git clone https://github.com/<votre-compte>/doctogreed-hackathon.git
   cd doctogreed-hackathon/backend
2.  **Créer un environnement virtuel** (optionnel, mais recommandé) :
    
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    ```
    
3.  **Installer les dépendances** :
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Configurer la connexion à la base de données** :
    
    Dans un environnement local, vous pouvez définir la variable `DATABASE_URL`, par exemple :
    
    ```bash
    export DATABASE_URL="postgres://user:password@localhost:5432/mydatabase"
    ```
    
    Assurez-vous d’avoir PostgreSQL installé et démarré.
    
5.  **Lancer l’application** :
    
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
    
    L’API sera disponible sur [http://localhost:8000](http://localhost:8000).
    

----------

## Utilisation via Docker Compose

Avec la configuration Docker Compose située à la racine du projet (`docker-compose.yaml`), il suffit de lancer :

```bash
docker-compose up --build
```

Le service **backend** écoute alors sur le port `8000`.  
Vous pouvez tester l’API via l’interface interactive : [http://localhost:8000/docs](http://localhost:8000/docs).

----------

## Endpoints principaux

La définition détaillée des endpoints se trouve dans le fichier `routes.py`. Quelques exemples :

-   **Créer un patient** :
    -   **Path** : `/create/patient/`
    -   **Méthode** : `POST`
    -   **Exemple de requête** :
        
        ```bash
        curl -X POST http://localhost:8000/create/patient/ \
        -H "Content-Type: application/json" \
        -d '{"nom": "Jean Dupont"}'
        ```
        
-   **Créer un docteur** :
    -   **Path** : `/create/docteur/`
    -   **Méthode** : `POST`
-   **Obtenir la liste de questions** :
    -   **Path** : `/diagnostic` (GET)
-   **Recevoir et stocker un diagnostic** :
    -   **Path** : `/recup-diagnostic/` (POST)
-   **Récupérer la liste des diagnostics** :
    -   **Path** : `/get_diagnostique/` (GET)

----------

## Migration de schéma (Tortoise + Aerich)

Le projet utilise [Tortoise ORM](https://tortoise-orm.readthedocs.io/) et peut exploiter [Aerich](https://github.com/tortoise/aerich) pour la gestion des migrations.

-   **Installation d’Aerich** (si ce n’est pas déjà dans `requirements.txt`) :
    
    ```bash
    pip install aerich
    ```
    
-   **Initialiser Aerich** :
    
    ```bash
    aerich init -t db_models  # Par exemple
    ```
    
-   **Générer une migration** :
    
    ```bash
    aerich migrate
    ```
    
-   **Appliquer la migration** :
    
    ```bash
    aerich upgrade
    ```
    

Note : Assurez-vous que la variable d’environnement `DATABASE_URL` soit correctement définie avant de lancer ces commandes.

----------

## Variables d’environnement

-   `DATABASE_URL` (obligatoire) : ex. `postgres://user:password@db:5432/mydatabase`
-   Autres variables éventuelles (API Key Scaleway / OpenAI, etc.) dans `ds.py`.

----------

## Contribuer

Les contributions sont bienvenues !

-   N’hésitez pas à ouvrir des **Issues** ou à soumettre des **Pull Requests**.
-   Pour des modifications majeures, merci de créer une branche dédiée.

Pour plus d’informations, reportez-vous à la documentation globale.
