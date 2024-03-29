from configparser import ConfigParser
from sqlalchemy import create_engine, Engine, Column
from sqlalchemy.orm import sessionmaker, Session, declarative_base

config = ConfigParser()
config.read("config.ini")
db_config = config["database"]

DATABASE_URI = f"postgresql+psycopg2://{db_config["user"]}:{db_config["password"]}"\
    f"@{db_config["host"]}/{db_config["name"]}"

db: Engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

Base = declarative_base()


# def get_obj_in_db(model: any, value: any, column_name="id") -> any:
#     session: Session = SessionLocal()
#     column: Column = model.__table__.columns[column_name]
#     obj = session.query(model).filter(column == value).first()
#     session.close()
#     return obj
#
#
# def get_list_in_db(model: any):
#     session: Session = SessionLocal()
#     objects = session.query(model).all()
#     session.close()
#     return objects
