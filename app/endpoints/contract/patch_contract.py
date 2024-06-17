from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from prefect import flow
from app.core.models import User, Contract, Role
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, ContractSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def patch_contract_flow(user: UserSchema, contract_id: int, body: dict) -> dict:
    db.update_obj(model=Contract, data=body, id=contract_id)
    return {"result": "Values updated successfully"}


@flow
def patch_related_contract_flow(user: UserSchema, contract_id: int, body: dict) -> dict:
    contract_targeted = db.get_obj(model=Contract, id=contract_id)
    if not contract_targeted:
        raise HTTPException(status_code=404, detail="Contract not found")
    if contract_targeted.salesman_id != user.id:
        raise HTTPException(status_code=401, detail="Action not permitted")
    db.update_obj(model=Contract, data=body, id=contract_id)
    return {"result": "Values updated successfully"}


@router.patch("/contract/{contract_id}")
def manager_patch_contract(
    contract_id: int,
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion:
            return patch_contract_flow(UserSchema(**user.__dict__), contract_id, body)
        case Role.commercial:
            return patch_related_contract_flow(UserSchema(**user.__dict__), contract_id, body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
