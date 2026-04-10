# OpenGRC aligned with EDEN

Application Django + React alignée sur les modules metier principaux de EDEN tout en conservant le design frontend existant.

## Ce qui a ete aligne

- Conservation du layout React existant, du menu, des composants CRUD et du style.
- Correction du routage frontend des modules.
- CRUD generique frontend pilote par les metadonnees DRF pour creation, modification et suppression.
- Ajout des ressources EDEN manquantes:
  - `org.sites`
  - `org.facilities`
  - `people.contacts`
  - `people.identities`
  - `projects.activities`
  - `projects.tasks`
- Ajout de validations metier minimales:
  - coherence organisation/personne
  - coherence organisation/projet
  - coherence projet/activite
  - controles sur les dates de validite et de fin
- Ajout de migrations manuelles pour ces ressources.
- Ajout d'un jeu de donnees de demonstration via `seed_demo`.

## Prerequis

### Option Docker

- Docker
- Docker Compose

### Option locale

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Redis

## Installation

### 1. Cloner et ouvrir le projet

```bash
cd /home/brice-mboule/Documents/qualisys/opengrc
```

### 2. Backend Django en local

Creer un environnement virtuel puis installer les dependances:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```

Configurer les variables d'environnement si necessaire. Les valeurs par defaut sont definies dans `backend/config/settings/base.py`.

### 3. Frontend React en local

```bash
cd frontend
npm install
```

## Configuration

Les principales variables backend:

- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `CHANNEL_REDIS_URL`
- `CORS_ALLOWED_ORIGINS`

Variable frontend utile:

- `VITE_API_URL`, par defaut `/api`

## Migrations

Les migrations ajoutees pour l'alignement EDEN:

- [backend/apps/org/migrations/0002_site_facility.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/org/migrations/0002_site_facility.py)
- [backend/apps/people/migrations/0002_contact_identity.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/people/migrations/0002_contact_identity.py)
- [backend/apps/projects/migrations/0002_activity_task.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/projects/migrations/0002_activity_task.py)

Execution:

```bash
cd backend
python manage.py migrate
python manage.py seed_rbac
python manage.py seed_demo
```

## Lancement

### Backend local

```bash
cd backend
python manage.py runserver
```

### Frontend local

```bash
cd frontend
npm run dev
```

### Avec Docker

```bash
docker compose up --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_rbac
docker compose exec backend python manage.py seed_demo
```

## Comptes et donnees de test

Commande:

```bash
python manage.py seed_demo
```

Compte cree:

- Email: `admin@eden.local`
- Mot de passe: `Password123!`

Donnees chargees:

- 1 organisation de demonstration
- 1 site
- 1 facility
- 1 personne
- 1 contact
- 1 piece d'identite
- 1 projet
- 1 activite
- 1 tache

## Parcours de test recommande

1. Se connecter avec `admin@eden.local`.
2. Ouvrir `Organizations`, verifier la liste et creer une nouvelle organisation.
3. Ouvrir `Sites`, creer un site puis modifier ses coordonnees.
4. Ouvrir `Facilities`, creer une facility rattachee a un site.
5. Ouvrir `People`, creer une personne.
6. Ouvrir `Contacts`, creer un contact lie a la personne.
7. Ouvrir `Identities`, creer une piece d'identite et verifier les dates.
8. Ouvrir `Projects`, creer un projet.
9. Ouvrir `Activities`, creer une activite pour le projet.
10. Ouvrir `Tasks`, creer une tache pour l'activite.

## Tests

Tests ajoutes:

- [backend/apps/org/tests/test_site_facility_api.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/org/tests/test_site_facility_api.py)
- [backend/apps/people/tests.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/people/tests.py)
- [backend/apps/projects/tests/test_activity_task_api.py](/home/brice-mboule/Documents/qualisys/opengrc/backend/apps/projects/tests/test_activity_task_api.py)

Execution:

```bash
cd backend
pytest
```

## Limitations de validation dans cet environnement

Dans l'environnement de travail courant, les dependances Python et frontend n'etaient pas installees. J'ai donc pu:

- compiler statiquement les modules Python modifies
- ecrire les migrations manuellement

Je n'ai pas pu executer ici:

- `python manage.py makemigrations`
- `python manage.py migrate`
- `pytest`
- `npm run build`

car `django` et `vite` n'etaient pas disponibles localement au moment de la verification.
