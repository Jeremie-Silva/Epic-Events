from fastapi import APIRouter, Depends, HTTPException, Query
from prefect import flow
from app.core.models import User, Contract, Role, ContractState
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, ContractSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def get_all_contract_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=Contract)
    return {
        "user": user,
        "count": len(results),
        "results": [ContractSchema(**i.__dict__) for i in results]
    }


@flow
def get_not_signed_contract_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=Contract, state=ContractState.waiting)
    return {
        "user": user,
        "count": len(results),
        "results": [ContractSchema(**i.__dict__) for i in results]
    }


@flow
def get_not_paid_contract_flow(user: UserSchema) -> dict:
    results = db.get_all_objs_not_equal(model=Contract, amount_outstanding=0.0)
    return {
        "user": user,
        "count": len(results),
        "results": [ContractSchema(**i.__dict__) for i in results]
    }


@router.get("/contract")
def manager_get_contract(
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
    not_signed: bool = Query(False, description="Optional filter"),
    not_paid: bool = Query(False, description="Optional filter")
):
    match user.role:
        case Role.admin | Role.gestion | Role.support:
            return get_all_contract_flow(UserSchema(**user.__dict__))
        case Role.commercial:
            if not_signed:
                return get_not_signed_contract_flow(UserSchema(**user.__dict__))
            if not_paid:
                return get_not_paid_contract_flow(UserSchema(**user.__dict__))
            return get_all_contract_flow(UserSchema(**user.__dict__))
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
