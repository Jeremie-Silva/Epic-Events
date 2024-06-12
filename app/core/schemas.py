from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.core.models import ContractState


class UserSchema(BaseModel):
    id: int
    name: str
    role: str
    creation_date: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True


class CustomerSchema(BaseModel):
    id: Optional[int | None] = None
    salesman_id: Optional[int | None] = None
    name: str
    email: str
    phone: str
    company_name: str
    creation_date: Optional[datetime | None] = None
    last_update: Optional[datetime | None] = None

    class Config:
        orm_mode = True


class ContractSchema(BaseModel):
    id: Optional[int | None] = None
    customer_id: Optional[int | None] = None
    salesman_id: Optional[int | None] = None
    amount_total: float
    amount_outstanding: float
    state: ContractState
    creation_date: Optional[datetime | None] = None
    last_update: Optional[datetime | None] = None

    class Config:
        orm_mode = True


class EventSchema(BaseModel):
    id: int
    name: str
    contract_id: int
    customer_id: int
    support_contact_id: Optional[int | None] = None
    location: str
    attendees: int
    notes: str
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True