from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum, Boolean, event
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
from datetime import datetime
from passlib.hash import bcrypt
from email_validator import validate_email
from phonenumbers import parse, is_valid_number


Base = declarative_base()


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


class AbstractBaseModel:
    __abstract__ = True

    def convert_to_dict(self) -> dict:
        values = self.__dict__
        values.pop("_sa_instance_state", None)
        values.pop("password", None)
        return values


class Role(Base, AbstractBaseModel):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    permissions = relationship("Permission", backref="role")

    def __str__(self):
        return f"{self.name}"


class Permission(Base, AbstractBaseModel):
    __tablename__ = "permission"
    id = Column(Integer, primary_key=True, autoincrement=True)
    scope = Column(SQLEnum(Scope), default=Scope.me, nullable=False)
    action = Column(SQLEnum(Action), default=Action.read, nullable=False)
    entity = Column(SQLEnum(Entity), default=Entity.user, nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

    def __str__(self):
        return f"{self.name}"


class User(Base, AbstractBaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), default=1, nullable=False)
    role = relationship("Role", backref="users")

    def __str__(self):
        return f"User : {self.id} -> {self.name} ({self.role.name})"


class Customer(Base, AbstractBaseModel):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    salesman = relationship("User", backref="customers")
    salesman_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(255), index=True, nullable=False)
    email = Column(String(255))
    phone = Column(String(255))
    company_name = Column(String(255))
    creation_date = Column(DateTime, default=datetime.now())
    last_update = Column(DateTime, onupdate=datetime.now())

    def __str__(self):
        return f"Customer : {self.id} -> {self.name}"


@event.listens_for(Customer, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.last_update = datetime.now()


class Contract(Base, AbstractBaseModel):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer = relationship("Customer", backref="contracts")
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    salesman = relationship("User", backref="contracts")
    salesman_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount_total = Column(Integer)
    amount_outstanding = Column(Integer)
    creation_date = Column(DateTime, default=datetime.now())
    state = Column(SQLEnum(ContractState), default=ContractState.waiting, nullable=False)

    def __str__(self):
        return f"Contract : {self.id} -> {self.salesman_id} for {self.customer_id}"


class Event(Base, AbstractBaseModel):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
