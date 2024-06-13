from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum, Boolean, event, Float
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum
from datetime import datetime
from passlib.hash import bcrypt
from email_validator import validate_email
from phonenumbers import parse, is_valid_number


Base = declarative_base()


class ContractState(Enum):
    signed = "signed"
    waiting = "waiting"


class Role(Enum):
    admin = "admin"
    support = "support"
    commercial = "commercial"
    gestion = "gestion"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), default=Role.commercial, nullable=False, index=True)
    creation_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)

    def __str__(self):
        return f"User : {self.id} -> {self.name} ({self.role})"


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    salesman_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    salesman = relationship("User", backref="customers")
    name = Column(String(255), index=True, nullable=False, unique=True)
    email = Column(String(255))
    phone = Column(String(255))
    company_name = Column(String(255))
    creation_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)

    def __str__(self):
        return f"Customer : {self.id} -> {self.name}"


class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=True)
    customer = relationship("Customer", backref="contracts")
    salesman_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    salesman = relationship("User", backref="contracts")
    amount_total = Column(Float)
    amount_outstanding = Column(Float)
    creation_date = Column(DateTime, default=datetime.now)
    last_update = Column(DateTime, onupdate=datetime.now)
    state = Column(SQLEnum(ContractState), default=ContractState.waiting, nullable=False, index=True)

    def __str__(self):
        return f"Contract : {self.id} -> {self.salesman_id} for {self.customer_id}"


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    contract_id = Column(Integer, ForeignKey("contract.id", ondelete="CASCADE"), nullable=True)
    contract = relationship("Contract", backref="events")
    customer_id = Column(Integer, ForeignKey("customer.id", ondelete="CASCADE"), nullable=True)
    customer = relationship("Customer", backref="events")
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime)
    support_contact_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    support = relationship("User", backref="supported_events")
    location = Column(String(255))
    attendees = Column(Integer, default=0)
    notes = Column(String(255), nullable=True)


# @event.listens_for(Customer, "before_update", propagate=True)
# def timestamp_before_update(mapper, connection, target):
#     target.last_update = datetime.now
#
#
# @event.listens_for(Contract, "before_update", propagate=True)
# def timestamp_before_update(mapper, connection, target):
#     target.last_update = datetime.now
#
#
# @event.listens_for(User, "before_update", propagate=True)
# def timestamp_before_update(mapper, connection, target):
#     target.last_update = datetime.now
