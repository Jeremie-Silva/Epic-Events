from configparser import ConfigParser
from sqlalchemy import create_engine, Engine


config = ConfigParser()
config.read("config.ini")
db_config = config["database"]

DATABASE_URI = f"postgresql+psycopg2://{db_config["user"]}:{db_config["password"]}"\
    f"@{db_config["host"]}/{db_config["name"]}"

db: Engine = create_engine(DATABASE_URI)
# Base.metadata.create_all(engine)
