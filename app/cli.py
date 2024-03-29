from argparse import ArgumentParser, Namespace

from app.core.models import User, Customer, Permission
from tabulate import tabulate

parser = ArgumentParser(description="Prompt a username and password for authentication.")
parser.add_argument("--username", required=True, help="User's username")
parser.add_argument("--password", required=True, help="User's username")
parser.add_argument("--init", action="store_true", default=False, help="User's username")
args: Namespace = parser.parse_args()

username: str = args.username
password: str = args.password
init: bool = args.init


def user_authenticated(username: str, password: str):
    user: User | None = User.get_item(name=username, password=password)
    if User.get_item(name=username, password=password):
        return user
    return PermissionError("Error : User and password invalid")


def menu_gestion(user: User):
    # print(
    #     tabulate(
    #         tabular_data=,
    #         headers="keys",
    #         tablefmt="rounded_grid",
    #         showindex="always",
    #         missingval="?",
    #         numalign="center",
    #         stralign="center",
    #         floatfmt="center",
    #     )
    # )
    print("1 -> see all clients")
    # match "1":
    match input("Enter a number : "):
        case "1":
            # if user.role.has_permission()
            customers = Customer.get_list()
            print(
                tabulate(
                    tabular_data=[customer.convert_to_dict() for customer in customers],
                    headers="keys",
                    tablefmt="rounded_grid",
                    showindex="always",
                    missingval="?",
                    numalign="center",
                    stralign="center",
                    floatfmt="center",
                )
            )


if __name__ == "__main__":
    user: User = user_authenticated(username=username, password=password)
    if init:
        # Role.generate_roles()
        Permission.generate_permissions()
        # Role.add_permissions()



    # print(f"Hello {user.name}, what you want to do ?")
    # while True:
        # match user.role:
        #     case UserRole.gestion:
        #         menu_gestion(user)
        #     case UserRole.commercial:
        #         print("commercial")
        #     case UserRole.support:
        #         print("support")
