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
def get_all_user_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=User)
    return {
        "user": UserSchema(**user.__dict__),
        "count": len(results),
        "results": [UserSchema(**i.__dict__) for i in results]
    }


@router.get("/user")  # pragma: no cover
def manager_get_user(
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion | Role.commercial | Role.support:
            return get_all_user_flow(UserSchema(**user.__dict__))
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
