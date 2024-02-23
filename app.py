from argparse import ArgumentParser, Namespace
from database import db


parser = ArgumentParser(description="Prompt a username and password for authentication.")
parser.add_argument("--username", required=True, help="User's username")
parser.add_argument("--password", required=True, help="User's username")
args: Namespace = parser.parse_args()

username: str = args.username
password: str = args.password


if __name__ == "__main__":
    print(db)
    # print(password)
