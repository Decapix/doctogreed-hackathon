
# DoctoGreed Hackathon – Infrastructure IA pour la cardiologie
Bienvenue dans ce projet de chatbot IA dédié à la cardiologie, conçu pour aider à la **pré-évaluation** des patients, la **génération de rapports médicaux structurés** et le **suivi post-consultation**. L’architecture globale est orchestrée via **Docker Compose**, et comprend :

- Un **backend** en [FastAPI](https://fastapi.tiangolo.com/) (Python) utilisant [Tortoise ORM](https://tortoise-orm.readthedocs.io/) pour la base de données **PostgreSQL**.
- Un **frontend** en [Streamlit](https://streamlit.io/) permettant l’interaction avec le patient (questionnaire, post-consultation) et avec le médecin (interface de suivi, génération de PDF, etc.).
- Une base de données **PostgreSQL** pour stocker les informations relatives aux patients, diagnostics et médecins.
## Table des matières
1. [Contexte : use case IA en cardiologie](#contexte--use-case-ia-en-cardiologie)
2. [Fonctionnalités principales](#fonctionnalités-principales)
3. [Structure du projet](#structure-du-projet)
4. [Prérequis](#prérequis)
5. [Comment lancer le projet ?](#comment-lancer-le-projet-)
6. [Contribution & Licence](#contribution--licence)

---  

## Contexte : use case IA en cardiologie
Ce projet répond à un besoin concret dans le domaine médical :
- **Pénurie de cardiologues** et répartition inégale de l’expertise.- **Triage non optimisé** des patients, sans évaluation médicale préalable.- **Perte de temps** en consultation (questions de base).- **Manque de suivi structuré** post-consultation.  
  **Objectif** : Un assistant IA qui prépare et optimise les consultations :- Pré-évalue le patient avant la prise de rendez-vous.
- Génère un rapport structuré des symptômes / historique médical.
- Aide le cardiologue à prioriser les cas les plus urgents.
- Assure un suivi post-consultation intelligent (rappels, alertes, etc.).

---  

## Fonctionnalités principales
1. **Triage des patients** : Analyse des réponses et priorisation des cas urgents.
2. **Consultation préliminaire** : Rassemble les informations importantes (symptômes, historique, traitements en cours).
3. **Suivi post-consultation** : Rappels de prise de médicament, vérification de l’évolution, alertes si aggravation.
4. **Génération de rapports** : Export PDF, affichage côté médecin, éventuellement notifications pour le patient.

--- 
## Structure du projet
```  
decapix-doctogreed-hackathon/  
├── README.md                <-- Vous êtes ici (présentation globale)  
├── docker-compose.yaml      <-- Configuration Docker Compose  
├── .dockerignore            <-- Fichiers ignorés par Docker  
├── backend/  
│   ├── backend.md           <-- Documentation spécifique au backend  
│   ├── Dockerfile           <-- Dockerfile du backend  
│   ├── requirements.txt     <-- Dépendances Python du backend  
│   └── app/  
│       ├── __init__.py  
│       ├── db_models.py  
│       ├── ds.py  
│       ├── enter_model.py  
│       ├── main.py  
│       └── routes.py  
└── frontend/  
    ├── frontend.md          <-- Documentation spécifique au frontend  
    ├── Dockerfile           <-- Dockerfile du frontend  
    ├── requirements.txt     <-- Dépendances Python du frontend  
    └── pages/  
    ├── doctor.py  
    └── patient.py  
```  
  
---  

## Prérequis

- [Docker](https://www.docker.com/) (version 20+ recommandée)
- [Docker Compose](https://docs.docker.com/compose/) (version 3.8+)
- (Optionnel) Connaissances basiques de **FastAPI**, **Streamlit** et **PostgreSQL** pour personnaliser l’application.

---  

## Comment lancer le projet ?

1. **Cloner le dépôt** :  
   ```bash 
   git clone https://github.com/<votre-compte>/doctogreed-hackathon.git 
   cd doctogreed-hackathon 
   ```
2. **(Facultatif) Mettre à jour les variables d’environnement** dans `docker-compose.yaml` si nécessaire (ex. `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.).

3. **Lancer Docker Compose** :  
   ``docker-compose up --build``

Cela va lancer :
- Le service **backend** sur le port `8000`
- Le service **frontend** sur le port `8501`
- Le service **db** (PostgreSQL) sur le port `5432`

4. **Accéder aux applications** :
    - **Backend** (FastAPI) : [http://localhost:8000/docs](http://localhost:8000/docs) pour la doc auto (Swagger).
    - **Frontend** (Streamlit) : [http://localhost:8501](http://localhost:8501) pour l’interface utilisateur.

5. **Vérifier la base de données** :
    - Par défaut, le container PostgreSQL est accessible sur le port `5432`.
    - Les identifiants (ex: `user / password`) sont définis dans `docker-compose.yaml`.

6. **Arrêter l’environnement** :  
   ``docker-compose down``
---  

## Contribution & Licence

- **Contributions** : Les PR, issues et suggestions sont les bienvenues.
- **Licence** : Ce projet est sous licence libre (à spécifier selon votre besoin : MIT, Apache 2.0, etc.).

Pour plus de détails, référez-vous aux README spécifiques :
- [BACKEND.md](./backend/BACKEND.md) dans le dossier `backend`.
- [FRONTEND.md](./frontend/FRONTEND.md) dans le dossier `frontend`.
