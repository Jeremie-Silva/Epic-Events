from app.core.database import DBSessionManager
from app.core.models import User, Role
from app.core.permissions import hash_password
from rich import print as rprint
from getpass import getpass

db: DBSessionManager = DBSessionManager()


def ask_password() -> str:
    while True:
        first_try_password: str = getpass("Password: ")
        second_try_password: str = getpass("Password again: ")
        if first_try_password == second_try_password:
            return first_try_password
        else:
            print("Passwords do not match")


def create_admin(username: str, hash_password: str):
    admin_role: Role | None = db.get_obj(model=Role, name="admin")
    if admin_role is None:
        rprint(f"[bold red]Admin role not exist")
        return
    db.add_objs(
        User(name=username, password=hash_password, role_id=admin_role.id),
    )
    rprint(f"[bold green]Admin created")


if __name__ == "__main__":
    username: str = input("Username: ")
    hash_password: str = hash_password(ask_password())
    create_admin(username, hash_password)
