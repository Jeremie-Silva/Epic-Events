from fastapi import APIRouter, Depends, HTTPException
from prefect import flow
from app.core.models import User, Role
from app.core.permissions import (
    check_token,
    retrieve_user,
)
from app.core.database import DBSessionManager
from app.core.schemas import UserSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def patch_user_flow(user: UserSchema, user_id: int, body: dict) -> dict:
    db.update_obj(model=User, data=body, id=user_id)
    return {"result": "Values updated successfully"}


@router.patch("/user/{user_id}")  # pragma: no cover
def manager_patch_user(
    user_id: int,
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion:
            return patch_user_flow(UserSchema(**user.__dict__), user_id, body)
        case _:
            raise HTTPException(status_code=401, detail="Action not permitted")
