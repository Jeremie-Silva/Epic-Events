from argparse import ArgumentParser, Namespace

from database import get_obj_in_db, get_list_in_db
from models import User

parser = ArgumentParser(description="Prompt a username and password for authentication.")
parser.add_argument("--username", required=True, help="User's username")
parser.add_argument("--password", required=True, help="User's username")
args: Namespace = parser.parse_args()

username: str = args.username
password: str = args.password


if __name__ == "__main__":
    x = get_obj_in_db(model=User, key="id", value=1)
    print(x)
    y = get_list_in_db(model=User)
    for i in y:
        print(i)
