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
def post_customer_flow(user: UserSchema, body: dict) -> dict:
    body.setdefault("salesman_id", user.id)
    try:
        valid_customer: User = CustomerSchema(**body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    new_customer = Customer(**valid_customer.__dict__)
    db.add_objs(new_customer)
    return {
        "result": "Customer created successfully",
        "new_customer": CustomerSchema(**new_customer.__dict__)
    }


@router.post("/customer")
def manager_post_customer(
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.commercial:
            return post_customer_flow(UserSchema(**user.__dict__), body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
