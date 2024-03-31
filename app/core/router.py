from fastapi import FastAPI

from app.workflows.get_user_flow import get_user_flow

app = FastAPI()


@app.get("")
def get_user():
    return get_user_flow()


"""
    - customer
    - event
    - user
    - contract
"""