import typer
from rich import print as rprint
from tabulate import tabulate
from fastapi import HTTPException
from app.core.models import User
from app.core.schemas import UserSchema
from app.endpoints.contract.get_contract import get_all_contract_flow, get_not_signed_contract_flow, \
    get_not_paid_contract_flow
from app.endpoints.contract.patch_contract import patch_contract_flow, patch_related_contract_flow
from app.endpoints.contract.post_contract import post_contract_flow
from app.endpoints.customer.get_customer import get_all_customer_flow
from app.endpoints.customer.patch_customer import patch_related_customer_flow
from app.endpoints.customer.post_customer import post_customer_flow
from app.endpoints.event.patch_event import patch_event_flow, patch_related_event_flow
from app.endpoints.event.post_event import post_event_flow
from app.endpoints.user.delete_user import delete_user_flow
from app.endpoints.user.get_user import get_all_user_flow
from app.endpoints.user.patch_user import patch_user_flow
from app.endpoints.user.post_user import post_user_flow
from app.endpoints.event.get_event import get_all_event_flow, get_no_support_event_flow, get_related_event_flow


def ask_body_data(*args) -> dict:
    rprint(f"[bold yellow]Laisser le champ vide pour passer à la propriété suivante")
    body: dict = {}
    for arg in args:
        new_value = typer.prompt(text=f"Propriété {str(arg).upper()} ", default="", show_default=False)
        if new_value:
            body[str(arg)] = new_value
    return body


def cli_get_all_user(user: User):
    data: dict = get_all_user_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des utilidateurs : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_patch_user(user: User):
    user_id: int = int(typer.prompt(text="ID de l'utilisateur "))
    body: dict = ask_body_data("name")
    data: dict = patch_user_flow(UserSchema(**user.__dict__), user_id, body)
    rprint(f"[bold green]{data['result']}")


def cli_post_user(user: User):
    body: dict = ask_body_data("name", "password", "role")
    data: dict = post_user_flow(UserSchema(**user.__dict__), body)
    rprint(f"[bold green]{data['result']}")
    rprint(
        tabulate(
            tabular_data=[data['new_user'].__dict__],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, 2)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_delete_user(user: User):
    user_id: int = int(typer.prompt(text="ID de l'utilisateur "))
    data: dict = delete_user_flow(UserSchema(**user.__dict__), user_id)
    rprint(f"[bold green]{data['result']}")


def cli_get_all_customer(user: User):
    data: dict = get_all_customer_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des clients : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_patch_related_customer(user: User):
    customer_id: int = int(typer.prompt(text="ID du client "))
    body: dict = ask_body_data("salesman_id", "name", "email", "phone", "company_name")
    try:
        data: dict = patch_related_customer_flow(UserSchema(**user.__dict__), customer_id, body)
        rprint(f"[bold green]{data['result']}")
    except HTTPException:
        rprint(f"[bold red] Action not permitted")


def cli_post_customer(user: User):
    body: dict = ask_body_data("salesman_id", "name", "email", "phone", "company_name")
    data: dict = post_customer_flow(UserSchema(**user.__dict__), body)
    rprint(f"[bold green]{data['result']}")
    rprint(
        tabulate(
            tabular_data=[data['new_customer'].__dict__],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, 2)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_get_all_event(user: User):
    data: dict = get_all_event_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des évènements : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_get_no_support_event(user: User):
    data: dict = get_no_support_event_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des évènements sans support : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_get_related_event(user: User):
    data: dict = get_related_event_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des évènements sans support : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_patch_event(user: User):
    event_id: int = int(typer.prompt(text="ID de l'évènement "))
    body: dict = ask_body_data("name", "contract_id", "customer_id",
                               "support_contact_id", "location", "attendees", "notes")
    data: dict = patch_event_flow(UserSchema(**user.__dict__), event_id, body)
    rprint(f"[bold green]{data['result']}")


def cli_patch_related_event(user: User):
    event_id: int = int(typer.prompt(text="ID de l'évènement "))
    body: dict = ask_body_data("name", "contract_id", "customer_id",
                               "support_contact_id", "location", "attendees", "notes")
    try:
        data: dict = patch_related_event_flow(UserSchema(**user.__dict__), event_id, body)
        rprint(f"[bold green]{data['result']}")
    except HTTPException:
        rprint(f"[bold red] Action not permitted")


def cli_post_event(user: User):
    body: dict = ask_body_data("name", "contract_id", "customer_id",
                               "support_contact_id", "location", "attendees", "notes")
    data: dict = post_event_flow(UserSchema(**user.__dict__), body)
    rprint(f"[bold green]{data['result']}")
    rprint(
        tabulate(
            tabular_data=[data['new_event'].__dict__],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, 2)),
            missingval="?",
            numalign="center",
            stralign="center",
            floatfmt="center",
        )
    )


def cli_get_all_contract(user: User):
    data: dict = get_all_contract_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des contrats : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
        )
    )


def cli_get_not_signed_contract(user: User):
    data: dict = get_not_signed_contract_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des contrats : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
        )
    )


def cli_get_not_paid_contract(user: User):
    data: dict = get_not_paid_contract_flow(UserSchema(**user.__dict__))
    rprint(f"[bold green]Liste des contrats : {data['count']} résultats")
    rprint(
        tabulate(
            tabular_data=[i.__dict__ for i in data['results']],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, data['count'] + 1)),
            missingval="?",
            numalign="center",
            stralign="center",
        )
    )


def cli_patch_contract(user: User):
    contract_id: int = int(typer.prompt(text="ID du contrat "))
    body: dict = ask_body_data(
        "customer_id", "salesman_id", "amount_total", "amount_outstanding", "state"
    )
    data: dict = patch_contract_flow(UserSchema(**user.__dict__), contract_id, body)
    rprint(f"[bold green]{data['result']}")


def cli_patch_related_contract(user: User):
    contract_id: int = int(typer.prompt(text="ID du contrat "))
    body: dict = ask_body_data(
        "customer_id", "salesman_id", "amount_total", "amount_outstanding", "state"
    )
    try:
        data: dict = patch_related_contract_flow(UserSchema(**user.__dict__), contract_id, body)
        rprint(f"[bold green]{data['result']}")
    except HTTPException:
        rprint(f"[bold red] Action not permitted")


def cli_post_contract(user: User):
    body: dict = ask_body_data(
        "customer_id", "salesman_id", "amount_total", "amount_outstanding", "state"
    )
    data: dict = post_contract_flow(UserSchema(**user.__dict__), body)
    rprint(f"[bold green]{data['result']}")
    rprint(
        tabulate(
            tabular_data=[data['new_contract'].__dict__],
            headers="keys",
            tablefmt="rounded_grid",
            showindex=list(range(1, 2)),
            missingval="?",
            numalign="center",
            stralign="center",
        )
    )
