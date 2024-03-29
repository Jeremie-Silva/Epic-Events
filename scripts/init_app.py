from configparser import ConfigParser


def retrieve_permissions(role_name: str) -> list[str]:
    config = ConfigParser()
    config.read("config.ini")
    permissions = config["permissions"].get(role_name)
    return permissions.replace("\n", " ").strip().split(", ")


"""
sudo apt install postgresql
sudo -u postgres psql
CREATE DATABASE epic_events;
CREATE USER admin WITH ENCRYPTED PASSWORD '';
GRANT ALL PRIVILEGES ON DATABASE epic_events TO admin;
"""