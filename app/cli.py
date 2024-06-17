from rich import print as rprint
from rich.console import Console
import typer
from app.cli_tree.commercial_menu import menu_commercial
from app.cli_tree.support_menu import menu_support
from app.core.database import DBSessionManager
from app.core.models import User, Role
from app.core.permissions import verify_password
from app.cli_tree.gestion_menu import menu_gestion
import sentry_sdk


console = Console()
db: DBSessionManager = DBSessionManager()
LOGO: str = """   
 ____________________________________________________________________________________________________________________
|                                                                                                                    |
|      /$$$$$$$$           /$$                   /$$$$$$$$                                  /$$                      |
|     | $$_____/          |__/                  | $$_____/                                 | $$                      |
|     | $$        /$$$$$$  /$$  /$$$$$$$        | $$       /$$    /$$  /$$$$$$  /$$$$$$$  /$$$$$$    /$$$$$$$        |
|     | $$$$$    /$$__  $$| $$ /$$_____/ /$$$$$$| $$$$$   |  $$  /$$/ /$$__  $$| $$__  $$|_  $$_/   /$$_____/        |
|     | $$__/   | $$  \ $$| $$| $$      |______/| $$__/    \  $$/$$/ | $$$$$$$$| $$  \ $$  | $$    |  $$$$$$         |
|     | $$      | $$  | $$| $$| $$              | $$        \  $$$/  | $$_____/| $$  | $$  | $$ /$$ \____  $$        |
|     | $$$$$$$$| $$$$$$$/| $$|  $$$$$$$        | $$$$$$$$   \  $/   |  $$$$$$$| $$  | $$  |  $$$$/ /$$$$$$$/        |
|     |________/| $$____/ |__/ \_______/        |________/    \_/     \_______/|__/  |__/   \___/  |_______/         |
|               | $$                                                                                                 |
|               | $$                                                                                                 |
|               |__/                                                                                                 |
|                                                                                                                    |
|____________________________________________________________________________________________________________________|
"""


def menu_authentication() -> User | None:
    username: str = typer.prompt(text="Username ")
    password: str = typer.prompt(text="Password ", hide_input=True)
    user: User | None = db.get_obj(model=User, name=username)
    if user is None:
        return rprint(f"[bold red]Invalid username or password.")
    if not verify_password(user.password, password):
        return rprint(f"[bold red]Invalid username or password.")
    return user


def hello():
    rprint(f"[bold blue]{LOGO}")
    rprint(f"[bold yellow]Bienvenue dans l'interface en lignes de commandes, veuillez vous authentifer.")


def main():
    hello()
    while (user := menu_authentication()) is None:
        user = menu_authentication()

    match user.role:
        case Role.gestion:
            menu_gestion(user)
        case Role.commercial:
            menu_commercial(user)
        case Role.support:
            menu_support(user)
        case Role.admin:
            return rprint(f"[bold red]Vous ètes admin, veuillez modifier votre role.")
        case _:
            return rprint(f"[bold red]Resource non accessible.")


if __name__ == "__main__":
    sentry_sdk.init(
        dsn="https://a4181e4aaa9429fe233bd21261ddc96d@o4507430341902336.ingest.de.sentry.io/4507446729900112",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    try:
        typer.run(main)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
