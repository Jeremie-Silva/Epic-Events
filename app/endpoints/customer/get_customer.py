from fastapi import APIRouter, Depends, HTTPException
from prefect import flow
from app.core.models import User, Customer, Role
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, CustomerSchema

router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def get_all_customer_flow(user: User) -> dict:
    results = db.get_all_objs(model=Customer)
    return {
        "user": UserSchema(**user.__dict__),
        "count": len(results),
        "results": [CustomerSchema(**i.__dict__) for i in results]
    }


@router.get("/customer")
def manager_get_customer(
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.gestion | Role.commercial | Role.support:
            return get_all_customer_flow(user)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
