from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from prefect import flow
from app.core.models import User, Event, Role, Customer
from app.core.database import DBSessionManager
from app.core.permissions import retrieve_user, check_token
from app.core.schemas import UserSchema, EventSchema


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def post_event_flow(user: UserSchema, body: dict) -> dict:
    customer_targeted = db.get_obj(model=Customer, id=body["customer_id"])
    if not customer_targeted:
        raise HTTPException(status_code=404, detail="Customer not found")
    if customer_targeted.salesman_id != user.id:
        raise HTTPException(status_code=401, detail="Action not permitted")
    try:
        valid_event = EventSchema(**body)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    new_event = Event(**valid_event.__dict__)
    db.add_objs(new_event)
    return {
        "result": "Event created successfully",
        "new_event": EventSchema(**new_event.__dict__)
    }


@router.post("/event")  # pragma: no cover
def manager_post_event(
    body: dict,
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
):
    match user.role:
        case Role.admin | Role.commercial:
            return post_event_flow(UserSchema(**user.__dict__), body)
        case _:
            raise HTTPException(status_code=401, detail="Resource not permitted")
