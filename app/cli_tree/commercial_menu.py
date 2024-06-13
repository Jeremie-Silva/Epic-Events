import inquirer
from rich import print as rprint
from app.cli_tree.utils import cli_get_all_user, cli_get_all_customer, cli_patch_related_customer, cli_post_customer
from app.core.models import User


def _ask_choices() -> dict:
    return inquirer.prompt([
        inquirer.List(
            name="choice",
            message="Veuillez sélectionner une option",
            choices=[
                "1 - Liste des UTILISATEURS",
                "2 - Liste des CLIENTS",
                "3 - Modifier un CLIENT",
                "4 - Créer un CLIENT",
                "Exit"
            ],
            carousel=True
        )
    ])


def menu_commercial(user: User):
    answers: dict = _ask_choices()
    match answers["choice"]:
        case "1 - Liste des UTILISATEURS":
            cli_get_all_user(user)
        case "2 - Liste des CLIENTS":
            cli_get_all_customer(user)
        case "3 - Modifier un CLIENT":
            cli_patch_related_customer(user)
        case "4 - Créer un CLIENT":
            cli_post_customer(user)
        case "Exit":
            rprint(f"[bold green]Au revoir.")
            return
    menu_commercial(user)
