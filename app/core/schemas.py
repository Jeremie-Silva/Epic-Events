from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserSchema(BaseModel):
    id: int
    name: str
    role: str
    creation_date: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True


class CustomerSchema(BaseModel):
    id: int
    salesman_id: int
    name: str
    email: str
    phone: str
    company_name: str
    creation_date: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True


class ContractSchema(BaseModel):
    id: int
    customer_id: int
    salesman_id: int
    amount_total: float
    amount_outstanding: float
    state: str
    creation_date: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: int
    name: str
    contract_id: int
    customer_id: int
    support_contact_id: int
    location: str
    attendees: int
    notes: str
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True