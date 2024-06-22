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
def post_contract_flow(user: UserSchema, body: dict) -> dict:
    try:
        valid_contract = ContractSchema(**body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    new_contract = Contract(**valid_contract.__dict__)
    db.add_objs(new_contract)
    return {
        "result": "Contract created successfully",
        "new_contract": ContractSchema(**new_contract.__dict__)
    }


@router.post("/contract")  # pragma: no cover
def manager_post_contract(
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion:
            return post_contract_flow(UserSchema(**user.__dict__), body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
