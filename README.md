pipenv install
pipenv shell
pipenv run python3.12 app.py 



sudo apt install pass
pass init [public username]
pass insert [word]
$(pass ldap)


add a config.ini and manage values
[database]
user = yourusername
password = yourpassword
host = localhost
name = mydatabase



sudo apt install postgresql
sudo -u postgres psql
CREATE DATABASE epic_events;
CREATE USER admin WITH ENCRYPTED PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE epic_events TO admin;
