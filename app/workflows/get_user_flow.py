from prefect import flow
from app.core.models import User


@flow
def get_user_flow(user: User):
    return {"user": user}
