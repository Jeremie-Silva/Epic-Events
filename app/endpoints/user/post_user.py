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
def post_user_flow(user: UserSchema, body: dict) -> dict:
    new_user: User = User(**body)
    db.add_objs(new_user)
    return {
        "result": "User created successfully",
        "new_user": UserSchema(**new_user.__dict__)
    }


@router.post("/user")
def manager_post_user(
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion:
            return post_user_flow(UserSchema(**user.__dict__), body)
        case _:
            raise HTTPException(status_code=401, detail="Action not permitted")
