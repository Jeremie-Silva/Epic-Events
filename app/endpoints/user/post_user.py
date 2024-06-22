from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from prefect import flow
from app.core.models import User, Role
from app.core.permissions import (
    check_token,
    retrieve_user, hash_password,
)
from app.core.database import DBSessionManager
from app.core.schemas import UserSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def post_user_flow(user: UserSchema, body: dict) -> dict:
    body["password"] = hash_password(body.pop("password"))
    try:
        valid_user = UserSchema(**body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    new_user = User(**valid_user.__dict__)
    db.add_objs(new_user)
    return {
        "result": "User created successfully",
        "new_user": UserSchema(**new_user.__dict__)
    }


@router.post("/user")  # pragma: no cover
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
