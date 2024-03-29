from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship, Session
from enum import Enum
from datetime import datetime
from passlib.hash import bcrypt
from email_validator import validate_email
from phonenumbers import parse, is_valid_number
from app.core.database import Base, SessionLocal
from scripts.init_app import retrieve_permissions


class InvalidData(Exception):
    pass


class AbstractBaseModel:
    __abstract__ = True

    @classmethod
    def create(cls, **kwargs):
        if "phone" in kwargs:
            cls.is_valid_phone_number(kwargs["phone"])
        if "password" in kwargs:
            kwargs["password"] = bcrypt.hash(kwargs["password"])
        if "email" in kwargs:
            cls.is_valid_email(kwargs["email"])
        return cls(**kwargs)

    @classmethod
    def is_valid_phone_number(cls, phone: str):
        if not is_valid_number(parse(phone)):
            raise InvalidData("Invalid phone number")

    @classmethod
    def is_valid_email(cls, email: str):
        if not validate_email(email):
            raise InvalidData("Invalid email")

    @classmethod
    def get_item(cls, **conditions) -> object | None:
        session: Session = SessionLocal()
        accumulated_query = session.query(cls)
        for field, value in conditions.items():
            accumulated_query = accumulated_query.filter(getattr(cls, field) == value)
        return accumulated_query.first()

    @classmethod
    def get_list(cls) -> list[object]:
        session: Session = SessionLocal()
        return session.query(cls).all()

    def convert_to_dict(self) -> dict:
        values = self.__dict__
        values.pop("_sa_instance_state", None)
        values.pop("password", None)
        return values


class Action(Enum):
    read = "read"
    create = "create"
    update = "update"
    delete = "delete"


class Scope(Enum):
    me = "me"
    linked = "linked"
    all = "all"


class Entity(Enum):
    role = "role"
    permission = "permission"
    user = "user"
    customer = "customer"
    contract = "contract"
    event = "event"


class ContractState(Enum):
    signed = "signed"
    waiting = "waiting"


class Role(Base, AbstractBaseModel):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    permissions = relationship("Permission", backref="role")

    @staticmethod
    def generate_roles():
        session: Session = SessionLocal()
        session.add(Role(name="admin"))
        session.add(Role(name="gestion"))
        session.add(Role(name="commercial"))
        session.add(Role(name="support"))
        session.commit()

    @staticmethod
    def add_permissions():
        session: Session = SessionLocal()
        for role in Role.get_list():
            match role.name:
                case "admin":
                    print(role.permissions)
                    print([a.name for a in role.permissions])
        session.commit()


class Permission(Base, AbstractBaseModel):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    scope = Column(SQLEnum(Scope), default=Scope.me, nullable=False)
    action = Column(SQLEnum(Action), default=Action.read, nullable=False)
    entity = Column(SQLEnum(Entity), default=Entity.user, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_allowed = Column(Boolean, default=False, nullable=False)

    def __str__(self):
        return f"{self.name}"

    @staticmethod
    def generate_permissions():
        session: Session = SessionLocal()
        for role in Role.get_list():
            role_permissions = retrieve_permissions(role.name)
            # print(role_permissions)
            for permission in role_permissions:
                session.add(
                    Permission(
                        name=permission,
                        action=getattr(Action, permission.split("_")[0]),
                        entity=getattr(Entity, permission.split("_")[1]),
                        scope=getattr(Scope, permission.split("_")[2]),
                        role_id=role.id,
                        is_allowed=True
                    )
                )
                session.commit()


class User(Base, AbstractBaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), default=1, nullable=False)
    role = relationship("Role", backref="users")
    # manage default value

    def __str__(self):
        return f"User : {self.id} -> {self.name}"


class Customer(Base, AbstractBaseModel):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    salesman = relationship("User", backref="customers")
    salesman_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255))
    phone = Column(String(255))
    company_name = Column(String(255))
    creation_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"Customer : {self.id} -> {self.name}"


class Contract(Base, AbstractBaseModel):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer = relationship("Customer", backref="contracts")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    salesman = relationship("User", backref="contracts")
    salesman_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_total = Column(Integer)
    amount_outstanding = Column(Integer)
    creation_date = Column(DateTime, default=datetime.now())
    state = Column(SQLEnum(ContractState), default=ContractState.waiting, nullable=False)

    def __str__(self):
        return f"Contract : {self.id} -> {self.salesman_id} for {self.customer_id}"


class Event(Base, AbstractBaseModel):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)
