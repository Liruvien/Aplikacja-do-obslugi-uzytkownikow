import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

from clcrypto import check_password
from models import User


parser = argparse.ArgumentParser(description="User management script for PostgreSQL database.")
parser.add_argument("-u", "--username", help="Specify the username for operations.")
parser.add_argument("-p", "--password", help="Specify the password (min 8 characters).")
parser.add_argument("-n", "--new_pass", help="Specify the new password for editing (min 8 characters).")
parser.add_argument("-l", "--list", help="List all users in the database.", action="store_true")
parser.add_argument("-d", "--delete", help="Delete a user from the database.", action="store_true")
parser.add_argument("-e", "--edit", help="Edit a user's password.", action="store_true")

args = parser.parse_args()


def edit_user(cur, username, password, new_pass):
    """
    Edit a user's password in the database.

    Args:
        cur: Database cursor.
        username (str): Username of the user to edit.
        password (str): Current password of the user.
        new_pass (str): New password to set for the user.

    Returns:
        None
    """
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is too short. It should have a minimum of 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("Password changed.")
    else:
        print("Incorrect password.")


def delete_user(cur, username, password):
    """
    Delete a user from the database.

    Args:
        cur: Database cursor.
        username (str): Username of the user to delete.
        password (str): Password of the user to authenticate deletion.

    Returns:
        None
    """
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print("User deleted.")
    else:
        print("Incorrect password.")


def create_user(cur, username, password):
    """
    Create a new user in the database.

    Args:
        cur: Database cursor.
        username (str): Username for the new user.
        password (str): Password for the new user (min 8 characters).

    Returns:
        None
    """
    if len(password) < 8:
        print("Password is too short. It should have a minimum of 8 characters.")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print("User created.")
        except UniqueViolation as e:
            print("User already exists.", e)


def list_users(cur):
    """
    List all users in the database.

    Args:
        cur: Database cursor.

    Returns:
        None
    """
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)


if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()

        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()

        cnx.close()
    except OperationalError as err:
        print("Connection Error:", err)