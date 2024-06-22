from fastapi import APIRouter, Depends, HTTPException, Query
from prefect import flow
from app.core.models import User, Event, Role
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, EventSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def get_all_event_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=Event)
    return {
        "user": UserSchema(**user.__dict__),
        "count": len(results),
        "results": [EventSchema(**i.__dict__) for i in results]
    }


@flow
def get_no_support_event_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=Event, support_contact_id=None)
    return {
        "user": UserSchema(**user.__dict__),
        "count": len(results),
        "results": [EventSchema(**i.__dict__) for i in results]
    }


@flow
def get_related_event_flow(user: UserSchema) -> dict:
    results = db.get_all_objs(model=Event, support_contact_id=user.id)
    return {
        "user": UserSchema(**user.__dict__),
        "count": len(results),
        "results": [EventSchema(**i.__dict__) for i in results]
    }


@router.get("/event")  # pragma: no cover
def manager_get_event(
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
    support: bool = Query(False, description="Optional filter"),
    related_to_me: bool = Query(False, description="Optional filter")
):
    match user.role:
        case Role.admin | Role.gestion | Role.commercial:
            if support:
                return get_no_support_event_flow(UserSchema(**user.__dict__))
            return get_all_event_flow(UserSchema(**user.__dict__))
        case Role.support:
            if support:
                return get_no_support_event_flow(UserSchema(**user.__dict__))
            if related_to_me:
                return get_related_event_flow(UserSchema(**user.__dict__))
            return get_all_event_flow(UserSchema(**user.__dict__))
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
