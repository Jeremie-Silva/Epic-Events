from app.core.database import DBSessionManager
import yaml
from app.core.models import Role, Permission


db: DBSessionManager = DBSessionManager()


def get_permissions_config() -> list[dict]:
    with open("permissions.yaml", "r") as file:
        return yaml.safe_load(file)["roles"]


def allow_permissions(role: Role, permissions: list[str]) -> None:
    for permission in permissions:
        action: str = permission.split()[0]
        entity: str = permission.split()[1]
        scope: str = permission.split()[2]
        db.add_obj(
            Permission(
                action=action,
                entity=entity,
                scope=scope,
                role_id=role.id,
            )
        )


if __name__ == "__main__":
    permissions_config: list[dict] = get_permissions_config()
    for role_config in permissions_config:
        new_role: Role = Role(name=role_config["name"])
        db.add_obj(obj=new_role)
        allow_permissions(role=new_role, permissions=role_config["permissions"])
