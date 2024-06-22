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
def delete_user_flow(user: UserSchema, user_id: int) -> dict:
    user_targeted = db.get_obj(model=User, id=user_id)
    if not user_targeted:
        raise HTTPException(status_code=404, detail="User not found")
    if user_targeted.role == Role.admin:
        raise HTTPException(status_code=401, detail="Action not permitted")
    db.delete_obj(user_targeted)
    return {"result": "User deleted successfully"}


@router.delete("/user/{user_id}")  # pragma: no cover
def manager_delete_user(
    user_id: int,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion:
            return delete_user_flow(UserSchema(**user.__dict__), user_id)
        case _:
            raise HTTPException(status_code=401, detail="Action not permitted")
