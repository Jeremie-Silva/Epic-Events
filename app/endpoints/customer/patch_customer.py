from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from prefect import flow
from app.core.models import User, Customer, Role
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, CustomerSchema

router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def patch_related_customer_flow(user: UserSchema, customer_id: int, body: dict) -> dict:
    customer_targeted = db.get_obj(model=Customer, id=customer_id)
    if not customer_targeted:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer_targeted.salesman_id != user.id:
        raise HTTPException(status_code=401, detail="Action not permitted")
    db.update_obj(model=Customer, data=body, id=customer_id)
    return {"result": "Values updated successfully"}


@flow
def patch_customer_flow(user: UserSchema, customer_id: int, body: dict) -> dict:
    db.update_obj(model=Customer, data=body, id=customer_id)
    return {"result": "Values updated successfully"}


@router.patch("/customer/{customer_id}")  # pragma: no cover
def manager_patch_customer(
    customer_id: int,
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin:
            return patch_customer_flow(UserSchema(**user.__dict__), customer_id, body)
        case Role.commercial:
            return patch_related_customer_flow(UserSchema(**user.__dict__), customer_id, body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
