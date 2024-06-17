import inquirer
from rich import print as rprint
from app.cli_tree.utils import cli_get_all_user, cli_get_all_customer, cli_patch_related_customer, cli_post_customer, \
    cli_get_all_contract, cli_get_not_signed_contract, cli_get_not_paid_contract, cli_patch_related_contract, \
    cli_get_all_event, cli_get_no_support_event, cli_patch_event, cli_post_event
from app.core.models import User


def _ask_choices() -> dict:
    return inquirer.prompt([
        inquirer.List(
            name="choice",
            message="Veuillez sélectionner une option",
            choices=[
                " 1 - Liste des UTILISATEURS",
                " 2 - Liste des CLIENTS",
                " 3 - Modifier un CLIENT",
                " 4 - Créer un CLIENT",
                " 5 - Liste des CONTRATS",
                " 6 - Liste des CONTRATS non signés",
                " 7 - Liste des CONTRATS non payés",
                " 8 - Modifier un de mes CONTRATS",
                " 9 - Liste des EVENEMENTS",
                "10 - Liste des EVENEMENTS sans support",
                "11 - Modifier un EVENEMENT",
                "12 - Créer un EVENEMENT",
                "Sortie"
            ],
            carousel=True
        )
    ])


def menu_commercial(user: User):
    answers: dict = _ask_choices()
    match answers["choice"]:
        case " 1 - Liste des UTILISATEURS":
            cli_get_all_user(user)
        case " 2 - Liste des CLIENTS":
            cli_get_all_customer(user)
        case " 3 - Modifier un de mes CLIENTS":
            cli_patch_related_customer(user)
        case " 4 - Créer un CLIENT":
            cli_post_customer(user)
        case " 5 - Liste des CONTRATS":
            cli_get_all_contract(user)
        case " 6 - Liste des CONTRATS non signés":
            cli_get_not_signed_contract(user)
        case " 7 - Liste des CONTRATS non payés":
            cli_get_not_paid_contract(user)
        case " 8 - Modifier un de mes CONTRATS":
            cli_patch_related_contract(user)
        case " 9 - Liste des EVENEMENTS":
            cli_get_all_event(user)
        case "10 - Liste des EVENEMENTS sans support":
            cli_get_no_support_event(user)
        case "11 - Modifier un EVENEMENT":
            cli_patch_event(user)
        case "12 - Créer un EVENEMENT":
            cli_post_event(user)
        case "Sortie":
            rprint(f"[bold green]Au revoir.")
            return
    menu_commercial(user)
