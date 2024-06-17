[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
# Epic-Events
---
### Pré-requis
Avoir un OS **Linux** avec **Python 3.11** installé  
<br/>

### Installation
Executer ces commandes dans un terminal **bash**
pour installer installer le projet
```bash
git clone git@github.com:Jeremie-Silva/Epic-Events.git
cd books_reviews
```
```bash
virtualenv -p3.11 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
<br/>

lancer l'application en local :
```bash
pipenv run start_api
google-chrome http://127.0.0.1:8000/
# dans un autre terminal :
pipenv run start_prefect
```
(remplacer google-chrome par le nom de votre navigateur)


<br/>

