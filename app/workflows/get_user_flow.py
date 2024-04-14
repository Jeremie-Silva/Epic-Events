from prefect import flow
from app.core.models import User
from app.core.database import DBSessionManager


db: DBSessionManager = DBSessionManager()


@flow
def get_user_flow(user: User, is_authenticated: bool, scope: str):
    if scope == "all":
        filtered_results = DBSessionManager().get_all_objs(model=User)
    else:
        filtered_results = DBSessionManager().get_all_objs(
            model=User, linked_model=User, linked_filters={"id": user.id}
        )
    return {
        "is_authenticated": is_authenticated,  #to remove
        "user": user,  #to remove
        "scope": scope,  #to remove
        "count": len(filtered_results),
        "results": filtered_results
    }
