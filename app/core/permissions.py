from fastapi import HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from decouple import config
from jwt import decode as jwt_decode, DecodeError
from pendulum import now as pendulum_now, parse as pendulum_parse
from app.core.database import DBSessionManager
from app.core.models import User
from fastapi import Header, Depends


hasher: PasswordHasher = PasswordHasher()
db: DBSessionManager = DBSessionManager()


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(hashed_password: str, plain_password: str) -> bool:
    try:
        return hasher.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False


def decrypt_token(token: str = Header(...)) -> dict[str]:
    try:
        return jwt_decode(
            jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"]
        )
    except DecodeError:
        raise HTTPException(status_code=401, detail="The token is invalid")


def check_token(payload: str = Depends(decrypt_token)) -> bool:
    expiry_date = pendulum_parse(text=payload["expiry"], tz="UTC")
    if pendulum_now(tz="UTC") > expiry_date:
        raise HTTPException(status_code=401, detail="The token is invalid")
    return True


def retrieve_user(payload: str = Depends(decrypt_token)) -> User:
    user: User | None = db.get_obj(model=User, name=payload["username"])
    if not user:
        raise HTTPException(status_code=401, detail="The token is invalid")
    return user
