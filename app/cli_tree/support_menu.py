import inquirer
from rich import print as rprint

from app.cli_tree.utils import cli_get_all_user, cli_get_all_customer, cli_get_all_event, cli_get_no_support_event, \
    cli_get_related_event, cli_patch_related_event, cli_get_all_contract
from app.core.models import User


def _ask_choices():
    return inquirer.prompt([
        inquirer.List(
            name="choice",
            message="Veuillez sélectionner une option",
            choices=[
                "1 - Liste des UTILISATEURS",
                "2 - Liste des CLIENTS",
                "3 - Liste des EVENEMENTS",
                "4 - Liste des EVENEMENTS sans support",
                "5 - Liste de mes EVENEMENTS",
                "6 - Modifier un de mes EVENEMENTS",
                "7 - Liste des CONTRATS",
                "Sortie"
            ],
            carousel=True
        )
    ])


def menu_support(user: User):
    answers: dict = _ask_choices()
    match answers["choice"]:
        case "1 - Liste des UTILISATEURS":
            cli_get_all_user(user)
        case "2 - Liste des CLIENTS":
            cli_get_all_customer(user)
        case "3 - Liste des EVENEMENTS":
            cli_get_all_event(user)
        case "4 - Liste des EVENEMENTS sans support":
            cli_get_no_support_event(user)
        case "5 - Liste de mes EVENEMENTS":
            cli_get_related_event(user)
        case "6 - Modifier un de mes EVENEMENTS":
            cli_patch_related_event(user)
        case "7 - Liste des CONTRATS":
            cli_get_all_contract(user)
        case "Sortie":
            rprint(f"[bold green]Au revoir.")
            return
    menu_support(user)
