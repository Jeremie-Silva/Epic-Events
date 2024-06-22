from prefect import flow
from fastapi import APIRouter, HTTPException
from jwt import decode as jwt_decode, encode as jwt_encode
from decouple import config
from pendulum import now as pendulum_now
from app.core.database import DBSessionManager
from app.core.models import User
from app.core.permissions import verify_password


router = APIRouter()
db: DBSessionManager = DBSessionManager()


@flow
def post_token_flow(username: str, encrypted_password: str) -> dict:
    user: User | None = db.get_obj(model=User, name=username)

    password: str = jwt_decode(
        jwt=encrypted_password, key=config("SECRET_KEY"), algorithms=["HS256"]
    )["password"]

    if user is None or not verify_password(user.password, password):
        raise HTTPException(status_code=404, detail="Invalid username or password")

    expiry: str = pendulum_now(tz="UTC").add(hours=int(config("TOKEN_EXPIRY"))).to_iso8601_string()
    token: str = jwt_encode(
        payload={"username": user.name, "expiry": expiry},
        key=config("SECRET_KEY"),
        algorithm="HS256"
    )
    return {"message": f"Hello {user.name} 👋", "token": token}


@router.post("/token")  # pragma: no cover
def post_token(username: str, password: str):
    encrypted_password: str = jwt_encode(
        payload={"password": password},
        key=config("SECRET_KEY"),
        algorithm="HS256"
    )
    return post_token_flow(username, encrypted_password)
