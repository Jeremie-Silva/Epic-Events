from typing import TypeVar, Union, Any

from sqlalchemy import create_engine, Engine, Column, update, and_
from sqlalchemy.orm import sessionmaker, Session
from decouple import config

from app.core.models import Event, Contract, Customer, User, Permission, Role

DATABASE_URI = f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@"\
    f"{config('POSTGRES_HOST')}:{int(config('POSTGRES_PORT'))}/{config('POSTGRES_DB')}"

db: Engine = create_engine(DATABASE_URI)
SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=db)


AnyModels: TypeVar = TypeVar(
    name="AnyModels",
    bound=Union[Role, Permission, User, Customer, Contract, Event]
)


def get_obj_in_db(model: AnyModels, value: Any, column_name="id") -> AnyModels | None:
    session: Session = SessionLocal()
    column: Column = model.__table__.columns[column_name]
    obj: AnyModels | None = session.query(model).filter(column == value).first()
    session.close()
    return obj


def get_all_objs_in_db(model: AnyModels) -> list[AnyModels]:
    session: Session = SessionLocal()
    objs: list[AnyModels] = session.query(model).all()
    session.close()
    return objs


def add_obj_in_db(obj: AnyModels) -> None:
    session: Session = SessionLocal()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()


def update_obj_in_db(model: AnyModels, data: dict, **kwargs) -> None:
    session: Session = SessionLocal()
    conditions: list = []
    for column_name, value in kwargs.items():
        column: Column = model.__table__.columns[column_name]
        conditions.append(column == value)
    session.execute(
        update(model).where(and_(*conditions)).values(data)
    )
    session.commit()
    session.close()


def delete_obj_from_db(obj: AnyModels) -> None:
    session: Session = SessionLocal()
    session.delete(obj)
    session.commit()
    session.close()
