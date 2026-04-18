# Export De La Base De Données Courante

Ce dossier contient un export de la base actuelle afin qu'un collègue puisse repeupler une base vide avec les données existantes.

## Fichiers Générés

- [restore-current-db.sh](/home/darunbc/OpenGRC/docs/database-seed/restore-current-db.sh)
  - Script unique de restauration
  - Supporte `full`, `data-only` et `fixture`
  - Permet à ton collègue de restaurer la base sans reconstituer manuellement les commandes

- [opengrc-current-full.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-full.sql)
  - Dump PostgreSQL complet
  - Contient le schéma et les données
  - C'est l'option recommandée si le but est de reconstruire une base Docker/PostgreSQL identique

- [opengrc-current-data.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-data.sql)
  - Dump PostgreSQL `data-only`
  - À utiliser seulement si le schéma existe déjà
  - Attention : PostgreSQL a signalé des contraintes circulaires sur certains objets, donc cette voie est moins sûre que le dump complet

- [opengrc-current-data.json](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-data.json)
  - Fixture Django JSON
  - Utile si le collègue veut :
    - lancer les migrations
    - puis injecter les données via `loaddata`

- [opengrc-reset-sequences.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-reset-sequences.sql)
  - Reset des séquences PostgreSQL
  - À utiliser après `loaddata` si la voie fixture Django est choisie

- [opengrc-current-data.counts.txt](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-data.counts.txt)
  - Inventaire du nombre d'enregistrements par modèle
  - Permet de vérifier rapidement que la restauration est cohérente

## Recommandation

### Option recommandée

Utiliser :

- [restore-current-db.sh](/home/darunbc/OpenGRC/docs/database-seed/restore-current-db.sh)
- puis en mode `full`
- ou directement [opengrc-current-full.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-full.sql)

Commande :

```bash
docs/database-seed/restore-current-db.sh full
```

ou :

- [opengrc-current-full.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-full.sql)

Pourquoi :

- c'est le chemin le plus simple pour ton collègue s'il build une image Docker/PostgreSQL avec une base déjà remplie
- il évite les problèmes de séquences
- il évite les problèmes potentiels liés aux contraintes circulaires du dump `data-only`

## Option 1 : Restauration PostgreSQL Complète

### Cas d'usage

À utiliser si le collègue veut recréer une base complète à partir du dump actuel.

### Commande simple

```bash
psql -h 127.0.0.1 -U relief_user -d relief_db -f docs/database-seed/opengrc-current-full.sql
```

### Avec le script unique

```bash
docs/database-seed/restore-current-db.sh full
```

### Cas Docker

Si ton collègue utilise l'image officielle PostgreSQL, il peut copier ce fichier dans :

```text
/docker-entrypoint-initdb.d/01-opengrc-current-full.sql
```

Alors PostgreSQL l'exécutera automatiquement lors de l'initialisation d'une base neuve.

### Important

Cette méthode est la plus pratique si :

- la base cible est vide
- l'objectif est d'obtenir un clone fidèle de la base actuelle

## Option 2 : Restauration `data-only`

### Cas d'usage

À utiliser si :

- le schéma existe déjà
- la base a déjà été migrée
- on veut juste réinjecter les données SQL

### Commande

```bash
psql -h 127.0.0.1 -U relief_user -d relief_db -f docs/database-seed/opengrc-current-data.sql
```

### Avec le script unique

```bash
docs/database-seed/restore-current-db.sh data-only
```

### Avertissement

PostgreSQL a remonté des avertissements sur des contraintes circulaires.

Donc :

- cette option est moins sûre que le dump complet
- elle n'est pas la voie recommandée pour ton collègue

## Option 3 : Restauration Via Django Fixture

### Cas d'usage

À utiliser si le collègue préfère :

1. créer une base vide
2. lancer les migrations Django
3. injecter les données applicatives

### Étapes

#### Option scriptée

```bash
docs/database-seed/restore-current-db.sh fixture
```

#### Option manuelle

##### 1. Lancer les migrations

```bash
cd backend
source .venv/bin/activate
DB_HOST=127.0.0.1 DB_PORT=5432 DB_NAME=relief_db DB_USER=relief_user DB_PASSWORD=relief_pass python manage.py migrate
```

##### 2. Charger la fixture

```bash
cd backend
source .venv/bin/activate
DB_HOST=127.0.0.1 DB_PORT=5432 DB_NAME=relief_db DB_USER=relief_user DB_PASSWORD=relief_pass python manage.py loaddata ../docs/database-seed/opengrc-current-data.json
```

##### 3. Réinitialiser les séquences

```bash
psql -h 127.0.0.1 -U relief_user -d relief_db -f docs/database-seed/opengrc-reset-sequences.sql
```

### Pourquoi faire le reset des séquences

Après `loaddata`, PostgreSQL peut garder des séquences en retard sur les IDs injectés.

Résultat possible sans reset :

- la création de nouveaux enregistrements peut échouer
- ou créer des conflits de clé primaire

## Vérification Après Restauration

Comparer les volumes restaurés avec :

- [opengrc-current-data.counts.txt](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-data.counts.txt)

Par exemple, tu dois retrouver notamment :

- `cybergrc.Stakeholder: 129`
- `cybergrc.CriticalInfrastructure: 60`
- `cybergrc.RiskRegisterEntry: 153`
- `cybergrc.GovernanceArtifact: 82`
- `cybergrc.AuditFramework: 41`
- `cybergrc.DeliverableMilestone: 62`

## Recommandation Finale Pour Ton Collègue

Si ton collègue est en charge :

- du Docker
- de PostgreSQL
- d'une image avec base déjà préremplie

alors il doit privilégier :

1. [opengrc-current-full.sql](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-full.sql)
2. puis seulement en plan B [opengrc-current-data.json](/home/darunbc/OpenGRC/docs/database-seed/opengrc-current-data.json)

Le dump complet est le plus robuste pour son cas.
