from typing import TypeVar, Union
from sqlalchemy import create_engine, Engine, Column, update, and_
from sqlalchemy.orm import sessionmaker, Session, Query
from decouple import config
from app.core.models import Event, Contract, Customer, User, Permission, Role


DATABASE_URI = f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@"\
    f"{config('POSTGRES_HOST')}:{int(config('POSTGRES_PORT'))}/{config('POSTGRES_DB')}"

db_engine: Engine = create_engine(DATABASE_URI)
SessionLocal: Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


AnyModels: TypeVar = TypeVar(
    name="AnyModels",
    bound=Union[Role, Permission, User, Customer, Contract, Event]
)


class DBSessionManager:
    def __init__(self, session: Session = None) -> None:
        self.session = session or SessionLocal()

    def get_obj(self, model: AnyModels, join_filters={}, **filters) -> AnyModels | None:
        """exemple of join_filters needed"""
        query:  Query = self.session.query(model)
        for model_join, conditions in join_filters.items():
            for column_name, value in conditions.items():
                column: Column = model_join.__table__.columns[column_name]
                query = query.join(model_join).filter(column == value)
        for column_name, value in filters.items():
            column: Column = model.__table__.columns[column_name]
            query = query.filter(column == value)
        obj: AnyModels | None = query.first()
        self.session.close()
        return obj

    def get_all_objs(
        self,
        model: AnyModels,
        filters: dict = {},
        linked_model: AnyModels = User,
        linked_filters: dict = {},
    ) -> list[AnyModels]:
        conditions: list = []
        for column_name, value in filters.items():
            column: Column = model.__table__.columns[column_name]
            conditions.append(column == value)
        for column_name, value in linked_filters.items():
            column: Column = linked_model.__table__.columns[column_name]
            conditions.append(column == value)
        objs: list[AnyModels] = self.session.query(model).filter(and_(*conditions)).all()
        self.session.close()
        return objs

    def add_objs(self, *objs: list[AnyModels]) -> None:
        for obj in objs:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            self.session.close()

    def update_obj(self, model: AnyModels, data: dict, **kwargs) -> None:
        conditions: list = []
        for column_name, value in kwargs.items():
            column: Column = model.__table__.columns[column_name]
            conditions.append(column == value)
        self.session.execute(
            update(model).where(and_(*conditions)).values(data)
        )
        self.session.commit()
        self.session.close()

    def delete_obj(self, obj: AnyModels) -> None:
        self.session.delete(obj)
        self.session.commit()
        self.session.close()


db: DBSessionManager = DBSessionManager()
