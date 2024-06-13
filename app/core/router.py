from fastapi import FastAPI
from decouple import config
from jwt import encode as jwt_encode
from app.core.models import User, Role
from app.core.permissions import (
    check_token,
    retrieve_user,
)

from app.endpoints.token.post_token import router as post_token_router

from app.endpoints.user.get_user import router as get_user_router
from app.endpoints.user.patch_user import router as patch_user_router
from app.endpoints.user.post_user import router as post_user_router
from app.endpoints.user.delete_user import router as delete_user_router

from app.endpoints.customer.get_customer import router as get_customer_router
from app.endpoints.customer.post_customer import router as post_customer_router
from app.endpoints.customer.patch_customer import router as patch_customer_router

from app.endpoints.contract.get_contract import router as get_contract_router
from app.endpoints.contract.post_contract import router as post_contract_router
from app.endpoints.contract.patch_contract import router as patch_contract_router

from app.endpoints.event.get_event import router as get_event_router
from app.endpoints.event.patch_event import router as patch_event_router
from app.endpoints.event.post_event import router as post_event_router


app = FastAPI()
app.include_router(post_token_router)

app.include_router(get_user_router)
app.include_router(patch_user_router)
app.include_router(post_user_router)
app.include_router(delete_user_router)

app.include_router(get_customer_router)
app.include_router(post_customer_router)
app.include_router(patch_customer_router)

app.include_router(get_contract_router)
app.include_router(post_contract_router)
app.include_router(patch_contract_router)

app.include_router(get_event_router)
app.include_router(patch_event_router)
app.include_router(post_event_router)
