from fastapi import APIRouter, Depends, HTTPException, Query
from prefect import flow
from app.core.models import User, Event, Role
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, EventSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def patch_event_flow(user: UserSchema, event_id: int, body: dict) -> dict:
    db.update_obj(model=Event, data=body, id=event_id)
    return {"result": "Values updated successfully"}


@router.patch("/event/{event_id}")
def manager_patch_event(
    event_id: int,
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
    support: bool = Query(False, description="Optional filter")
):
    match user.role:
        case Role.admin | Role.gestion | Role.commercial | Role.support:
            return patch_event_flow(UserSchema(**user.__dict__), event_id, body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
