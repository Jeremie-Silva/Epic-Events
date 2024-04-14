from fastapi import FastAPI, Depends
from decouple import config
from jwt import encode as jwt_encode
from app.core.models import User
from app.core.permissions import (
    check_token,
    retrieve_user,
    define_scope,
)
from app.workflows.get_user_flow import get_user_flow
from app.workflows.post_token_flow import post_token_flow
from functools import partial


app = FastAPI()


@app.get("/user")
def get_user(
    user: User = Depends(retrieve_user),
    is_authenticated: bool = Depends(check_token),
    scope: str = Depends(partial(define_scope, action="read", entity="user"))
):
    return get_user_flow(user, is_authenticated, scope)


@app.post("/token")
def post_token(username: str, password: str):
    encrypted_password: str = jwt_encode(
        payload={"password": password},
        key=config("SECRET_KEY"),
        algorithm="HS256"
    )
    return post_token_flow(username, encrypted_password)
