[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
# Epic-Events
---
### Pré-requis
Avoir un OS **Linux** avec **Python 3.11** installé et **Postgres 14**
<br/>
<br/>

### Installation
Executer ces commandes dans un terminal **bash**
pour installer installer le projet
```bash
git clone git@github.com:Jeremie-Silva/Epic-Events.git
cd Epic-Events
pipenv install
pipenv shell
```
<br/>

### Environnement
Vous devez créer un fichier `.env` à la racine du projet et y ajouter les variables suivantes 
(remplacer les valeurs entre accolades par ce que vous voulez) :
```bash
POSTGRES_USER={user}
POSTGRES_PASSWORD={password}
POSTGRES_DB={database}
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TOKEN_EXPIRY=4  # le temps de validité des tokens (en heures)
PREFECT_API_URL=http://127.0.0.1:4200/api
```
<br/>

### Initialisation
lancer l'application en local :
```bash
# Créer une base de données à partir de votre fichier .env
pipenv run init_database

# Créer un utilisateur avec le role admin
pipenv run create_admin

# Générer des fausses données si besoin
pipenv run generate_fake_data

pipenv run start_prefect  # dans un autre terminal
yes n | pipenv run flow_deploy
```
<br/>

### Lancement
lancer l'application en local :
```bash
pipenv run start_prefect

# Démarrer le server web pour utiliser l'API
pipenv run start_api  # dans un autre terminal

# Démarrer l'app en lignes de commandes
pipen run cli  # dans un autre terminal
```
