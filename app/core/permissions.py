from fastapi import Header, HTTPException
from decouple import config
from jwt import decode as jwt_decode
from pendulum import now as pendulum_now, parse as pendulum_parse
from app.core.database import DBSessionManager
from app.core.models import User


def check_token(token: str = Header(None)) -> User:
    payload: dict[str] = jwt_decode(
        jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"]
    )
    expiry_date = pendulum_parse(text=payload["expiry"], tz="UTC")
    if pendulum_now(tz="UTC") > expiry_date:
        raise HTTPException(status_code=401, detail="The token is invalid")
    user: User = DBSessionManager().get_obj_in_db(model=User, name=payload["username"])
    return user
