import inquirer
from rich import print as rprint
from app.cli_tree.utils import cli_get_all_user, cli_patch_user, cli_post_user, cli_delete_user, cli_get_all_customer, \
    cli_get_all_event, cli_get_no_support_event, cli_patch_event, cli_get_all_contract, cli_patch_contract, \
    cli_post_contract
from app.core.models import User


def _ask_choices() -> dict:
    return inquirer.prompt([
        inquirer.List(
            name="choice",
            message="Veuillez sélectionner une option",
            choices=[
                " 1 - Liste des UTILISATEURS",
                " 2 - Modifier un UTILISATEUR",
                " 3 - Créer un UTILISATEUR",
                " 4 - Supprimer un UTILISATEUR",
                " 5 - Liste des CLIENTS",
                " 6 - Liste des EVENEMENTS",
                " 7 - Liste des EVENEMENTS sans support",
                " 8 - Modifier un EVENEMENT",
                " 9 - Liste des CONTRATS",
                "10 - Modifier un CONTRAT",
                "11 - Créer un CONTRAT",
                "Exit"
            ],
            carousel=True
        )
    ])


def menu_gestion(user: User):
    answers: dict = _ask_choices()
    match answers["choice"]:
        case " 1 - Liste des UTILISATEURS":
            cli_get_all_user(user)
        case " 2 - Modifier un UTILISATEUR":
            cli_patch_user(user)
        case " 3 - Créer un UTILISATEUR":
            cli_post_user(user)
        case " 4 - Supprimer un UTILISATEUR":
            cli_delete_user(user)
        case " 5 - Liste des CLIENTS":
            cli_get_all_customer(user)
        case " 6 - Liste des EVENEMENTS":
            cli_get_all_event(user)
        case " 7 - Liste des EVENEMENTS sans support":
            cli_get_no_support_event(user)
        case " 8 - Modifier un EVENEMENT":
            cli_patch_event(user)
        case " 9 - Liste des CONTRATS":
            cli_get_all_contract(user)
        case "10 - Modifier un CONTRAT":
            cli_patch_contract(user)
        case "11 - Créer un CONTRAT":
            cli_post_contract(user)
        case "Exit":
            rprint(f"[bold green]Au revoir.")
            return
    menu_gestion(user)
