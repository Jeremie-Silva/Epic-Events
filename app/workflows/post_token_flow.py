from passlib.handlers.bcrypt import bcrypt
from prefect import flow
from fastapi import HTTPException
from jwt import decode as jwt_decode, encode as jwt_encode
from decouple import config
from pendulum import now as pendulum_now
from app.core.database import DBSessionManager
from app.core.models import User


@flow
def post_token_flow(username: str, encrypted_password: str) -> dict:
    """TODO: describe logical line by line"""
    user: User | None = DBSessionManager().get_obj_in_db(model=User, name=username)

    password: str = jwt_decode(
        jwt=encrypted_password, key=config("SECRET_KEY"), algorithms=["HS256"]
    )["password"]

    if user is None or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=404, detail="Invalid username or password")

    expiry: str = pendulum_now(tz="UTC").add(hours=4).to_iso8601_string()
    token: str = jwt_encode(
        payload={"username": user.name, "expiry": expiry},
        key=config("SECRET_KEY"),
        algorithm="HS256"
    )
    return {"message": f"Hello {user.name} 👋", "token": token}
