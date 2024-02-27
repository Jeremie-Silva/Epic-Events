from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
from datetime import datetime
from passlib.hash import bcrypt
from email_validator import validate_email
from phonenumbers import parse, is_valid_number


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


Base = declarative_base(cls=AbstractBaseModel)


class UserRole(Enum):
    gestion = "gestion"
    commercial = "commercial"
    support = "support"


class ContractState(Enum):
    signed = "signed"
    waiting = "waiting"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.gestion, nullable=False)

    def __str__(self):
        return f"User : {self.id} -> {self.name}"

    def verify_password(self, plain_password):
        return bcrypt.verify(plain_password, self.password)


class Customer(Base):
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


class Contract(Base):
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
